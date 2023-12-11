import asyncio

from ew.backend import item as bknd_item
from ew.static import cfg as ewcfg
from ew.static import poi as poi_static
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import move as move_utils
from ew.utils import prank as prank_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.frontend import EwResponseContainer
from ew.utils.transport import EwTransport, get_transports_at_stop

""" Enter a transport vehicle from a transport stop """


async def embark(cmd):
    # can only use movement commands in location channels
    if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    response = ""

    if ewutils.active_restrictions.get(user_data.id_user) != None and ewutils.active_restrictions.get(user_data.id_user) > 0:
        response = "You can't do that right now."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if user_data.get_inhabitee():
        # prevent ghosts currently inhabiting other players from moving on their own
        response = "You might want to **{}** of the poor soul you've been tormenting first.".format(ewcfg.cmd_letgo)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # poi = ewmap.fetch_poi_if_coordless(cmd.message.channel.name)

    # must be at a transport stop to enter a transport
    if poi != None and poi.id_poi in poi_static.transport_stops:
        transport_ids = get_transports_at_stop(id_server=user_data.id_server, stop=poi.id_poi)

        # can't embark, when there's no vehicles to embark on
        if len(transport_ids) == 0:
            response = "There are currently no transport vehicles to embark on here."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        # automatically embark on the only transport at the station, if no arguments were provided
        elif len(transport_ids) == 1 and cmd.tokens_count < 2:
            transport_data = EwTransport(id_server=user_data.id_server, poi=transport_ids[0])
            target_name = transport_data.current_line

        # get target name from command arguments
        else:
            target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])

        # report failure, if the vehicle to be boarded couldn't be ascertained
        if target_name == None or len(target_name) == 0:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Which transport line?"))

        if target_name in ['green', 'blue', 'red', 'yellow', 'white']:
            for transport in transport_ids:
                if target_name in transport:
                    transport_data = EwTransport(id_server=user_data.id_server, poi=transport)
                    target_name = transport_data.current_line

        transport_line = poi_static.id_to_transport_line.get(target_name)

        # report failure, if an invalid argument was given
        if transport_line == None:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Never heard of it."))

        for transport_id in transport_ids:
            transport_data = EwTransport(id_server=user_data.id_server, poi=transport_id)

            # check if one of the vehicles at the stop matches up with the line, the user wants to board
            if transport_data.current_line == transport_line.id_line:
                ticket = None

                if ewcfg.dh_active and ewcfg.dh_stage >= 1:
                    user_data = EwUser(member = cmd.message.author)
                    if user_data.poi in [ewcfg.poi_id_dt_subway_station, ewcfg.poi_id_rr_subway_station, ewcfg.poi_id_jr_subway_station]:
                        if transport_line.id_line in [ewcfg.transport_line_subway_white_eastbound, ewcfg.transport_line_subway_white_westbound]:
                            ticket = bknd_item.find_item(item_search=ewcfg.item_id_whitelineticket, id_user=cmd.message.author.id,  id_server=cmd.message.guild.id)
                            if ticket is None:

                                response = "You need a ticket to embark on the White Line."
                                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

                last_stop_poi = poi_static.id_to_poi.get(transport_line.last_stop)
                response = "Embarking on {}.".format(transport_line.str_name)
                # schedule tasks for concurrent execution
                message_task = asyncio.ensure_future(fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response)))
                wait_task = asyncio.ensure_future(asyncio.sleep(ewcfg.time_embark))

                # Take control of the move for this player.
                move_utils.move_counter += 1
                move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
                await message_task
                await wait_task

                # check if the user entered another movement command while waiting for the current one to be completed
                if move_current == ewutils.moves_active[cmd.message.author.id]:
                    user_data = EwUser(member=cmd.message.author)

                    transport_data = EwTransport(id_server=user_data.id_server, poi=transport_id)

                    # check if the transport is still at the same stop
                    if transport_data.current_stop == poi.id_poi:
                        user_data.poi = transport_data.poi
                        user_data.persist()

                        transport_poi = poi_static.id_to_poi.get(transport_data.poi)

                        response = "You enter the {}.".format(transport_data.transport_type)
                        if ticket is not None:
                            bknd_item.item_delete(ticket.get("id_item"))
                        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
                        await user_data.move_inhabitants(id_poi=transport_data.poi)
                        return await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, transport_poi.channel), fe_utils.formatMessage(cmd.message.author, response))
                    else:
                        response = "The {} starts moving just as you try to get on.".format(transport_data.transport_type)
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        response = "There is currently no vehicle following that line here."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


    else:
        response = "No transport vehicles stop here. Try going to a subway station or a ferry port."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Exit a transport vehicle into its current stop """


async def disembark(cmd):
    # can only use movement commands in location channels
    if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))
    user_data = EwUser(member=cmd.message.author)
    response = ""
    resp_cont = EwResponseContainer(client=cmd.client, id_server=user_data.id_server)

    # prevent ghosts currently inhabiting other players from moving on their own
    if user_data.get_inhabitee():
        response = "You might want to **{}** of the poor soul you've been tormenting first.".format(ewcfg.cmd_letgo)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # can only disembark when you're on a transport vehicle
    elif user_data.poi in poi_static.transports:
        transport_data = EwTransport(id_server=user_data.id_server, poi=user_data.poi)
        response = "{}ing.".format(cmd.tokens[0][1:].lower()).capitalize()

        stop_poi = poi_static.id_to_poi.get(transport_data.current_stop)
        # if stop_poi.is_subzone:
        # 	stop_poi = poi_static.id_to_poi.get(stop_poi.mother_district)

        if move_utils.inaccessible(user_data=user_data, poi=stop_poi):
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You're not allowed to go there (bitch)."))

        # schedule tasks for concurrent execution
        message_task = asyncio.ensure_future(fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response)))
        wait_task = asyncio.ensure_future(asyncio.sleep(ewcfg.time_embark))

        # Take control of the move for this player.
        move_utils.move_counter += 1
        move_current = ewutils.moves_active[cmd.message.author.id] = move_utils.move_counter
        await message_task
        await wait_task

        # check if the user entered another movement command while waiting for the current one to be completed
        if move_current != ewutils.moves_active[cmd.message.author.id]:
            return

        user_data = EwUser(member=cmd.message.author)
        transport_data = EwTransport(id_server=user_data.id_server, poi=transport_data.poi)

        # cancel move, if the user has left the transport while waiting for movement to be completed (e.g. by dying)
        if user_data.poi != transport_data.poi:
            return

        stop_poi = poi_static.id_to_poi.get(transport_data.current_stop)

        # juvies can't swim
        if transport_data.current_stop == ewcfg.poi_id_slimesea and user_data.life_state != ewcfg.life_state_corpse:
            if user_data.life_state == ewcfg.life_state_kingpin:
                response = "You try to heave yourself over the railing as you're hit by a sudden case of sea sickness. You puke into the sea and sink back on deck."
                response = fe_utils.formatMessage(cmd.message.author, response)
                return await fe_utils.send_message(cmd.client, cmd.message.channel, response)
            user_data.poi = ewcfg.poi_id_slimesea
            user_data.trauma = ewcfg.trauma_id_environment
            die_resp = await user_data.die(cause=ewcfg.cause_drowning)
            resp_cont.add_response_container(die_resp)

            response = "{} jumps over the railing of the ferry and promptly drowns in the slime sea.".format(cmd.message.author.display_name)
            resp_cont.add_channel_response(channel=ewcfg.channel_slimesea, response=response)
            resp_cont.add_channel_response(channel=ewcfg.channel_ferry, response=response)
        # they also can't fly
        elif transport_data.transport_type == ewcfg.transport_type_blimp and not stop_poi.is_transport_stop and user_data.life_state != ewcfg.life_state_corpse:
            user_mutations = user_data.get_mutations()
            if user_data.life_state == ewcfg.life_state_kingpin:
                response = "Your life flashes before your eyes, as you plummet towards your certain death. A lifetime spent being a piece of shit and playing videogames all day. You close your eyes and... BOING! You open your eyes again to see a crew of workers transporting the trampoline that broke your fall. You get up and dust yourself off, sighing heavily."
                response = fe_utils.formatMessage(cmd.message.author, response)
                resp_cont.add_channel_response(channel=stop_poi.channel, response=response)
                user_data.poi = stop_poi.id_poi
                user_data.persist()
                await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
                return await resp_cont.post()

            elif ewcfg.mutation_id_lightasafeather in user_mutations or ewcfg.mutation_id_airlock in user_mutations:
                response = "With a running jump you launch yourself out of the blimp and begin falling to your soon-to-be demise... but then a strong updraft breaks your fall and you land unscathed. "
                response = fe_utils.formatMessage(cmd.message.author, response)
                resp_cont.add_channel_response(channel=stop_poi.channel, response=response)
                user_data.poi = stop_poi.id_poi
                user_data.persist()
                await user_data.move_inhabitants(id_poi=stop_poi.id_poi)
                await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
                return await resp_cont.post()
            district_data = EwDistrict(id_server=user_data.id_server, district=stop_poi.id_poi)
            district_data.change_slimes(n=user_data.slimes)
            district_data.persist()
            user_data.poi = stop_poi.id_poi
            user_data.trauma = ewcfg.trauma_id_environment
            die_resp = await user_data.die(cause=ewcfg.cause_falling)
            resp_cont.add_response_container(die_resp)
            response = "SPLAT! A body collides with the asphalt with such force, that it is utterly annihilated, covering bystanders in blood and slime and guts."
            resp_cont.add_channel_response(channel=stop_poi.channel, response=response)

        # update user location, if move successful
        else:
            # if stop_poi.is_subzone:
            # 	stop_poi = poi_static.id_to_poi.get(stop_poi.mother_district)

            if move_utils.inaccessible(user_data=user_data, poi=stop_poi):
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You're not allowed to go there (bitch)."))

            user_data.poi = stop_poi.id_poi
            user_data.persist()
            await user_data.move_inhabitants(id_poi=stop_poi.id_poi)
            response = "You enter {}".format(stop_poi.str_name)
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
            await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, stop_poi.channel), fe_utils.formatMessage(cmd.message.author, response))

            # SWILLDERMUK
            await prank_utils.activate_trap_items(stop_poi.id_poi, user_data.id_server, user_data.id_user)

            return
        return await resp_cont.post()
    else:
        response = "You are not currently riding any transport."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def check_schedule(cmd):
    if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)
    response = ""

    if poi.is_transport_stop:
        response = "The following public transit lines stop here:"
        for line in poi.transport_lines:
            line_data = poi_static.id_to_transport_line.get(line)
            response += "\n-" + line_data.str_name
    elif poi.is_transport:
        transport_data = EwTransport(id_server=user_data.id_server, poi=poi.id_poi)
        transport_line = poi_static.id_to_transport_line.get(transport_data.current_line)
        response = "This {} is following {}.".format(transport_data.transport_type, transport_line.str_name.replace("The", "the"))
    else:
        response = "There is no schedule to check here."

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
