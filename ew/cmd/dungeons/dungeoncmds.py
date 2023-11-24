import asyncio
import random

from ew.static import poi as poi_static
from ew.static import weapons as wep_static
from ew.static import npc as npc_static
from ew.utils import dungeons as dungeon_utils
from ew.utils import frontend as fe_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils import core as ewutils
from ew.utils.combat import EwUser
from . import dungeonutils
import ew.static.community_cfg as comm_cfg
from ew.backend.dungeons import EwBlurb
import ew.static.cfg as ewcfg
from ew.utils import cmd as cmd_utils
import ew.backend.core as bknd_core


async def tutorial_cmd(cmd):
    user_data = EwUser(member=cmd.message.author)
    client = cmd.client

    if user_data.poi not in poi_static.tutorial_pois:
        return

    if user_data.id_user not in dungeonutils.user_to_tutorial_state:
        return await dungeon_utils.begin_tutorial(cmd.message.author)

    tutorial_state = dungeonutils.user_to_tutorial_state.get(user_data.id_user)

    tutorial_scene = poi_static.dungeon_tutorial[tutorial_state]

    cmd_content = cmd.message.content[1:].lower()

    # Administrators can skip the tutorial
    if cmd_content == "skiptutorial" and cmd.message.author.guild_permissions.administrator:
        new_state = 20
        dungeonutils.user_to_tutorial_state[user_data.id_user] = new_state

        scene = poi_static.dungeon_tutorial[new_state]

        if scene.poi != None:
            user_data.poi = scene.poi

        if scene.life_state != None:
            user_data.life_state = scene.life_state

        user_data.persist()

        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

        response = dungeon_utils.format_tutorial_response(scene)

        poi_def = poi_static.id_to_poi.get(user_data.poi)
        channels = [poi_def.channel]
        return await fe_utils.post_in_channels(cmd.guild.id, fe_utils.formatMessage(cmd.message.author, response), channels)

    if cmd_content in tutorial_scene.options:
        new_state = tutorial_scene.options.get(cmd_content)
        dungeonutils.user_to_tutorial_state[user_data.id_user] = new_state

        scene = poi_static.dungeon_tutorial[new_state]

        if scene.poi != None:
            user_data.poi = scene.poi

        if scene.life_state != None:
            user_data.life_state = scene.life_state

        user_data.persist()

        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

        response = dungeon_utils.format_tutorial_response(scene)

        poi_def = poi_static.id_to_poi.get(user_data.poi)
        channels = [poi_def.channel]
        return await fe_utils.post_in_channels(cmd.guild.id, fe_utils.formatMessage(cmd.message.author, response), channels)


    else:
        """ couldn't process the command. bail out!! """
        """ bot rule 0: be cute """
        randint = random.randint(1, 3)
        msg_mistake = "ENDLESS WAR is growing frustrated."
        if randint == 2:
            msg_mistake = "ENDLESS WAR denies you his favor."
        elif randint == 3:
            msg_mistake = "ENDLESS WAR pays you no mind."

        msg = await fe_utils.send_message(client, cmd.message.channel, msg_mistake)
        await asyncio.sleep(2)
        try:
            await msg.delete()
            pass
        except:
            pass

        # response = dungeon_utils.format_tutorial_response(tutorial_scene)
        # return await fe_utils.send_message(client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        return


async def add_blurb(cmd):
    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        channel = fe_utils.get_channel(server=cmd.guild, channel_name='suggestion-box')
        if cmd.tokens_count >= 2:
            cmd.tokens[1] = "\"" + cmd.tokens[1] + "\""
        prompt = " ".join(cmd.tokens)
        sugg_response = "blurb from {}({}):\n{}".format(cmd.message.author.display_name, cmd.message.author.id, prompt)
        await fe_utils.send_message(cmd.client, channel, sugg_response)
        response = "Added a blurb to suggestion-box."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        if len(cmd.tokens) > 5 or len(cmd.tokens) < 3:
            response = "The syntax is !addblurb \"blurb\" \"context\" \"subcontext\" \"subsubcontext\" Only the first context is required."
        else:
            blurb_obj = EwBlurb()
            blurb_obj.id_server = cmd.guild.id
            blurb_obj.blurb = cmd.tokens[1]
            blurb_obj.context = cmd.tokens[2]
            if len(cmd.tokens) > 3:
                blurb_obj.subcontext = cmd.tokens[3]
            if len(cmd.tokens) > 4:
                blurb_obj.subsubcontext = cmd.tokens[4]
            blurb_obj.persist()

            if blurb_obj.context == 'npc':
                npc = npc_static.active_npcs_map.get(blurb_obj.subcontext)
                if npc.dialogue.get(blurb_obj.subsubcontext) is not None:
                    npc.dialogue[blurb_obj.subsubcontext].append(blurb_obj.blurb)
                else:
                    npc.dialogue[blurb_obj.subsubcontext] = [blurb_obj.blurb]
            elif blurb_obj.context == 'districtkey':
                poi = poi_static.id_to_poi.get(blurb_obj.subcontext)
                poi.keyword_blurbs[blurb_obj.subsubcontext] = blurb_obj.blurb
            elif blurb_obj.context == 'district':
                comm_cfg.district_blurbs[blurb_obj.subcontext].append(blurb_obj.blurb)
            elif blurb_obj.context == 'vendor':
                ewcfg.vendor_dialogue[blurb_obj.subcontext].append(blurb_obj.blurb)
            elif blurb_obj.context == 'vendororder':
                ewcfg.vendor_order_dialogue[blurb_obj.subcontext].append(blurb_obj.blurb)
            elif blurb_obj.context == 'killtext':
                wep_obj = wep_static.weapon_map.get(blurb_obj.subcontext)
                if wep_obj is not None:
                    wep_obj.str_kill.append(blurb_obj.blurb)
            list_to_update = comm_cfg.blurb_context_map.get(blurb_obj.context)
            if list_to_update is not None:
                list_to_update.append(blurb_obj.blurb)

            response = "Added a blurb."

        await fe_utils.send_message(cmd.client, cmd.message.channel,fe_utils.formatMessage(cmd.message.author, response))




async def displayblurbs(cmd):
    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        return await cmd_utils.fake_failed_command(cmd)

    context = None
    subcontext = None
    subsubcontext = None


    if len(cmd.tokens) > 1:
        context = cmd.tokens[1]
    if len(cmd.tokens) > 2:
        subcontext = cmd.tokens[2]
    if len(cmd.tokens) > 3:
        subsubcontext = cmd.tokens[3]


    query = "SELECT {col_id_id_blurb}, {col_id_blurb} from blurbs".format(col_id_blurb=ewcfg.col_id_blurb, col_id_id_blurb=ewcfg.col_id_id_blurb)


    if context is not None:
        query += " WHERE {} = '{}'".format(ewcfg.col_id_context, context)
    if subcontext is not None:
        query += " AND {} = '{}'".format(ewcfg.col_id_subcontext, subcontext)
    if subsubcontext is not None:
        query += " AND {} = '{}'".format(ewcfg.col_id_subsubcontext, subsubcontext)

    data_chunk = bknd_core.execute_sql_query(query)

    resp_cont = fe_utils.EwResponseContainer(id_server=cmd.guild.id)

    response = "\n"
    for data in data_chunk:
        response += "Blurb {}: {}\n".format(data[0], data[1][0:50])

    resp_cont.add_channel_response(cmd.message.channel, response)
    await resp_cont.post()
    #await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def display_blurb_context(cmd):
    response = comm_cfg.context_guide
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def delete_blurb(cmd):
    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        return await cmd_utils.fake_failed_command(cmd)
    
    to_delete = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)
    checked = EwBlurb(id_server=cmd.guild.id, id_blurb=to_delete)
    if checked.context != "" and checked.context != None:
        query = "DELETE from blurbs WHERE {col_id_id_blurb} = %s".format(col_id_id_blurb=ewcfg.col_id_id_blurb)
        bknd_core.execute_sql_query(query, (to_delete,))
        response = "Done."
    else:
        response = "No such blurb."
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
