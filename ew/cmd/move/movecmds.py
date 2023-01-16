import asyncio
import math
import random
import time

import discord

from ew.backend import ads as bknd_ads
from ew.backend import core as bknd_core
from ew.backend.ads import EwAd
from ew.backend.dungeons import EwGamestate
from ew.backend.market import EwMarket
from ew.backend.mutation import EwMutation
from ew.backend.player import EwPlayer
from ew.backend import worldevent as bknd_worldevent
from ew.cmd import apt as ewapt
from ew.static import cfg as ewcfg
from ew.static import community_cfg as commcfg
from ew.static import poi as poi_static
try:
    from ew.cmd.debug import zone_bonus_flavor
except:
    from ew.cmd.debug_dummy import zone_bonus_flavor
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import move as move_utils
from ew.utils import prank as prank_utils
from ew.utils import rolemgr as ewrolemgr
try:
    from ew.utils import rutils as rutils
except:
    from ew.utils import rutils_dummy as rutils
from ew.utils import stats as ewstats
from ew.utils.ads import format_ad_response
from ew.utils.combat import EwEnemy
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.backend.apt import EwApartment
from ew.utils.frontend import EwResponseContainer
from ew.utils.move import EwPath
from ew.utils.transport import EwTransport
from .moveutils import get_enemies_look_resp
from .moveutils import get_players_look_resp
from .moveutils import get_slimes_resp
from .moveutils import get_items_resp
from .moveutils import get_void_connections_resp
from .moveutils import get_world_events_look_resp
from .moveutils import one_eye_dm
from .moveutils import send_arrival_response
from .moveutils import enemy_lock_impose_restrictions

"""
    Player command to move themselves from one place to another.
"""


async def move(cmd = None, isApt = False, continuousMove = -1):
    server_data = ewcfg.server_list[cmd.guild.id]
    member_object = cmd.message.author
    player_data = EwPlayer(id_user=cmd.message.author.id)
    user_data = EwUser(id_user=cmd.message.author.id, id_server=player_data.id_server, data_level=1)
    poi_current = poi_static.id_to_poi.get(user_data.poi)
    time_move_start = int(time.time())
    isDM = False

    if not hasattr(cmd.message.channel, 'name'):
        isDM = True

    if isApt == False and isDM == False and ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        channelid = fe_utils.get_channel(cmd.guild, poi_current.channel)
        return await fe_utils.send_message(
            cmd.client,
            cmd.message.channel,
            fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.\n{}".format(cmd.tokens[0], "<#{}>".format(channelid.id)))
        )

    target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])

    if target_name == None or len(target_name) == 0:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Where to?"))

    if target_name in poi_static.streets:
        return await fe_utils.send_message(
            cmd.client,
            cmd.message.channel,
            fe_utils.formatMessage(cmd.message.author, "https://www.goodreads.com/quotes/106313-the-beginning-of-wisdom-is-to-call-things-by-their ...bitch")
        )

    poi = poi_static.id_to_poi.get(target_name)
    if poi_current.is_apartment == True:
        isApt = True
    if target_name in ['apt', 'apartment']:
        apartment = EwApartment(id_server=cmd.guild.id, id_user=cmd.message.author.id)
        intoApt = True
        poi = poi_static.id_to_poi.get(apartment.poi)
        target_name = apartment.poi
        if not poi:
            response = "You don't have an apartment."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        intoApt = False

    movement_method = ""

    if user_data.get_inhabitee():
        # prevent ghosts currently inhabiting other players from moving on their own
        response = "You might want to **{}** of the poor soul you've been tormenting first.".format(ewcfg.cmd_letgo)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if ewutils.active_restrictions.get(user_data.id_user) != None and ewutils.active_restrictions.get(user_data.id_user) > 0:
        district = EwDistrict(id_server=user_data.id_server, district=user_data.poi)

        if user_data.poi in poi_static.enemy_lock_districts and district.get_enemies_in_district() == []:
            ewutils.active_restrictions[user_data.id_user] = 0
        else:
            response = "You can't do that right now."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if poi == None:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Never heard of it."))

    user_channel_poi = poi_static.chname_to_poi.get(cmd.message.channel.name) # The channel 

    if not ewutils.DEBUG  and isDM == False and not isApt and user_channel_poi.id_poi != user_data.poi and user_channel_poi.enemy_lock != True:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in your current district.").format(cmd.tokens[0]))

    if user_data.poi == ewcfg.debugroom:
        movement_method = "descending"
        try:
            if poi.id_poi == ewcfg.poi_id_slimeoidlab:
                movement_method = "walking"
        except:
            pass
    else:
        movement_method = "walking"

    if user_data.poi == ewcfg.debugroom and cmd.tokens[0] != (
            ewcfg.cmd_descend) and poi.id_poi != ewcfg.poi_id_slimeoidlab:
        return await fe_utils.send_message(
            cmd.client,
            cmd.message.channel,
            fe_utils.formatMessage(cmd.message.author, "You can't move forwards or backwards in an {}, bitch.".format(ewcfg.debugroom_short))
        )
    elif user_data.poi != ewcfg.debugroom and cmd.tokens[0] == (ewcfg.cmd_descend):
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You can't move downwards on a solid surface, bitch."))

    # if fetch_poi_if_coordless(poi.channel) is not None: # Triggers if your destination is a sub-zone.
    # 	poi = fetch_poi_if_coordless(poi.channel)
    # 	mother_poi = poi_static.id_to_poi.get(poi.mother_district)
    # 	if mother_poi is not None: # Reroute you to the sub-zone's mother district if possible.
    # 		target_name = poi.mother_district
    # 		poi = mother_poi

    if poi.id_poi == user_data.poi:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You're already there, bitch."))
    elif isApt and poi.id_poi == user_data.poi[3:]:
        return await ewapt.aptcmds.depart(cmd=cmd)

    if move_utils.inaccessible(user_data=user_data, poi=poi):
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You're not allowed to go there (bitch)."))

    if user_data.life_state == ewcfg.life_state_corpse and time.time() - user_data.time_lastdeath < ewcfg.time_to_manifest:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You're not used to being dead yet, it takes a while to learn how to manifest your ghost and move around."))
    if isApt:
        poi_current = poi_static.id_to_poi.get(user_data.poi[3:])

    # if poi.coord == None or poi_current == None or poi_current.coord == None:
    if user_data.life_state == ewcfg.life_state_corpse and poi.id_poi == ewcfg.poi_id_thesewers:
        path = EwPath(cost=60)
    elif len(poi.neighbors.keys()) == 0 or poi_current == None or len(poi_current.neighbors.keys()) == 0:
        path = None
    else:
        path = move_utils.path_to(
            poi_start=poi_current.id_poi,
            poi_end=target_name,
            user_data=user_data
        )
        if path != None:
            path.cost = int(path.cost / user_data.move_speed)

    if path == None:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You don't know how to get there."))
    if isApt or intoApt:
        path.cost += 20
    # global move_counter

    # Check if we're already moving. If so, cancel move and change course. If not, register this course.
    if continuousMove == -1:
        move_current = ewutils.moves_active.get(cmd.message.author.id)
        move_utils.move_counter += 1
        move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
    else:
        move_current = continuousMove
    # Take control of the move for this player.


    # Hard lock path costs to not be lower than 5 seconds.
    path.cost = max(path.cost, 5)

    if path.cost > 1000:
        distance_log = ewstats.get_stat(id_server=player_data.id_server, id_user=player_data.id_user, metric='distance_walked')
        path.cost -= distance_log * 400

    minutes = int(path.cost / 60)
    seconds = path.cost % 60

    life_state = user_data.life_state
    faction = user_data.faction

    # walking_into_sewers = (user_data.life_state != ewcfg.life_state_corpse) and (poi.id_poi == ewcfg.poi_id_thesewers)
    walking_into_sewers = poi.id_poi == ewcfg.poi_id_thesewers

    if user_data.has_soul == 1:
        walk_text = "walking"
    else:
        walk_text = "hopelessly trudging"

    if intoApt:
        aptText = " Apartments"
    else:
        aptText = ""



    if movement_method == "descending":
        msg_walk_start = await fe_utils.send_message(
            cmd.client,
            cmd.message.channel,
            fe_utils.formatMessage(cmd.message.author, "You press the button labeled {}. You will arrive in {} seconds.".format(poi.str_name, seconds)))
    else:
        distance_text = (" It's {} minute{}{} away.".format(
            minutes,
            ("s" if minutes != 1 else ""),
            (" and {} seconds".format(seconds) if seconds > 4 else "")
        ) if minutes > 0 else (" It's {} seconds away.".format(seconds) if seconds > 4 else ""))
        walk_response = None

        location = poi.str_name

        if walking_into_sewers:
            if user_data.life_state == ewcfg.life_state_corpse:
                walk_response = "You begin to sink through the earth, retreating to your corpse deep in {}.{}".format(poi.str_name, distance_text)
            else:
                walk_response = "You begin your descent to {}.{}\nI'm sure you've heard, but people who go down there don't come back alive. You still have time to **{}**, if you'd like.".format(
                    location,
                    distance_text,
                    ewcfg.cmd_halt_alt1
                )
        else:
            walk_response = "You begin {} to {}{}.{}".format(walk_text, location, aptText, distance_text)

        msg_walk_start = await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, walk_response))

        if isApt:
            await ewapt.aptcmds.depart(cmd=cmd, isGoto=True, movecurrent=move_current)

    time_move_end = int(time.time())

    # print('pathfinding in move function took {} seconds'.format(time_move_end - time_move_start))
    # Moving to or from a place not on the map (e.g. the sewers)
    # if poi.coord == None or poi_current == None or poi_current.coord == None:
    if len(poi.neighbors.keys()) == 0 or poi_current == None or len(poi_current.neighbors.keys()) == 0 or (walking_into_sewers and life_state == ewcfg.life_state_corpse):
        if path.cost > 0:
            await asyncio.sleep(path.cost)

        if ewutils.moves_active[cmd.message.author.id] != move_current or ewutils.moves_active[cmd.message.author.id] == 0:
            return

        user_data = EwUser(id_user=cmd.message.author.id, id_server=player_data.id_server)

        # If the player dies or enlists or whatever while moving, cancel the move.
        if user_data.life_state != life_state or faction != user_data.faction:
            try:
                await msg_walk_start.delete()
                pass
            except:
                pass

            return




        await ewrolemgr.updateRoles(client=cmd.client, member=member_object, new_poi=poi.id_poi)
        user_data.poi = poi.id_poi
        user_data.time_lastenter = int(time.time())

        user_data.persist()
        await rutils.movement_checker(user_data, poi_current, poi, cmd)
        ewutils.end_trade(user_data.id_user)
        enemy_lock_impose_restrictions(id_user=user_data.id_user, poi=poi.id_poi)
        await one_eye_dm(id_user=user_data.id_user, id_server=user_data.id_server, poi=poi.id_poi)
        #await ewrolemgr.updateRoles(client=client, member=member_object)

        # Send the message in the channel for this POI if possible, else in the origin channel for the move.
        for ch in server_data.channels:
            if ch.name == poi.channel:
                channel = ch
                break

        msg_walk_enter = await send_arrival_response(cmd, poi, channel)
        try:
            await msg_walk_start.delete()
            await asyncio.sleep(30)
            await msg_walk_enter.delete()
            pass
        except:
            pass

    else:
        boost = 0

        step_list = []
        for step in path.steps:
            step_list.append(step.str_name)
        # print('path steps: {}'.format(step_list))

        # Perform move.
        for i in range(1, len(path.steps)):

            step = path.steps[i]

            val = poi_current.neighbors.get(step.id_poi)

            poi_last = poi_current
            poi_current = step

            user_data = EwUser(id_user=cmd.message.author.id, id_server=player_data.id_server, data_level=1)
            # mutations = user_data.get_mutations()
            if poi_current != None:

                # Prevent access to the zone if it's closed.
                if poi_current.closed == True:
                    try:
                        if poi_current.str_closed != None:
                            message_closed = poi_current.str_closed
                        else:
                            message_closed = "The way into {} is blocked.".format(poi_current.str_name)
                    finally:
                        error_channel = fe_utils.get_channel(server=cmd.message.guild, channel_name=poi_last.channel)
                        return await fe_utils.send_response(message_closed, cmd, channel=error_channel)

                if len(user_data.faction) > 0 and user_data.poi in poi_static.capturable_districts:
                    district = EwDistrict(
                        id_server=user_data.id_server,
                        district=user_data.poi
                    )

                    if district != None and len(district.controlling_faction) > 0 and i < (len(path.steps) - 1):
                        if user_data.faction == district.controlling_faction:
                            val -= ewcfg.territory_time_gain
                        else:
                            val += ewcfg.territory_time_gain

                val = int(val / user_data.move_speed)
                if val > 1000:
                    distance_log = ewstats.get_stat(id_server=player_data.id_server, id_user=player_data.id_user, metric='distance_walked')
                    val -= distance_log * 400
                    while val > 0:
                        await asyncio.sleep(400)
                        val -= 400
                        ewstats.increment_stat(id_server=player_data.id_server, id_user=player_data.id_user, metric='distance_walked')
                    if val <= 0:
                        ewstats.set_stat(id_server=player_data.id_server, id_user=player_data.id_user, metric='distance_walked', value=0)
                else:
                    ewstats.set_stat(id_server=player_data.id_server, id_user=player_data.id_user, metric='distance_walked', value=0)
                    await asyncio.sleep(val)

                # Check to see if we have been interrupted and need to not move any farther.
                if ewutils.moves_active[cmd.message.author.id] != move_current or move_current == 0:
                    break

                user_data = EwUser(id_user=cmd.message.author.id, id_server=player_data.id_server)

                # If the player dies or enlists or whatever while moving, cancel the move.
                if user_data.life_state != life_state or faction != user_data.faction:
                    try:
                        await msg_walk_start.delete()
                        pass
                    except:
                        pass

                    return

                channel = cmd.message.channel

                # Send the message in the channel for this POI if possible, else in the origin channel for the move.
                for ch in server_data.channels:
                    if ch.name == poi_current.channel:
                        channel = ch
                        break

                if user_data.poi != poi_current.id_poi:
                    if walking_into_sewers and poi_current.id_poi == ewcfg.poi_id_thesewers:
                        die_resp = await user_data.die(cause=ewcfg.cause_suicide)
                        return await die_resp.post()

                    poi_previous = poi_static.id_to_poi.get(user_data.poi)
                    # print('previous poi: {}'.format(poi_previous))



                    user_data.poi = poi_current.id_poi
                    user_data.time_lastenter = int(time.time())

                    user_data.persist()
                    await rutils.movement_checker(user_data, poi_previous, poi_current, cmd)
                    ewutils.end_trade(user_data.id_user)
                    enemy_lock_impose_restrictions(id_user=user_data.id_user, poi=poi.id_poi)

                    await ewrolemgr.updateRoles(client=cmd.client, member=member_object)
                    await one_eye_dm(id_server=user_data.id_server, id_user=user_data.id_user, poi=poi_current.id_poi)

                    # also move any ghosts inhabiting the player
                    await user_data.move_inhabitants(id_poi=poi_current.id_poi)

                    try:
                        await msg_walk_start.delete()
                        pass
                    except:
                        pass

                    msg_walk_start = await send_arrival_response(cmd, poi_current, channel)

                    # SWILLDERMUK
                    await prank_utils.activate_trap_items(poi.id_poi, user_data.id_server, user_data.id_user)

                    if poi_current.has_ads:
                        ads = bknd_ads.get_ads(id_server=user_data.id_server)
                        if len(ads) > 0:
                            id_ad = random.choice(ads)
                            ad_data = EwAd(id_ad=id_ad)
                            ad_response = format_ad_response(ad_data)
                            await fe_utils.send_message(cmd.client, channel, fe_utils.formatMessage(cmd.message.author, ad_response))

        if intoApt and ewutils.moves_active[cmd.message.author.id] == move_current and move_current != 0:
            await ewapt.aptcmds.retire(cmd=cmd, isGoto=True, movecurrent=move_current)

        await asyncio.sleep(30)
        try:
            await msg_walk_start.delete()
            pass
        except:
            pass


async def dm_move(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.poi not in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown]:
        response = "Nah, move in the gameplay channel. That only works in gang bases."
        await fe_utils.send_message(cmd.client, cmd.message.author, fe_utils.formatMessage(cmd.message.author, response))
    else:
        return await move(cmd=cmd)

"""
    Go down the rabbit hole
"""


async def descend(cmd):
    user_data = EwUser(member=cmd.message.author, data_level=1)
    void_connections = bknd_worldevent.get_void_connection_pois(cmd.guild.id)
    world_events = bknd_worldevent.get_world_events(id_server=user_data.id_server, active_only=True)

    raid_den = False

    for id_event in world_events:
        if world_events.get(id_event) == ewcfg.event_type_raid_den:
            event_data = bknd_worldevent.EwWorldEvent(id_event=id_event)
            if event_data.event_props.get('poi') == user_data.poi:
                raid_den = True

    if user_data.poi in void_connections or raid_den == True:
        # enter the void
        if user_data.poi in void_connections and raid_den == False:
            travel_duration = int(ewcfg.travel_time_district / user_data.move_speed)
            response = "You descend down the flight of stairs and begin walking down a lengthy tunnel towards an identical set of ascending stairs. You will arrive on the other side in {} seconds.".format(travel_duration)
            descent_message = await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            
            dest_poi = poi_static.id_to_poi.get(ewcfg.poi_id_thevoid)
            response = "You go up the flight of stairs and find yourself in {}.".format(dest_poi.str_name)

            destination_poi = ewcfg.poi_id_thevoid

        # Go into raid den
        else:
            travel_duration = int((ewcfg.travel_time_outskirt * 1.5) / user_data.move_speed)
            response = "You descend into the earth itself, entering a cavern that only goes deeper and deeper. You will hit the point of no return in {} seconds.".format(travel_duration)
            descent_message = await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            dest_poi = poi_static.id_to_poi.get(ewcfg.poi_id_raiddenentryway)
            response = "You pass the point of no return and **ENTER THE RAID DEN**.\n\nYou must **kill all enemies** before moving further inward."

            destination_poi = ewcfg.poi_id_raiddenentryway

        # global move_counter
        move_current = ewutils.moves_active.get(cmd.message.author.id)
        move_utils.move_counter += 1
        move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter

        life_state = user_data.life_state
        faction = user_data.faction
        await asyncio.sleep(travel_duration)
        try:
            await descent_message.delete()
        except:
            pass

        user_data = EwUser(member=cmd.message.author)
        if move_current == ewutils.moves_active[cmd.message.author.id] and user_data.life_state == life_state and faction == user_data.faction:
            if raid_den == False:
                await ewrolemgr.updateRoles(client=ewutils.get_client(), member=cmd.message.author, new_poi=ewcfg.poi_id_thevoid)
            elif raid_den == True:
                await ewrolemgr.updateRoles(client=ewutils.get_client(), member=cmd.message.author, new_poi=ewcfg.poi_id_raiddenentryway)
            user_data.poi = destination_poi
            user_data.time_lastenter = int(time.time())

            user_data.persist()
            ewutils.end_trade(user_data.id_user)

            if raid_den:
                ewutils.active_restrictions[user_data.id_user] = 2

            await user_data.move_inhabitants(id_poi=destination_poi)
            #await ewrolemgr.updateRoles(client=ewutils.get_client(), member=cmd.message.author, new_poi=ewcfg.poi_id_thevoid)
            msg = await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, dest_poi.channel), fe_utils.formatMessage(cmd.message.author, response))
            await asyncio.sleep(20)
            try:
                await msg.delete()
                pass
            except:
                pass
            return
    
    else:
        return await move(cmd)


"""
    Cancel any in progress move.
"""


async def halt(cmd):
    ewutils.moves_active[cmd.message.author.id] = 0
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You {} dead in your tracks.".format(cmd.cmd[1:])))


"""
    Dump out the visual description of the area you're in.
"""


async def look(cmd):
    user_data = EwUser(member=cmd.message.author)

    poi = poi_static.id_to_poi.get(user_data.poi)

    district_data = EwDistrict(district=poi.id_poi, id_server=user_data.id_server)
    market_data = EwMarket(id_server=user_data.id_server)
    void_resp = get_void_connections_resp(poi.id_poi, user_data.id_server)

    if poi.is_apartment:
        return await ewapt.aptcmds.apt_look(cmd)

    bonus_flavor_list = zone_bonus_flavor.get(poi.id_poi)
    if bonus_flavor_list is not None:
        str_desc = poi.str_desc.format(bonusflavor = random.choice(bonus_flavor_list))
    elif ewcfg.status_thinned_id in user_data.getStatusEffects():
        str_desc = random.choice(commcfg.district_blurbs.get(poi.id_poi))
    else:
        str_desc = poi.str_desc

    if poi.is_subzone or poi.id_poi == ewcfg.poi_id_thevoid:  # Triggers if you input the command in the void or a sub-zone.
        wikichar = '\n\n<{}>'.format(poi.wikipage) if poi.wikipage != '' else ''
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author,
                                                                                                   "You stand {} {}.\n\n{}{}{}".format(
                                                                                                       poi.str_in,
                                                                                                       poi.str_name,
                                                                                                       str_desc,
                                                                                                       wikichar,
                                                                                                       void_resp,

                                                                                                   )
                                                                                                   ))

    # if it's a subzone, check who owns the actual district
    if poi.is_subzone:
        controlled_poi = poi_static.id_to_poi.get(poi.mother_districts[0] if len(poi.mother_districts) > 0 else poi.father_district)
        controlled_data = EwDistrict(district=controlled_poi.id_poi, id_server=user_data.id_server)
    else:
        controlled_data = district_data

    capped_resp = "This district is controlled by {}.\n\n".format("the " + controlled_data.controlling_faction.capitalize() if controlled_data.controlling_faction != "" else "no one")
    slimes_resp = get_slimes_resp(user_data, district_data)
    items_resp = get_items_resp(user_data, district_data)
    players_resp = get_players_look_resp(user_data, district_data)
    enemies_resp = get_enemies_look_resp(user_data, district_data)
    worldevents_resp = get_world_events_look_resp(user_data, district_data)
    soul_resp = ""
    extra_resp = ""

    if poi.is_apartment:
        slimes_resp = ""
        items_resp = ""
        players_resp = ""
    if user_data.has_soul == 0:
        soul_resp = "\n\nYour soul brought color to the world. Now it all looks so dull."
    else:
        soul_resp = ""

    ad_resp = ""
    ad_formatting = ""
    if poi.has_ads:
        ads = bknd_ads.get_ads(id_server=user_data.id_server)
        if len(ads) > 0:
            id_ad = random.choice(ads)
            ad_data = EwAd(id_ad=id_ad)
            ad_resp = format_ad_response(ad_data)
            ad_formatting = "\n\n..."

    if poi.id_poi in['westoutskirts', 'ufoufo'] and ewcfg.dh_active and ewcfg.dh_stage >= 300:
        state = EwGamestate(id_server=user_data.id_server, id_state='shipstate')
        if poi.id_poi == 'westoutskirts' and state.bit == 1:
            extra_resp = '\nThere\'s a UFO landed here.'
        if poi.id_poi == 'ufoufo' and state.bit == 1:
            extra_resp = 'The UFO is currently landed.'


    # post result to channel
    if poi != None:
        wikichar = '\n\n<{}>'.format(poi.wikipage) if poi.wikipage != '' else ''
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(
            cmd.message.author,
            "You stand {} {}.\n\n{}{}{}...".format(
                poi.str_in,
                poi.str_name,
                str_desc,
                wikichar,
                void_resp
            )
        ))

        if poi.id_poi == ewcfg.poi_id_thesphere:
            return

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(
            cmd.message.author,
            "{}{}{}{}{}{}{}{}{}{}".format(
                capped_resp,
                slimes_resp,
                items_resp,
                players_resp,
                enemies_resp,
                worldevents_resp,
                soul_resp,
                extra_resp,
                ("\n\n{}".format(
                    ewutils.weather_txt(market_data)
                ) if cmd.guild != None else ""),
                ad_formatting
            )  # + get_random_prank_item(user_data, district_data) # SWILLDERMUK
        ))
        if len(ad_resp) > 0:
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(
                cmd.message.author,
                ad_resp
            ))


async def survey(cmd):
    user_data = EwUser(member=cmd.message.author)
    district_data = EwDistrict(district=user_data.poi, id_server=user_data.id_server)
    market_data = EwMarket(id_server=user_data.id_server)
    poi = poi_static.id_to_poi.get(user_data.poi)

    # if it's a subzone, check who owns the actual district
    if poi.is_subzone:
        controlled_poi = poi_static.id_to_poi.get(poi.mother_districts[0] if len(poi.mother_districts) > 0 else poi.father_district)
        controlled_data = EwDistrict(district=controlled_poi.id_poi, id_server=user_data.id_server)
    else:
        controlled_data = district_data

    capped_resp = "This district is controlled by {}.\n\n".format("the " + controlled_data.controlling_faction.capitalize() if controlled_data.controlling_faction != "" else "no one")
    slimes_resp = get_slimes_resp(user_data, district_data)
    items_resp = get_items_resp(user_data, district_data)
    players_resp = get_players_look_resp(user_data, district_data)
    enemies_resp = get_enemies_look_resp(user_data, district_data)
    worldevents_resp = get_world_events_look_resp(user_data, district_data)

    if poi.is_apartment:
        slimes_resp = ""
        items_resp = ""
        players_resp = ""

    direction_image = ""
    if poi.is_capturable or poi.id_poi in[ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown]:
        direction_image = '\nhttp://rfck.app/img/direction/{}_directions.png'.format(poi.id_poi)
    # post result to channel
    if poi != None:
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(
            cmd.message.author,
            "You stand {} {}.\n\n{}{}{}{}{}{}{}{}".format(
                poi.str_in,
                poi.str_name,
                capped_resp,
                slimes_resp,
                items_resp,
                players_resp,
                enemies_resp,
                worldevents_resp,
                ("\n\n{}".format(
                    ewutils.weather_txt(market_data)
                ) if cmd.guild != None else ""),
                direction_image,

            )  # + get_random_prank_item(user_data, district_data) # SWILLDERMUK
        ))


"""
    Get information about an adjacent zone.
"""


async def scout(cmd):
    user_data = EwUser(member=cmd.message.author)
    user_poi = poi_static.id_to_poi.get(user_data.poi)

    if ewutils.channel_name_is_poi(str(cmd.message.channel)) is False:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

    market_data = EwMarket(id_server=cmd.guild.id)
    mutations = user_data.get_mutations()

    # if user_data.life_state == ewcfg.life_state_corpse:
    #	response = "Who cares? These meatbags all look the same to you."
    #	return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # if no arguments given, scout own location
    if not len(cmd.tokens) > 1:
        poi = user_poi
    else:
        target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])
        poi = poi_static.id_to_poi.get(target_name)

    if poi == None:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Never heard of it."))

    else:
        # Check if the user has 'scopic retinas
        extended_range = False
        if ewcfg.mutation_id_scopicretinas in mutations:
            extended_range = True

        # Create a list of all valid pois
        valid_pois = set()
        valid_pois.add(user_data.poi)
        neighbors = []
        neighbors.extend(poi_static.poi_neighbors.get(user_data.poi))
        if user_poi.is_apartment:
            neighbors.extend(user_poi.mother_districts)

        # If the user is on any transport, the current stop is treated as a neighbor
        if user_poi.is_transport:
            transport_data = EwTransport(id_server=user_data.id_server, poi=user_poi.id_poi)
            neighbors.append(transport_data.current_stop)

        # Add neighbors to list, plus their neighbors if extended range
        for neigh in neighbors:
            valid_pois.add(neigh)
            if extended_range:
                valid_pois.update(poi_static.poi_neighbors.get(neigh))

        world_events_resp = ""
        world_events = bknd_worldevent.get_world_events(id_server=user_data.id_server, active_only=True)
        # For all presently-happening world events
        for id_event in world_events:
            # If the world event is a smog warning
            if world_events.get(id_event) in [ewcfg.event_type_smog_warning]:
                # Get the EVENT DATA
                event_data = bknd_worldevent.EwWorldEvent(id_event=id_event)
                smog_poi = event_data.event_props.get('poi')

                # If you're in the smog district or scouting it
                if user_data.poi == smog_poi or poi.id_poi == smog_poi:
                    response = "You wheeze and cry due to the noxious smog. None of your senses can break the veil."
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            # If there's a raid den open, make it scoutable.
            if world_events.get(id_event) == ewcfg.event_type_raid_den:
                # Get the EVENT DATA
                event_data = bknd_worldevent.EwWorldEvent(id_event=id_event)
                den_opening_poi = event_data.event_props.get('poi')

                # If you're in the raid district
                if user_data.poi == den_opening_poi:
                    valid_pois.add("raiddenentryway")
                    
            # If there's a world event in the scouted district, give corresponding flavor text
            elif world_events.get(id_event) in ewcfg.poi_events:
                event_data = bknd_worldevent.EwWorldEvent(id_event=id_event)

                if poi.id_poi == event_data.event_props.get('poi'):
                    event_def = poi_static.event_type_to_def.get(event_data.event_type)
                    # Just in case there's more than 1 somehow
                    world_events_resp += event_def.str_event_ongoing + "\n"

        if poi.id_poi not in valid_pois:    
            response = "You can't {} that far.".format(cmd.tokens[0])
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        district_data = EwDistrict(district=poi.id_poi, id_server=user_data.id_server)

        # don't show low level players or enemies
        min_level = math.ceil((1 / 10) ** 0.25 * user_data.slimelevel)

        life_states = [ewcfg.life_state_enlisted]

        if ewcfg.slimernalia_active:
            life_states.append(ewcfg.life_state_juvenile)
        
        # get information about players in the district
        players_in_district = district_data.get_players_in_district(min_level=min_level, life_states=life_states)
        if user_data.id_user in players_in_district:
            players_in_district.remove(user_data.id_user)

        num_players = 0
        players_resp = "\n"
        detailed_players_resp = "You pick up the scent of the following gangsters:"
        for player in players_in_district:
            scoutee_data = EwUser(id_user=player, id_server=user_data.id_server)
            scoutee_player = EwPlayer(id_user=player)
            scoutee_mutations = scoutee_data.get_mutations()
            if (ewcfg.mutation_id_whitenationalist in scoutee_mutations or ewcfg.mutation_id_airlock in scoutee_mutations) and market_data.weather == "snow":
                continue
            if ewcfg.mutation_id_threesashroud in scoutee_mutations and scoutee_data.life_state == ewcfg.life_state_enlisted:
                allies_in_district = district_data.get_players_in_district(min_level=min_level, life_states=[ewcfg.life_state_enlisted], factions=[scoutee_data.faction])
                if len(allies_in_district) > 3:
                    continue
            if ewcfg.mutation_id_chameleonskin in scoutee_mutations:
                member = cmd.guild.get_member(scoutee_data.id_user)
                if member == None or member.status == discord.Status.offline:
                    continue

            if ewcfg.mutation_id_aposematicstench in scoutee_mutations:
                num_players += math.floor(scoutee_data.slimelevel / 5)
                continue

            detailed_players_resp += "\n" + scoutee_player.display_name

            num_players += 1

        # No filtering is done on enemies themselves. Enemies that pose a threat to the player are filtered instead.
        enemies_in_district = district_data.get_enemies_in_district(scout_used=True)
        threats_in_district = district_data.get_enemies_in_district(min_level=min_level, scout_used=True)

        num_enemies = 0
        enemies_resp = ""

        num_threats = len(threats_in_district)
        threats_resp = ""

        detailed_enemies_resp = "You pick up the scent of the following enemies:\n"
        for enemy in enemies_in_district:
            enemy_data = EwEnemy(id_enemy=enemy)
            detailed_enemies_resp += "\n**{}**\n".format(enemy_data.display_name)
            num_enemies += 1

        if num_players == 0:
            players_resp += "You don’t notice any activity from this district."
        elif num_players == 1:
            players_resp += "You can hear the occasional spray of a spray can from a gangster in this district."
        elif num_players <= 5:
            players_resp += "You can make out a distant conversation between a few gangsters in this district."
        elif num_players <= 10:
            players_resp += "You can hear shouting and frequent gunshots from a group of gangsters in this district."
        else:
            players_resp += "You feel the ground rumble from a stampeding horde of gangsters in this district."

        if ewcfg.mutation_id_keensmell in mutations and num_players >= 1:
            players_resp += " " + detailed_players_resp

        # to avoid visual clutter, no scouting message is sent out for 0 enemies, and by extension, threats.
        if num_enemies == 0:
            enemies_resp = ""
        elif num_enemies == 1:
            enemies_resp += "You can faintly hear the bleating of an enemy coming from this district."
        elif num_enemies <= 5:
            enemies_resp += "You manage to pick up the sound of a few enemies howling amongst each other in this district."
        elif num_enemies <= 10:
            enemies_resp += "Your nerves tense due to the incredibly audible savagery coming from several enemies in this district."
        else:
            enemies_resp += "You feel shivers down your spine from the sheer amount of enemies ramping and raving within this district."

        if ewcfg.mutation_id_keensmell in mutations and num_enemies >= 1:
            enemies_resp += " " + detailed_enemies_resp

        if num_threats == 0:
            threats_resp = "The district doesn't really give off any strong sense of radiation."
        elif num_threats == 1:
            threats_resp += "You feel a small tingling sensation from nearby radiation."
        elif num_threats <= 5:
            threats_resp += "The radiation emanating from the district is giving you a slight headache."
        elif num_threats <= 10:
            threats_resp += "The radiation seeping in from the district is overwhelming. You feel like you're gonna puke."
        else:
            threats_resp += "Your skin begins to peel like a potato from the sheer amount of radiation close by!"

        if num_players == 0 and num_enemies >= 1:
            players_resp = ""
        elif num_players >= 1 and num_enemies == 0:
            enemies_resp = ""
            threats_resp = ""
        elif num_players == 0 and num_enemies == 0:
            threats_resp = ""

        # post result to channel
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(
            cmd.message.author,
            "**{}**:{}\n{}\n{}{}".format(
                poi.str_name,
                players_resp,
                enemies_resp,
                world_events_resp,
                threats_resp,
            )
        ))


async def teleport(cmd):
    blj_used = False
    if cmd.tokens[0] == (ewcfg.cmd_prefix + 'blj'):
        blj_used = True

    if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

    time_now = int(time.time())
    user_data = EwUser(member=cmd.message.author)
    poi_now = user_data.poi
    mutations = user_data.get_mutations()
    response = ""
    resp_cont = EwResponseContainer(id_server=cmd.guild.id)
    target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])

    if ewutils.active_restrictions.get(user_data.id_user) != None and ewutils.active_restrictions.get(user_data.id_user) > 0:
        response = "You can't do that right now."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if ewcfg.mutation_id_quantumlegs in mutations:
        mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_quantumlegs)
        if len(mutation_data.data) > 0:
            time_lastuse = int(mutation_data.data)
        else:
            time_lastuse = 0

        if time_lastuse + 60 * 60 > time_now:
            response = "You can't do that again yet. Try again in about {} minute(s)".format(math.ceil((time_lastuse + 60 * 60 - time_now) / 60))
            return await fe_utils.send_response(response, cmd)

        if cmd.tokens_count < 2 and not blj_used:
            response = "Teleport where?"
            return await fe_utils.send_response(response, cmd)
        elif cmd.tokens_count < 2 and blj_used:
            response = "Backwards Long Jump where?"
            return await fe_utils.send_response(response, cmd)

        poi = poi_static.id_to_poi.get(target_name)

        if poi is None:
            return await fe_utils.send_response("Never heard of it.", cmd)

        elif poi.id_poi == user_data.poi:
            return await fe_utils.send_response("You're already there, bitch.", cmd)

        elif poi.closed:
            return await fe_utils.send_response(poi.str_closed + " (bitch)", cmd)

        elif move_utils.inaccessible(user_data=user_data, poi=poi):
            return await fe_utils.send_response("You're not allowed to go there (bitch).", cmd)

        valid_destinations = set()
        neighbors = poi_static.poi_neighbors.get(user_data.poi)
        for neigh in neighbors:
            valid_destinations.add(neigh)
            valid_destinations.update(poi_static.poi_neighbors.get(neigh))

        if poi.id_poi not in valid_destinations:
            response = "You can't {} that far.".format(cmd.tokens[0])
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        # 15 second windup before teleport goes through (changing timeout to 15 is  = all i need to do right?)
        windup_finished = True

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You get a running start to charge up your Quantum Legs..."))

        ewutils.last_warps[user_data.id_user] = time_now
        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

        try:
            msg = await cmd.client.wait_for('message', timeout=15, check=lambda message: message.author == cmd.message.author and
                                                                                         cmd.message.content.startswith(ewcfg.cmd_prefix))

            if msg != None:
                windup_finished = False

        except:
            windup_finished = True

        user_data = EwUser(member=cmd.message.author)

        if windup_finished and user_data.poi == poi_now:
            mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_quantumlegs)

            mutation_data.data = str(time_now)
            mutation_data.persist()

            if not blj_used:
                response = "WHOOO-"
            else:
                response = "YAHOO! YAHOO! Y-Y-Y-Y-Y-"

            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            poi_channel = fe_utils.get_channel(cmd.guild, poi.channel)

            await fe_utils.send_message(cmd.client, poi_channel, "A rift in time and space is pouring open! Something's coming through!!")

            await asyncio.sleep(5)

            if not blj_used:
                response = "-OOOP!"
            else:
                response = "-AHOO!"

            user_data = EwUser(member=cmd.message.author)

            ewutils.moves_active[cmd.message.author.id] = 0



            if poi.id_poi == ewcfg.poi_id_thesewers:
                die_resp = await user_data.die(cause=ewcfg.cause_suicide)
                return await die_resp.post()

            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author, new_poi=poi.id_poi)
            user_data.poi = poi.id_poi
            user_data.time_lastenter = int(time.time())



            user_data.persist()
            await rutils.movement_checker(user_data, poi_static.id_to_poi.get(user_data.poi), poi, cmd)

            enemy_lock_impose_restrictions(id_user=user_data.id_user, poi=poi.id_poi)
            await one_eye_dm(id_user=user_data.id_user, id_server=user_data.id_server, poi=poi.id_poi)
            await user_data.move_inhabitants(id_poi=poi.id_poi)
            resp_cont.add_channel_response(poi.channel, fe_utils.formatMessage(cmd.message.author, response))
            await resp_cont.post()

            # SWILLDERMUK
            await prank_utils.activate_trap_items(poi.id_poi, user_data.id_server, user_data.id_user)

            return
        else:
            mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_quantumlegs)

            mutation_data.data = str(time_now)
            mutation_data.persist()

            # Get the channel for the poi the user is currently in, just in case they've moved to a different poi before the teleportation went through.
            current_poi = poi_static.id_to_poi.get(user_data.poi)
            current_channel = fe_utils.get_channel(cmd.guild, current_poi.channel)

            response = "You slow down before the teleportation goes through."
            return await fe_utils.send_message(cmd.client, current_channel, fe_utils.formatMessage(cmd.message.author, response))
    else:

        if not blj_used:
            response = "You don't have any toilet paper."
        else:
            response = "You don't even know what that MEANS."

        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def teleport_player(cmd):
    author = cmd.message.author
    user_data = EwUser(member=author)

    if not (ewutils.DEBUG or author.guild_permissions.administrator or user_data.life_state == ewcfg.life_state_kingpin):
        return

    if cmd.mentions_count == 1:
        target = cmd.mentions[0]
    else:
        target = author

    if target.id == author.id and cmd.mentions_count != 1:
        destination = cmd.tokens[1].lower()
    else:
        destination = cmd.tokens[2].lower()


    new_poi = poi_static.id_to_poi.get(destination)


    if target != None and new_poi != None:
        target_user = EwUser(member=target)
        target_player = EwPlayer(id_user=target_user.id_user)

        ewutils.moves_active[target_user.id_user] = 0

        target_user.poi = new_poi.id_poi
        target_user.persist()

        response = "{} has been teleported to {}".format(target_player.display_name, new_poi.id_poi)

        await ewrolemgr.updateRoles(client=cmd.client, member=target)

        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Get information about all the pois in the poi list
"""


async def print_map_data(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    districts_count = 0
    subzones_count = 0
    apartments_count = 0
    outskirts_count = 0
    streets_count = 0
    transports_count = 0

    for poi in poi_static.poi_list:

        if poi.is_district:
            districts_count += 1

            # print(poi.major_role)
            # print(poi.minor_role)

        if poi.is_subzone:
            subzones_count += 1
        if poi.is_apartment:
            apartments_count += 1
        if poi.is_outskirts:
            outskirts_count += 1
        if poi.is_street:
            streets_count += 1

            # print(poi.minor_role)

        if poi.is_transport:
            transports_count += 1

        neighbor_count = 0

        # print('\n\nNeighbors for {}\n====================='.format(poi.str_name))
        for neighbor_poi in poi_static.poi_list:

            if neighbor_poi.id_poi in poi.neighbors.keys() and poi.id_poi not in neighbor_poi.neighbors.keys():
                print('\n========================\nsevered connection for POIs {} and {}'.format(poi.str_name, neighbor_poi.str_name))
            elif poi.id_poi in neighbor_poi.neighbors.keys() and neighbor_poi.id_poi not in poi.neighbors.keys():
                print('\n========================\nsevered connection for POIs {} and {}'.format(poi.str_name, neighbor_poi.str_name))

        if poi.is_subzone:
            for neighbor in poi.neighbors.keys():
                if neighbor not in poi.mother_districts:
                    ewutils.logMsg('Subzone {} has invalid mother district(s)'.format(poi.str_name))

            # if neighbor_poi.id_poi in poi.neighbors.keys():
            # if poi.id_poi in neighbor_poi.neighbors.keys():
            # neighbor_count += 1
            # print(neighbor_poi.str_name)

        # if poi.is_outskirts:
        # print('found {} neighbors for {}'.format(neighbor_count, poi.id_poi))

    # client = ewutils.get_client()
    # server = client.get_server(cmd.guild.id)
    #
    # rolenames = []
    # for role in server.roles:
    # 	rolenames.append(role.name)
    #
    # rolenames.sort()
    # for name in rolenames:
    # 	print(name)

    print("\n\nPOI LIST STATISTICS:\n{} districts\n{} subzones\n{} apartments\n{} outskirts\n{} streets\n{} transports\n\n".format(districts_count, subzones_count, apartments_count, outskirts_count, streets_count, transports_count))


"""
    Command that moves everyone from one district to another
"""


async def boot(cmd):
    author = cmd.message.author
    user_data = EwUser(member=cmd.message.author)

    if not author.guild_permissions.administrator and user_data.life_state != ewcfg.life_state_kingpin:
        response = "You do not have the power to move the masses from one location to another."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if len(cmd.tokens) != 3:
        response = 'Usage: !boot [location A] [location B]'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    destination_a = cmd.tokens[1]
    destination_b = cmd.tokens[2]

    old_poi = poi_static.id_to_poi.get(destination_a)
    new_poi = poi_static.id_to_poi.get(destination_b)

    if old_poi != None and new_poi != None:

        district_data = EwDistrict(district=old_poi.id_poi, id_server=user_data.id_server)

        users = district_data.get_players_in_district()

        for user in users:
            moved_user_data = EwUser(id_user=user, id_server=user_data.id_server)
            moved_user_data.poi = new_poi.id_poi
            moved_user_data.persist()
        response = "Everyone in {} has been moved to {}!".format(old_poi.id_poi, new_poi.id_poi)

    if destination_a == "all" and new_poi != None:
        for district in poi_static.poi_list:
            district_data = EwDistrict(district=district.id_poi, id_server=user_data.id_server)

            users = district_data.get_players_in_district()

            for user in users:
                moved_user_data = EwUser(id_user=user, id_server=user_data.id_server)
                moved_user_data.poi = new_poi.id_poi
                moved_user_data.persist()

        response = "@everyone has been moved to {}".format(new_poi.id_poi)

    else:
        response = '**DEBUG:** Invalid POIs'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Enter and exit the breakroom
"""





async def flush_subzones(cmd):
    member = cmd.message.author

    if not member.guild_permissions.administrator:
        return

    subzone_to_mother_districts = {}

    for poi in poi_static.poi_list:
        if poi.is_subzone:
            subzone_to_mother_districts[poi.id_poi] = poi.mother_districts

    for subzone in subzone_to_mother_districts:
        mother_districts = subzone_to_mother_districts.get(subzone)

        used_mother_district = mother_districts[0]

        item_cache = bknd_core.get_cache(obj_type = "EwItem")
        if item_cache is not False:
            targets_data = item_cache.find_entries(criteria={"id_owner": subzone, "id_server": cmd.guild.id})
            for itm_dat in targets_data:
                itm_dat.update({"id_owner": used_mother_district})
                item_cache.set_entry(data=itm_dat)

        bknd_core.execute_sql_query("UPDATE items SET {id_owner} = %s WHERE {id_owner} = %s AND {id_server} = %s".format(
            id_owner=ewcfg.col_id_user,
            id_server=ewcfg.col_id_server
        ), (
            used_mother_district,
            subzone,
            cmd.guild.id
        ))

        subzone_data = EwDistrict(district=subzone, id_server=cmd.guild.id)
        district_data = EwDistrict(district=used_mother_district, id_server=cmd.guild.id)

        district_data.change_slimes(n=subzone_data.slimes)
        subzone_data.change_slimes(n=-subzone_data.slimes)

        district_data.persist()
        subzone_data.persist()


async def flush_streets(cmd):
    member = cmd.message.author

    if not member.guild_permissions.administrator:
        return

    for poi in poi_static.poi_list:
        if poi.is_street:

            street_data = EwDistrict(district=poi.id_poi, id_server=cmd.guild.id)

            players = street_data.get_players_in_district()
            for player in players:
                user_data = EwUser(id_user=player, id_server=cmd.guild.id)
                user_data.poi = ewcfg.poi_id_juviesrow
                user_data.persist()
                member = cmd.guild.get_member(player)
                await ewrolemgr.updateRoles(client=cmd.client, member=member)

            item_cache = bknd_core.get_cache(obj_type = "EwItem")
            if item_cache is not False:
                targets_data = item_cache.find_entries(criteria={"id_owner": poi.id_poi, "id_server": cmd.guild.id})
                for itm_dat in targets_data:
                    itm_dat.update({"id_owner": poi.father_district})
                    item_cache.set_entry(data=itm_dat)

            bknd_core.execute_sql_query("UPDATE items SET {id_owner} = %s WHERE {id_owner} = %s AND {id_server} = %s".format(
                id_owner=ewcfg.col_id_user,
                id_server=ewcfg.col_id_server
            ), (
                poi.father_district,
                poi.id_poi,
                cmd.guild.id
            ))

            district_data = EwDistrict(district=poi.father_district, id_server=cmd.guild.id)

            district_data.change_slimes(n=street_data.slimes)
            street_data.change_slimes(n=-street_data.slimes)

            district_data.persist()
            street_data.persist()

            ewutils.logMsg("Cleared {}.".format(poi.id_poi))

    ewutils.logMsg("Finished flushing streets.")


async def loop(cmd):
    if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

    time_now = int(time.time())
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    resp_cont = EwResponseContainer(id_server=cmd.guild.id)
    dest_poi = poi_static.landlocked_destinations.get(user_data.poi)
    dest_poi_obj = poi_static.id_to_poi.get(dest_poi)

    if ewutils.active_restrictions.get(user_data.id_user) != None and ewutils.active_restrictions.get(user_data.id_user) > 0:
        response = "You can't do that right now."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if ewcfg.mutation_id_landlocked not in mutations:
        response = "You don't feel very loopy at the moment. Just psychotic, mostly."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        mutation_data = EwMutation(id_mutation=ewcfg.mutation_id_landlocked, id_user=cmd.message.author.id, id_server=cmd.message.guild.id)

        if len(mutation_data.data) > 0:
            time_lastuse = int(mutation_data.data)
        else:
            time_lastuse = 0

        if time_lastuse + 60 * 60 > time_now:
            response = "You can't do that again yet. Try again in about {} minute(s)".format(math.ceil((time_lastuse + 60 * 60 - time_now) / 60))
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        if user_data.poi not in poi_static.landlocked_destinations.keys():
            response = "You need to be on the edge of the map to !loop through it. Try a district bordering an outskirt, the ferry, or Slime's End Cliffs."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        # global move_counter
        move_utils.move_counter += 1
        move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You start looping to {}.".format(dest_poi_obj.str_name)))
        await asyncio.sleep(20)

        if move_current == ewutils.moves_active[cmd.message.author.id]:
            mutation_data = EwMutation(id_mutation=ewcfg.mutation_id_landlocked, id_user=cmd.message.author.id, id_server=cmd.message.guild.id)

            mutation_data.data = str(time_now)
            mutation_data.persist()

            user_data = EwUser(member=cmd.message.author)
            ewutils.moves_active[cmd.message.author.id] = 0
            user_data.time_lastenter = int(time.time())
            ewutils.active_target_map[user_data.id_user] = ""
            ewutils.end_trade(user_data.id_user)
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author, new_poi=dest_poi)
            user_data.poi = dest_poi
            user_data.persist()
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "**VOIIII-**".format(dest_poi_obj.str_name)))

            await user_data.move_inhabitants(id_poi=dest_poi_obj.id_poi)
            await prank_utils.activate_trap_items(dest_poi_obj.id_poi, user_data.id_server, user_data.id_user)
            return await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, dest_poi_obj.channel), fe_utils.formatMessage(cmd.message.author, "**-OIIIIP!!!**\n\n{} jumps out of a wormhole!".format(cmd.message.author.display_name)))
        else:
            pass


async def surveil(cmd):
    user_data = EwUser(member=cmd.message.author)
    players = []
    districts = []
    response = ""
    if user_data.poi != ewcfg.poi_id_thebreakroom:
        response = "You need to be in the Slimecorp Breakroom to spy on the masses."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    for poi in poi_static.poi_list:
        if poi.is_district and poi.is_capturable == True:
            districts.append(poi)

    for district in districts:
        dist_obj = EwDistrict(id_server=cmd.guild.id, district=district.id_poi)
        if dist_obj.capture_points >= ewcfg.max_capture_points[dist_obj.property_class] and dist_obj.cap_side == 'slimecorp':
            players.extend(dist_obj.get_players_in_district(life_states=[ewcfg.life_state_enlisted]))

    if len(players) > 0:
        for player in players:
            target_obj = EwUser(id_user=player, id_server=cmd.guild.id)
            player_obj = EwPlayer(id_user=player, id_server=cmd.guild.id)
            poi = poi_static.id_to_poi.get(target_obj.poi)
            response += "{} is in {}.\n".format(player_obj.display_name, poi.str_name)
    else:
        response = "Nobody's out on the cameras now."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
