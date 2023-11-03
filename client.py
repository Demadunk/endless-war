#!/usr/bin/python3
#
# endless-war
# mperron (2018)
#
# a chat bot for the RFCK discord server

import asyncio
import json
import logging
import os
import random
import re
import shlex
import subprocess
import sys
import time
import traceback

import discord

# Ensure arguments get through before initializations
import ew.utils.core as ewutils
import ew.static.cfg as ewcfg

debug = False
db_prefix = '--db='
while sys.argv:
    arg_lower = sys.argv[0].lower()
    if arg_lower == '--debug':
        debug = True
    elif arg_lower == '--debugallon': #set all debug option true at startup
        debug = True
        for option in ewutils.DEBUG_OPTIONS:
            ewutils.DEBUG_OPTIONS[option] = True
    elif arg_lower == '--initiate':
        makebp = True
    elif arg_lower.startswith(db_prefix):
        ewcfg.database = arg_lower[len(db_prefix):]

    for arg in sys.argv:
        if arg[2:].lower() in ewutils.DEBUG_OPTIONS.keys() and arg[:2] == "--":
            ewutils.DEBUG_OPTIONS[arg[2:]] = True
            ewutils.logMsg('Enabled the {} debug option.'.format(arg[2:]))

    sys.argv = sys.argv[1:]

from ew.cmd import cmd_map, dm_cmd_map, apt_dm_cmd_map
import ew.cmd.cmds as ewcmd
try:
    from ew.cmd import debug as ewdebug
except:
    from ew.cmd import debug_dummy as ewdebug
import ew.cmd.dungeons as ewdungeons
import ew.cmd.item as ewitem

import ew.utils.apt as apt_utils
import ew.utils.cmd as cmd_utils
import ew.utils.combat as combat_utils
import ew.utils.cosmeticitem as cosmetic_utils
import ew.utils.dungeons as dungeon_utils
import ew.utils.frontend as fe_utils
import ew.utils.item as itm_utils
import ew.utils.leaderboard as bknd_leaderboard
import ew.utils.loop as loop_utils
import ew.utils.move as move_utils
import ew.utils.rolemgr as ewrolemgr
import ew.utils.slimeoid as slimeoid_utils
import ew.utils.sports as sports_utils
import ew.utils.transport as transport_utils
import ew.utils.weather as bknd_weather
import ew.utils.mutations as mut_utils
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.user import add_xp

from ew.cmd.race.racecmds import ree as racecmdsree
from ew.cmd.slimetwitter.slimetwitterutils import separate_id_from_slimetwitter_embed
from ew.cmd.slimetwitter.slimetwitterutils import send_qrt_command

import ew.backend.core as bknd_core
import ew.backend.farm as bknd_farm
import ew.backend.item as bknd_item
import ew.backend.player as bknd_player
import ew.backend.server as bknd_server

from ew.backend.item import EwItem
from ew.backend.market import EwMarket
from ew.backend.player import EwPlayer
from ew.backend.status import EwStatusEffect
from ew.backend.fish import EwRecord

import ew.static.cosmetics as cosmetics
import ew.static.food as static_food
import ew.static.items as static_items
import ew.static.poi as poi_static

ewutils.logMsg('Starting up...')
init_complete = False

# output discord logs to console
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s]:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()

client = discord.Client(intents=intents)

# A map containing user IDs and the last time in UTC seconds since we sent them
# the help doc via DM. This is to prevent spamming.
last_helped_times = {}

# Map of server ID to a map of active users on that server.
active_users_map = {}

# When debug is enabled, additional commands are turned on.
if debug == True:
    ewutils.DEBUG = True
    ewutils.logMsg('Debug mode enabled.')

if ewutils.DEBUG_OPTIONS['trackapi'] == True:
    client._enable_debug_events = True

ewutils.logMsg('Using database: {}'.format(ewcfg.database))

# This can be done in debug inits please
ewcfg.debugpiers = ewdebug.debugpiers
ewcfg.debugfish_response = ewdebug.debugfish_response
ewcfg.debugfish_goal = ewdebug.debugfish_goal

# ewcfg.debug5 = ewdebug.debug5

ewcfg.cmd_debug8 = ewcfg.cmd_prefix + ewdebug.cmd_debug8
ewcfg.cmd_debug9 = ewcfg.cmd_prefix + ewdebug.cmd_debug9

re_awoo_g = re.compile('.*![a]+[w]+o[o]+.*') #taking these out of on_message so they only need to be compiled once
re_moan_g = re.compile('.*![b]+[r]+[a]+[i]+[n]+[z]+.*')
re_measure_g = re.compile('!measure.*')
re_yoslimernalia_g = re.compile('.*![y]+[o]+[s]+[l]+[i]+[m]+[e]+[r]+[n]+[a]+[l]+[i]+[a]+.*')
re_ree_g = re.compile('.*![r]+[e]+[e]+.*')


@client.event
async def on_member_remove(member):
    # Kill players who leave the server.
    try:
        user_data = EwUser(member=member)

        # don't kill players who haven't cleared the tutorial yet
        if user_data.poi in poi_static.tutorial_pois:
            return

        user_data.trauma = ewcfg.trauma_id_suicide
        await user_data.die(updateRoles=False, cause=ewcfg.cause_leftserver)

        ewutils.logMsg('Player killed for leaving the server.')
    except Exception as e:
        ewutils.logMsg(f'Failed to kill member who left the server: {e}')


@client.event
async def on_presence_update(before, after):
    # update last offline time if they went from offline to online
    try:
        if before.status == discord.Status.offline and after.status != discord.Status.offline:
            user_data = EwUser(member=after)
            user_data.time_lastoffline = int(time.time())
            user_data.persist()

    except Exception as e:
        ewutils.logMsg(f'Failed to update member\'s last offline time: {e}')

"""
@client.event
async def on_member_update(before, after):
    # update last offline time if they went from offline to online
    try:
        if before.status == discord.Status.offline and after.status != discord.Status.offline:
            user_data = EwUser(member=after)
            user_data.time_lastoffline = int(time.time())
            user_data.persist()

    except Exception as e:
        ewutils.logMsg(f'Failed to update member\'s last offline time: {e}')
"""

@client.event
async def on_ready():

    try:
        await client.change_presence(activity=discord.Game(name="EW " + ewcfg.version))
    except:
        ewutils.logMsg("Failed to change_presence!")

    global init_complete
    if init_complete:
        return
    init_complete = True
    ewcfg.set_client(client)
    ewutils.logMsg('Logged in as {} ({}).'.format(client.user.name, client.user.id))

    ewutils.logMsg("Loaded NLACakaNM world map. ({}x{})".format(move_utils.map_width, move_utils.map_height))
    move_utils.map_draw()

    # Flatten role names to all lowercase, no spaces.
    fake_observer = EwUser()
    fake_observer.life_state = ewcfg.life_state_observer
    for poi in poi_static.poi_list:
        # This just cleans poi roles, why is this here?
        if poi.role != None:
            poi.role = ewutils.mapRoleName(poi.role)

        neighbors = []
        neighbor_ids = []
        if len(poi.neighbors.keys()) > 0:
            neighbors = move_utils.path_to(poi_start=poi.id_poi, user_data=fake_observer)

        if neighbors != None:

            for neighbor in neighbors:
                neighbor_ids.append(neighbor.id_poi)

        poi_static.poi_neighbors[poi.id_poi] = set(neighbor_ids)

    for id_poi in poi_static.landmark_pois:
        ewutils.logMsg("beginning landmark precomputation for " + id_poi)
        # Set each landmark's value to a dictionary of all pois, and their total cost from that landmark
        move_utils.landmarks[id_poi] = move_utils.score_map_from(
            poi_start=id_poi,
            user_data=fake_observer,
            landmark_mode=True
        )

    ewutils.logMsg("finished landmark precomputation")

    # Channels in the connected discord servers to send stock market updates to. Map of server ID to channel.
    channels_stockmarket = {}
    dungeon_utils.load_npc_blurbs()
    dungeon_utils.load_other_blurbs()

    for server in client.guilds:
        # Force discord to send all users, even offline ones
        await server.chunk()

        # Update server data in the database
        bknd_server.server_update(server=server)

        # store the list of channels in an ewutils field
        ewcfg.update_server_list(server=server)

        # find roles and add them tom the database
        ewrolemgr.setupRoles(client=client, id_server=server.id)

        # Grep around for channels
        ewutils.logMsg("connected to server: {}".format(server.name))

        # Map a bunch of the main channels
        fe_utils.map_channels(server)

        ewdebug.initialize_gamestate(id_server=server.id)

        mut_utils.initialize_rotation(id_server=server.id)

        # get or make the weapon items for fists and fingernails
        combat_utils.set_unarmed_items(server.id)

        # create all the districts in the database
        for poi_object in poi_static.poi_list:
            poi = poi_object.id_poi
            # call the constructor to create an entry if it doesnt exist yet
            dist = EwDistrict(id_server=server.id, district=poi)
            # change the ownership to the faction that's already in control to initialize topic names
                # initialize gang bases
            if poi == ewcfg.poi_id_rowdyroughhouse:
                dist.controlling_faction = ewcfg.faction_rowdys
            elif poi == ewcfg.poi_id_copkilltown:
                dist.controlling_faction = ewcfg.faction_killers

            resp_cont = dist.change_ownership(new_owner=dist.controlling_faction, actor="init", client=client)
            dist.persist()
            await resp_cont.post()

        asyncio.ensure_future(loop_utils.capture_tick_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.bleed_tick_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.enemy_action_tick_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.burn_tick_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.remove_status_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.event_tick_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.decrease_food_multiplier())

        # SWILLDERMUK
        if ewcfg.swilldermuk_active:
            asyncio.ensure_future(loop_utils.spawn_prank_items_tick_loop(id_server = server.id))
            asyncio.ensure_future(loop_utils.generate_credence_tick_loop(id_server = server.id))

        # Enemies do spawn randomly
        asyncio.ensure_future(loop_utils.spawn_enemies_tick_loop(id_server=server.id))

        await transport_utils.init_transports(id_server=server.id)
            
        asyncio.ensure_future(bknd_weather.weather_tick_loop(id_server=server.id))

        asyncio.ensure_future(bknd_farm.farm_tick_loop(id_server=server.id))
        
        asyncio.ensure_future(sports_utils.slimeball_tick_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.clock_tick_loop(id_server=server.id))

        asyncio.ensure_future(loop_utils.reset_brick_loop(id_server=server.id))

        print('\nNUMBER OF CHANNELS IN SERVER: {}\n'.format(len(server.channels)))


    try:
        ewutils.logMsg('Creating message queue directory.')
        os.mkdir(ewcfg.dir_msgqueue)
    except FileExistsError:
        ewutils.logMsg('Message queue directory already exists.')

    ewutils.logMsg('Ready.')

    """
        Set up for infinite loop to perform periodic tasks.
    """
    time_now = int(time.time())
    time_last_pvp = time_now

    # Every three hours we log a message saying the periodic task hook is still active. On startup, we want this to happen within about 60 seconds, and then on the normal 3 hour interval.
    time_last_logged = time_now - ewcfg.update_hookstillactive + 60

    stream_live = None

    ewutils.logMsg('Beginning periodic hook loop.')
    while not ewutils.TERMINATE:
        time_now = int(time.time())

        # Periodic message to log that this stuff is still running.
        if (time_now - time_last_logged) >= ewcfg.update_hookstillactive:
            time_last_logged = time_now

            ewutils.logMsg("Periodic hook still active.")

        # Parse files dumped into the msgqueue directory and send messages as needed.
        try:
            for msg_file in os.listdir(ewcfg.dir_msgqueue):
                fname = "{}/{}".format(ewcfg.dir_msgqueue, msg_file)

                msg = fe_utils.readMessage(fname)
                os.remove(fname)

                msg_channel_names = []
                msg_channel_names_reverb = []

                if msg.channel != None:
                    msg_channel_names.append(msg.channel)

                if msg.poi != None:
                    poi = poi_static.id_to_poi.get(msg.poi)
                    if poi != None:
                        if poi.channel != None and len(poi.channel) > 0:
                            msg_channel_names.append(poi.channel)

                        if msg.reverb == True:
                            pois_adjacent = move_utils.path_to(poi_start=msg.poi)

                            for poi_adjacent in pois_adjacent:
                                if poi_adjacent.channel != None and len(poi_adjacent.channel) > 0:
                                    msg_channel_names_reverb.append(poi_adjacent.channel)

                if len(msg_channel_names) == 0:
                    ewutils.logMsg('in file {} message for channel {} (reverb {})\n{}'.format(msg_file, msg.channel, msg.reverb, msg.message))
                else:
                    # Send messages to every connected server.
                    for server in client.guilds:
                        for channel in server.channels:
                            if channel.name in msg_channel_names:
                                await fe_utils.send_message(client, channel, "**{}**".format(msg.message))
                            elif channel.name in msg_channel_names_reverb:
                                await fe_utils.send_message(client, channel, "**Something is happening nearby...\n\n{}**".format(msg.message))
        except:
            ewutils.logMsg('An error occurred while trying to process the message queue:')
            traceback.print_exc(file=sys.stdout)

        # Wait a while before running periodic tasks.
        await asyncio.sleep(15)


@client.event
async def on_member_join(member):
    ewutils.logMsg("New member \"{}\" joined. Configuring default roles / permissions now.".format(member.display_name))
    await ewrolemgr.updateRoles(client=client, member=member)
    bknd_player.player_update(
        member=member,
        server=member.guild
    )
    user_data = EwUser(member=member)
    if member.joined_at.timestamp() - member.created_at.timestamp() < 604800:
        user_data.poi = 'altlock'
        user_data.persist()


    # attempt to force discord.py to cache the user
    await member.guild.query_members(user_ids=[member.id], presences=True)

    if user_data.poi in poi_static.tutorial_pois:
        await dungeon_utils.begin_tutorial(member)
    
    # Assumedly first time joining
    if user_data.poi != "thesewers":
        # give the user a game guide
        gameguide = static_items.item_map.get('gameguide')
        item_props = itm_utils.gen_item_props(gameguide)
        bknd_item.item_create(
            id_user=member.id,
            id_server=member.guild.id,
            item_type=ewcfg.it_item,
            item_props=item_props
        )
        # Wait a bit, send a message
        await asyncio.sleep(30)
        try:
            if random.random() < 0.0666:
                await fe_utils.send_message(client, member, fe_utils.formatMessage(member, "https://cdn.discordapp.com/attachments/431275470902788107/1042615477492535337/jessie.png"))
            else:
                await fe_utils.send_message(client, member, fe_utils.formatMessage(member, ewcfg.server_join_message))
        except discord.errors.Forbidden:
            ewutils.logMsg("New user {} had DMs blocked.".format(member.id))


@client.event
async def on_socket_raw_send(payload):
    if ewutils.DEBUG_OPTIONS['trackapi'] == True:
        try:
            f = open("apifile.txt", "a")
            f.write("{}\n".format(str(payload)))
        except:
            pass


@client.event
async def on_message_delete(message):
    if message != None and message.guild != None and message.author.id != client.user.id and message.content.startswith(ewcfg.cmd_prefix):
        user_data = EwUser(member=message.author)
        mutations = user_data.get_mutations()

        if ewcfg.mutation_id_amnesia not in mutations:
            ewutils.logMsg("deleted message from {}: {}".format(message.author.display_name, message.content))
            await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, '**I SAW THAT.**'))


# consolidates the debug conditions into their own function. poorly ordered because no function prototyping in python, boo
async def debugHandling(message, cmd, cmd_obj):
    # Test item creation
    time_now = int(time.time())
    market = EwMarket(id_server=cmd_obj.guild.id)
    if cmd == (ewcfg.cmd_prefix + 'enemytick'):
        x = await bknd_leaderboard.make_freshness_top_board(server = cmd_obj.guild.id)
        print(x)


    elif cmd == (ewcfg.cmd_prefix + 'quickrevive'):
        print("Created {} Joined {}".format(message.author.created_at.timestamp(), message.author.joined_at.timestamp()))
        """if cmd.mentions_count == 1 and cmd.tokens_count == 3:
            member = cmd.mentions[0]
            user = EwUser(member = member)
            cmd_fnc =  cmd_map.get('!revive')
            await cmd_fnc(cmd=cmd_obj, player_auto = member.id)
            cmd_fnc =  cmd_map.get('!tpp')
            await cmd_fnc(cmd=cmd_obj)"""


    elif cmd ==  (ewcfg.cmd_prefix + 'moverelics'):
        await itm_utils.move_relics(id_server=cmd_obj.guild.id)

    elif cmd == (ewcfg.cmd_prefix + 'releaseprisoners'):
        await loop_utils.release_timed_prisoners_and_blockparties(market.id_server, market.day)
    elif cmd == (ewcfg.cmd_prefix + 'createtestitem'):
        item_id = bknd_item.item_create(
            item_type='medal',
            id_user=message.author.id,
            id_server=message.guild.id,
            item_props={
                'medal_name': 'Test Award',
                'medal_desc': '**{medal_name}**: *Awarded to Krak by Krak for testing shit.*'
            }
        )

        ewutils.logMsg('Created item: {}'.format(item_id))
        item = EwItem(id_item=item_id)
        item.item_props['test'] = 'meow'
        item.persist()

        item = EwItem(id_item=item_id)

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, ewitem.item_look(item)))

        # Creates a poudrin
    elif cmd == (ewcfg.cmd_prefix + 'createpoudrin'):
        for item in static_items.item_list:
            if item.context == "poudrin":
                poudrin_count = 1
                if cmd_obj.tokens_count > 1:
                    try:
                        poudrin_count = int(cmd_obj.tokens[1])
                    except:
                        poudrin_count = 1
                for i in range(poudrin_count):
                    bknd_item.item_create(
                        item_type=ewcfg.it_item,
                        id_user=message.author.id,
                        id_server=message.guild.id,
                        item_props={
                            'id_item': item.id_item,
                            'context': item.context,
                            'item_name': item.str_name,
                            'item_desc': item.str_desc,
                        }
                    )
                    ewutils.logMsg('Created item: {}'.format(item.id_item))
        else:
            pass

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, "Poudrin(s) created."))

        # Shows damage
    elif cmd == (ewcfg.cmd_prefix + 'damage'):
        user_data = EwUser(member=message.author, data_level=1)
        slimes_spent = int(ewutils.slime_bylevel(user_data.slimelevel) / 60)
        # disabled until held items update
        # attack_stat_multiplier = 1 + (user_data.attack / 50) # 2% more damage per stat point
        attack_stat_multiplier = 1
        weapon_skill_multiplier = 1 + ((user_data.weaponskill * 5) / 100)  # 5% more damage per skill point
        slimes_damage = int(
            10 * slimes_spent * attack_stat_multiplier * weapon_skill_multiplier)  # ten times slime spent, multiplied by both multipliers
        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, "{}".format(slimes_damage)))

    elif cmd == ewcfg.cmd_prefix + 'decaytick':
        #await loop_utils.decaySlimes(id_server=cmd_obj.guild.id)
        #await loop_utils.release_timed_prisoners_and_blockparties(id_server=cmd_obj.guild.id,day = market.day)
        #await move_utils.kick(id_server=cmd_obj.guild.id)
        itm_utils.cull_slime_sea(id_server=message.guild.id)
        #await itm_utils.move_relics(id_server=cmd_obj.guild.id)
        #await move_utils.send_gangbase_messages(server_id=message.guild.id, clock=market.clock)

        # Gives the user some slime
    elif cmd == (ewcfg.cmd_prefix + 'getslime'):
        user_data = EwUser(member=message.author)
        user_initial_level = user_data.slimelevel

        response = "You get 1,000,000 slime!"

        levelup_response = user_data.change_slimes(n=1000000)

        was_levelup = True if user_initial_level < user_data.slimelevel else False

        if was_levelup:
            response += " {}".format(levelup_response)

        user_data.persist()
        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))
    elif cmd == (ewcfg.cmd_prefx + 'getcredence'):
        
        response = "You get 1,000 credence!"
        user_data.change_stat(id_server=cmd.guild.id, id_user=cmd.message.author.id, metric = ewcfg.stat_credence, n=1000)

        await fe_utils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
    elif cmd == (ewcfg.cmd_prefix + 'getcoin'):
        user_data = EwUser(member=message.author)
        user_data.change_slimecoin(n=1000000000000, coinsource=ewcfg.coinsource_spending)

        response = "You get 1,000,000,000,000 slimecoin!"

        user_data.persist()
        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

        # Deletes all items in your inventory.
    elif cmd == (ewcfg.cmd_prefix + 'clearinv'):
        user_data = EwUser(member=message.author)
        bknd_item.item_destroyall(id_server=message.guild.id, id_user=message.author.id)
        response = "You destroy every single item in your inventory."
        user_data.persist()
        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

    elif cmd == (ewcfg.cmd_prefix + 'createapple'):
        item_id = bknd_item.item_create(
            id_user=message.author.id,
            id_server=message.guild.id,
            item_type=ewcfg.it_food,
            item_props={
                'id_food': "direapples",
                'food_name': "Dire Apples",
                'food_desc': "This sure is a illegal Dire Apple!",
                'recover_hunger': 500,
                'str_eat': "You chomp into this illegal Dire Apple.",
                'time_expir': int(time.time() + ewcfg.farm_food_expir)
            }
        )

        ewutils.logMsg('Created item: {}'.format(item_id))
        item = EwItem(id_item=item_id)
        item.item_props['test'] = 'meow'
        item.persist()

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, "Apple created."))

    elif cmd == (ewcfg.cmd_prefix + 'createhat'):
        patrician_rarity = 20
        patrician_smelted = random.randint(1, patrician_rarity)
        patrician = False

        if patrician_smelted == 1:
            patrician = True

        items = []

        for cosmetic in cosmetics.cosmetic_items_list:
            if patrician and cosmetic.rarity == ewcfg.rarity_patrician:
                items.append(cosmetic)
            elif not patrician and cosmetic.rarity == ewcfg.rarity_plebeian:
                items.append(cosmetic)

        item = items[random.randint(0, len(items) - 1)]

        item_props = itm_utils.gen_item_props(item)

        item_id = bknd_item.item_create(
            item_type=item.item_type,
            id_user=message.author.id,
            id_server=message.guild.id,
            item_props=item_props
        )

        ewutils.logMsg('Created item: {}'.format(item_id))
        item = EwItem(id_item=item_id)
        item.item_props['test'] = 'meow'
        item.persist()

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, "Hat created."))

    elif cmd == (ewcfg.cmd_prefix + 'createfood'):
        item = static_food.food_list[random.randint(0, len(static_food.food_list) - 1)]

        item_id = bknd_item.item_create(
            item_type=ewcfg.it_food,
            id_user=message.author.id,
            id_server=message.guild.id,
            item_props={
                'id_food': item.id_food,
                'food_name': item.str_name,
                'food_desc': item.str_desc,
                'recover_hunger': item.recover_hunger,
                'str_eat': item.str_eat,
                'time_expir': item.time_expir
            }
        )

        ewutils.logMsg('Created item: {}'.format(item_id))
        item = EwItem(id_item=item_id)
        item.item_props['test'] = 'meow'
        item.persist()

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, "Food created."))

    elif cmd == (ewcfg.cmd_prefix + 'createdye'):
        item = static_items.dye_list[random.randint(0, len(static_items.dye_list) - 1)]

        item_props = itm_utils.gen_item_props(item)

        bknd_item.item_create(
            item_type=item.item_type,
            id_user=message.author.id,
            id_server=message.guild.id,
            item_props=item_props
        )

        await fe_utils.send_message(client, message.channel,
                                    fe_utils.formatMessage(message.author, "{} created.".format(item.str_name)))

    elif cmd == (ewcfg.cmd_prefix + 'createoldhat'):
        patrician_rarity = 20
        patrician_smelted = random.randint(1, patrician_rarity)
        patrician = False

        if patrician_smelted == 1:
            patrician = True

        cosmetics_list = []

        for result in cosmetics.cosmetic_items_list:
            if result.acquisition == ewcfg.acquisition_smelting:
                cosmetics_list.append(result)
            else:
                pass

        items = []

        for cosmetic in cosmetics_list:
            if patrician and cosmetic.rarity == ewcfg.rarity_patrician:
                items.append(cosmetic)
            elif not patrician and cosmetic.rarity == ewcfg.rarity_plebeian:
                items.append(cosmetic)

        item = items[random.randint(0, len(items) - 1)]

        bknd_item.item_create(
            item_type=ewcfg.it_cosmetic,
            id_user=message.author.id,
            id_server=message.guild.id,
            item_props={
                'id_cosmetic': item.id_cosmetic,
                'cosmetic_name': item.str_name,
                'cosmetic_desc': item.str_desc,
                'rarity': item.rarity,
                'adorned': 'false'
            }
        )

        response = "Success! You've smelted a {}!".format(item.str_name)

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))
    elif cmd == (ewcfg.cmd_prefix + 'createoldscalp'):
        bknd_item.item_create(
            item_type=ewcfg.it_cosmetic,
            id_user=message.author.id,
            id_server=message.guild.id,
            item_props={
                'id_cosmetic': 'scalp',
                'cosmetic_name': "My scalp",
                'cosmetic_desc': "A scalp.",
                'adorned': 'false'
            }
        )
        response = "Success! You've smelted a scalp!"

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))
    elif cmd == (ewcfg.cmd_prefix + 'createoldsoul'):
        bknd_item.item_create(
            id_user=message.author.id,
            id_server=message.guild.id,
            item_type=ewcfg.it_cosmetic,
            item_props={
                'id_cosmetic': "soul",
                'cosmetic_name': "My soul",
                'cosmetic_desc': "The immortal soul of me. It dances with a vivacious energy inside its jar.\n If you listen to it closely you can hear it whispering numbers: me.",
                'rarity': ewcfg.rarity_patrician,
                'adorned': 'false',
                'user_id': "usermodel.id_user",
            }
        )

        response = "Success! You've smelted a soul!"

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

        # FIXME debug
        # Test item deletion
    elif cmd == (ewcfg.cmd_prefix + 'delete'):
        items = bknd_item.inventory(
            id_user=message.author.id,
            id_server=message.guild.id
        )

        for item in items:
            bknd_item.item_delete(
                id_item=item.get('id_item')
            )

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, 'ok'))
    elif cmd == (ewcfg.cmd_prefix + 'setrole'):

        response = ""

        if cmd_obj.mentions_count == 0:
            response = 'Set who\'s role?'
        else:
            id_server = cmd_obj.guild.id
            roles_map = ewrolemgr.roles_map[id_server]
            role_target = cmd_obj.tokens[1]
            role = roles_map.get(role_target)

            if role != None:
                for user in cmd_obj.mentions:
                    try:
                        user = await user.edit(roles=[role])
                    except:
                        ewutils.logMsg('Failed to replace_roles for user {} with {}.'.format(user.display_name, role.name))

                response = 'Done.'
            else:
                response = 'Unrecognized role.'

        await fe_utils.send_message(client, cmd_obj.message.channel, fe_utils.formatMessage(message.author, response))

    elif cmd == (ewcfg.cmd_prefix + 'getrowdy'):
        response = "You get rowdy. Fuck. YES!"
        user_data = EwUser(member=message.author)
        user_data.life_state = ewcfg.life_state_enlisted
        user_data.faction = ewcfg.faction_rowdys
        user_data.time_lastenlist = time_now + ewcfg.cd_enlist
        user_data.persist()
        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

    elif cmd == (ewcfg.cmd_prefix + 'getkiller'):
        response = "You uh... 'get' killer. Sure."
        user_data = EwUser(member=message.author)
        user_data.life_state = ewcfg.life_state_enlisted
        user_data.faction = ewcfg.faction_killers
        user_data.time_lastenlist = time_now + ewcfg.cd_enlist
        user_data.persist()
        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

    # Toggles rain on and off
    elif cmd == (ewcfg.cmd_prefix + 'toggledownfall'):
        market_data = EwMarket(id_server=message.guild.id)

        if market_data.weather == ewcfg.weather_bicarbonaterain:
            newweather = ewcfg.weather_sunny

            market_data.weather = newweather
            response = "Bicarbonate rain turned OFF. Weather was set to {}.".format(newweather)
        else:
            market_data.weather = ewcfg.weather_bicarbonaterain
            response = "Bicarbonate rain turned ON."

        market_data.persist()
        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

    elif cmd == (ewcfg.cmd_prefix + 'dayforward'):
        market_data = EwMarket(id_server=message.guild.id)

        market_data.day += 1
        market_data.persist()

        response = "Time has progressed 1 day forward manually."

        if ewutils.check_moon_phase(market_data) == ewcfg.moon_full:
            response += "\nIt's a full moon!"

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

    elif cmd == (ewcfg.cmd_prefix + 'hourforward'):
        market_data = EwMarket(id_server=message.guild.id)
        market_data.clock += 1
        response = "Time has progressed 1 hour forward manually."

        if market_data.clock >= 24 or market_data.clock < 0:
            market_data.clock = 0
            market_data.day += 1
            response += "\nMidnight has come. 1 day progressed forward."

        if ewutils.check_moon_phase(market_data) == ewcfg.moon_full:
            response += "\nIt's a full moon!"

        market_data.persist()

        await bknd_weather.weather_cycle(id_server=message.guild.id)

        await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

    elif cmd == (ewcfg.cmd_prefix + 'postleaderboard'):
        try:
            for server in client.guilds:
                await bknd_leaderboard.post_leaderboards(client=client, server=server)
        except:
            pass

    elif cmd == (ewcfg.cmd_prefix + 'genslimeoid'):
        user_data = EwUser(member=message.author)
        if user_data.active_slimeoid == -1:
            slimeoid_utils.generate_slimeoid(id_owner=user_data.id_user, id_server=user_data.id_server, persist=True)
            return await fe_utils.send_message(client, message.channel,
                                               "Generated slimeoid for user. Take care of them!")
        else:
            return await fe_utils.send_message(client, message.channel, "You already have a slimeoid, bub!")

    elif cmd == (ewcfg.cmd_prefix + 'massgenslimeoidnames'):
        response = ""
        for sl in range(10):
            new_sl = slimeoid_utils.generate_slimeoid()
            if new_sl.hue != "":
                hue_str = " **" + new_sl.hue + "** "
            else:
                hue_str = ""
            response += ("\n" + hue_str + new_sl.name)
        return await fe_utils.send_message(client, message.channel, response)


@client.event
async def on_message(message):
    time_now = int(time.time())
    ewcfg.set_client(client)

    """ do not interact with our own messages """
    if message.author.id == client.user.id or message.author.bot == True:
        return

    # Ignore messages in certain channels
    if hasattr(message.channel, "name") and message.channel.name in ewcfg.forbidden_channels:
        return

    if message.guild is not None:
        # Note that the user posted a message.
        active_map = active_users_map.get(message.guild.id)
        if active_map is None:
            active_map = {}
            active_users_map[message.guild.id] = active_map
        active_map[message.author.id] = True

        # Update player information.
        bknd_player.player_update(
            member=message.author,
            server=message.guild
        )

    content_tolower = message.content.lower()
    content_tolower_list = content_tolower.split(" ")

    re_awoo = re_awoo_g
    re_moan = re_moan_g
    re_measure = re_measure_g
    re_yoslimernalia = re_yoslimernalia_g
    re_ree = re_ree_g

    playermodel = EwPlayer(id_user=message.author.id)
    usermodel = EwUser(id_user=message.author.id, id_server=playermodel.id_server)

    # update the player's time_last_action which is used for kicking AFK players out of subzones
    if message.guild is not None:

        try:
            usermodel.time_last_action = int(time.time())
            bknd_core.execute_sql_query("UPDATE users SET {time_last_action} = %s WHERE id_user = %s AND id_server = %s".format(
                time_last_action=ewcfg.col_time_last_action
            ), (
                int(time.time()),
                int(message.author.id),
                message.guild.id
            ))
        except Exception as e:
            ewutils.logMsg('server {}: failed to update time_last_action for {}: {}'.format(message.guild.id, message.author.id, e))

        statuses = usermodel.getStatusEffects()

        if ewcfg.status_strangled_id in statuses:
            strangle_effect = EwStatusEffect(id_status=ewcfg.status_strangled_id, user_data=usermodel)
            source = EwPlayer(id_user=strangle_effect.source, id_server=message.guild.id)
            response = "You manage to break {}'s garrote wire!".format(source.display_name)
            usermodel.clear_status(ewcfg.status_strangled_id)
            return await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

        if ewutils.active_restrictions.get(usermodel.id_user) == 3:
            usermodel.trauma = ewcfg.trauma_id_environment
            die_resp = await usermodel.die(cause=ewcfg.cause_praying)
            await die_resp.post()

            response = "ENDLESS WAR completely and utterly obliterates {} with a bone-hurting beam.".format(message.author.display_name).replace("@", "\{at\}")
            return await fe_utils.send_message(client, message.channel, response)
        if str(message.channel) in ["nurses-office", "suggestion-box", "detention-center", "community-service", "playground", "graffiti-wall", "post-slime-drip", "outside-the-lunchroom", "outside-the-lunchrooom", "outside-the-lunchroooom"] or message.channel.type in [discord.ChannelType.public_thread, discord.ChannelType.private_thread]:
            if usermodel.hogtied == 1:
                response = random.choice(["MMMPH!", "MBBBBB", "HMMHM", "MMMMMHMMF!"])
                await fe_utils.send_message(client, message.channel, response)
                await message.delete()
                return

    """ -------------------------------
    ########## THREAD CUTOFF ##########
    ------------------------------- """

    # Never treat a message like a command if it's in a thread
    if message.channel.type not in [discord.ChannelType.text, discord.ChannelType.private]:
        return

    if message.content.startswith(ewcfg.cmd_prefix) or message.content in ewdebug.debug_content_check or message.guild is None or (any(swear in content_tolower for swear in ewcfg.curse_words.keys())) or message.channel in ["nurses-office", "suggestion-box", "detention-center", "community-service", "playground", "graffiti-wall", "post-slime-drip", "outside-the-lunchroom", "outside-the-lunchrooom", "outside-the-lunchroooom"]:
        """
            Wake up if we need to respond to messages. If it's in a basic channel, Could be:
                message starts with !
                direct message (server == None)
                Inaccurate - user is new/has no roles (len(roles) < 4)
                user - Inaccurate - is a security officer and - ok - has cussed
                Message is in a designated non-gameplay channel
        """

        # Ignore users with weird characters in their name

        try:
            message.author.display_name[:3].encode('utf-8').decode('ascii')
        except UnicodeError:
            return await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, "We don't take kindly to moon runes around here."))

        # tokenize the message. the command should be the first word.
        try:
            tokens = shlex.split(message.content)  # it's split with shlex now because shlex regards text within quotes as a single token
        except:
            tokens = message.content.split(' ')  # if splitting via shlex doesnt work (odd number of quotes), use the old splitting method so it doesnt give an exception

        tokens_count = len(tokens)
        cmd = tokens[0].lower() if tokens_count >= 1 else ""

        mentions = message.mentions
        mentions_count = len(mentions)

        if message.guild is None:
            guild_used = ewcfg.server_list[playermodel.id_server]
            admin_permissions = False
        else:
            guild_used = message.guild
            admin_permissions = message.author.guild_permissions.administrator

        # Create command object
        cmd_obj = cmd_utils.EwCmd(
            tokens=tokens,
            message=message,
            client=client,
            mentions=mentions,
            guild=guild_used,
            admin=admin_permissions
        )

        # remove mentions to us #moved below cmd_obj because of EwIds #TODO: remove this and move debug commands somewhere else
        mentions = list(filter(lambda user: user.id != client.user.id, message.mentions))
        mentions_count = len(mentions)

        """
            Punish the user for swearing.
            The swear_jar attribute has been repurposed for SlimeCorp security officers
        """


        usermodel.persist()
        if await ewdebug.contentCheck(cmd=cmd_obj, line=content_tolower) == True:
            return
        usermodel = EwUser(id_user=message.author.id, id_server=playermodel.id_server)

        # if the message wasn't a command, we can stop here
        if not message.content.startswith(ewcfg.cmd_prefix):
            return

        """
            Handle direct messages.
        """
        if message.guild is None:

            poi = poi_static.id_to_poi.get(usermodel.poi)
            cmd_obj.guild = ewcfg.server_list[playermodel.id_server]
            cmd_obj.message.author = await fe_utils.get_member(cmd_obj.guild, playermodel.id_user)

            # Handle DM compatible commands
            if cmd in dm_cmd_map:
                cmd_fnc = dm_cmd_map.get(cmd)
                if cmd_fnc:
                    return await cmd_fnc(cmd_obj)
            elif poi.is_apartment and cmd in apt_dm_cmd_map:
                cmd_fnc = apt_dm_cmd_map.get(cmd)
                if cmd_fnc:
                    return await cmd_fnc(cmd_obj)
            else:
                # Only send the help response once every thirty seconds. There's no need to spam it.
                # Also, don't send out response if the user doesn't actually type a command.
                if message.content.startswith(ewcfg.cmd_prefix):
                    time_last = last_helped_times.get(message.author.id, 0)
                    if (time_now - time_last) > 30:
                        last_helped_times[message.author.id] = time_now
                        direct_help_response = "ENDLESS WAR doesn't allow you to do that command in DMs.\nIf you're confused about what you're doing, you might want to get some **!help** over at the server."
                        await fe_utils.send_message(client, message.channel, direct_help_response)
                else:
                    return

            # Nothing else to do in a DM.
            return

        # assign the appropriate roles to a user with less than @everyone, faction, both location roles
        if usermodel.arrested > 0:
            return

        if usermodel.poi == 'altlock':
            response = 'You\'re locked from the game because your account was created too close to your join date. Dirty little sneak. Talk to a mod if there\'s some good reason to get it unlocked.'
            return await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))
        mutations = usermodel.get_mutations()
        # Scold/ignore offline players.
        if message.author.status == discord.Status.offline:

            if (ewcfg.mutation_id_chameleonskin not in mutations or cmd not in ewcfg.offline_cmds) and ewutils.DEBUG_OPTIONS['playoffline'] == False:
                response = "You cannot participate in the ENDLESS WAR while offline."

                return await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

        if usermodel.time_lastoffline > time_now - ewcfg.time_offline:

            if ewcfg.mutation_id_chameleonskin not in mutations or cmd not in ewcfg.offline_cmds:
                response = "You are too paralyzed by ENDLESS WAR's judgemental stare to act."

                return await fe_utils.send_message(client, message.channel, fe_utils.formatMessage(message.author, response))

        statuses = usermodel.getStatusEffects()
        # Ignore stunned players
        if ewcfg.status_stunned_id in statuses:
            return

        # Check the main command map for the requested command.
        #global cmd_map
        cmd_fn = cmd_map.get(cmd.replace(ewcfg.cmd_prefix, '!', 1))

        if usermodel.poi in ewdebug.act_pois.keys():
            keycontent = ewutils.flattenTokenListToString(content_tolower)
            if keycontent in ewdebug.act_pois.get(usermodel.poi).keys() or content_tolower in ewdebug.act_pois.get(usermodel.poi).keys():
                return await ewdebug.act(cmd=cmd_obj, content_tolower=content_tolower)
                #function = ewdebug.act_pois.get(usermodel.poi).get(keycontent)
                #if function is None:
                #    function = ewdebug.act_pois.get(usermodel.poi).get(content_tolower)
                #return await function(cmd=cmd_obj)

        if cmd_fn is not None:
            # Execute found command
            return await cmd_fn(cmd_obj)
        # AWOOOOO
        elif re_awoo.match(cmd):
            return await ewcmd.cmdcmds.cmd_howl(cmd_obj)
        elif re_moan.match(cmd):
            return await ewcmd.cmdcmds.cmd_moan(cmd_obj)
        elif re_yoslimernalia.match(cmd) and ewcfg.slimernalia_active:
            return await ewcmd.cmdcmds.yoslimernalia(cmd_obj)
        elif re_measure.match(cmd):
            return await ewcmd.cmdcmds.cockdraw(cmd_obj)
        elif re_ree.match(cmd):
            return await racecmdsree(cmd_obj)
        elif debug and cmd in ewcfg.client_debug_commands:
            return await debugHandling(message=message, cmd=cmd, cmd_obj=cmd_obj)

        # didn't match any of the command words.
        else:
            """ couldn't process the command. bail out!! """
            """ bot rule 0: be cute """
            randint = random.randint(1, 3)
            msg_mistake = "ENDLESS WAR is growing frustrated."
            if randint == 2:
                msg_mistake = "ENDLESS WAR denies you his favor."
            elif randint == 3:
                msg_mistake = "ENDLESS WAR pays you no mind."

            return await fe_utils.send_response(msg_mistake, cmd_obj, 2)

    elif content_tolower.find(ewcfg.cmd_howl) >= 0 or content_tolower.find(ewcfg.cmd_howl_alt1) >= 0 or re_awoo.match(content_tolower):
        """ Howl if !howl is in the message at all. """
        return await ewcmd.cmdcmds.cmd_howl(cmd_utils.EwCmd(
            message=message,
            client=client,
            guild=message.guild
        ))
    elif content_tolower.find(ewcfg.cmd_moan) >= 0 or re_moan.match(content_tolower):
        return await ewcmd.cmdcmds.cmd_moan(cmd_utils.EwCmd(
            message=message,
            client=client,
            guild=message.guild
        ))
    elif content_tolower.find(ewcfg.cmd_yoslimernalia) >= 0 or re_yoslimernalia.match(content_tolower):
        if ewcfg.slimernalia_active:
            return await ewcmd.cmdcmds.yoslimernalia(cmd_utils.EwCmd(
                message=message,
                client=client,
                guild=message.guild
            ))
        else:
            return
    elif content_tolower.find(ewcfg.cmd_ree) >= 0 or re_ree.match(content_tolower):
        return await racecmdsree(cmd_utils.EwCmd(
            message=message,
            client=client,
            guild=message.guild
        ))


@client.event
async def on_raw_reaction_add(payload):
    if ewutils.DEBUG:
        emoji_req = 2
    else:
        emoji_req = 10

    # Currently only respond to reactions in the main server
    if payload.guild_id is None:
        # Was a DM
        return
    
    # Don't handle our own reactions
    if payload.user_id == client.user.id:
        return

    server = client.get_guild(payload.guild_id)

    slime_twitter = fe_utils.get_channel(server, ewcfg.channel_slimetwitter)
    deviant_splaart = fe_utils.get_channel(server, ewcfg.channel_deviantsplaart)
    community_service = fe_utils.get_channel(server, ewcfg.channel_communityservice)

    # Slime Twitter Emote Handling
    if slime_twitter is not None and payload.channel_id == slime_twitter.id:
        message = await slime_twitter.fetch_message(payload.message_id)
        if len(message.embeds) > 0:
            embed = message.embeds[0]
            userid = "<@!{}>".format(payload.user_id)
            # If the person reacting made the tweet
            if embed.description.startswith(userid):
                # If the reply is :blank:
                if str(payload.emoji) == ewcfg.emote_delete_tweet:
                    await message.delete()
            # If person reacting didn't make the tweet
            else:
                # If the reply is :slimetwitterlike:
                if str(payload.emoji) in [ewcfg.emote_slimetwitter_like, ewcfg.emote_slimetwitter_like_debug]:
                    try:
                        og_id_user = separate_id_from_slimetwitter_embed(embed)
                        await add_xp(og_id_user, payload.guild_id, ewcfg.goonscape_clout_stat, 13000)
                    except:
                        ewutils.logMsg('Failed to increase Clout XP for user with ID {}.'.format(og_id_user))
                # If the reply is :slimeresplat:
                elif str(payload.emoji) in [ewcfg.emote_slimetwitter_resplat, ewcfg.emote_slimetwitter_resplat_debug]:
                    try:
                        await send_qrt_command(client, server, payload.user_id, payload.message_id)
                        og_id_user = separate_id_from_slimetwitter_embed(embed)
                        await add_xp(og_id_user, payload.guild_id, ewcfg.goonscape_clout_stat, 4300)
                    except:
                        ewutils.logMsg('Failed to increase Clout XP for user with ID {}, and failed to send Quote Resplat message to user with ID {}'.format(og_id_user, payload.id_user))

    # Deviant Splaart Emote Handling
    elif deviant_splaart is not None and payload.channel_id == deviant_splaart.id:
        message = await deviant_splaart.fetch_message(payload.message_id)
        if str(payload.emoji) == ewcfg.emote_111 or str(payload.emoji) == ewcfg.emote_111_debug:
            for react in message.reactions:
                if react.count >= emoji_req and react.emoji.id in [720412882143150241, 431547758181220377]:
                    msgtext = "--------------------------------------------------------------------------------------------------\n" + message.content
                    title = message.content.split('::', 1)
                    current_record = EwRecord(id_server=payload.guild_id, record_type=title[0])
                    current_record.legality = 0
                    current_record.persist()

                    art_exhibits = fe_utils.get_channel(server, ewcfg.channel_artexhibits)
                    await fe_utils.send_message(client, art_exhibits, msgtext)
                    await message.delete()

    # Community Service Clout
    elif community_service is not None and payload.channel_id == community_service.id:
        message = await community_service.fetch_message(payload.message_id)
        await add_xp(message.author.id, payload.guild_id, ewcfg.goonscape_clout_stat, 6500)

# find our REST API token
token = ewutils.getToken()

if token == None or len(token) == 0:
    ewutils.logMsg('Please place your API token in a file called "token", in the same directory as this script.')
    sys.exit(0)

# Load the cache before connecting to discord, this way we arent missing heartbeats
ewutils.logMsg("Initializing caches...")

# Set all predefined caches to enabled and initialize them
for cache_type_name in ewcfg.cacheable_types:
    ewutils.logMsg("Initializing {} cache.".format(cache_type_name))
    bknd_core.enabled_caches.append(cache_type_name)
    bknd_core.ObjCache(ew_obj_type=cache_type_name)

# connect to discord and run indefinitely
try:
    client.run(token, log_handler=None)
finally:
    ewutils.TERMINATE = True
    ewutils.logMsg("main thread terminated.")
