import datetime
import math
import random
import re
import string
import time

from sys import getsizeof, stderr
from itertools import chain

import discord

from ..backend import core as bknd_core
from ..static import cfg as ewcfg
from ..static import mutations as static_mutations
from ..static import poi as poi_static
from ..static import weather as weather_static
try:
    from . import rutils as rutils
except:
    from . import rutils_dummy as rutils


TERMINATE = False
DEBUG = False

DEBUG_OPTIONS = {
    'no_race_cooldown': False,
    'duperelics': False,
    'speed2x': False,
    'lightspeed': False,
    'verbose_burn': False,
    'alternate_talk':False,
    'transport': False,
}

# Map of user IDs to their course ID.
moves_active = {}

last_warps = {}

food_multiplier = {}

# Contains who players are trading with and the state of the trades
active_trades = {}
# Contains the items being offered by players
trading_offers = {}

# Map of users to their target. This includes apartments, potential Russian Roulette players, potential Slimeoid Battle players, etc.
active_target_map = {}
# Map of users to their restriction level, typically in a mini-game. This prevents people from moving, teleporting, boarding, retiring, or suiciding in Russian Roulette/Duels
active_restrictions = {}

# Map of users that have their butthole clenched
clenched = {}

# When using SSOD, adjusted paths are listed here.
path_ssod = {}

active_slimeoidbattles = {}

active_televisions = {}

tv_counter = 0


conversations = {}

square_duel = 0

class EwVector2D:
    vector = [0, 0]

    def __init__(self, vector):
        self.vector = vector

    def scalar_product(self, other_vector):
        result = 0

        for i in range(2):
            result += self.vector[i] * other_vector.vector[i]

        return result

    def add(self, other_vector):
        result = []

        for i in range(2):
            result.append( self.vector[i] + other_vector.vector[i] )

        return EwVector2D(result)

    def subtract(self, other_vector):
        result = []

        for i in range(2):
            result.append( self.vector[i] - other_vector.vector[i] )

        return EwVector2D(result)

    def norm (self):
        result = self.scalar_product(self)
        result = result ** 0.5
        return result

    def normalize(self):
        result = []

        norm = self.norm()

        if norm == 0:
            return EwVector2D([0, 0])

        for i in range(2):
            result.append(round(self.vector[i] / norm, 3))

        return EwVector2D(result)


def logMsg(string):
    """ Write the string to stdout with a timestamp. """
    print("[{}] {}".format(datetime.datetime.now(), string))

    return string


def getValueFromFileContents(fname):
    """ Read a file named fname and return its contents as a string """
    token = ""

    try:
        f_token = open(fname, "r")
        f_token_lines = f_token.readlines()

        for line in f_token_lines:
            line = line.rstrip()
            if len(line) > 0:
                token = line
    except IOError:
        token = ""
        print("Could not read {} file.".format(fname))
    finally:
        f_token.close()

    return token


def getToken():
    """ Returns the Discord API token from the config file on disk """
    return getValueFromFileContents("token")


def formatNiceList(names=[], conjunction="and"):
    """ Return a string made from a list of strings with nice commas and grammar """
    l = len(names)

    if l == 0:
        return ''

    if l == 1:
        return names[0]

    return ', '.join(names[0:-1]) + '{comma} {conj} '.format(comma=(',' if l > 2 else ''), conj=conjunction) + names[-1]


def formatNiceTime(seconds=0, round_to_minutes=False, round_to_hours=False) -> str:
    """ Return a timestamp with nice commas and grammer. """
    try:
        seconds = int(seconds)
    except:
        seconds = 0

    if round_to_minutes:
        minutes = round(seconds / 60)
    else:
        minutes = int(seconds / 60)

    if round_to_hours:
        hours = round(minutes / 60)
    else:
        hours = int(minutes / 60)

    minutes = minutes % 60
    seconds = seconds % 60
    time_tokens = []
    if hours > 0:
        if hours == 1:
            token_hours = "1 hour"
        else:
            token_hours = "{} hours".format(hours)
        time_tokens.append(token_hours)

    if round_to_hours:
        if len(time_tokens) == 0:
            time_tokens.append("0 hours")
        return formatNiceList(names = time_tokens, conjunction = "and")

    if minutes > 0:
        if minutes == 1:
            token_mins = "1 minute"
        else:
            token_mins = "{} minutes".format(minutes)
        time_tokens.append(token_mins)

    if round_to_minutes:
        if len(time_tokens) == 0:
            time_tokens.append("0 minutes")
        return formatNiceList(names = time_tokens, conjunction = "and")

    if seconds > 0:
        if seconds == 1:
            token_secs = "1 second"
        else:
            token_secs = "{} seconds".format(seconds)
        time_tokens.append(token_secs)

    if len(time_tokens) == 0:
        time_tokens.append("0 seconds")
    return formatNiceList(names = time_tokens, conjunction = "and")


def weightedChoice(weight_map):
    """ weighted choice. takes a dict of element -> weight and returns a random element """
    weight_sum = 0
    elem_list = []
    weight_sums = []
    for elem in weight_map:
        weight_sum += weight_map.get(elem)
        elem_list.append(elem)
        weight_sums.append(weight_sum)

    rand = random.random() * weight_sum

    for i in range(len(weight_sums)):
        weight = weight_sums[i]
        if rand < weight:
            return elem_list[i]


def userListToNameString(list_user) -> str:
    """ Return a nice list of user names from a list of discord Members """
    names = []

    for user in list_user:
        names.append(user.display_name)

    return formatNiceList(names)


def getRoleMap(roles) -> dict:
    """ Returns a map of name -> role from a list of roles """
    roles_map = {}

    for role in roles:
        roles_map[mapRoleName(role.name)] = role

    return roles_map


def getRoleIdMap(roles) -> dict:
    """ Returns a map of id -> role from a list of roles """
    roles_map = {}

    for role in roles:
        roles_map[mapRoleName(role.id)] = role

    return roles_map


def mapRoleName(roleName) -> str:
    """ Returns canonical lowercase no space name for a role """
    if type(roleName) == int:
        return roleName
    return roleName.replace(" ", "").lower()


def getIntToken(tokens = [], allow_all = False, negate = False) -> int:
    """ Parse a list of tokens and return an integer value. If allow_all, return -1 if the word 'all' is present. """
    value = None

    for token in tokens[1:]:
        try:
            value = int(token.replace(",", ""))
            if value < 0 and not negate:
                value = None
            elif value > 0 and negate:
                value = None
            elif negate:
                value = -value
            break
        except:
            if allow_all and ("{}".format(token)).lower() == 'all':
                return -1
            else:
                value = None

    return value


def weaponskills_get(id_server=None, id_user=None, member=None) -> dict:
    """ Return a map of weapon skills for the specified player. {weaponskill -> int} """

    weaponskills = {}

    if member:
        id_server = member.guild.id
        id_user = member.id

    data = bknd_core.execute_sql_query("SELECT {weapon}, {weaponskill} FROM weaponskills WHERE {id_server} = %s AND {id_user} = %s".format(
        weapon=ewcfg.col_weapon,
        weaponskill=ewcfg.col_weaponskill,
        id_server=ewcfg.col_id_server,
        id_user=ewcfg.col_id_user
    ), (
        id_server,
        id_user
    ))

    if data:
        for row in data:
            weaponskills[row[0]] = row[1]

    return weaponskills


def weaponskills_set(id_server=None, id_user=None, member=None, weapon=None, weaponskill=0):
    """ Set an individual weapon skill value for a player. """
    if member:
        id_server = member.guild.id
        id_user = member.id

    bknd_core.execute_sql_query("REPLACE INTO weaponskills({id_server}, {id_user}, {weapon}, {weaponskill}) VALUES(%s, %s, %s, %s)".format(
        id_server=ewcfg.col_id_server,
        id_user=ewcfg.col_id_user,
        weapon=ewcfg.col_weapon,
        weaponskill=ewcfg.col_weaponskill
    ), (
        id_server,
        id_user,
        weapon,
        weaponskill
    ))


def weaponskills_clear(id_server=None, id_user=None, member=None, weaponskill=None):
    """ Clear all weapon skills for a player (probably called on death). """
    if member:
        id_server = member.guild.id
        id_user = member.id

    # Clear any records that might exist.
    bknd_core.execute_sql_query(
        "UPDATE weaponskills SET {weaponskill} = %s WHERE {weaponskill} > %s AND {id_server} = %s AND {id_user} = %s".format(
            weaponskill=ewcfg.col_weaponskill,
            id_server=ewcfg.col_id_server,
            id_user=ewcfg.col_id_user

        ), (
            weaponskill,
            weaponskill,
            id_server,
            id_user
        ))


re_flattener = re.compile("[ '\"!@#$%^&*().,/?{}\[\];:]")


def flattenTokenListToString(tokens, keepPunctuation=0) -> str:
    """ Return a single word (no spaces or punctuation) with all lowercase letters from an array of tokens. """
    global re_flattener
    target_name = ""

    if type(tokens) == list:
        for token in tokens:
            if keepPunctuation == 1 and token.startswith('<@') == False:
                target_name += token.lower().replace(" ", "")
            elif not token.startswith('<@'):
                target_name += re_flattener.sub("", token.lower())
    elif keepPunctuation == 1 and tokens.startswith('<@') == False:
        target_name = tokens.lower().replace(" ", "")
    elif not tokens.startswith('<@'):
        target_name = re_flattener.sub("", tokens.lower())

    return target_name


def get_faction(user_data=None, life_state=0, faction="") -> str:
    """ Return the role name of a user's faction. Takes user data object or life_state and faction tag """

    if user_data:
        life_state = user_data.life_state
        faction = user_data.faction

    faction_role = ewcfg.role_corpse

    if life_state == ewcfg.life_state_juvenile or life_state == ewcfg.life_state_vigilante:
        faction_role = ewcfg.role_juvenile

    elif life_state == ewcfg.life_state_enlisted:
        if faction == ewcfg.faction_killers:
            faction_role = ewcfg.role_copkillers

        elif faction == ewcfg.faction_rowdys:
            faction_role = ewcfg.role_rowdyfuckers

        elif faction == ewcfg.faction_slimecorp:
            faction_role = ewcfg.role_slimecorp

        else:
            faction_role = ewcfg.role_juvenile

    elif life_state == ewcfg.life_state_kingpin:

        if faction == ewcfg.faction_killers:
            faction_role = ewcfg.role_copkiller
        elif faction == ewcfg.faction_rowdys:
            faction_role = ewcfg.role_rowdyfucker

    elif life_state == ewcfg.life_state_grandfoe:
        faction_role = ewcfg.role_grandfoe

    elif life_state == ewcfg.life_state_executive:
        faction_role = ewcfg.role_executive

    elif life_state == ewcfg.life_state_lucky:
        faction_role = ewcfg.role_executive

    return faction_role


def get_faction_symbol(faction_role="", lifestate="") -> str:
    """ Returns faction-specific emote based on faction role strings or user_data lifestates """
    result = None

    # Special lifestate symbols
    if lifestate == ewcfg.life_state_kingpin:
        if lifestate == ewcfg.faction_rowdys:
            result = ewcfg.emote_rowdyfucker
        elif lifestate == ewcfg.faction_killers:
            result = ewcfg.emote_copkiller
    elif lifestate == ewcfg.life_state_corpse:
        result = ewcfg.emote_ghost
    elif lifestate == ewcfg.life_state_juvenile:
        result = ewcfg.emote_slime3

    if result is None:
        if faction_role == ewcfg.role_copkillers:
            result = ewcfg.emote_ck
        elif faction_role == ewcfg.role_rowdyfuckers:
            result = ewcfg.emote_rf
        elif faction_role == ewcfg.role_slimecorp:
            result = ewcfg.emote_slimecorp
        else:
            result = ewcfg.emote_blank

    return result


def slime_bylevel(slimelevel) -> int:
    """ Calculate the slime amount needed to reach a certain level """
    return int(slimelevel ** 4)


def level_byslime(slime) -> int:
    """ Calculate what level the player should be at, given their slime amount """
    return int(abs(slime) ** 0.25)


def sap_max_bylevel(slimelevel) -> int:
    """ Calculate the maximum sap amount a player can have at their given slime level """
    return int(1.6 * slimelevel ** 0.75)


def hunger_max_bylevel(slimelevel, has_bottomless_appetite=0) -> int:
    """ Calculate the maximum hunger level at the player's slimelevel """
    mult = 1
    if has_bottomless_appetite == 1:
        mult = 2
    return max(ewcfg.min_stamina, slimelevel ** 2) * mult


def hunger_cost_mod(slimelevel) -> int:
    """ Calculate how much more stamina activities should cost """
    return hunger_max_bylevel(slimelevel) // 200


def food_carry_capacity_bylevel(slimelevel) -> int:
    """ Calculate how much food the player can carry """
    return math.ceil(slimelevel / ewcfg.max_food_in_inv_mod)


def weapon_carry_capacity_bylevel(slimelevel) -> int:
    """ Calculate how many weapons the player can carry """
    return math.floor(slimelevel / ewcfg.max_weapon_mod) + 1


def max_adornspace_bylevel(slimelevel) -> int:
    """ Calculates how many cosmetics the player can adorn """
    if slimelevel < 4:
        adorn_space = 0
    else:

        adorn_space = math.floor(math.sqrt(slimelevel - 2) - 0.40)

    return adorn_space


def get_client() -> discord.Client:
    """ Returns the discord Client the bot is running on """
    return ewcfg.get_client()


def get_slimeoids_in_poi(id_server=None, poi=None, sltype=None) -> list:
    """ Returns a list of slimeoid ids in the district """
    slimeoids = []
    if id_server is None:
        return slimeoids

    query = "SELECT {id_slimeoid} FROM slimeoids WHERE {id_server} = %s".format(
        id_slimeoid=ewcfg.col_id_slimeoid,
        id_server=ewcfg.col_id_server
    )

    if sltype is not None:
        query += " AND {} = '{}'".format(ewcfg.col_type, sltype)

    if poi is not None:
        query += " AND {} = '{}'".format(ewcfg.col_poi, poi)

    data = bknd_core.execute_sql_query(query, (
        id_server,
    ))

    for row in data:
        slimeoids.append(row[0])

    return slimeoids


def number_civilians(id_server):
    query = bknd_core.execute_sql_query("SELECT COUNT(*) from enemies where enemytype in ('civilian', 'innocent') and id_server = id_server")
    for counts in query:
        if counts[0] < 20:
            return 1
        else:
            return 0


def is_otp(user_data):
    poi = poi_static.id_to_poi.get(user_data.poi)
    return user_data.poi not in [ewcfg.poi_id_thesewers, ewcfg.poi_id_juviesrow, ewcfg.poi_id_copkilltown, ewcfg.poi_id_rowdyroughhouse] and (not poi.is_apartment)


def check_accept_or_refuse(string):
    if string.content.lower() == ewcfg.cmd_accept or string.content.lower() == ewcfg.cmd_refuse:
        return True


def check_confirm_or_cancel(string):
    if string.content.lower() == ewcfg.cmd_confirm or string.content.lower() == ewcfg.cmd_cancel:
        return True


def check_trick_or_treat(string):
    if string.content.lower() == ewcfg.cmd_treat or string.content.lower() == ewcfg.cmd_trick:
        return True


def check_is_command(string):
    if string.content.startswith(ewcfg.cmd_prefix):
        return True


def end_trade(id_user):
    # Cancel an ongoing trade
    if active_trades.get(id_user) != None and len(active_trades.get(id_user)) > 0:
        trader = active_trades.get(id_user).get("trader")

        active_trades[id_user] = {}
        active_trades[trader] = {}

        trading_offers[trader] = []
        trading_offers[id_user] = []


def calc_half_life(user_data):

    relative_level = rutils.debug36(user_data)
    # relative_level = level_byslime(user_data.slimes) - 54
    
    if relative_level > 0:
        return (60 * 60 * 24 * 14) / relative_level
    else:
        return 60 * 60 * 24 * 14  # standard slime half life


def text_to_regional_indicator(text):
    """ Note that inside the quotes below is a zero-width space,
    used to prevent the regional indicators from turning into flags.
    Also note that this only works for digits and english letters """

    return "‎".join([c + '\ufe0f\u20e3' if c.isdigit() else chr(0x1F1E6 + string.ascii_uppercase.index(c)) for c in text.upper()])


def generate_captcha_random(length=4):
    return "".join([random.choice(ewcfg.alphabet) for _ in range(length)]).upper()


def generate_captcha(length = 4, user_data = None):
    length_final = length
    if user_data is not None:
        mutations = user_data.get_mutations()
        if ewcfg.mutation_id_dyslexia in mutations:
            length_final = max(1, length_final - 1)
    try:
        return random.choice([captcha for captcha in ewcfg.captcha_dict if len(captcha) == length_final])
    except:
        return generate_captcha_random(length=length_final)


def check_moon_phase(market_data):
    # Get the current day, accounting for the morning wrapping around
    day = market_data.day % 29
    if market_data.clock < 6:
        day -= 1
        if day == -1:
            day = 28

    # Get current moon phase.
    if day == 0:  # 1 night of the new moon
        moon_phase = ewcfg.moon_new
    elif day <= 6:  # 6 of waxing first half
        moon_phase = ewcfg.moon_waxing_start
    elif day <= 12:  # 6 of waxing second half
        moon_phase = ewcfg.moon_waxing_end
    elif day <= 14:  # 2 of full moon
        moon_phase = ewcfg.moon_full
    elif day <= 20:  # 6 of waning first half
        moon_phase = ewcfg.moon_waning_start
    elif day <= 26:  # 6 of waning second half
        moon_phase = ewcfg.moon_waning_end
    elif day <= 27:  # 1 of new moon
        moon_phase = ewcfg.moon_new
    else:  # inbetween the 2 nights of the new moon, have a Green Moon night.
        moon_phase = ewcfg.moon_special

    # Add "day" to the end of the string if it's daytime. Will stop any checks that don't specify for day, but can include if specified.
    if market_data.clock >= 6 and market_data.clock < 20:
        moon_phase += "day"

    return moon_phase


# Get the player with the most festivity
def get_most_festive(server):
    # New coolness
    data = bknd_core.execute_sql_query(

        "SELECT {id_user}, {stat_value} from stats where {stat_metric} = %s AND {id_server} = %s ORDER BY {stat_value} DESC LIMIT 1".format(

            id_user=ewcfg.col_id_user,
            stat_value=ewcfg.col_stat_value,
            stat_metric=ewcfg.col_stat_metric,
            id_server=ewcfg.col_id_server
        ), (
            ewcfg.stat_festivity,
            server.id
        )
    )
    return data[0][0]


def calculatePvpTimer(current_time_expirpvp, timer, enlisted = False):
    """ Returns the latest value, so that short PvP timer actions don't shorten remaining PvP time. """
    if enlisted:
        timer *= 1

    desired_time_expirpvp = int(time.time()) + timer

    if desired_time_expirpvp > current_time_expirpvp:
        return desired_time_expirpvp

    return current_time_expirpvp


def channel_name_is_poi(channel_name):
    """ Returns true if the specified name is used by any POI. -thats not what this does """
    if channel_name:
        return channel_name in poi_static.chname_to_poi

    return False


def mention_type(cmd, ew_id):
    if cmd.client_id.user == ew_id.user:
        return "ew"
    elif cmd.author_id.user == ew_id.user:
        return "self"
    else:
        return "other"


def get_mutation_alias(name):
    if static_mutations.mutations_map.get(name) != None:
        return name
    else:

        for mutation in static_mutations.mutations_map:
            for alias in static_mutations.mutations_map.get(mutation).alias:
                if name == alias:
                    return mutation
        return 0


def messagesplit(stringIn, whitespace = '\n'):
    currentMessage = stringIn
    messagearray = []
    while len(currentMessage) > 1500:
        index = currentMessage.rfind(whitespace, 0, 1500)
        messagearray.append(currentMessage[:index])
        currentMessage = currentMessage[index:]

    messagearray.append(currentMessage)
    return messagearray


def is_player_inventory(id_inventory, id_server):
    """
        Return true if inventory has associated User table entry
        and a member object from selected server.
        Member ensures they are present in game.
    """
    if id_server is None or id_inventory is None:
        return False

    if isinstance(id_inventory, int):
        pass
    elif not id_inventory.isdigit():
        return False

    # Grab the Discord Client
    client = get_client()
    discord_result = client.get_guild(id_server).get_member(id_inventory)

    # Try to grab a value from a user with given id
    db_result = bknd_core.execute_sql_query("SELECT {} FROM users WHERE id_user = %s AND id_server = %s".format(
        ewcfg.col_rand_seed
    ), (
        id_inventory,
        id_server
    ))

    if db_result and discord_result:
        return True
    else:
        return False


def weather_txt(market_data):
    response = ""
    time_current = market_data.clock
    displaytime = str(time_current)
    ampm = ''

    # Get the text for the display time in 12-hour time
    if time_current <= 12:
        ampm = 'AM'
    if time_current > 12:
        displaytime = str(time_current - 12)
        ampm = 'PM'

    # If it's noon or midnight, display that special text.
    if time_current == 0:
        displaytime = 'midnight'
        ampm = ''
    if time_current == 12:
        displaytime = 'high noon'
        ampm = ''

    # Get flavor text for the weather and corresponding time of day.
    flair = ''
    weather_data = weather_static.weather_map.get(market_data.weather)
    if weather_data != None:
        if time_current >= 6 and time_current <= 7:
            flair = weather_data.str_sunrise
        if time_current >= 8 and time_current <= 17:
            flair = weather_data.str_day
        if time_current >= 18 and time_current <= 19:
            flair = weather_data.str_sunset
        if time_current >= 20 or time_current <= 5:
            moonphase = check_moon_phase(market_data)
            # If it's nighttime, get the moon phase that corresponds with the weather.
            if moonphase == ewcfg.moon_new:
                flair = weather_data.str_night_new
            elif moonphase == ewcfg.moon_waxing_start:
                flair = weather_data.str_night_waxing_start
            elif moonphase == ewcfg.moon_waxing_end:
                flair = weather_data.str_night_waxing_end
            elif moonphase == ewcfg.moon_full:
                flair = weather_data.str_night_full
            elif moonphase == ewcfg.moon_waning_start:
                flair = weather_data.str_night_waning_start
            elif moonphase == ewcfg.moon_waning_end:
                flair = weather_data.str_night_waning_end
            else:
                flair = weather_data.str_night_special

    response += "It is currently {}{} in NLACakaNM.{}".format(displaytime, ampm, (' ' + flair))
    return response


def total_size(o, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.
    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, dict, set and frozenset.
    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


def is_district_empty(poi = ''):  # quick function to check presence in a district
    time_now = int(time.time())
    data = bknd_core.execute_sql_query('SELECT {id_user} FROM users WHERE {poi} = %s and ({time_last_action} > %s or {time_last_enter} > %s) LIMIT 1'.format(
        poi=ewcfg.col_poi,
        id_user=ewcfg.col_id_user,
        time_last_action=ewcfg.col_time_last_action,
        time_last_enter = ewcfg.col_time_lastenter),
        (poi, time_now-120, time_now-120))
    if len(data) > 0:
        return False
    else:
        return True
