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
from ew.backend.worldevent import delete_world_event
from ew.backend.dungeons import EwGamestate
from ew.static import cfg as ewcfg
from ew.static import weapons as static_weapons
from ew.static import poi as poi_static
from ew.static import vendors
from ew.static import items as static_items
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import item as itm_utils
from ew.utils import stats as ewstats
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.frontend import EwResponseContainer
try:
    import ew.cmd.debug as ewdebug
    from ew.static.rstatic import digup_relics
    from ew.static.rstatic import relic_map
    from ew.static.rstatic import question_map

except:
    import ew.cmd.debug_dummy as ewdebug
    from ew.static.rstatic_dummy import digup_relics
    from ew.static.rstatic_dummy import relic_map
    from ew.static.rstatic_dummy import question_map

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

    variation = 0

    def __init__(self, grid = [], grid_type = ""):
        self.grid = grid
        self.grid_type = grid_type
        self.message = ""
        self.wall_message = ""
        self.times_edited = 0
        self.time_last_posted = 0
        self.cells_mined = 0
        self.variation = 0


class EwMineAction:
    valid = False

    hunger_cost_multiplier = 0
    slime_yield = 0
    bonus_slime_yield = 0
    value_mod = 0.0

    collapse = False
    collapse_penalty = 0.0

    unearthed_item_chance = 0.0
    unearthed_item_amount = 0
    unearthed_item_type = ""

    response = ""
    toolused = ""

    grid_effect = 0

    user_data = None

    def __init__(self,
                 valid = False,
                 hunger_cost_multiplier = 0,
                 slime_yield = 0,
                 bonus_slime_yield = 0,
                 value_mod = 0.0,
                 collapse = False,
                 collapse_penalty = 0.0,
                 unearthed_item_chance = 0.0,
                 unearthed_item_amount = 0,
                 unearthed_item_type = "",
                 response = "",
                 toolused = "",
                 grid_effect = 0,
                 user_data = None):
        self.valid = valid
        self.hunger_cost_multiplier = hunger_cost_multiplier
        self.slime_yield = slime_yield
        self.bonus_slime_yield = bonus_slime_yield
        self.value_mod = value_mod
        self.collapse = collapse
        self.collapse_penalty = collapse_penalty
        self.unearthed_item_chance = unearthed_item_chance
        self.unearthed_item_amount = unearthed_item_amount
        self.unearthed_item_type = unearthed_item_type
        self.response = response
        self.toolused = toolused
        self.grid_effect = grid_effect
        self.user_data = user_data


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

    # world_events = bknd_worldevent.get_world_events(id_server=cmd.guild.id)
    # event_data = None
    # captcha = None

    if mismined['count'] >= 11:  # up to 6 messages can be buffered by discord and people have been dying unfairly because of that

        mine_action = mine_collapse(id_user=cmd.message.author.id, id_server=cmd.guild.id) 
        # user_data
        if mine_action.collapse_penalty != 0.0:
            if user_data.slimes > 1:
                user_data.change_slimes(n=-(user_data.slimes * mine_action.collapse_penalty))
        elif mine_action.hunger_cost_multiplier != 1:
            user_data.hunger += (ewcfg.hunger_permine * mine_action.hunger_cost_multiplier)

        user_data.persist()

        # Don't ratelimit the bot c_c
        if mismined['count'] <= 12 or mismined['count'] % 4 == 0:
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, mine_action.response))

    # Don't ratelimit the bot v_v
    elif mismined['count'] < 2:
        if cause == "exhaustion":
            response = "You've exhausted yourself from mining. You'll need some refreshment before getting back to work."
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
            # Make the new cell the same as the previous cell
            if randomn < 0.15 and j > 0:
                cell = row[-1]
            # Make the new cell the same as the cell "below" it.
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


async def print_grid(cmd, poi, grid_cont):
    # poi = mine_action.user_data.poi
    # id_server = cmd.guild.id

    # if poi in mines_map:
        # grid_map = mines_map.get(poi)
        # if id_server not in grid_map:
        #     init_grid(poi, id_server)
        # grid_cont = grid_map.get(id_server)

    if grid_cont.grid_type == ewcfg.mine_grid_type_minesweeper:
        return await print_grid_minesweeper(cmd, poi, grid_cont)
    elif grid_cont.grid_type == ewcfg.mine_grid_type_bubblebreaker:
        return await print_grid_bubblebreaker(cmd, poi, grid_cont)


async def print_grid_minesweeper(cmd, poi, grid_cont):
    grid_str = ""
    poi = poi
    id_server = cmd.guild.id
    time_now = int(time.time())
    
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


async def print_grid_bubblebreaker(cmd, poi, grid_cont):
    grid_str = ""
    poi = poi
    id_server = cmd.guild.id
    time_now = int(time.time())

    use_emotes = False
    if grid_cont.variation == 1:
        use_emotes = True
    grid = grid_cont.grid

    # grid_str += "   "
    for j in range(len(grid[0])):
        letter = ewcfg.alphabet[j]
        if use_emotes:
            grid_str += ":regional_indicator_{}:".format(letter)
        else:
            grid_str += "{} ".format(letter)
    grid_str += "\n"
    for i in range(len(grid)):
        row = grid[i]
        # if i+1 < 10:
        #	grid_str += " "

        # grid_str += "{} ".format(i+1)
        for j in range(len(row)):
            cell = row[j]
            cell_str = get_cell_symbol_bubblebreaker(cell) + " "
            if use_emotes:
                cell_str = ewcfg.bubble_emote_map.get(cell)
            grid_str += cell_str
        # grid_str += "{}".format(i+1)
        grid_str += "\n"

    # grid_str += "   "
    for j in range(len(grid[0])):
        letter = ewcfg.alphabet[j]
        if use_emotes:
            grid_str += ":regional_indicator_{}:".format(letter)
        else:
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
def check_and_explode(grid, cells_to_check, combo):
    slime_yield = 0
    increase_combo = False

    for coords in cells_to_check:
        bubble = grid[coords[0]][coords[1]]
        if bubble == ewcfg.cell_bubble_empty:
            continue

        bubble_cluster = [coords]
        to_check = [coords]
        globs = []
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
                    if grid[neigh[0]][neigh[1]] == ewcfg.cell_bubble_glob:
                        globs.append(neigh)

            to_check = to_check_next

        if len(bubble_cluster) >= ewcfg.bubbles_to_burst:
            for coord in bubble_cluster:
                grid[coord[0]][coord[1]] = ewcfg.cell_bubble_empty
                slime_yield += (1 * combo)
            for coord in globs:
                grid[coord[0]][coord[1]] = ewcfg.cell_bubble_empty
                slime_yield += (10 * combo)
                combo += 2
            increase_combo = True

    if increase_combo:
        combo += 1

    return slime_yield, combo


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
        # Make the new cell the same as the previous cell
        if randomn < 0.15 and i > 0:
            cell = new_row[-1]
        # Make the new cell the same as the cell "above" it.
        elif randomn < 0.3:
            cell = grid[0][i]
        
        if cell in [ewcfg.cell_bubble_empty, ewcfg.cell_bubble_glob]:
            cell = random.choice(ewcfg.cell_bubbles)
        
        if 0.3 < randomn < 0.31:  # 1% chance
            cell = ewcfg.cell_bubble_glob

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


def get_mining_yield_by_grid_type(cmd, mine_action, grid_cont):
    if grid_cont.grid_type == ewcfg.mine_grid_type_minesweeper:
        return get_mining_yield_minesweeper(cmd, mine_action, grid_cont)
    elif grid_cont.grid_type == ewcfg.mine_grid_type_bubblebreaker:
        return get_mining_yield_bubblebreaker(cmd, mine_action, grid_cont)
    else:
        mine_action.slime_yield = get_mining_yield_default(mine_action.user_data)
        mine_action.valid = True
        return mine_action

def get_mining_yield_minesweeper(cmd, mine_action, grid_cont):
    grid = grid_cont.grid
    row = -1
    col = -1

    if cmd.tokens_count < 2:
        mine_action.response = "Please specify which Minesweeper vein to mine."
        return mine_action

    for token in cmd.tokens[1:]:

        coords = token.lower()
        if coords == "reset":
            # Reset grid and cost hunger
            mine_action.valid = True
            mine_action.hunger_cost_multiplier *= int(ewcfg.hunger_perminereset)
            mine_action.grid_effect = 2
            return mine_action

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
        mine_action.response = "Invalid Minesweeper vein."
        return mine_action
        
    if grid[row][col] in [ewcfg.cell_empty_marked, ewcfg.cell_mine_marked]:
        mine_action.response = "This vein has been flagged as dangerous. Remove the flag to mine here."
        return mine_action

    if grid[row][col] == ewcfg.cell_empty_open:
        mine_action.response = "This vein has already been mined dry."
        return mine_action

    if grid[row][col] == ewcfg.cell_mine:
        # Set a collapse to happen and its properties
        mine_action.valid = True
        mine_action.collapse = True
        mine_action.grid_effect = 2
        # Beginning cell immunity
        if grid_cont.cells_mined <= 1:
            mine_action.collapse_penalty = 0.0
            mine_action.hunger_cost_multiplier = 1
        else:
            mine_action.hunger_cost_multiplier *= int(ewcfg.hunger_perlmcollapse)
            mine_action.collapse_penalty = 0.3


    elif grid[row][col] == ewcfg.cell_empty:
        # Set cell to open and get slime yield
        grid[row][col] = ewcfg.cell_empty_open
        grid_cont.cells_mined += 1
        grid_multiplier = grid_cont.cells_mined ** 0.4        
        mine_action.valid = True
        mine_action.slime_yield = grid_multiplier * 1.7 * get_mining_yield_default(mine_action.user_data)
        mine_action.grid_effect = 1

    # If grid is empty, create a new one
    unmined_cells = get_unmined_cell_count(grid_cont)
    if unmined_cells == 0:
        mine_action.grid_effect = 2

    return mine_action


def get_mining_yield_bubblebreaker(cmd, mine_action, grid_cont):
    grid = grid_cont.grid
    row = -1
    col = -1
    combo = 1
    bubble_add = None
    overlimit = False

    if cmd.tokens_count < 2:
        mine_action.response = "Please specify which Bubble Breaker vein to mine."
        return mine_action

    for token in cmd.tokens[1:]:
        token_lower = token.lower()

        coords = token_lower
        if coords == "reset":
            # Reset grid and cost hunger
            mine_action.valid = True
            mine_action.hunger_cost_multiplier *= int(ewcfg.hunger_perminereset)
            mine_action.grid_effect = 2
            return mine_action
        # Manage switching between numbers and emotes
        if coords in ["fruit", "emote", "fruits", "emotes", "emoji", "emojis"]:
            mine_action.valid = True
            mine_action.grid_effect = 1
            grid_cont.variation = 1
            return mine_action
        if coords in ["number", "numbers", "original", "default"]:
            mine_action.valid = True
            mine_action.grid_effect = 1
            grid_cont.variation = 0
            return mine_action

        if col < 1:
            for char in token_lower:
                if col != -1:
                    break
                if char in ewcfg.alphabet:
                    col = ewcfg.alphabet.index(char)
                    token_lower = token_lower[1:]
        if bubble_add == None:
            bubble = token_lower
            # Change from letter to corresponding number
            if bubble in ewcfg.letter_to_cell.keys():
                bubble = ewcfg.letter_to_cell[bubble]
            if bubble in ewcfg.cell_bubbles:
                bubble_add = bubble

    row = len(grid)
    row -= 1

    if col not in range(len(grid[0])):
        mine_action.response = "Invalid Bubble Breaker vein."
        return mine_action

    if bubble_add == None:
        mine_action.response = "Invalid Bubble Breaker bubble."
        return mine_action


    # If row is full, do overlimit
    if grid[row][col] != ewcfg.cell_bubble_empty:
        overlimit = True
    else:
        grid[row][col] = bubble_add
        mine_action.valid = True    

        # Apply gravity and drop the added bubble
        cells_to_check = apply_gravity(grid)
        cells_to_check.append((row, col))
        slimes_pertile = 1.8 * get_mining_yield_default(mine_action.user_data)
        mine_action.value_mod = 0.0
        
        # Check dropped cell, if exploded re-apply gravity and keep checking cells.
        while len(cells_to_check) > 0:
            bubbles_popped, combo = check_and_explode(grid, cells_to_check, combo)
            mine_action.value_mod += bubbles_popped * (4/17)  # Every 4 !mines, 13 bubbles spawn. Thus, 4/17.
            mine_action.slime_yield += slimes_pertile * bubbles_popped
            mine_action.grid_effect = 1

            cells_to_check = apply_gravity(grid)

        if grid_cont.cells_mined <= 13:
            mine_action.slime_yield /= 2

        grid_cont.cells_mined += 1
        grid_height = get_height(grid)

        # Every 4th bubble, or if the highest part of the grid goes below 5 rows, add a row. If added row goes above limit, do overlimit.
        if grid_cont.cells_mined % 4 == 3 or grid_height < 5:
            if grid_height < len(grid):
                add_row(grid)
            else:
                overlimit = True

    if overlimit:
        # Set a collapse to happen and its properties
        mine_action.valid = True
        mine_action.slime_yield = 0
        mine_action.collapse = True
        mine_action.hunger_cost_multiplier *= int(ewcfg.hunger_perlmcollapse)
        mine_action.collapse_penalty = 0.3
        mine_action.grid_effect = 2

    return mine_action


# Returns an int rather than a class
def get_mining_yield_default(user_data):
    if user_data.poi in [ewcfg.poi_id_mine, ewcfg.poi_id_mine_sweeper, ewcfg.poi_id_mine_bubble]: # JR mines
        slime_yield = 50
    else:
        slime_yield = 200

    if user_data.poi in [ewcfg.poi_id_mine, ewcfg.poi_id_tt_mines, ewcfg.poi_id_cv_mines]: # Spam mines
        slime_yield = int(slime_yield * 1.3)

    return slime_yield


def check_for_minecollapse(cmd, world_events, mine_action):
    for id_event in world_events:

        # Check for minecollapse    
        if world_events.get(id_event) == ewcfg.event_type_minecollapse:
            event_data = EwWorldEvent(id_event=id_event)
            # If the mine collapse corresponds to the user & the location
            if int(event_data.event_props.get('id_user')) == int(mine_action.user_data.id_user) and event_data.event_props.get('poi') == mine_action.user_data.poi:
                captcha = event_data.event_props.get('captcha').upper()
                
                # Check for captcha
                tokens_lower = []
                captcha_count = 0

                for token in cmd.tokens[1:]:
                    tokens_lower.append(token.lower())
                for token in tokens_lower:
                    if token.upper() in ewcfg.captcha_dict:
                        captcha_count += 1

                # If the player enters the right captcha
                if (captcha.lower() in tokens_lower) and captcha_count == 1:
                    if mine_action.toolused == ewcfg.weapon_id_sledgehammer and ewcfg.slimernalia_active:
                        mine_action.valid = True
                        mine_action.collapse = False
                        mine_action.bonus_slime_yield += random.randint(4000, 5000) 
                        mine_action.response = f"You bludgeon the shifting earth around you, keeping the mineshaft intact while exposing pockets of slime.\
                            \nYour reckless mining has gotten you an extra {mine_action.bonus_slime_yield} slime!\n"
                    else:
                        mine_action.valid = True
                        mine_action.collapse = False

                        mine_action.response = "You escape from the collapsing mineshaft."

                    # Delete worldevent - YIKES! I know, but I can't think of a better way to handle these ugly things.
                    bknd_worldevent.delete_world_event(id_event=id_event)
                # Player doesn't enter the right captcha, or !mines normally
                else:
                    if int(event_data.event_props.get('mines')) <= 10:
                        event_data.event_props['mines'] = int(event_data.event_props['mines']) + 1
                        event_data.persist()

                        if int(event_data.event_props.get('mines')) <= 1:
                            mine_action.response = "The mineshaft is collapsing around you!\nGet out of there! (!mine {})\n".format(ewutils.text_to_regional_indicator(event_data.event_props.get('captcha')))

                    else:
                        mine_action.valid = True
                        mine_action.collapse = True
                        mine_action.collapse_penalty = 0.5
                        mine_action.hunger_cost_multiplier *= ewcfg.hunger_perlmcollapse
                        
                        bknd_worldevent.delete_world_event(id_event=id_event)

                continue


def dig_hole(cmd, mine_action, poi):
    
    # Get hole gamestate
    minestate = EwGamestate(id_server=mine_action.user_data.id_server, id_state=poi.mother_districts[0] + 'hole')
    added = random.randint(5, 15)
    checked_dict = digup_relics.get(poi.mother_districts[0])
    # print(checked_dict)
    # Check if you hit an associated relic's depth
    dug_relics = [x for x in checked_dict.keys() if int(minestate.value) <= int(x) <= int(minestate.value) + added]

    if len(dug_relics) > 0:
        props = itm_utils.gen_item_props(relic_map.get(checked_dict.get(dug_relics[0])))
        bknd_item.item_create(
            item_type=ewcfg.it_relic,
            id_user=cmd.message.author.id,
            id_server=cmd.guild.id,
            item_props=props
        )
        mine_action.response += "You ram your shovel back into the ground and hear a CLANK. Oh shit, we got one! You pull out a {}! \n".format(relic_map.get(checked_dict.get(dug_relics[0])).str_name)
    
    # Increment mine depth by random number between 5 and 15
    minestate.value = str(int(minestate.value) + added)
    minestate.persist()



def check_for_mining_world_events(world_events, mine_action):

    for id_event in world_events:        
        
        # Double slimegain
        if world_events.get(id_event) == ewcfg.event_type_slimefrenzy:
            event_data = EwWorldEvent(id_event=id_event)
            if event_data.event_props.get('poi') == mine_action.user_data.poi and int(event_data.event_props.get('id_user')) == int(mine_action.user_data.id_user):
                mine_action.slime_yield *= 2

        # Get a poudrin every !mine
        elif world_events.get(id_event) == ewcfg.event_type_poudrinfrenzy:
            event_data = EwWorldEvent(id_event=id_event)
            if event_data.event_props.get('poi') == mine_action.user_data.poi and int(event_data.event_props.get('id_user')) == int(mine_action.user_data.id_user):
                mine_action.unearthed_item_chance = 1
                mine_action.unearthed_item_amount = 1
            
        # Get a poudrin or bone every !mine
        elif world_events.get(id_event) == ewcfg.event_type_spookyskeleton:
            event_data = EwWorldEvent(id_event=id_event)
            if event_data.event_props.get('poi') == mine_action.user_data.poi and int(event_data.event_props.get('id_user')) == int(mine_action.user_data.id_user):
                mine_action.unearthed_item_chance = 1
                mine_action.unearthed_item_amount = 1
                # Set the item pool to skeleton
                mine_action.unearthed_item_type = "skeleton"

        # Triple slimegain and ectoplasm every !mine
        elif world_events.get(id_event) == ewcfg.event_type_spookyghost:
            event_data = EwWorldEvent(id_event=id_event)
            if event_data.event_props.get('poi') == mine_action.user_data.poi and int(event_data.event_props.get('id_user')) == int(mine_action.user_data.id_user):
                mine_action.slime_yield *= 3
                mine_action.unearthed_item_chance = .85
                mine_action.unearthed_item_amount = 1
                # Set the item pool to ghost
                mine_action.unearthed_item_type = "ghost"

        # Halve hunger cost
        elif world_events.get(id_event) == ewcfg.event_type_gas_leak:
            event_data = EwWorldEvent(id_event=id_event)
            if event_data.event_props.get('poi') == mine_action.user_data.poi:
                mine_action.hunger_cost_multiplier /= 2



def create_mining_event(cmd, mine_action, mutations, grid_type):
    event_chance = 0.04 * mine_action.value_mod  # base chance

    # If the probability is not 0
    if event_chance != 0.0:
        # If user is a juvie/has a pickaxe, flat +0.5%. If user has Lucky, flat +0.5%. If a user has Light Miner, flat +0.25%
        if mine_action.toolused == "pickaxe" or mine_action.user_data.life_state == ewcfg.life_state_juvenile:
            event_chance += 0.005
        if ewcfg.mutation_id_lucky in mutations:
            event_chance += 0.005
        if ewcfg.mutation_id_lightminer in mutations:
            event_chance += 0.0025

    if random.random() < event_chance:
        randomn = random.random()
        time_now = int(time.time())
        mine_district_data = EwDistrict(district=mine_action.user_data.poi, id_server=mine_action.user_data.id_server)

        life_states = [ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]
        num_miners = len(mine_district_data.get_players_in_district(life_states=life_states, ignore_offline=True))

        # To be safe
        if num_miners == 0:
            num_miners = 1

        common_event_chance = 0.7  # 7/10, not used
        uncommon_event_chance = 0.3  # 3/10
        rare_event_chance = 0.05 / num_miners  #  1/2 usual chance for 2 miners, 1/3 for 3 miners etc.
        event_type = ""

        common_event_triggered = False
        uncommon_event_triggered = False
        rare_event_triggered = False

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
            if mine_action.toolused == ewcfg.weapon_id_sledgehammer and ewcfg.slimernalia_active:
                event_type = ewcfg.event_type_minecollapse
            elif randomn < 0.5:
                event_type = ewcfg.event_type_slimeglob  # 4x glob of slime
            else:
                event_type = ewcfg.event_type_slimefrenzy  # 30 second slimefrenzy

        # uncommon event
        elif uncommon_event_triggered:
            randomn = random.random()
            # mine shaft collapse
            if randomn < 0.45:
                event_type = ewcfg.event_type_minecollapse
            elif randomn < 0.9:
                event_type = ewcfg.event_type_poudrinfrenzy  # 5 second poudrin frenzy
            else:
                event_type = ewcfg.event_type_poudringlob  # 3-6 poudrins

        # rare event
        elif rare_event_triggered:
            randomn = random.random()
            if randomn < 0.5:
                event_type = ewcfg.event_type_voidhole  # gap into the void
            elif randomn < 0.75:
                event_type = ewcfg.event_type_spookyskeleton  # 15 second mine poudrins and bones
            else:
                event_type = ewcfg.event_type_spookyghost  # 15 second triple slime and mine ectoplasm


        if event_type != "":
            # Correct from time-based spam events to individual events in MS and BB
            if grid_type in [ewcfg.mine_grid_type_bubblebreaker, ewcfg.mine_grid_type_minesweeper]:  
                if event_type in [ewcfg.event_type_spookyghost]:  # slime-focused
                    event_type = ewcfg.event_type_slimeglob
                elif event_type in [ewcfg.event_type_poudrinfrenzy, ewcfg.event_type_spookyskeleton]:  # poudrin-focused
                    event_type = ewcfg.event_type_poudringlob

            if event_type == ewcfg.event_type_slimeglob:  # Slime glob isn't a worldevent
                mine_action.slime_yield *= 4
                mine_action.response += "You mined an extra big glob of slime! {}\n".format(ewcfg.emote_slime1)

            elif event_type == ewcfg.event_type_poudringlob:  # Poudrin glob isn't a worldevent
                mine_action.unearthed_item_chance = 1
                mine_action.unearthed_item_amount = random.randrange(3, 6) 
                mine_action.response += "You mine into an underground vein! "                
            
            else:
                event_props = {}
                # Time table for how many seconds events should last
                event_to_time = {
                    ewcfg.event_type_slimefrenzy: 30,
                    ewcfg.event_type_minecollapse: 60,
                    ewcfg.event_type_poudrinfrenzy: 5,
                    ewcfg.event_type_voidhole: 30,
                    ewcfg.event_type_spookyskeleton: 15,
                    ewcfg.event_type_spookyghost: 15,
                }

                # Get the expiry time and event definition
                time_expir = time_now + event_to_time.get(event_type)
                event_def = poi_static.event_type_to_def.get(event_type)
                str_event_start = event_def.str_event_start

                # Create generic event props
                event_props['id_user'] = cmd.message.author.id
                event_props['poi'] = mine_action.user_data.poi
                event_props['channel'] = cmd.message.channel.name

                # Create mine collapse-specific props
                if event_type == ewcfg.event_type_minecollapse:
                    event_props['captcha'] = ewutils.generate_captcha(length=8, user_data=mine_action.user_data)
                    event_props['mines'] = 0
                    str_event_start = str_event_start.format(cmd=ewcfg.cmd_mine, captcha=ewutils.text_to_regional_indicator(event_props.get('captcha')))

                # Create the world event
                bknd_worldevent.create_world_event(
                    id_server=cmd.guild.id,
                    event_type=event_type,
                    time_activate=time_now,
                    time_expir=time_expir,
                    event_props=event_props
                )
                
                # Add event creation to the !mine response
                mine_action.response += str_event_start + "\n"


def unearth_item(cmd, mine_action, mutations):

    # Unearth item check        
    if random.random() < mine_action.unearthed_item_chance:
        unearth_icon = ""

        # If there are multiple possible products, randomly select one.
        if mine_action.unearthed_item_type == "ghost":
            item = random.choice([static_items.item_map.get('ectoplasm')])
        elif mine_action.unearthed_item_type == "skeleton":
            item = random.choice(vendors.mine_results + [static_items.item_map.get('bone')])
        else:
            item = random.choice(vendors.mine_results)
        
        if mine_action.unearthed_item_amount == 0:
            mine_action.unearthed_item_amount = 1


        # If the player has inventory capacity, create unearthed items
        if bknd_item.check_inv_capacity(user_data=mine_action.user_data, item_type=item.item_type):

            item_props = itm_utils.gen_item_props(item)

            for creation in range(mine_action.unearthed_item_amount):
                bknd_item.item_create(
                    item_type=item.item_type,
                    id_user=cmd.message.author.id,
                    id_server=cmd.guild.id,
                    item_props=item_props
                )

            # Change POUDRINING stat, add poudrin icon
            if item.str_name == "Slime Poudrin":
                ewstats.change_stat(user=mine_action.user_data, metric=ewcfg.stat_lifetime_poudrins, n=mine_action.unearthed_item_amount)
                unearth_icon = ewcfg.emote_poudrin

            # Give correct response
            if mine_action.unearthed_item_type != "":
                mine_action.response += "You {} {} {} out of the {}! {}\n".format(random.choice(["beat", "smack", "strike", "!mine", "brutalize"]), mine_action.unearthed_item_amount, item.str_name, mine_action.unearthed_item_type, unearth_icon)
            elif mine_action.unearthed_item_amount == 1:
                mine_action.response += "You unearthed a {}! {}\n".format(item.str_name, unearth_icon)
            else:
                mine_action.response += "You unearthed {} {}s! {}\n".format(mine_action.unearthed_item_amount, item.str_name, unearth_icon)



# Run lightminer and big john checks
def mine_collapse(mine_action=None, mutations=None, id_user=None, id_server=None): 
    # If id_user and id_server were given, get user_data and mutations
    if mine_action == None and id_user != None and id_server != None:
        user_data = EwUser(id_user=id_user, id_server=id_server)
        mutations = user_data.get_mutations()
        
        mine_action = EwMineAction(user_data=user_data,
                                   response="",
                                   collapse_penalty=0.5,
                                   hunger_cost_multiplier=ewcfg.hunger_perlmcollapse,
        )

    # 1/4 chance for Big John and no penalty
    if random.randrange(4) == 0:
        collapse_response = "Big John arrives just in time to save you from your mining accident!\nhttps://cdn.discordapp.com/attachments/431275470902788107/743629505876197416/mine2.jpg\n"
        mine_action.hunger_cost_multiplier = 1
        mine_action.collapse_penalty = 0.0
    else:
        # If Light Miner, set slime penalty to 0. Otherwise, set hunger penalty to 0.
        if ewcfg.mutation_id_lightminer in mutations:
            collapse_response = "You instinctively jump out of the way of the live mine, barely escaping with your life. Whew, really gets your blood pumping.\n"
            mine_action.collapse_penalty = 0.0
        else:
            collapse_response = "You have lost an arm and a leg in a mining accident. 'Tis but a scratch.\n"
            mine_action.hunger_cost_multiplier = 1

    mine_action.response += collapse_response

    return mine_action

    




def gen_scavenge_captcha(n = 0, user_data = None):
    captcha_length = math.ceil(n / 3)

    return ewutils.generate_captcha(length=captcha_length, user_data=user_data)
