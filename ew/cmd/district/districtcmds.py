import asyncio
from time import time

from ew.static import cfg as ewcfg
from ew.static import poi as poi_static
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.backend.dungeons import EwGamestate
from ew.backend.item import EwItem
from ew.backend import item as bknd_item


try:
    from ew.cmd import debug as ewdebug
except:
    from ew.cmd import debug_dummy as ewdebug

"""
	Informs the player about their current zone's capture progress
"""


async def capture_progress(cmd):
    user_data = EwUser(member=cmd.message.author)
    response = ""

    poi = poi_static.id_to_poi.get(user_data.poi)
    response += "**{}**: ".format(poi.str_name)

    if not user_data.poi in poi_static.capturable_districts:
        response += "This zone cannot be captured."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    district_data = EwDistrict(id_server=user_data.id_server, district=user_data.poi)
    percent_progress_after = int(district_data.capture_points / district_data.max_capture_points * 100)


    if district_data.capturing_faction not in ["", district_data.controlling_faction] and district_data.controlling_faction != '':
        response += "{} have been de-capturing this district. ".format(district_data.capturing_faction.capitalize())
    elif district_data.controlling_faction == district_data.capturing_faction and district_data.controlling_faction != '':
        response += "{} have been tightening control of this district. ".format(district_data.capturing_faction.capitalize())
    elif district_data.controlling_faction != "":
        response += "{} control this district. ".format(district_data.controlling_faction.capitalize())
    elif district_data.capturing_faction != "":
        response += "{} have been capturing this district. ".format(district_data.capturing_faction.capitalize())
    else:
        response += "Nobody has staked a claim to this district yet. "
    
    if district_data.time_unlock > 0:
        response += "\n\n**It's impossible to capture at the moment.**"
        if not district_data.all_neighbors_friendly():
            response += "But the lock is starting to decay..."

    response += "Current progress: {progress}%".format(progress=percent_progress_after)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))





async def change_spray(cmd):
    user_data = EwUser(member=cmd.message.author)
    newspray = cmd.message.content[(len(ewcfg.cmd_changespray)):].strip()

    if newspray == "":
        response = "You need to add an image link to change your spray."
    elif len(newspray) > 400:
        response = "Fucking christ, are you painting the Sistine Chapel? Use a shorter link."
    else:
        response = "Got it. Spray set."
        user_data.spray = newspray
        user_data.persist()

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def tag(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.life_state in (ewcfg.life_state_enlisted, ewcfg.life_state_kingpin):
        response = user_data.spray
    else:
        response = "Save the spraying for the gangsters. You're either too gay or dead to participate in this sort of thing."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def ufo_observe(cmd):
    user_data = EwUser(member = cmd.message.author)

    cosmetics = bknd_item.inventory(id_user=user_data.id_user, id_server=cmd.guild.id, item_type_filter=ewcfg.it_cosmetic)

    protected = False
    for cosmetic in cosmetics:
        cosmetic_data = EwItem(id_item=cosmetic.get('id_item'))
        if cosmetic_data.item_props.get('id_cosmetic') == 'skinsuit':
            if cosmetic_data.item_props.get('adorned') == 'true':
                protected = True

    shipstate = EwGamestate(id_state='shipstate', id_server=cmd.guild.id)

    if user_data.poi != 'ufoufo':
        return await ewdebug.scrutinize(cmd=cmd)
    elif not protected:
        response = "Those aliens would probably ass-probe the fuck out of you if you messed with their equipment. Better not."
    elif shipstate.bit == 1:
        response = "The ship is grounded. Can't see much from here."
    elif cmd.tokens_count <= 1:
        response = "Observe what?"
    elif not ewcfg.dh_active or ewcfg.dh_stage != 300:
        response = "Wait, your alien espionage is waaaay out of season."
    else:
        poi_seek = ewutils.flattenTokenListToString(cmd.tokens[1:])
        poi_sought = poi_static.id_to_poi.get(poi_seek)
        if poi_sought is None:
            response = "The aliens know all the district names. You don't have to make up weird shit."
        elif poi_sought.id_poi == 'ufoufo':
            return await ewdebug.scrutinize(cmd=cmd)
        elif poi_sought.is_street:
            response = "You try to zoom in on a specific street, but you're a little too high up to get that level of detail."
        elif poi_sought.id_poi == 'blackpond' or (not poi_sought.is_district and not poi_sought.is_outskirts and not poi_sought.is_pier and poi_sought.id_poi not in [ewcfg.poi_id_slimesendcliffs, ewcfg.poi_id_ferry, ewcfg.poi_id_sodafountain, ewcfg.poi_id_stockexchange, ewcfg.poi_id_ab_farms, ewcfg.poi_id_og_farms, ewcfg.poi_id_jr_farms]):
            response = "The X-ray vision on this viewport sucks. You can't really see indoors."
        elif poi_sought.id_poi in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown]:
            response = "Do you want to blow your cover, dumbass? Stop acting like a gangster. The gang bases are mostly indoors anyway."
        else:
            new_permissions = {"ufo-ufo": ["read", "send", "connect"]}
            new_permissions[poi_sought.channel] = ["read"]
            current_poi = poi_static.id_to_poi.get('ufoufo')
            response = ""
            if current_poi is not None:
                response = 'You point the observation reticle over at {}.'.format(poi_sought.str_name)
                district_data = EwDistrict(id_server=cmd.guild.id, district='ufoufo')
                poi_static.id_to_poi['ufoufo'].permissions = new_permissions
                players_in_district = district_data.get_players_in_district(min_slimes=0, life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_corpse, ewcfg.life_state_juvenile], ignore_offline=True)
                server = ewcfg.server_list[cmd.guild.id]
                for playerid in players_in_district:
                    member_object = await fe_utils.get_member(server, playerid)
                    await ewrolemgr.updateRoles(client=cmd.client, member=member_object)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def launch(cmd):
    user_data = EwUser(member=cmd.message.author)
    protected = False
    cosmetics = bknd_item.inventory(id_user=user_data.id_user, id_server=cmd.guild.id, item_type_filter=ewcfg.it_cosmetic)
    for cosmetic in cosmetics:
        cosmetic_data = EwItem(id_item=cosmetic.get('id_item'))
        if cosmetic_data.item_props.get('id_cosmetic') == 'skinsuit':
            if cosmetic_data.item_props.get('adorned') == 'true':
                protected = True

    if user_data.poi != 'ufoufo':
        response = "Launch what, dumbass? My patience?"
    elif not protected:
        response = "The aliens aren't gonna let you start the ship. You're basically their captive now."
    elif not ewcfg.dh_active or ewcfg.dh_stage != 300:
        response = "Wait, your alien espionage is waaaay out of season."
    else:
        launchstate = EwGamestate(id_state='shipstate', id_server=cmd.guild.id)
        if launchstate.bit == 1:
            response = "PCHOOOOOOOOOO! Weird bleeps and bloops begin to increase in frequency as the ship rises back into the air!"
            launchstate.bit = 0
            launchstate.persist()
        else:
            response = "WHOOOOOOOO -CRASH! Your poor piloting crashes the ship back down. Your fellow alien crew seems excited, like you just chugged a whole bottle of their galactic lager or something. Good thing the hull is so shock resistant or you wouldn't be able to joyride again."
            launchstate.bit = 1
            launchstate.persist()
    return await fe_utils.send_message(cmd.client, cmd.message.channel,fe_utils.formatMessage(cmd.message.author, response))


async def abduct(cmd):
    user_data = EwUser(member=cmd.message.author)
    item_sought = bknd_item.find_item(item_search='batterypack', id_user=cmd.message.author.id, id_server=cmd.guild.id)

    protected = False
    cosmetics = bknd_item.inventory(id_user=user_data.id_user, id_server=cmd.guild.id,
                                    item_type_filter=ewcfg.it_cosmetic)
    for cosmetic in cosmetics:
        cosmetic_data = EwItem(id_item=cosmetic.get('id_item'))
        if cosmetic_data.item_props.get('id_cosmetic') == 'skinsuit':
            if cosmetic_data.item_props.get('adorned') == 'true':
                protected = True

    shipstate = EwGamestate(id_server=user_data.id_server, id_state='shipstate')

    if user_data.poi != 'ufoufo':
        response = "Abduct what, dumbass? My patience?"
    elif not protected:
        response = "The aliens aren't gonna let you start the ship. You're basically their captive now."
    elif not ewcfg.dh_active or ewcfg.dh_stage != 300:
        response = "Wait, your alien espionage is waaaay out of season."
    elif cmd.mentions_count == 0:
        response = "Abduct who?"
    elif cmd.mentions_count > 1:
        response = "One victim at a time, please."
    elif shipstate.bit == 1:
        response = 'The ship\'s on the ground right now, it can\'t reach you.'

    else:
        if item_sought:
            target_data = EwUser(member = cmd.mentions[0])
            target_poi = poi_static.id_to_poi.get(target_data.poi)
            target_channel = fe_utils.get_channel(cmd.message.guild, target_poi.channel)

            if target_poi.id_poi == 'blackpond' or (
                        not target_poi.is_district and not target_poi.is_outskirts and not target_poi.is_pier and target_poi.id_poi not in [
                    ewcfg.poi_id_slimesendcliffs, ewcfg.poi_id_ferry, ewcfg.poi_id_sodafountain,
                    ewcfg.poi_id_stockexchange, ewcfg.poi_id_ab_farms, ewcfg.poi_id_og_farms, ewcfg.poi_id_jr_farms]):
                response = "The tractor beam on this ship sucks. You can't really see indoors."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            elif target_poi.id_poi in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown]:
                response = "Don't do that."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            bknd_item.item_delete(id_item=item_sought.get('id_item'))
            ewutils.moves_active[target_data.id_user] = 0
            response = 'You plug in your battery pack and begin to abduct {} They\'re 20 seconds away.'.format(cmd.mentions[0].display_name)
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            await fe_utils.send_message(cmd.client, target_channel, fe_utils.formatMessage(cmd.mentions[0], "You are being abducted by aliens. The ship is 20 seconds away."))
            ewutils.active_restrictions[target_data.id_user] = 2
            await asyncio.sleep(20)

            ewutils.active_restrictions[target_data.id_user] = 0
            ewutils.moves_active[cmd.message.author.id] = 0
            target_data.poi = 'ufoufo'
            user_data.persist()
            target_data.persist()

            await ewrolemgr.updateRoles(client=ewutils.get_client(), member=cmd.mentions[0])
            await target_data.move_inhabitants(id_poi='ufoufo')


        else:
            response = "The going energy cost for abduction is pretty expensive these days. You better have a battery pack before you do something like that."

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def beam_me_up(cmd):
    user_data = EwUser(member=cmd.message.author)
    protected = False
    cosmetics = bknd_item.inventory(id_user=user_data.id_user, id_server=cmd.guild.id,
                                    item_type_filter=ewcfg.it_cosmetic)
    for cosmetic in cosmetics:
        cosmetic_data = EwItem(id_item=cosmetic.get('id_item'))

        ewutils.logMsg(str(cosmetic_data.item_props))
        if cosmetic_data.item_props.get('id_cosmetic') == 'skinsuit':
            if cosmetic_data.item_props.get('adorned') == 'true':
                protected = True

    poi_sought = poi_static.id_to_poi.get(user_data.poi)

    shipstate = EwGamestate(id_server=user_data.id_server, id_state='shipstate')

    if not protected:
        response = "Why would aliens abduct you? What makes you so special?"
    elif poi_sought.id_poi == 'ufoufo':
        response = 'You\'re already in here.'
    elif poi_sought.id_poi != ewcfg.poi_id_west_outskirts:
        response = "Hey, get a bit closer. The ship's in the West Outskirts. Beam up power doesn't grow on trees, you know."
    elif shipstate.bit == 1:
        response = 'The ship\'s on the ground right now, it can\'t beam shit.'
    else:
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You are being abducted by aliens. The ship is 20 seconds away."))
        ewutils.active_restrictions[user_data.id_user] = 2
        await asyncio.sleep(20)

        ewutils.active_restrictions[user_data.id_user] = 0
        ewutils.moves_active[cmd.message.author.id] = 0
        user_data.poi = 'ufoufo'
        user_data.persist()

        await ewrolemgr.updateRoles(client=ewutils.get_client(), member=cmd.message.author)
        await user_data.move_inhabitants(id_poi='ufoufo')

    return await fe_utils.send_message(cmd.client, cmd.message.channel,fe_utils.formatMessage(cmd.message.author, response))

async def blockparty(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return
    else:
        blockstate = EwGamestate(id_server=cmd.guild.id, id_state='blockparty')
        if cmd.tokens_count > 1:
                if cmd.tokens[1] == 'slimegen':
                    blockstate.bit = 1
                    blockstate.persist()
                    response = "Slimegen turned on."
                elif cmd.tokens[1] == 'close':
                    blockstate.bit = 0
                    blockstate.value = ''
                    blockstate.persist()
                    response = "OK, closing up."
                else:
                    poi_sought = ewutils.flattenTokenListToString(cmd.tokens[1:])
                    poi = poi_static.id_to_poi.get(poi_sought)
                    if poi is not None:
                        time_end = int(time()) + (60 * 60 * 6) # 6 hours
                        blockstate.value = "{}{}".format(poi.id_poi, time_end)
                        blockstate.persist()
                        response = "Block party in {}! Everybody in!".format(poi.str_name)
                    else:
                        response = "Never heard of it."
        else:
            response = "I see you haven't gotten any smarter. Try !blockparty <setting>. Settings include 'close', 'slimegen', and any POI."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def hailcab(cmd):
    user_data = EwUser(member = cmd.message.author)
    blockstate = EwGamestate(id_server=cmd.guild.id, id_state='blockparty')
    poi = ''.join([i for i in blockstate.value if not i.isdigit()])
    if poi == 'outsidethe':
        poi = ewcfg.poi_id_711

    if poi != user_data.poi:
        response = "You can't hail a cab right now. All the cabbies are hiding for cover thanks to all the violence. Good job on that, by the way."
    else:
        if user_data.life_state in [ewcfg.life_state_enlisted, ewcfg.life_state_juvenile]:
            if user_data.faction == ewcfg.faction_rowdys and user_data.life_state == ewcfg.life_state_enlisted:
                dest = ewcfg.poi_id_rowdyroughhouse
            elif user_data.faction == ewcfg.faction_killers and user_data.life_state == ewcfg.life_state_enlisted:
                dest = ewcfg.poi_id_copkilltown
            else:
                dest = ewcfg.poi_id_juviesrow
            await asyncio.sleep(5)
            response = "**TAXI!** You shout into the crowd for a ride home. The drivers don't notice you're a miscreant, and pick you up without a second thought. They got nervous when you asked to return to your gang base, and forgot to ask for any fare. Nice!"
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            ewutils.moves_active[cmd.message.author.id] = 0
            user_data.poi = dest
            user_data.persist()
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
            return await user_data.move_inhabitants(id_poi=dest, visitor=user_data.id_user)

        elif user_data.life_state == ewcfg.life_state_corpse:
            response = "You're already dead. The cabbies unfortunately tend to avoid black people, so you should probably just float back to the sewers."
        else:
            response = "The cabbie looks confused. Why would a person like you need a cab?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

