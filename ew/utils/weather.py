import asyncio
import random
import time

from . import core as ewutils
from .combat import EwEnemy
from .combat import EwUser
from .district import EwDistrict
from .frontend import EwResponseContainer
from .slimeoid import EwSlimeoid
from ..backend import core as bknd_core
from ..backend import hunting as bknd_hunt
from ..backend import item as bknd_item
from ..backend import worldevent as bknd_worldevent
from ..backend.item import EwItem
from ..backend.market import EwMarket
from ..backend.player import EwPlayer
from ..static import cfg as ewcfg
from ..static import community_cfg as comm_cfg
from ..static import poi as poi_static
from ..static import weather as weather_static
from ..static import weapons as weapons_static
from ..static import items as items_static
from ..utils import frontend as fe_utils
from ..utils import rolemgr as ewrolemgr
from ..utils import item as item_utils
from ..cmd.move.movecmds import one_eye_dm

try:    
    from ew.utils import rutils 
except:
    from ew.utils import rutils_dummy as rutils

"""
	Coroutine that continually calls weather_tick; is called once per server, and not just once globally
"""


async def weather_tick_loop(id_server):
    interval = ewcfg.weather_tick_length
    while not ewutils.TERMINATE:
        await asyncio.sleep(interval)
        await weather_tick(id_server=id_server)


""" Bleed slime for all users """


async def weather_tick(id_server = None):
    if id_server != None:
        try:
            market_data = EwMarket(id_server=id_server)
            
            if market_data.weather == ewcfg.weather_sunny:
                exposed_pois = []
                exposed_pois.extend(poi_static.capturable_districts)
                exposed_pois.extend(poi_static.outskirts)
                exposed_pois = tuple(exposed_pois)

                users = bknd_core.execute_sql_query(
                    "SELECT id_user FROM users WHERE id_server = %s AND {poi} IN %s AND {life_state} > 0".format(
                        poi=ewcfg.col_poi,
                        life_state=ewcfg.col_life_state
                    ), (
                        id_server,
                        exposed_pois

                    ))
                for user in users:
                    try:
                        user_data = EwUser(id_user=user[0], id_server=id_server)
                        if user_data.life_state == ewcfg.life_state_kingpin:
                            continue
                        else:
                            mutations = user_data.get_mutations()
                            if ewcfg.mutation_id_airlock in mutations or ewcfg.mutation_id_monplanto in mutations:
                                user_data.hunger -= min(user_data.hunger, 5)
                    except:
                        ewutils.logMsg("Error occurred in weather tick for server {}".format(id_server))

            client = ewutils.get_client()
            world_events = bknd_worldevent.get_world_events(id_server=id_server, active_only=True)
            resp_cont_poi_event = EwResponseContainer(client=client, id_server=id_server)

            # For all presently-happening world events
            for id_event in world_events:
                # If the world event has an effect corresponding to a weather tick
                if world_events.get(id_event) in [ewcfg.event_type_firestorm, ewcfg.event_type_tornado, ewcfg.event_type_poudrin_hail, ewcfg.event_type_meteor_shower, ewcfg.event_type_jape_storm]:
                    # Get the EVENT DATA
                    event_data = bknd_worldevent.EwWorldEvent(id_event=id_event)
                    
                    # If the event is a firestorm
                    if event_data.event_type == ewcfg.event_type_firestorm:
                        district = event_data.event_props.get('poi')
                        district_data = EwDistrict(district=district, id_server=id_server)
                        players = district_data.get_players_in_district(life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]) # Ghosts can't get set on fire ):
                        # For all the players in the district of the firestorm
                        for player in players:
                            user_data = EwUser(id_user=player, id_server=id_server)
                            mutations = user_data.get_mutations()

                            # If the user has Napalm Snot, applying burn is unnecessary
                            if ewcfg.mutation_id_napalmsnot in mutations:
                                continue

                            # If the user hasn't been set burned by the firestorm yet, tell them they're being burned
                            statuses = user_data.getStatusEffects()
                            if ewcfg.status_burning_id not in statuses:
                                district_object = poi_static.id_to_poi.get(district)
                                player_data = EwPlayer(id_user=user_data.id_user, id_server=id_server)

                                # Figure out the player's name and account for amnesia
                                player_name = player_data.display_name
                                if ewcfg.mutation_id_amnesia in mutations:
                                    player_name = "?????"

                                response = "*{}*: You've been set alight by the **RAGING FIRESTORM**, <@{}>! ".format(player_name, player)
                                resp_cont_poi_event.add_channel_response(district_object.channel, response)

                            # Actually burn the user
                            user_data.applyStatus(id_status=ewcfg.status_burning_id, value=ewcfg.firestorm_slime_burn, source=-1)

                    elif event_data.event_type == ewcfg.event_type_tornado:
                        district = event_data.event_props.get('poi')
                        district_data = EwDistrict(district=district, id_server=id_server)
                        district_object = poi_static.id_to_poi.get(district)

                        players = district_data.get_players_in_district(life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]) # Ghosts are immune to tornadoes so inhabitants don't act weirdly
                        # For all the players in the district of the tornado
                        for player in players:
                            user_data = EwUser(id_user=player, id_server=id_server)
                            mutations = user_data.get_mutations()
                            eligible_districts = []

                            # If the user has Big Bones they're too heavy.
                            if ewcfg.mutation_id_bigbones in mutations:
                                continue
                            
                            # Create a list of eligible neighbor districts
                            for district in poi_static.poi_neighbors[district]:
                                if district in poi_static.capturable_districts:
                                    eligible_districts.append(district)
                            # If there are no eligible districts, ignore.
                            if eligible_districts == []:
                                continue
                            # Pick a district
                            deposited_district = random.choice(eligible_districts)
                            deposited_district_object = poi_static.id_to_poi.get(deposited_district)

                            # The member of the user
                            guild = client.get_guild(id_server)
                            member = guild.get_member(user_data.id_user)
                            # Stop movement
                            ewutils.moves_active[user_data.id_user] = 0
                            await rutils.movement_checker(user_data, poi_static.id_to_poi.get(user_data.poi), deposited_district)
                            # Move the player into the neighbor
                            await ewrolemgr.updateRoles(client=client, member=member, new_poi=deposited_district)
                            user_data.poi = deposited_district_object.id_poi
                            user_data.time_lastenter = int(time.time())
                            # Move ghosts and make possible oeo dms.
                            await one_eye_dm(id_user=user_data.id_user, id_server=user_data.id_server, poi=deposited_district)
                            await user_data.move_inhabitants(id_poi=deposited_district)
                            
                            # Take player's slime and put it into the neighbor district.
                            if user_data.slimes > 0:
                                deposited_district_data = EwDistrict(district=district, id_server=id_server)
                                # Splat
                                splatter = user_data.slimes // 3
                                user_data.change_slimes(n=-splatter, source=ewcfg.source_weather)
                                deposited_district_data.change_slimes(n=splatter, source=ewcfg.source_weather)

                                deposited_district_data.persist()
                            
                            response = "You are flung into {} by the **RAGING TORNADO** in {}, splattering slime everywhere. Watch out!".format(deposited_district_object.str_name, district_object.str_name)
                            resp_cont_poi_event.add_channel_response(deposited_district_object.channel, fe_utils.formatMessage(member, response))

                            user_data.persist()

                    elif event_data.event_type == ewcfg.event_type_poudrin_hail:
                        if random.random() <= 0.007: # 99.3% chance for nothing to occur
                            district = event_data.event_props.get('poi')
                            district_data = EwDistrict(district=district, id_server=id_server)
                            district_object = poi_static.id_to_poi.get(district)
                            players = district_data.get_players_in_district(life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]) # Ghosts are incorporeal to falling debris                            
                            
                            # If there are players in the district, pick one to have a poudrin fall on
                            if len(players) >= 1:
                                player = random.choice(players)
                                user_data = EwUser(id_user=player, id_server=id_server)
                                player_data = EwPlayer(id_user=user_data.id_user, id_server=id_server)
                                umbrella = False

                                # Check if the player has an umbrella equipped
                                equipped_weapon = EwItem(id_item=user_data.weapon)
                                weapon = weapons_static.weapon_map.get(equipped_weapon.item_props.get("weapon_type"))
                                if weapon != None:
                                    if weapon.id_weapon == ewcfg.weapon_id_umbrella:
                                        umbrella = True

                                # If the player does not have an umbrella equipped, kill them
                                if not umbrella:
                                    # !kill and make Sewers response
                                    die_resp = user_data.die(cause=ewcfg.cause_debris)
                                    resp_cont_poi_event.add_response_container(die_resp)
                                    user_data.persist()

                                    # Make channel response
                                    response = "A poudrin falls from the sky, landing squarely on {}'s soft, supple scalp. They are crushed to the pavement, dead on impact. {}".format(player_data.display_name, ewcfg.emote_slimeskull)
                                else:
                                    # Make channel response
                                    response = "A poudrin falls from the sky, landing squarely on {}'s strong, sturdy umbrella. The pure crystal of slime harmlessly falls to the ground.".format(player_data.display_name)
                            else:
                                response = "A poudrin falls from the sky."
                            
                            # Get poudrin item props
                            item = items_static.item_map.get('slimepoudrin')
                            item_props = item_utils.gen_item_props(item)
                            # Create poudrin on the ground
                            bknd_item.item_create(
                                item_type=item.item_type,
                                id_user=district,
                                id_server=id_server,
                                item_props=item_props,
                            )
                            # Create channel response for poudrin falling
                            resp_cont_poi_event.add_channel_response(district_object.channel, response)

                    elif event_data.event_type == ewcfg.event_type_meteor_shower:
                        district = event_data.event_props.get('poi')
                        district_data = EwDistrict(district=district, id_server=id_server)
                        players = district_data.get_players_in_district(life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]) # Ghosts can't see
                            
                        for player in players:
                            if random.random() <= 0.08: # 92% chance for no flavor for that player
                                district_object = poi_static.id_to_poi.get(district)
                                user_data = EwUser(id_user=player, id_server=id_server)
                                player_data = EwPlayer(id_user=player, id_server=id_server)

                                mutations = user_data.get_mutations()

                                # Figure out the player's name and account for amnesia
                                player_name = player_data.display_name
                                if ewcfg.mutation_id_amnesia in mutations:
                                    player_name = "?????"
                                
                                meteor_shower_flavor = random.choice(comm_cfg.meteor_shower_responses)
                                response = "*{}*: {}".format(player_name, meteor_shower_flavor)
                                resp_cont_poi_event.add_channel_response(district_object.channel, response)
                                
                                item_recieved = random.random()
                                if (ewcfg.mutation_id_lucky in mutations and item_recieved <= 0.15) or item_recieved <= 0.10: # 15/10% chance for moon dust vape juice
                                    item = items_static.item_map.get(ewcfg.item_id_moon_dust_pod)
                                    item_props = item_utils.gen_item_props(item)
                                    # create vape pod
                                    bknd_item.item_create(
                                        item_type=item.item_type,
                                        id_user=player,
                                        id_server=id_server,
                                        item_props=item_props,
                                    )
                                    response = "*{}*: A mysterious pod appears in your pocket.".format(player_name)
                                    resp_cont_poi_event.add_channel_response(district_object.channel, response)                                    
                                

                    # If the event is a japestorm
                    elif event_data.event_type == ewcfg.event_type_jape_storm:
                        district = event_data.event_props.get('poi')
                        district_data = EwDistrict(district=district, id_server=id_server)
                        district_object = poi_static.id_to_poi.get(district)
                        players = district_data.get_players_in_district(life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]) # Ghosts are immune to comedy

                        # If there are players in the district, pick one to get PRANK'D
                        if len(players) >= 1 and random.random() > 0.85:
                            player = random.choice(players)
                            user_data = EwUser(id_user=player, id_server=id_server)
                            player_data = EwPlayer(id_user=user_data.id_user, id_server=id_server)

                            mutations = user_data.get_mutations()

                            # User will get better prank items if they have the lucky mutation
                            if ewcfg.mutation_id_lucky in mutations:
                                item = random.choice(items_static.prank_items_forbidden)
                            else:
                                item = random.choice(items_static.prank_items_heinous + items_static.prank_items_scandalous)

                            item_props = item_utils.gen_item_props(item)
                            id_user = district

                            # Make channel response
                            response = "A {} is thrown at {}, clobbering their face. Thank god it wasn't lethal!".format(item_props['item_name'], player_data.display_name)
                        # Spawn a primed prank item
                        elif random.random() > 0.985: 
                            # Generate a trap to put on the ground
                            item = random.choice(items_static.prank_items_trap)
                            item_props = item_utils.gen_item_props(item)
                            item_props["trap_stored_credence"] = 0
                            item_props["trap_user_id"] = str(431446476112134144) # ENDLESS WAR's user ID

                            # Make the trap itemed primed
                            id_user = district + '_trap'

                            # Make channel response
                            response = "A primed {} appears on the ground.".format(item_props['item_name'])
                        # Cancel before going on if neither of the previous conditions were true
                        else: 
                            continue

                        # Create item on the ground
                        bknd_item.item_create(
                            item_type=item.item_type,
                            id_user=id_user,
                            id_server=id_server,
                            item_props=item_props,
                        )
                        # Create channel response
                        resp_cont_poi_event.add_channel_response(district_object.channel, response)
                            
            await resp_cont_poi_event.post()
            
        except:
            ewutils.logMsg("Error occurred in weather tick for server {}".format(id_server))

async def weather_cycle(id_server):
    try:
        market_data = EwMarket(id_server)
        valid_weather = False

        # In case the weather is somehow set to something un-weatherable
        for weather in weather_static.weather_list:
            if weather.name == market_data.weather:
                valid_weather = True

        # Seed the randomness based on day, clock, and a random unknown consistent stat 
        seed = (market_data.day * 24) + market_data.clock + (market_data.donated_poudrins + 1) 

        # Create a seeded random class
        market_random_class = random.Random(seed)

        # Potentially change the weather
        if market_random_class.randrange(3) == 0 or valid_weather == False:
                pattern_count = len(weather_static.weather_list)

                if pattern_count > 1:
                    weather_old = market_data.weather

                    # Randomly select a new weather pattern. Try again if we get the same one we currently have.
                    while market_data.weather == weather_old:
                        pick = market_random_class.randrange(len(weather_static.weather_list))
                        market_data.weather = weather_static.weather_list[pick].name
                    market_data.persist()
                # Log message for statistics tracking.
                ewutils.logMsg("The weather changed. It's now {}.".format(market_data.weather))
    except Exception as e:
        ewutils.logMsg(f"Failed to cycle weather in server {id_server}: {e}")


def forecast_txt(id_server=None, resp_type="long"):
    market_data = EwMarket(id_server)

    weather_icon_list = []
    moon_phase_list = []
    day_list = []
    blank = 0
    weather_icon = ewcfg.weather_icon_map.get(market_data.weather)

    current_weather = market_data.weather
    current_day = market_data.day
    current_clock = market_data.clock + 1
    if current_clock >= 24:
        current_day += 1
        current_clock = 0


    starting_position = (market_data.clock + 1) / 4

    while blank < starting_position:
        if resp_type == "long":
            weather_icon_list.append(ewcfg.emote_blank)
        elif resp_type == "short":
            weather_icon_list.append("〰️" if ewutils.DEBUG else ewcfg.emote_blank)
        blank += 1

    # Create a random class, to seed multiple times
    market_random_class = random.Random()

    # Simulate the next week, ig.
    while len(weather_icon_list) < 42:

        # Simulate weather
        seed = (current_day * 24) + current_clock + (market_data.donated_poudrins + 1) 

        # Re-initialize the random class
        market_random_class.seed(seed)

        if market_random_class.randrange(3) == 0:
            pattern_count = len(weather_static.weather_list)

            if pattern_count > 1:
                weather_old = current_weather

                # Randomly select a new weather pattern. Try again if we get the same one we currently have.
                while current_weather == weather_old:
                    pick = market_random_class.randrange(len(weather_static.weather_list))
                    current_weather = weather_static.weather_list[pick].name
                weather_icon = ewcfg.weather_icon_map.get(current_weather)

        # Place icon
        if current_clock % 4 == 0:
            chance = 1
            if (24 >= len(weather_icon_list) > 18) and market_random_class.randrange(2) != 0:
                chance = 2
            elif (30 >= len(weather_icon_list) > 24) and market_random_class.randrange(3) != 0:
                chance = 3
            elif len(weather_icon_list) > 30 and market_random_class.randrange(4) != 0:
                chance = 5

            if market_random_class.randrange(chance) != 0:
                weather_icon_list.append("❓")
            else:
                weather_icon_list.append(weather_icon)

        # Tick up clock
        current_clock += 1
        if current_clock >= 24:
            current_clock = 0
            current_day += 1

    # Figure out moon phases + days
    moon = 0
    while moon < 7:
        # Format day
        if resp_type == "long":
            day_str = "Day {:,}".format(market_data.day)
            day_list.append("\n`{:^11}`|".format(day_str))
        elif resp_type == "short":
            day_str = "{}d".format(market_data.day)
            day_list.append("\n`{:^6}`|".format(day_str))

        # Change date and figure out moon phase
        market_data.clock = 22
        moon_phase = ewutils.check_moon_phase(market_data)
        market_data.day += 1

        moon_phase_icon = ewcfg.moon_phase_icon_map.get(moon_phase)
        moon_phase_list.append(moon_phase_icon)

        moon += 1

    # Create forecast response
    if resp_type == "long":
        # 0-6 are day, 7-49 are weather, 49-55 are moon. {_} is replaced with 5 hair spaces and 1 ideographic space, for character limit reasons.
        forecast_response = "{_}{_}{_}{_}     12AM          4AM          8AM         12PM          4PM          8PM                      Moon" \
                            "{0}{_}{7}{_}|{_}{8}{_}|{_}{9}{_}|{_}{10}{_}|{_}{11}{_}|{_}{12}{_}|{_}{_}{_}{49}"\
                            "{1}{_}{13}{_}|{_}{14}{_}|{_}{15}{_}|{_}{16}{_}|{_}{17}{_}|{_}{18}{_}|{_}{_}{_}{50}"\
                            "{2}{_}{19}{_}|{_}{20}{_}|{_}{21}{_}|{_}{22}{_}|{_}{23}{_}|{_}{24}{_}|{_}{_}{_}{51}"\
                            "{3}{_}{25}{_}|{_}{26}{_}|{_}{27}{_}|{_}{28}{_}|{_}{29}{_}|{_}{30}{_}|{_}{_}{_}{52}"\
                            "{4}{_}{31}{_}|{_}{32}{_}|{_}{33}{_}|{_}{34}{_}|{_}{35}{_}|{_}{36}{_}|{_}{_}{_}{53}"\
                            "{5}{_}{37}{_}|{_}{38}{_}|{_}{39}{_}|{_}{40}{_}|{_}{41}{_}|{_}{42}{_}|{_}{_}{_}{54}"\
                            "{6}{_}{43}{_}|{_}{44}{_}|{_}{45}{_}|{_}{46}{_}|{_}{47}{_}|{_}{48}{_}|{_}{_}{_}{55}".format(*day_list, *weather_icon_list, *moon_phase_list, _ = "     　")
    elif resp_type == "short":
        forecast_response = "                    12   4     8    12   4    8     Moon" \
                            "{0}   {7} {8} {9} {10} {11} {12}{_}{49}"\
                            "{1}   {13} {14} {15} {16} {17} {18}{_}{50}"\
                            "{2}   {19} {20} {21} {22} {23} {24}{_}{51}"\
                            "{3}   {25} {26} {27} {28} {29} {30}{_}{52}"\
                            "{4}   {31} {32} {33} {34} {35} {36}{_}{53}"\
                            "{5}   {37} {38} {39} {40} {41} {42}{_}{54}"\
                            "{6}   {43} {44} {45} {46} {47} {48}{_}{55}".format(*day_list, *weather_icon_list, *moon_phase_list, _ = ("〰️" if ewutils.DEBUG else ewcfg.emote_blank))


    return forecast_response


async def create_poi_event(id_server, pre_chosen_event=None, # Events are natural disasters, pop-up events, etc.
                                      pre_chosen_poi=None, 
                                      pre_chosen_sisterpoi=None,
                                      pre_chosen_buffer=None, 
                                      pre_chosen_length=None, 
                                      pre_chosen_alert=None):
    # Create the props dict
    event_props = {}

    # Get a random event type from poi_events
    if pre_chosen_event != None:
        event_type = pre_chosen_event
    else:
        event_type = random.choice(ewcfg.random_poi_events)

    # Get the time right now and the event def
    time_now = int(time.time())    
    event_def = poi_static.event_type_to_def.get(event_type)

    # Choose the POI
    if pre_chosen_poi != None:
        event_props['poi'] = pre_chosen_poi
    elif event_def.pois != []:
        event_props['poi'] = random.choice(event_def.pois)
    else:
        for gup in range(100):
            district = random.choice(poi_static.capturable_districts)

            if district not in [ewcfg.poi_id_downtown, ewcfg.poi_id_greenlightdistrict]: # These two POIs shouldn't have dangerous natural disasters so EW -> JR is always 100% possible
                event_props['poi'] = district
                break

    # Get the buffer and length
    if pre_chosen_buffer != None:
        buffer = int(pre_chosen_buffer)
    else:
        buffer = event_def.buffer
    if pre_chosen_length != None:
        length = int(pre_chosen_length)
    else:
        length = event_def.length

    activation_time = time_now + (buffer * 60 * 15) + 6 # buffer x 15 minutes
    expiration_time = activation_time + (length * 60 * 15) # length x 15 minutes

    # Select type of alert - "" for none, "gangbase" for gangbase
    if pre_chosen_alert != None:
        alert = pre_chosen_alert
    else:
        alert = "gangbase" # always give specifics

    event_props['alert'] = alert


    # Does configuration for dimensional rifts - creates the second rift, as well as making the 2 POIs neighbors.
    if event_type == ewcfg.event_type_dimensional_rift:
        # Rift 1 is the original location
        rift1_poi = poi_static.id_to_poi.get(event_props['poi'])
        # Rift 2 is the sister location
        if pre_chosen_sisterpoi != None:
            rift2_poi_id = pre_chosen_sisterpoi
        else:
            rift2_poi_id = poi_static.landlocked_destinations.get(rift1_poi.id_poi)
        rift2_poi = poi_static.id_to_poi.get(rift2_poi_id)
        
        # Set both locations as neighbors
        rift1_poi.neighbors[rift2_poi_id] = ewcfg.travel_time_district
        rift2_poi.neighbors[rift1_poi.id_poi] = ewcfg.travel_time_district

        # Create the world event for 1st rift.
        event_props['sisterlocation'] = rift2_poi_id
        bknd_worldevent.create_world_event(
            id_server=id_server,
            event_type=event_type,
            time_activate=activation_time,
            time_expir=expiration_time,
            event_props=event_props
        )        

        # Set up props for the sister world event's creation
        event_props['poi'] = rift2_poi_id
        event_props['sisterlocation'] = rift1_poi.id_poi

    # Create world event
    bknd_worldevent.create_world_event(
        id_server=id_server,
        event_type=event_type,
        time_activate=activation_time,
        time_expir=expiration_time,
        event_props=event_props
    )  

    # Send gangbase forecast
    gangbase_resp_cont = EwResponseContainer(client=ewutils.get_client(), id_server=id_server)

    if alert == "gangbase":
        poi = poi_static.id_to_poi.get(event_props['poi'])

        gangbase_forecast = "It seems {} will begin in {} in {} hours NLACakaNMian time.".format(event_def.str_name, poi.str_name, event_def.buffer)
    else:
        gangbase_forecast = "It seems something is forming in NLACakaNM..."

    for channel in ewcfg.hideout_channels:
        gangbase_resp_cont.add_channel_response(channel, gangbase_forecast)

    await gangbase_resp_cont.post()