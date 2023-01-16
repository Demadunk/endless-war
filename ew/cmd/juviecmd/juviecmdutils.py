"""
	Commands and utilities related to Juveniles.
"""
import math
import random
import time

from ew.backend import item as bknd_item
from ew.backend.item import EwItem
from ew.backend import worldevent as bknd_worldevent
from ew.backend.worldevent import EwWorldEvent
from ew.static import cfg as ewcfg
from ew.static import weapons as static_weapons
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.frontend import EwResponseContainer

# Map of user ID to a map of recent miss-mining time to count. If the count
# exceeds 11 in 20 seconds, you die.
last_mismined_times = {}

juviesrow_mines = {}
toxington_mines = {}
cratersville_mines = {}
juviesrow_mines_minesweeper = {}
toxington_mines_minesweeper = {}
cratersville_mines_minesweeper = {}
juviesrow_mines_bubblebreaker = {}
toxington_mines_bubblebreaker = {}
cratersville_mines_bubblebreaker = {}

mines_map = {
    ewcfg.poi_id_mine: juviesrow_mines,
    ewcfg.poi_id_tt_mines: toxington_mines,
    ewcfg.poi_id_cv_mines: cratersville_mines,
    ewcfg.poi_id_mine_sweeper: juviesrow_mines_minesweeper,
    ewcfg.poi_id_tt_mines_sweeper: toxington_mines_minesweeper,
    ewcfg.poi_id_cv_mines_sweeper: cratersville_mines_minesweeper,
    ewcfg.poi_id_mine_bubble: juviesrow_mines_bubblebreaker,
    ewcfg.poi_id_tt_mines_bubble: toxington_mines_bubblebreaker,
    ewcfg.poi_id_cv_mines_bubble: cratersville_mines_bubblebreaker
}

scavenge_combos = {}
scavenge_captchas = {}
scavenge_locations = {}

class EwMineGrid:
    grid_type = ""

    grid = []

    message = ""
    wall_message = ""

    times_edited = 0

    time_last_posted = 0

    cells_mined = 0

    def __init__(self, grid = [], grid_type = ""):
        self.grid = grid
        self.grid_type = grid_type
        self.message = ""
        self.wall_message = ""
        self.times_edited = 0
        self.time_last_posted = 0
        self.cells_mined = 0


"""
	Mining in the wrong channel or while exhausted.
	This is deprecated anyway but let's sorta keep it around in case we need it.
"""


async def mismine(cmd, user_data, cause):
    time_now = int(time.time())
    global last_mismined_times

    mismined = last_mismined_times.get(cmd.message.author.id)

    if mismined is None:
        mismined = {
            'time': time_now,
            'count': 0
        }

    if time_now - mismined['time'] < 20:
        mismined['count'] += 1
    else:
        # Reset counter.
        mismined['time'] = time_now
        mismined['count'] = 1

    last_mismined_times[cmd.message.author.id] = mismined

    world_events = bknd_worldevent.get_world_events(id_server=cmd.guild.id)
    event_data = None
    captcha = None
    for id_event in world_events:
        if world_events.get(id_event) == ewcfg.event_type_minecollapse:
            event_data = EwWorldEvent(id_event=id_event)
            if int(event_data.event_props.get('id_user')) == user_data.id_user:
                mine_collapse = True
                captcha = event_data.event_props.get('captcha')

    if mismined['count'] >= 11:  # up to 6 messages can be buffered by discord and people have been dying unfairly because of that
        if cause == ewcfg.event_type_minecollapse:
            if event_data != None:
                bknd_worldevent.delete_world_event(id_event=event_data.id_event)
            else:
                return
        # Lose some slime
        last_mismined_times[cmd.message.author.id] = None
        # user_data.die(cause = ewcfg.cause_mining)

        accident_response = "You have lost an arm and a leg in a mining accident. Tis but a scratch."

        if random.randrange(4) == 0:
            accident_response = "Big John arrives just in time to save you from your mining accident!\nhttps://cdn.discordapp.com/attachments/431275470902788107/743629505876197416/mine2.jpg"
        else:
            mutations = user_data.get_mutations()
            if ewcfg.mutation_id_lightminer in mutations:
                response = "You instinctively jump out of the way of the collapsing shaft, not a scratch on you. Whew, really gets your blood pumping."
            else:
                user_data.change_slimes(n=-(user_data.slimes * 0.5))
                user_data.persist()

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, accident_response))
    # await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
    # sewerchannel = fe_utils.get_channel(cmd.guild, ewcfg.channel_sewers)
    # await fe_utils.send_message(cmd.client, sewerchannel, "{} ".format(ewcfg.emote_slimeskull) + fe_utils.formatMessage(cmd.message.author, "You have died in a mining accident. {}".format(ewcfg.emote_slimeskull)))
    else:
        if cause == "exhaustion":
            response = "You've exhausted yourself from mining. You'll need some refreshment before getting back to work."
        elif cause == ewcfg.event_type_minecollapse:
            if captcha != None:
                response = "The mineshaft is collapsing around you!\nGet out of there! ({cmd} {captcha})".format(cmd=ewcfg.cmd_mine, captcha=ewutils.text_to_regional_indicator(captcha))
            else:
                return
        else:
            response = "You can't mine in this channel. Go elsewhere."

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


def init_grid(poi, id_server):
    mining_type = ewcfg.mines_mining_type_map.get(poi)

    if mining_type == ewcfg.mining_type_minesweeper:
        return init_grid_minesweeper(poi, id_server)
    elif mining_type == ewcfg.mining_type_bubblebreaker:
        return init_grid_bubblebreaker(poi, id_server)
    else:
        return init_grid_none(poi, id_server)


def init_grid_minesweeper(poi, id_server):
    grid = []
    num_rows = 13
    num_cols = 13
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            row.append(ewcfg.cell_empty)
        grid.append(row)

    num_mines = 20

    row = random.randrange(num_rows)
    col = random.randrange(num_cols)
    for mine in range(num_mines):
        while grid[row][col] == ewcfg.cell_mine:
            row = random.randrange(num_rows)
            col = random.randrange(num_cols)
        grid[row][col] = ewcfg.cell_mine

    if poi in mines_map:
        grid_cont = EwMineGrid(grid=grid, grid_type=ewcfg.mine_grid_type_minesweeper)
        mines_map.get(poi)[id_server] = grid_cont


def init_grid_bubblebreaker(poi, id_server):
    grid = []
    num_rows = 13
    num_cols = 13
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            if i > 8:
                row.append(ewcfg.cell_bubble_empty)
                continue
            cell = random.choice(ewcfg.cell_bubbles)
            randomn = random.random()
            if randomn < 0.15 and j > 0:
                cell = row[-1]
            elif randomn < 0.3 and i > 0:
                cell = grid[-1][j]

            row.append(cell)
        grid.append(row)

    if poi in mines_map:
        grid_cont = EwMineGrid(grid=grid, grid_type=ewcfg.mine_grid_type_bubblebreaker)
        mines_map.get(poi)[id_server] = grid_cont


def init_grid_none(poi, id_server):
    if poi in mines_map:
        grid_cont = EwMineGrid(grid=None, grid_type=None)
        mines_map.get(poi)[id_server] = grid_cont


async def print_grid(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = user_data.poi
    channel = cmd.message.channel.name
    id_server = cmd.guild.id
    if poi in mines_map:
        grid_map = mines_map.get(poi)
        if id_server not in grid_map:
            init_grid(poi, id_server)
        grid_cont = grid_map.get(id_server)

        grid = grid_cont.grid

        if grid_cont.grid_type == ewcfg.mine_grid_type_minesweeper:
            return await print_grid_minesweeper(cmd)
        elif grid_cont.grid_type == ewcfg.mine_grid_type_bubblebreaker:
            return await print_grid_bubblebreaker(cmd)


async def print_grid_minesweeper(cmd):
    grid_str = ""
    user_data = EwUser(member=cmd.message.author)
    poi = user_data.poi
    channel = cmd.message.channel.name
    id_server = cmd.guild.id
    time_now = int(time.time())
    if poi in mines_map:
        grid_map = mines_map.get(poi)
        if id_server not in grid_map:
            init_grid_minesweeper(poi, id_server)
        grid_cont = grid_map.get(id_server)

        grid = grid_cont.grid

        grid_str += "   "
        for j in range(len(grid[0])):
            letter = ewcfg.alphabet[j]
            grid_str += "{} ".format(letter)
        grid_str += "\n"
        for i in range(len(grid)):
            row = grid[i]
            if i + 1 < 10:
                grid_str += " "

            grid_str += "{} ".format(i + 1)
            for j in range(len(row)):
                cell = row[j]
                cell_str = ""
                if cell == ewcfg.cell_empty_open:
                    neighbor_mines = 0
                    for ci in range(max(0, i - 1), min(len(grid), i + 2)):
                        for cj in range(max(0, j - 1), min(len(row), j + 2)):
                            if grid[ci][cj] > 0:
                                neighbor_mines += 1
                    cell_str = str(neighbor_mines)

                else:
                    cell_str = ewcfg.symbol_map_ms.get(cell)
                grid_str += cell_str + " "

            grid_str += "{}".format(i + 1)
            grid_str += "\n"

        grid_str += "   "
        for j in range(len(grid[0])):
            letter = ewcfg.alphabet[j]
            grid_str += "{} ".format(letter)

        grid_edit = "\n```\n{}\n```".format(grid_str)

        if time_now > grid_cont.time_last_posted + 10 or grid_cont.times_edited > 3 or grid_cont.message == "":
            grid_cont.message = await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, grid_edit))
            grid_cont.time_last_posted = time_now
            grid_cont.times_edited = 0
        else:
            grid_cont.message = await fe_utils.edit_message(cmd.client, grid_cont.message, fe_utils.formatMessage(cmd.message.author, grid_edit))
            grid_cont.times_edited += 1

        if grid_cont.wall_message == "":
            wall_channel = ewcfg.mines_wall_map.get(poi)
            resp_cont = EwResponseContainer(id_server=id_server)
            resp_cont.add_channel_response(wall_channel, grid_edit)
            msg_handles = await resp_cont.post()
            grid_cont.wall_message = msg_handles[0]
        else:
            grid_cont.wall_message = await fe_utils.edit_message(cmd.client, grid_cont.wall_message, grid_edit)


async def print_grid_bubblebreaker(cmd):
    grid_str = ""
    user_data = EwUser(member=cmd.message.author)
    poi = user_data.poi
    channel = cmd.message.channel.name
    id_server = cmd.guild.id
    time_now = int(time.time())
    use_emotes = False
    if poi in mines_map:
        grid_map = mines_map.get(poi)
        if id_server not in grid_map:
            init_grid(poi, id_server)
        grid_cont = grid_map.get(id_server)

        grid = grid_cont.grid

        # grid_str += "   "
        for j in range(len(grid[0])):
            letter = ewcfg.alphabet[j]
            grid_str += "{} ".format(letter)
        grid_str += "\n"
        for i in range(len(grid)):
            row = grid[i]
            # if i+1 < 10:
            #	grid_str += " "

            # grid_str += "{} ".format(i+1)
            for j in range(len(row)):
                cell = row[j]
                cell_str = get_cell_symbol_bubblebreaker(cell)
                if use_emotes:
                    cell_str = ewcfg.number_emote_map.get(int(cell))
                grid_str += cell_str + " "
            # grid_str += "{}".format(i+1)
            grid_str += "\n"

        # grid_str += "   "
        for j in range(len(grid[0])):
            letter = ewcfg.alphabet[j]
            grid_str += "{} ".format(letter)

        grid_edit = "\n```\n{}\n```".format(grid_str)
        if use_emotes:
            grid_edit = "\n" + grid_str
        if time_now > grid_cont.time_last_posted + 10 or grid_cont.times_edited > 8 or grid_cont.message == "":
            grid_cont.message = await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, grid_edit))
            grid_cont.time_last_posted = time_now
            grid_cont.times_edited = 0
        else:
            grid_cont.message = await fe_utils.edit_message(cmd.client, grid_cont.message, fe_utils.formatMessage(cmd.message.author, grid_edit))
            grid_cont.times_edited += 1

        if grid_cont.wall_message == "":
            wall_channel = ewcfg.mines_wall_map.get(poi)
            resp_cont = EwResponseContainer(id_server=id_server)
            resp_cont.add_channel_response(wall_channel, grid_edit)
            msg_handles = await resp_cont.post()
            grid_cont.wall_message = msg_handles[0]
        else:
            grid_cont.wall_message = await fe_utils.edit_message(cmd.client, grid_cont.wall_message, grid_edit)


# for pokemining


def get_cell_symbol_bubblebreaker(cell):
    if cell == ewcfg.cell_bubble_empty:
        return " "
    return cell


def get_cell_symbol_pokemine(cell):
    cell_str = " "
    # if cell > 2 * ewcfg.slimes_invein:
    #	cell_str = "&"
    # elif cell > 1.5 * ewcfg.slimes_invein:
    #	cell_str = "S"
    if cell > 0.4 * ewcfg.slimes_invein:
        cell_str = "~"
    # elif cell > 0.5 * ewcfg.slimes_invein:
    #	cell_str = ";"
    elif cell > 0:
        cell_str = ";"
    elif cell > -40 * ewcfg.slimes_pertile:
        cell_str = " "
    # elif cell > -40 * ewcfg.slimes_pertile:
    #	cell_str = "+"
    else:
        cell_str = "X"
    return cell_str


# for bubblebreaker
def apply_gravity(grid):
    cells_to_check = []
    for row in range(1, len(grid)):
        for col in range(len(grid[row])):
            coords = (row, col)
            new_coords = bubble_fall(grid, (row, col))
            if coords != new_coords:
                cells_to_check.append(new_coords)

    return cells_to_check


# for bubblebreaker
def bubble_fall(grid, coords):
    row = coords[0]
    col = coords[1]
    if grid[row][col] == ewcfg.cell_bubble_empty:
        return coords
    falling_bubble = grid[row][col]
    while row > 0 and grid[row - 1][col] == ewcfg.cell_bubble_empty:
        row -= 1

    grid[coords[0]][coords[1]] = ewcfg.cell_bubble_empty
    grid[row][col] = falling_bubble
    return (row, col)


# for bubblebreaker
def check_and_explode(grid, cells_to_check):
    slime_yield = 0

    for coords in cells_to_check:
        bubble = grid[coords[0]][coords[1]]
        if bubble == ewcfg.cell_bubble_empty:
            continue

        bubble_cluster = [coords]
        to_check = [coords]
        while len(to_check) > 0:
            to_check_next = []
            for coord in to_check:
                neighs = neighbors(grid, coord)
                for neigh in neighs:
                    if neigh in bubble_cluster:
                        continue
                    if grid[neigh[0]][neigh[1]] == bubble:
                        bubble_cluster.append(neigh)
                        to_check_next.append(neigh)
            to_check = to_check_next

        if len(bubble_cluster) >= ewcfg.bubbles_to_burst:
            for coord in bubble_cluster:
                grid[coord[0]][coord[1]] = ewcfg.cell_bubble_empty
                slime_yield += 1

    return slime_yield


# for bubblebreaker
def neighbors(grid, coords):
    neighs = []
    row = coords[0]
    col = coords[1]
    if row - 1 >= 0:
        neighs.append((row - 1, col))
    if row + 1 < len(grid):
        neighs.append((row + 1, col))
    if col - 1 >= 0:
        neighs.append((row, col - 1))
    if col + 1 < len(grid[row]):
        neighs.append((row, col + 1))
    return neighs


# for bubblebreaker
def add_row(grid):
    new_row = []
    for i in range(len(grid[0])):

        cell = random.choice(ewcfg.cell_bubbles)
        randomn = random.random()
        if randomn < 0.15 and i > 0:
            cell = new_row[-1]
        elif randomn < 0.3:
            cell = grid[0][i]
        if cell == ewcfg.cell_bubble_empty:
            cell = random.choice(ewcfg.cell_bubbles)

        new_row.append(cell)
    grid.insert(0, new_row)
    return grid.pop(-1)


# for bubblebreaker
def get_height(grid):
    row = 0

    while row < len(grid):
        is_empty = True
        for cell in grid[row]:
            if cell != ewcfg.cell_bubble_empty:
                is_empty = False
                break
        if is_empty:
            break
        row += 1

    return row


def get_unmined_cell_count(grid_cont):
    grid = grid_cont.grid
    unmined_cells = 0
    for row in grid:
        for cell in row:
            if cell in [ewcfg.cell_empty, ewcfg.cell_empty_marked]:
                unmined_cells += 1
    return unmined_cells


def get_mining_yield_by_grid_type(cmd, grid_cont):
    if grid_cont.grid_type == ewcfg.mine_grid_type_minesweeper:
        return get_mining_yield_minesweeper(cmd, grid_cont)
    elif grid_cont.grid_type == ewcfg.mine_grid_type_bubblebreaker:
        return get_mining_yield_bubblebreaker(cmd, grid_cont)
    else:
        return get_mining_yield_default(cmd)


def get_mining_yield_minesweeper(cmd, grid_cont):
    user_data = EwUser(member=cmd.message.author)
    grid = grid_cont.grid
    grid_multiplier = grid_cont.cells_mined ** 0.4

    hunger_cost_mod = ewutils.hunger_cost_mod(user_data.slimelevel)

    row = -1
    col = -1
    if cmd.tokens_count < 2:
        response = "Please specify which Minesweeper vein to mine."
        return response

    for token in cmd.tokens[1:]:

        coords = token.lower()
        if coords == "reset":
            user_data.hunger += int(ewcfg.hunger_perminereset * hunger_cost_mod)
            user_data.persist()
            init_grid_minesweeper(user_data.poi, user_data.id_server)
            return ""

        if col < 1:

            for char in coords:
                if char in ewcfg.alphabet:
                    col = ewcfg.alphabet.index(char)
                    coords = coords.replace(char, "")
        if row < 1:
            try:
                row = int(coords)
            except:
                row = -1

    row -= 1

    if row not in range(len(grid)) or col not in range(len(grid[row])):
        response = "Invalid Minesweeper vein."
        return response

    mining_yield = 0
    mining_accident = False

    if grid[row][col] in [ewcfg.cell_empty_marked, ewcfg.cell_mine_marked]:
        response = "This vein has been flagged as dangerous. Remove the flag to mine here."
        return response

    elif grid[row][col] == ewcfg.cell_empty_open:
        response = "This vein has already been mined dry."
        return response

    elif grid[row][col] == ewcfg.cell_mine:
        mining_accident = True

    elif grid[row][col] == ewcfg.cell_empty:
        grid[row][col] = ewcfg.cell_empty_open
        grid_cont.cells_mined += 1
        mining_yield = grid_multiplier * 1.7 * get_mining_yield_default(cmd)

    unmined_cells = get_unmined_cell_count(grid_cont)

    if unmined_cells == 0:
        init_grid_minesweeper(user_data.poi, user_data.id_server)

    if mining_accident:
        slimes_lost = 0.1 * grid_multiplier * user_data.slimes
        if slimes_lost <= 0:
            response = "You barely avoided getting into a mining accident."
        else:
            response = "You have lost an arm and a leg in a mining accident. Tis but a scratch."

            if random.randrange(4) == 0:
                response = "Big John arrives just in time to save you from your mining accident!\nhttps://cdn.discordapp.com/attachments/431275470902788107/743629505876197416/mine2.jpg"
            else:
                mutations = user_data.get_mutations()
                if ewcfg.mutation_id_lightminer in mutations:
                    response = "You instinctively jump out of the way of the live mine, barely escaping with your life. Whew, really gets your blood pumping."
                    user_data.hunger += int(ewcfg.hunger_perlmcollapse * hunger_cost_mod)
                    user_data.persist()
                else:
                    user_data.change_slimes(n=-(user_data.slimes * 0.3))
                    user_data.persist()

        init_grid_minesweeper(user_data.poi, user_data.id_server)

        return response

    else:
        return mining_yield


def get_mining_yield_bubblebreaker(cmd, grid_cont):
    user_data = EwUser(member=cmd.message.author)
    grid = grid_cont.grid

    hunger_cost_mod = ewutils.hunger_cost_mod(user_data.slimelevel)

    row = -1
    col = -1
    bubble_add = None
    if cmd.tokens_count < 2:
        response = "Please specify which Bubble Breaker vein to mine."
        return response

    for token in cmd.tokens[1:]:
        token_lower = token.lower()

        coords = token_lower
        if coords == "reset":
            user_data.hunger += int(ewcfg.hunger_perminereset * hunger_cost_mod)
            user_data.persist()
            init_grid_bubblebreaker(user_data.poi, user_data.id_server)
            return ""

        if col < 1:
            for char in token_lower:
                if char in ewcfg.alphabet:
                    col = ewcfg.alphabet.index(char)
                    token_lower = token_lower.replace(char, "")
        if bubble_add == None:
            bubble = token_lower
            if bubble in ewcfg.cell_bubbles:
                bubble_add = bubble

    row = len(grid)
    row -= 1

    if col not in range(len(grid[0])):
        response = "Invalid Bubble Breaker vein."
        return response

    if bubble_add == None:
        response = "Invalid Bubble Breaker bubble."
        return response

    mining_yield = 0
    mining_accident = False

    cells_to_clear = []

    slimes_pertile = 1.8 * get_mining_yield_default(cmd)
    if grid[row][col] != ewcfg.cell_bubble_empty:
        mining_accident = True
    else:
        grid[row][col] = bubble_add

        cells_to_check = apply_gravity(grid)

        cells_to_check.append((row, col))

        while len(cells_to_check) > 0:
            mining_yield += slimes_pertile * check_and_explode(grid, cells_to_check)

            cells_to_check = apply_gravity(grid)

    grid_cont.cells_mined += 1
    grid_height = get_height(grid)

    if grid_cont.cells_mined % 4 == 3 or grid_height < 5:
        if grid_height < len(grid):
            add_row(grid)
        else:
            mining_accident = True

    if mining_accident:

        response = "You have lost an arm and a leg in a mining accident. Tis but a scratch."

        if random.randrange(4) == 0:
            response = "Big John arrives just in time to save you from your mining accident!\nhttps://cdn.discordapp.com/attachments/431275470902788107/743629505876197416/mine2.jpg"
        else:
            mutations = user_data.get_mutations()
            if ewcfg.mutation_id_lightminer in mutations:
                response = "You instinctively jump out of the way of the collapsing shaft, not a scratch on you. Whew, really gets your blood pumping."
            else:
                user_data.change_slimes(n=-(user_data.slimes * 0.3))
                user_data.persist()

        init_grid_bubblebreaker(cmd.message.channel.name, user_data.id_server)

        return response
    else:
        return mining_yield


def get_mining_yield_default(cmd):
    if cmd.message.channel.name == ewcfg.channel_mines:
        return 50
    else:
        return 200


def create_mining_event(cmd, toolused=None):
    randomn = random.random()
    time_now = int(time.time())
    user_data = EwUser(member=cmd.message.author)
    mine_district_data = EwDistrict(district=user_data.poi, id_server=user_data.id_server)

    life_states = [ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]
    num_miners = len(mine_district_data.get_players_in_district(life_states=life_states, ignore_offline=True))

    common_event_chance = 0.7  # 7/10, not used
    uncommon_event_chance = 0.3  # 3/10
    rare_event_chance = 0.05 / num_miners  #  1/2 usual chance for 2 miners, 1/3 for 3 miners etc.

    common_event_triggered = False
    uncommon_event_triggered = False
    rare_event_triggered = False

    weapon_item = user_data.get_weapon_item()
    weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))

    if randomn < rare_event_chance: # 5% chance, divided by # of players
        rare_event_triggered = True
    elif randomn < (uncommon_event_chance + rare_event_chance): # Always 30%
        uncommon_event_triggered = True
    else:       # 70% - rare_event_chance (usually 5%)
        common_event_triggered = True 

    # common event
    if common_event_triggered:
        randomn = random.random()

        #Forces all common events into mineshaft collapses if you have a sledgehammer
        if weapon.id_weapon == ewcfg.weapon_id_sledgehammer:
            event_props = {}
            event_props['id_user'] = cmd.message.author.id
            event_props['poi'] = user_data.poi
            event_props['captcha'] = ewutils.generate_captcha(length=8, user_data=user_data)
            event_props['channel'] = cmd.message.channel.name
            return bknd_worldevent.create_world_event(
                id_server=cmd.guild.id,
                event_type=ewcfg.event_type_minecollapse,
                time_activate=time_now,
                event_props=event_props
            )
            
        # 4x glob of slime
        elif randomn < 0.5:
            event_props = {}
            event_props['id_user'] = cmd.message.author.id
            event_props['poi'] = user_data.poi
            event_props['channel'] = cmd.message.channel.name
            return bknd_worldevent.create_world_event(
                id_server=cmd.guild.id,
                event_type=ewcfg.event_type_slimeglob,
                time_activate=time_now,
                event_props=event_props
            )
        # 30 seconds slimefrenzy
        else:
            event_props = {}
            event_props['id_user'] = cmd.message.author.id
            event_props['poi'] = user_data.poi
            event_props['channel'] = cmd.message.channel.name
            return bknd_worldevent.create_world_event(
                id_server=cmd.guild.id,
                event_type=ewcfg.event_type_slimefrenzy,
                time_activate=time_now,
                time_expir=time_now + 30,
                event_props=event_props
            )

    # uncommon event
    elif uncommon_event_triggered:
        randomn = random.random()

        # gap into the void
        if randomn < 0.05:
            event_props = {}
            event_props['id_user'] = cmd.message.author.id
            event_props['poi'] = user_data.poi
            event_props['channel'] = cmd.message.channel.name
            return bknd_worldevent.create_world_event(
                id_server=cmd.guild.id,
                event_type=ewcfg.event_type_voidhole,
                time_activate=time_now,
                time_expir=time_now + 15, # should be longer than ratelimit
                event_props=event_props
            )
        # mine shaft collapse
        elif randomn < 0.5:
            event_props = {}
            event_props['id_user'] = cmd.message.author.id
            event_props['poi'] = user_data.poi
            event_props['captcha'] = ewutils.generate_captcha(length=8, user_data=user_data)
            event_props['channel'] = cmd.message.channel.name
            return bknd_worldevent.create_world_event(
                id_server=cmd.guild.id,
                event_type=ewcfg.event_type_minecollapse,
                time_activate=time_now,
                event_props=event_props
            )
        # 10 second poudrin frenzy
        else:
            if bknd_item.check_inv_capacity(user_data=user_data, item_type=ewcfg.it_item):
                event_props = {}
                event_props['id_user'] = cmd.message.author.id
                event_props['poi'] = user_data.poi
                event_props['channel'] = cmd.message.channel.name
                return bknd_worldevent.create_world_event(
                    id_server=cmd.guild.id,
                    event_type=ewcfg.event_type_poudrinfrenzy,
                    time_activate=time_now,
                    time_expir=time_now + 5,
                    event_props=event_props
                )

    # rare event
    elif rare_event_triggered:
        randomn = random.random()
        # You beat up a skeleton - get poudrins and monsterbones
        if randomn < 0.5:
            event_props = {}
            event_props['id_user'] = cmd.message.author.id
            event_props['poi'] = user_data.poi
            event_props['channel'] = cmd.message.channel.name
            return bknd_worldevent.create_world_event(
                id_server=cmd.guild.id,
                event_type=ewcfg.event_type_spookyskeleton,
                time_activate=time_now,
                time_expir=time_now + 15,
                event_props=event_props
            )
        # You beat up a ghost - get triple slime and mine ectoplasm
        else:
            event_props = {}
            event_props['id_user'] = cmd.message.author.id
            event_props['poi'] = user_data.poi
            event_props['channel'] = cmd.message.channel.name
            return bknd_worldevent.create_world_event(
                id_server=cmd.guild.id,
                event_type=ewcfg.event_type_spookyghost,
                time_activate=time_now,
                time_expir=time_now + 15,
                event_props=event_props
            )




def gen_scavenge_captcha(n = 0, user_data = None):
    captcha_length = math.ceil(n / 3)

    return ewutils.generate_captcha(length=captcha_length, user_data=user_data)
