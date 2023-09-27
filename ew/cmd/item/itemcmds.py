import asyncio
import random
import re
import sys
import time
from copy import copy, deepcopy

import discord

from ew.backend import core as bknd_core
from ew.backend import item as bknd_item
from ew.backend.item import EwItem
from ew.backend.player import EwPlayer
from ew.cmd import faction, apt
try:
    from ew.cmd import debug as ewdebug
except:
    from ew.cmd import debug_dummy as ewdebug
from ew.static import cfg as ewcfg
from ew.static import cosmetics
from ew.static import fish as static_fish
from ew.static import food as static_food
from ew.static import hue as hue_static
from ew.static import items as static_items
from ew.static import poi as poi_static
from ew.static import weapons as static_weapons
from ew.static import community_cfg as comm_cfg
from ew.static import npc as static_npc
try:
    import ew.static.rstatic as static_relic
except:
    import ew.static.rstatic_dummy as static_relic
from ew.utils import apt as apt_utils
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import item as itm_utils
from ew.backend.apt import EwApartment
from . import itemutils as itm_u
from ew.utils import stats as ewstats
from ew.utils import loop as loop_utils
from ew.utils import prank as prank_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils import combat as cmbt_utils
try:
    from ew.cmd import debugr as debugr
except:
    from ew.cmd import debugr_dummy as debugr

async def soulextract(cmd):
    usermodel = EwUser(member=cmd.message.author)
    playermodel = EwPlayer(id_user=cmd.message.author.id, id_server=cmd.guild.id)
    if usermodel.has_soul == 1 and (ewutils.active_target_map.get(usermodel.id_user) == None or ewutils.active_target_map.get(usermodel.id_user) == ""):
        bknd_item.item_create(
            id_user=cmd.message.author.id,
            id_server=cmd.guild.id,
            item_type=ewcfg.it_cosmetic,
            item_props={
                'id_cosmetic': "soul",
                'cosmetic_name': "{}'s soul".format(playermodel.display_name),
                'cosmetic_desc': "The immortal soul of {}. It dances with a vivacious energy inside its jar.\n If you listen to it closely you can hear it whispering numbers: {}.".format(playermodel.display_name, cmd.message.author.id),
                'str_onadorn': ewcfg.str_soul_onadorn,
                'str_unadorn': ewcfg.str_soul_unadorn,
                'str_onbreak': ewcfg.str_soul_onbreak,
                'rarity': ewcfg.rarity_patrician,
                'attack': 6,
                'defense': 6,
                'speed': 6,
                'ability': None,
                'durability': ewcfg.soul_durability,
                'size': 6,
                'fashion_style': ewcfg.style_cool,
                'freshness': 10,
                'adorned': 'false',
                'user_id': usermodel.id_user
            }
        )

        usermodel.has_soul = 0
        usermodel.persist()
        response = "You tremble at the thought of trying this. Nothing ventured, nothing gained, you suppose. With all your mental fortitude you jam your hand deep into your chest and begin to pull out the very essence of your being. Your spirit, aspirations, everything that made you who you are begins to slowly drain from your mortal effigy until you feel absolutely nothing. Your soul flickers about, taunting you from outside your body. You capture it in a jar, almost reflexively.\n\nWow. Your personality must suck now."
    elif usermodel.has_soul == 1 and ewutils.active_target_map.get(usermodel.id_user) != "":
        response = "Now's not the time to be playing with your soul, dumbass! You have to focus on pointing the gun at your head!"
    else:
        response = "There's nothing left in you to extract. You already spent the soul you had."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def returnsoul(cmd):
    usermodel = EwUser(member=cmd.message.author)
    # soul = bknd_item.find_item(item_search="soul", id_user=cmd.message.author.id, id_server=cmd.guild.id)
    user_inv = bknd_item.inventory(id_user=cmd.message.author.id, id_server=cmd.guild.id, item_type_filter=ewcfg.it_cosmetic)
    soul_item = None
    soul = None
    eldritch = False
    for inv_object in user_inv:
        soul = inv_object
        soul_item = EwItem(id_item=soul.get('id_item'))
        if soul_item.item_props.get('id_cosmetic') == 'eldritchsoul':
            eldritch = True
            break
        elif str(soul_item.item_props.get('user_id')) == str(cmd.message.author.id):
            break

    if usermodel.has_soul == 1:
        response = "Your current soul is a little upset you tried to give it a roommate. Only one fits in your body at a time."

    elif soul:
        if eldritch:
            response = "The eldritch soul jar shudders for a second. You hesitate, but decide to open it. Black tendrils begin to emerge, slowly rooting deep into your chest and stomach. You don't even notice at first but you can't stop cackling. Your hands convulse, like they want to be invited inside that bystander's ribcage over there. Perhaps you'll indulge them. You're cackling so hard you can't breathe. You don't remember collapsing to the ground, but you're kneeling in the shards of the soul jar and a growing pool of your own blood.\n\nBut after a few minutes things seem to be back to normal. You can feel a soul inside you that actually resembles yours. You suppose those cosmic entities kept their promise then.\n\nAs long as this doesn't come back to haunt you, anyway."
            bknd_item.item_delete(id_item=soul.get('id_item'))
            usermodel.has_soul = 1
            usermodel.persist()

        elif soul.get('item_type') == ewcfg.it_cosmetic and soul_item.item_props.get('id_cosmetic') == "soul":
            if str(soul_item.item_props.get('user_id')) != str(cmd.message.author.id):
                response = "That's not your soul. Nice try, though."
            else:
                response = "You open the soul jar and hold the opening to your chest. The soul begins to crawl in, and a warmth returns to your body. Not exactly the warmth you had before, but it's too wonderful to pass up. You feel invigorated and ready to take on the world."
                bknd_item.item_delete(id_item=soul.get('id_item'))
                usermodel.has_soul = 1
                usermodel.persist()
        else:
            response = "Nice try, but your mortal coil recognizes a fake soul when it sees it."
    else:
        response = "You don't have a soul to absorb. Hopelessness is no fun, but don't get all delusional on us now."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def squeeze(cmd):
    usermodel = EwUser(member=cmd.message.author)
    soul_inv = bknd_item.inventory(id_user=cmd.message.author.id, id_server=cmd.guild.id, item_type_filter=ewcfg.it_cosmetic)

    if usermodel.life_state == ewcfg.life_state_corpse:
        response = "Alas, you lack the mortal appendages required to wring the slime out of someone's soul."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count <= 0:
        response = "Specify a soul you want to squeeze the life out of."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    target = cmd.mentions[0]
    if target.id == cmd.message.author.id:
        targetmodel = usermodel
    else:
        targetmodel = EwUser(member=target)

    if cmd.mentions_count > 1:
        response = "One dehumanizing soul-clutch at a time, please."
    elif targetmodel.life_state == ewcfg.life_state_corpse:
        response = "Enough already. They're dead."
    else:

        playermodel = EwPlayer(id_user=targetmodel.id_user)
        receivingreport = ""  # the receiver of the squeeze gets this in their channel

        squeezetext = re.sub("<.+>", "", cmd.message.content[(len(cmd.tokens[0])):]).strip()
        if len(squeezetext) > 500:
            squeezetext = squeezetext[:-500]

        poi = None
        target_item = None
        for soul in soul_inv:
            soul_item = EwItem(id_item=soul.get('id_item'))
            if soul_item.item_props.get('id_cosmetic') == 'soul' and int(soul_item.item_props.get('user_id')) == targetmodel.id_user:
                target_item = soul

        if targetmodel.has_soul == 1:
            response = "They look pretty soulful right now. You can't do anything to them."
        elif target_item == None:
            response = "You don't have their soul."
        elif (int(time.time()) - usermodel.time_lasthaunt) < ewcfg.cd_squeeze:
            timeleft = ewcfg.cd_squeeze - (int(time.time()) - usermodel.time_lasthaunt)
            response = "It's still all rubbery and deflated from the last time you squeezed it. Give it {} seconds.".format(timeleft)
        else:
            if squeezetext != "":
                receivingreport = "A voice in your head screams: \"{}\"\nSuddenly, you feel searing palpitations in your chest, and vomit slime all over the floor. Dammit, {} must be fucking around with your soul.".format(squeezetext, cmd.message.author.display_name)
            else:
                receivingreport = "You feel searing palpitations in your chest, and vomit slime all over the floor. Dammit, {} must be fucking with your soul.".format(cmd.message.author.display_name)

            poi = poi_static.id_to_poi.get(targetmodel.poi)

            usermodel.time_lasthaunt = int(time.time())
            usermodel.persist()

            penalty = (targetmodel.slimes * -0.25)
            targetmodel.change_slimes(n=penalty, source=ewcfg.source_haunted)
            targetmodel.persist()

            district_data = EwDistrict(district=targetmodel.poi, id_server=cmd.guild.id)
            district_data.change_slimes(n=-penalty, source=ewcfg.source_squeeze)
            district_data.persist()

            if receivingreport != "":
                loc_channel = fe_utils.get_channel(cmd.guild, poi.channel)
                await fe_utils.send_message(cmd.client, loc_channel, fe_utils.formatMessage(target, receivingreport))

            response = "You tightly squeeze {}'s soul in your hand, jeering into it as you do so. This thing was worth every penny.".format(playermodel.display_name)

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Dump out a player's inventory.
"""


inv_channel_ids = []


async def inventory_print(cmd):
    # Setup basic variables
    target_channel = cmd.message.channel
    target_inventory = cmd.message.author.id
    inventory_type = "player"
    targeting_dms = False

    # Retrieve indirect data
    player = EwPlayer(id_user=cmd.message.author.id)
    user_data = EwUser(id_user=player.id_user, id_server=player.id_server)
    poi_data = poi_static.id_to_poi.get(user_data.poi)

    # Note if this is in dms or not, so dms don't get formatted
    if isinstance(cmd.message.channel, discord.DMChannel):
        targeting_dms = True

    # Check if it's a chest or not
    if cmd.tokens[0].lower() == ewcfg.cmd_communitychest:

        # Stop now if there's no community chest
        if poi_data.community_chest is None:
            resp_txt = "There is no community chest here."
            response = fe_utils.formatMessage(cmd.message.author, resp_txt) if not targeting_dms else resp_txt

            return await fe_utils.send_message(cmd.client, target_channel, response)

        # Ensure they are checking chests in the poi channel or their dms
        if (not targeting_dms) and (target_channel.name != poi_data.channel):
                resp_txt = "You can't see the community chest from here."
                response = fe_utils.formatMessage(cmd.message.author, resp_txt) if not targeting_dms else resp_txt

                return await fe_utils.send_message(cmd.client, target_channel, response)

        # Mark as search for chest
        inventory_type = "chest"
        target_inventory = poi_data.community_chest

    elif cmd.tokens[0].lower() == ewcfg.cmd_collectioninventory:

        # Must specify a collection
        if len(cmd.tokens) < 2:
            response = "You have to specify a collection to check the contents of."
            response = fe_utils.formatMessage(cmd.message.author, response) if not targeting_dms else response
            return await fe_utils.send_message(cmd.client, target_channel, response)

        else:
            # Search for collection
            collection_seek = ewutils.flattenTokenListToString(cmd.tokens[1]).lower()
            
            # Check the user's inventory
            collection = bknd_item.find_item(item_search=collection_seek, id_user=user_data.id_user, id_server=user_data.id_server)
            # Check the current apt if not in inventory
            if collection is None and poi_data.is_apartment:
                if user_data.visiting == ewcfg.location_id_empty:
                    collection = bknd_item.find_item(item_search=collection_seek, id_user="{}{}".format(user_data.id_user, "decorate"),id_server=user_data.id_server)
                else:
                    collection = bknd_item.find_item(item_search=collection_seek, id_user="{}{}".format(user_data.visiting, "decorate"),id_server=user_data.id_server)

            if collection is None:
                response = "You don't seem to have that collection."
                response = fe_utils.formatMessage(cmd.message.author, response) if not targeting_dms else response
                return await fe_utils.send_message(cmd.client, target_channel, response)

            collection_item = EwItem(id_item=collection.get('id_item'))
            collectiontype = collection_item.item_props.get('id_furniture')
            if collectiontype not in ['largeaquarium', 'soulcylinder', 'weaponchest', 'scalpcollection', 'generalcollection', 'portablegreenhouse']:
                response = "You can't look at the contents of something that's not a collection."
                response = fe_utils.formatMessage(cmd.message.author, response) if not targeting_dms else response
                return await fe_utils.send_message(cmd.client, target_channel, response)

            # Make sure this is in DMs or the poi channel
            if (not targeting_dms) and target_channel.name != poi_data.channel:
                response = "You can't look at the contents of that collection here."
                response = fe_utils.formatMessage(cmd.message.author, response) if not targeting_dms else response
                return await fe_utils.send_message(cmd.client, target_channel, response)

            # Mark as search for collection
            inventory_type = "collection"
            target_inventory = "{}collection".format(collection.get("id_item"))

    else:
        # Ensure the inventory response in sent in dms, in case they requested it from in-server
        target_channel = cmd.message.author.dm_channel
        # User.dm_channel can just decide to be none if it would like, so create it if it's not there
        if target_channel is None:
            target_channel = await cmd.message.author.create_dm()

        targeting_dms = True

    # Don't interrupt if there is already an inventory printing in that channel
    if target_channel.id in inv_channel_ids:
        resp_txt = "Let the last inventory finish, prick."
        response = fe_utils.formatMessage(cmd.message.author, resp_txt) if not targeting_dms else resp_txt

        return await fe_utils.send_message(cmd.client, target_channel, response)

    # Check if the user has the bot blocked from dms, by dming them of course
    if targeting_dms:
        try:
            resp_txt = "__You are holding:__" if inventory_type == "player" else "__The community chest contains:__" if inventory_type == "chest" else "__The collection contains:__"
            await fe_utils.send_message(cmd.client, target_channel, resp_txt)
        except:
            # you can only tell them to unblock you if the channel they sent it through isn't their dms
            if cmd.message.channel.id != cmd.message.author.id:
                resp_txt = "You'll have to allow Endless War to send you DMs to check your inventory!"
                response = fe_utils.formatMessage(cmd.message.author, resp_txt)
                return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

    # All checks passed, let other prints know this channel is busy until the response is sent
    inv_channel_ids.append(target_channel.id)

    # Set default formatting and filtering parameters
    sort_by_type = False
    sort_by_name = False
    sort_by_id = False

    stacking = True
    search = False
    item_type = None
    prop_hunt = {}
    display_hue = False
    display_weapon_type = False

    # Set new parameters if given
    if cmd.tokens_count > 1:
        # standardize case
        lower_token_list = list(map(lambda tok: tok.lower(), cmd.tokens))

        # Sort by type
        if 'type' in lower_token_list:
            sort_by_type = True
        # Sort by name
        elif 'name' in lower_token_list:
            sort_by_name = True
        # Sort by id
        elif 'id' in lower_token_list:
            sort_by_id = True

        # Stack items of same name
        if 'nostack' in lower_token_list or 'unstack' in lower_token_list:
            stacking = False

        # Filter to general items
        if 'general' in lower_token_list or 'misc' in lower_token_list:
            item_type = ewcfg.it_item

        # Filter to Weapon items
        if 'weapon' in lower_token_list or 'weapons' in lower_token_list:
            item_type = ewcfg.it_weapon

        # Filter to furniture items
        if 'furniture' in lower_token_list:
            item_type = ewcfg.it_furniture

        # Filter to cosmetic items
        if 'cosmetic' in lower_token_list or 'cosmetics' in lower_token_list:
            item_type = ewcfg.it_cosmetic

        # Filter to food items
        if 'food' in lower_token_list:
            item_type = ewcfg.it_food

        # Filter to zines
        if 'book' in lower_token_list or 'books' in lower_token_list or 'zines' in lower_token_list:
            item_type = ewcfg.it_book

        # Filter to relic items
        if 'relic' in lower_token_list or 'relics' in lower_token_list:
            item_type = ewcfg.it_relic
        
        # Filter to preserved items (rigor mortis)
        if "preserved" in lower_token_list:
            prop_hunt["preserved"] = str(cmd.message.author.id)
        
        if "fish" in lower_token_list:
            prop_hunt["acquisition"] = ewcfg.acquisition_fishing
        
        if ewcfg.fish_rarity_common in lower_token_list:
            prop_hunt["rarity"] = ewcfg.fish_rarity_common
        elif ewcfg.fish_rarity_uncommon in lower_token_list:
            prop_hunt["rarity"] = ewcfg.fish_rarity_uncommon
        elif ewcfg.fish_rarity_rare in lower_token_list:
            prop_hunt["rarity"] = ewcfg.fish_rarity_rare
        elif ewcfg.fish_rarity_promo in lower_token_list:
            prop_hunt["rarity"] = ewcfg.fish_rarity_promo

        # Less tokens exist than colours or weapons. Search each token instead of each colour/weapon
        
        i = 1
        while i < len(lower_token_list):
            token = lower_token_list[i]

            #Filter by colour
            hue_prop = hue_static.hue_map.get(token)
            if(hue_prop):
                prop_hunt["hue"] = hue_prop.id_hue
                i += 1 # this is basically a simple for loop except when a token is identified in 1 way, the while loop moves to the next token instead of checking if its also something else.
                continue

            #Filter by weapon
            weapon_prop = static_weapons.weapon_map.get(token)
            if(weapon_prop):
                prop_hunt["weapon_type"] = weapon_prop.id_weapon
                i += 1
                continue

            style_prop = token in ewcfg.fashion_styles
            if(style_prop):
                prop_hunt["fashion_style"] = token
                i += 1
                continue

            i += 1
        
        if(not prop_hunt):
            prop_hunt = None

        #Display the colour infront of the name, or not
        if 'color' in lower_token_list or 'hue' in lower_token_list or 'colour' in lower_token_list:
            display_hue = True
        #Display the weapon type's name after the weapon's name
        if "weapontype" in lower_token_list:
            display_weapon_type = True
        # Search for a particular item. Ignore formatting parameters
        if 'search' in lower_token_list:
            stacking = False
            sort_by_id = False
            sort_by_name = False
            sort_by_type = False
            search = True

    # Finally, actually grab the inventory
    if sort_by_id:
        items = bknd_item.inventory(
            id_user=target_inventory,
            id_server=user_data.id_server,
            item_sorting_method='id',
            item_type_filter=item_type,
            item_prop_method=prop_hunt
        )
    elif sort_by_type:
        items = bknd_item.inventory(
            id_user=target_inventory,
            id_server=user_data.id_server,
            item_sorting_method='type',
            item_type_filter=item_type,
            item_prop_method=prop_hunt
        )
    elif search == True:
        items = itm_utils.find_item_all(
            item_search=ewutils.flattenTokenListToString(cmd.tokens[2:]),
            id_server=user_data.id_server,
            id_user=target_inventory,
            exact_search=False,
            search_names=True
        )
    else:
        items = bknd_item.inventory(
            id_user=target_inventory,
            id_server=user_data.id_server,
            item_type_filter=item_type,
            item_prop_method=prop_hunt
        )

    # Strip unnecessary data
    items = list(map(lambda dat: {
        "id_item": dat.get("id_item"),
        "quantity": dat.get("quantity"),
        "name": dat.get("name"),
        "soulbound": dat.get("soulbound"),
        "item_type": dat.get("item_type"),
        "hue": dat.get("item_props").get("hue"),
        "weapon_type": dat.get("item_props").get("weapon_type"),
        "id_furniture": dat.get("item_props").get("id_furniture"),
    }, items))
    
    # sort by name if requested
    if sort_by_name:
        items = sorted(items, key=lambda item: item.get('name').lower())

    # Setup a response container so the item data can get nuked ASAP, regardless of messages getting ratelimited
    resp_ctn = fe_utils.EwResponseContainer(client=cmd.client, id_server=cmd.guild.id)

    # Chests get to have the special empty response if they arent checked in dms, invs just cant be checked elsewhere
    if not targeting_dms:
        # Change string based on inventory type used
        inventory_string = "community chest" if inventory_type == "chest" else "item collection"    

        # Generate first message
        if len(items) == 0:
            response = fe_utils.formatMessage(cmd.message.author, f"The {inventory_string} is empty.")
        else:
            response = fe_utils.formatMessage(cmd.message.author, f"__The {inventory_string} contains:__")

        # set it to be sent
        resp_ctn.add_channel_response(target_channel, response)

    if len(items) > 0:

        # Set variable defaults
        stacked_item_map = {}
        response = ""
        current_type = ""

        for item in items:

            if not stacking:
                # Generate the item's line in the response based on the specified formatting
                response_part = "\n{id_item}: {soulbound_style}{hue}{name}{weapon_type_name}{soulbound_style}{quantity}{tag}".format(
                    id_item=item.get('id_item'),
                    name=item.get('name'),
                    hue=(item.get('hue') +" " if (item.get('hue') and display_hue) else "").capitalize(),
                    weapon_type_name=(", "+ static_weapons.weapon_map.get(item.get("weapon_type")).str_weapon if (display_weapon_type and item.get("weapon_type")) else ""),
                    soulbound_style=("**" if item.get('soulbound') else ""),
                    quantity=(" x{:,}".format(item.get("quantity")) if (item.get("quantity") > 1) else ""),
                    tag=(" [📦]" if (item.get("id_furniture") in static_items.furniture_collection) else ""), 
                )

                # Print item type labels if sorting by type and showing a new type of items
                if sort_by_type:
                    if current_type != item.get('item_type'):
                        current_type = item.get('item_type')
                        response_part = "\n**=={}==**".format(current_type.upper()) + response_part

            else:
                if display_hue:
                    item_hue = item.get('hue')
                    item_stack_name = "{hue}{name}".format(hue = item_hue +" " if item_hue else "",name = item.get('name'))
                    if item_stack_name in stacked_item_map:
                        stacked_item = stacked_item_map.get(item_stack_name)
                        stacked_item['quantity'] += item.get('quantity')
                    else:
                        stacked_item_map[item_stack_name] = item
                else:
                    # Add item quantity to existing stack
                    if item.get('name') in stacked_item_map:
                        stacked_item = stacked_item_map.get(item.get("name"))
                        stacked_item['quantity'] += item.get('quantity')
                    # Create stack for new item name
                    else:
                        stacked_item_map[item.get("name")] = item


            if not stacking and len(response) + len(response_part) > 1492:
                # Format the response if necessary and add to the container
                response = fe_utils.formatMessage(cmd.message.author, response) if not targeting_dms else response
                resp_ctn.add_channel_response(target_channel, response)

                response = ""

            if not stacking:
                response += response_part

        if stacking:
            # Setup variables
            current_type = ""
            item_names = stacked_item_map.keys()

            # Sort the names if necessary
            if sort_by_name:
                item_names = sorted(item_names)

            # iterate through all stacks
            for item_name in item_names:
                # Get the stack's item data
                item = stacked_item_map.get(item_name)

                # Generate the stack's line in the response
                response_part = "\n{id_item}: {soulbound_style}{hue}{name}{weapon_type_name}{soulbound_style}{quantity}{tag}".format(
                    id_item=item.get('id_item'),
                    name=item.get('name'),
                    hue=(item.get('hue') +" " if (item.get('hue') and display_hue) else "").capitalize(),
                    weapon_type_name=(", "+ static_weapons.weapon_map.get(item.get("weapon_type")).str_weapon if display_weapon_type and item.get("weapon_type") else ""),
                    soulbound_style=("**" if item.get('soulbound') else ""),
                    quantity=(" **x{:,}**".format(item.get("quantity")) if (item.get("quantity") > 0) else ""),
                    tag=(" [📦]" if (item.get("id_furniture") in static_items.furniture_collection) else ""),
                )

                # Print item type labels if sorting by type and showing a different type of items
                if sort_by_type:
                    if current_type != item.get('item_type'):
                        current_type = item.get('item_type')
                        response_part = "\n**=={}==**".format(current_type.upper()) + response_part

                # If the message is getting too long to send
                if len(response) + len(response_part) > 1492:
                    # Add it to the responses, and start a new one
                    # Format the response if necessary and add to the container
                    response = fe_utils.formatMessage(cmd.message.author, response) if not targeting_dms else response
                    resp_ctn.add_channel_response(target_channel, response)

                    response = ""

                # Add the generated line to the response
                response += response_part

        # Now that we have the responses, get the data out of memory
        del items

        # Format the response if necessary and add to the container
        response = fe_utils.formatMessage(cmd.message.author, response) if not targeting_dms else response
        resp_ctn.add_channel_response(target_channel, response)

    else:
        resp_txt = "Nothing."
        response = fe_utils.formatMessage(cmd.message.author, resp_txt) if not targeting_dms else resp_txt
        resp_ctn.add_channel_response(target_channel, response)


    # Send the response(s) then remove the target channel from the list of places already receiving inventories
    await resp_ctn.post()
    inv_channel_ids.remove(target_channel.id)

    return


"""
    Dump out the visual description of an item.
"""


async def item_look(cmd):
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    author = cmd.message.author
    player = EwPlayer(id_user=cmd.message.author.id)
    server = player.id_server
    user_data = EwUser(id_user=cmd.message.author.id, id_server=server)
    poi = poi_static.id_to_poi.get(user_data.poi)
    mutations = user_data.get_mutations()

    if user_data.visiting != ewcfg.location_id_empty:
        user_data = EwUser(id_user=user_data.visiting, id_server=server)

    item_dest = []
    collection_inv = bknd_item.inventory(id_user=str(user_data.id_user) + ewcfg.compartment_id_decorate, id_server=user_data.id_server, item_type_filter=ewcfg.it_furniture)
    item_sought_inv = bknd_item.find_item(item_search=item_search, id_user=author.id, id_server=server)
    item_dest.append(item_sought_inv)

    iterate = 0
    response = ""

    if poi.is_apartment:
        item_sought_closet = bknd_item.find_item(item_search=item_search,
                                                 id_user=str(user_data.id_user) + ewcfg.compartment_id_closet, id_server=server)
        item_sought_fridge = bknd_item.find_item(item_search=item_search,
                                                 id_user=str(user_data.id_user) + ewcfg.compartment_id_fridge, id_server=server)
        item_sought_decorate = bknd_item.find_item(item_search=item_search,
                                                   id_user=str(user_data.id_user) + ewcfg.compartment_id_decorate,
                                                   id_server=server)


        for collected in collection_inv:

            if collected.get('template') in ['largeaquarium', 'soulcylinder', 'weaponchest', 'scalpcollection', 'generalcollection', 'portablegreenhouse'] and collected.get('item_type') == ewcfg.it_furniture:
                item_sought_collection = bknd_item.find_item(item_search=item_search, id_user='{}collection'.format(collected.get('id_item')), id_server=server)
                item_dest.append(item_sought_collection)

        item_dest.append(item_sought_closet)
        item_dest.append(item_sought_fridge)
        item_dest.append(item_sought_decorate)

    for item_sought in item_dest:
        iterate += 1
        if item_sought:
            item = EwItem(id_item=item_sought.get('id_item'))

            message = item.item_props.get('item_message')

            id_item = item.id_item
            name = item_sought.get('name')
            response = static_items.item_def_map.get(item_sought.get('item_type')).str_desc

            # Replace up to two levels of variable substitutions.
            if response.find('{') >= 0:
                response = response.format_map(item.item_props)

                if response.find('{') >= 0:
                    try:
                        response = response.format_map(item.item_props)
                    except:
                        pass

            if item.item_type == ewcfg.it_food:
                # Some rotten fish randomly have their item.id_owner turned into an integer, so it turns into a string here before the fridge check.
                if type(item.id_owner) == int:
                    item.id_owner = str(item.id_owner)

                # Checks if food is expired and, if it's expired, whether or not item.id_owner has "fridge" at the end of it. Only changes flavor text.
                if float(item.item_props.get('time_expir') if not None else 0) < time.time() and item.id_owner[
                                                                                                 -6:] != ewcfg.compartment_id_fridge:
                    response += " This food item is rotten"
                    if ewcfg.mutation_id_spoiledappetite in mutations:
                        response += ". Yummy!"
                    else:
                        response += "."
                    # itm_utils.item_drop(id_item)
                if item.item_props.get('poisoned') == 'yes':
                    response += " It...smells awful funny."

            if item.item_type == ewcfg.it_weapon:
                response += "\n\n"

                if item.item_props.get("married") != "":
                    previous_partner = EwPlayer(id_user=int(item.item_props.get("married")), id_server=server)

                    if not user_data.weaponmarried or int(item.item_props.get("married")) != str(
                            user_data.id_user) or item.id_item != user_data.weapon:
                        response += "There's a barely legible engraving on the weapon that reads *{} :heart: {}*.\n\n".format(
                            previous_partner.display_name, name)
                    else:
                        response += "Your beloved partner. You can't help but give it a little kiss on the handle.\n"

                weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))

                if ewcfg.weapon_class_ammo in weapon.classes:
                    response += "Ammo: {}/{}".format(item.item_props.get("ammo"), weapon.clip_size) + "\n"

                if ewcfg.weapon_class_captcha in weapon.classes:
                    captcha = item.item_props.get("captcha")
                    if captcha not in [None, ""]:
                        response += "Security Code: **{}**".format(ewutils.text_to_regional_indicator(captcha)) + "\n"

                totalkills = int(item.item_props.get("totalkills", 0))
                totalhunts = int(item.item_props.get("totalhunts", 0))
                totalsuicides = int(item.item_props.get("totalsuicides", 0))



                if totalkills < 10:
                    response += "It looks brand new" + (
                        ".\n" if totalkills == 0 else ", having only killed {} people.\n".format(totalkills))
                elif totalkills < 100:
                    response += "There's some noticeable wear and tear on it. It has killed {} people.\n".format(
                        totalkills)
                else:
                    response += "A true legend in the battlefield, it has killed {} people.\n".format(totalkills)

                if totalhunts > 0:
                    response += "It also has {} hunts on it.\n".format(totalhunts)

                if totalsuicides > 0:
                    response += "Through sheer idiocy, it has killed {} of its own users.\n".format(totalsuicides)

                response += "You have killed {} people and hunted {} others with it.".format(item.item_props.get("kills", 0), item.item_props.get("hunts", 0))

            if item.item_type == ewcfg.it_cosmetic:
                response += "\n\n"

                response += "It's an article of {rarity} rank.\n".format(rarity=item.item_props['rarity'])
                """
                if any(stat in item.item_props.keys() for stat in ewcfg.playerstats_list):
                    response += "Adorning it "
                    stats_breakdown = []
                    for stat in ewcfg.playerstats_list:
                        if abs(int(item.item_props[stat])) > 0:
                            if int(item.item_props[stat]) > 0:
                                stat_response = "increases your "
                            else:
                                stat_response = "decreases your "
                            stat_response += "{stat} by {amount}".format(stat = stat, amount = item.item_props[stat])
                            stats_breakdown.append(stat_response)
                    if len(stats_breakdown) == 0:
                        response += "doesn't affect your stats at all.\n"
                    else:
                        response += ewutils.formatNiceList(names = stats_breakdown, conjunction = "and") + ". \n"
                """
                if item.item_props['durability'] is None:
                    response += "It can't be destroyed.\n"
                else:
                    if item.item_props['id_cosmetic'] == "soul":
                        original_durability = ewcfg.soul_durability
                    elif item.item_props['id_cosmetic'] == 'scalp':
                        if 'original_durability' in item.item_props.keys():
                            original_durability = int(float(item.item_props['original_durability']))
                        else:
                            original_durability = ewcfg.generic_scalp_durability
                    else:
                        if item.item_props.get('rarity') == ewcfg.rarity_princeps:
                            original_durability = ewcfg.base_durability * 100
                            original_item = None  # Princeps do not have existing templates
                        else:
                            try:
                                original_item = cosmetics.cosmetic_map.get(item.item_props['id_cosmetic'])
                                original_durability = original_item.durability
                            except:
                                original_durability = ewcfg.base_durability

                    current_durability = int(item.item_props['durability'])

                    # print('DEBUG -- DURABILITY COMPARISON\nCURRENT DURABILITY: {}, ORIGINAL DURABILITY: {}'.format(current_durability, original_durability))

                    if current_durability == original_durability:
                        response += "It looks brand new.\n"

                    elif original_durability != 0:
                        relative_change = round(current_durability / original_durability * 100)

                        if relative_change > 80:
                            response += "Its got a few minor scratches on it.\n"
                        elif relative_change > 60:
                            response += "It's a little torn from use.\n"
                        elif relative_change > 40:
                            response += "It's not looking so great...\n"
                        elif relative_change > 20:
                            response += "It's going to break soon!\n"

                    else:
                        response += "You have no idea how much longer this'll last. "

                if item.item_props['size'] == 0:
                    response += "It doesn't take up any space at all.\n"
                else:
                    response += "It costs about {amount} space to adorn.\n".format(amount=item.item_props['size'])

                if item.item_props['fashion_style'] == ewcfg.style_cool:
                    response += "Its got a cool feel to it. "
                if item.item_props['fashion_style'] == ewcfg.style_tough:
                    response += "It's lookin' tough as hell, my friend. "
                if item.item_props['fashion_style'] == ewcfg.style_smart:
                    response += "Its got sort of a smart vibe. "
                if item.item_props['fashion_style'] == ewcfg.style_beautiful:
                    response += "Its got a beautiful, refined feel. "
                if item.item_props['fashion_style'] == ewcfg.style_cute:
                    response += "It's super cuuuutttiieeeeeeeeeeeee~ deeeessuusususususususuusususufuswvgslgerphi4hjetbhjhjbetbjtrrpo"
                if item.item_props['fashion_style'] == ewcfg.style_evil:
                    response += "It's got an evil energy to it."
                if item.item_props['fashion_style'] == ewcfg.style_skill:
                    response += "It exudes the creator's skill. "

                response += "\n\nIts freshness rating is {rating}.".format(rating=bknd_item.get_base_freshness(item_id=item, seed=user_data.fashion_seed))#item.item_props['freshness']

                hue = hue_static.hue_map.get(item.item_props.get('hue'))
                hue2 = hue_static.hue_map.get(item.item_props.get('hue2'))
                pattern = item.item_props.get('pattern')
                if hue != None and pattern == None:
                    response += " Its been dyed in {} paint.".format(hue.str_name)
                elif hue != None and hue2 != None and pattern in hue_static.singular_patterns:
                    response += " Its been dyed in {} paint with a {} {}." .format(hue.str_name, hue2.str_name, pattern)
                elif hue != None and hue2 != None and pattern != None:
                    response += " It has a {} and {} {} pattern." .format(hue.str_name, hue2.str_name, pattern)

            if item.item_type == ewcfg.it_furniture:
                furnlist = static_items.furniture_map
                furn_obj = furnlist.get(item.item_props.get('id_furniture'))
                hue = hue_static.hue_map.get(item.item_props.get('hue'))
                if hue != None:
                    response += " Its been dyed in {} paint.".format(hue.str_name)

                if furn_obj is not None and furn_obj.furn_set == 'collection':

                    # Replaced with inventory_print
                    # if 'contents' in cmd.tokens[0] and 'general_collection' not in response:
                    #     response = response.format(scalp_inspect = '{general_collection}', aquarium_inspect = '{general_collection}', soul_cylinder = '{general_collection}', weapon_chest = '{general_collection}')
                    if 'scalp_inspect' in response:
                        response = response.format(scalp_inspect=itm_u.get_scalp_collection(id_item=item.id_item, id_server=item.id_server))
                    elif 'aquarium_inspect' in response:
                        response = response.format(aquarium_inspect=itm_u.get_fish_collection(id_item=item.id_item, id_server=item.id_server))
                    elif 'soul_cylinder' in response:
                        response = response.format(soul_cylinder=itm_u.get_soul_collection(id_item=item.id_item, id_server=item.id_server))
                    elif 'weapon_chest' in response:
                        response = response.format(weapon_chest = itm_u.get_weapon_collection(id_item=item.id_item, id_server=item.id_server))
                    elif 'greenhouse_inspect' in response:
                        response = response.format(greenhouse_inspect = itm_u.get_crop_collection(id_item=item.id_item, id_server=item.id_server))
                    elif 'general_collection' in response:
                        response = response.format(general_collection = itm_u.get_general_collection(id_item=item.id_item, id_server=item.id_server))

            durability = item.item_props.get('durability')
            if durability != None and item.item_type == ewcfg.it_item:
                if item.item_props.get('id_item') in ewcfg.durability_items:
                    if durability == 1:
                        response += " It can only be used one more time."
                    else:
                        response += " It has about {} uses left.".format(durability)

            response = name + (" x{:,}".format(item.stack_size) if (item.stack_size >= 1) else "") + "\n\n" + response
            if message is not None and message != "":
                response += "\n\nIt has a message attached: " + message
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(player, response))
        else:
            if iterate == len(item_dest) and response == "":
                if item_search:  # if they didnt forget to specify an item and it just wasn't found
                    response = "You don't have one."
                else:
                    response = "Inspect which item? (check **!inventory**)"

                await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


# this is basically just the item_look command with some other stuff at the bottom
async def item_use(cmd):
    use_mention_displayname = False

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    author = cmd.message.author
    server = cmd.guild

    item_sought = bknd_item.find_item(item_search=item_search, id_user=author.id, id_server=server.id)

    if item_sought:
        # Load the user before the item so that the right item props are used
        user_data = EwUser(member=author)

        item = EwItem(id_item=item_sought.get('id_item'))

        response = "The item doesn't have !use functionality"  # if it's not overwritten
        responses = []
        resp_ctn = fe_utils.EwResponseContainer(client=cmd.client, id_server=cmd.guild.id)

        secret_use = await ewdebug.secret_context(user_data, item, cmd)
        if secret_use is True:
            return

        if item.item_type == ewcfg.it_food:
            response = None
            responses = await user_data.eat(item)
            user_data.persist()

        if item.item_type == ewcfg.it_weapon:
            response = user_data.equip(item)
            user_data.persist()

        if item.item_type == ewcfg.it_relic:
            id = item.item_props.get('id_relic')
            function = debugr.relic_functions.get(id)
            if function is not None:
                return await function(cmd=cmd)

        if item.item_type in [ewcfg.it_item, ewcfg.it_cosmetic]:
            name = item_sought.get('name')
            context = item.item_props.get('context')
            if (context == "cardpack" or context == "promocardpack" or context == "boosterbox"):
                repeats = 0
                rarity = 1000
                if context == "promocardpack":
                    rarity = 500
                elif context == "boosterbox":
                    repeats = 36
                response = itm_utils.unwrap(id_user=author, id_server=server, item=item, repeats=repeats, rarity=rarity)
            elif (context == 'repel' or context == 'superrepel' or context == 'maxrepel'):
                statuses = user_data.getStatusEffects()
                if ewcfg.status_repelaftereffects_id in statuses:
                    response = "You need to wait a bit longer before applying more body spray."
                else:
                    if context == 'repel':
                        response = user_data.applyStatus(ewcfg.status_repelled_id)
                    elif context == 'superrepel':
                        response = user_data.applyStatus(ewcfg.status_repelled_id, multiplier=2)
                    elif context == 'maxrepel':
                        response = user_data.applyStatus(ewcfg.status_repelled_id, multiplier=4)
                    bknd_item.item_delete(item.id_item)
            elif context == 'pheromones':
                response = user_data.applyStatus(ewcfg.status_pheromones_id)
                bknd_item.item_delete(item.id_item)

            elif context == 'rain':
                response = "You begin the rain dance, jumping about with the feather as you perform the ancient ritual. The skys darken and grow heavy with the burden of moisture. Finally, in a final flourish to unleash the downpour, you fucking trip and fall flat on your face. Good job, dumbass!"
           

            elif context == ewcfg.item_id_gellphone:

                if user_data.has_gellphone():
                    gellphones = itm_utils.find_item_all(item_search=ewcfg.item_id_gellphone, id_user=user_data.id_user, id_server=user_data.id_server, item_type_filter=ewcfg.it_item)

                    for phone in gellphones:
                        phone_data = EwItem(id_item=phone.get('id_item'))
                        phone_data.item_props['gellphoneactive'] = 'false'
                        phone_data.persist()

                    response = "You turn off your gellphone."

                else:
                    response = "You turn on your gellphone."
                    item.item_props['gellphoneactive'] = 'true'
                    item.persist()
                
                await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)


            elif context == ewcfg.context_prankitem:
                item_action = ""
                side_effect = ""

                if cmd.message.guild is None or not ewutils.channel_name_is_poi(cmd.message.channel.name):  # or (user_data.poi not in poi_static.capturable_districts):
                    response = "You need to be on the city streets to unleash that prank item's full potential."
                else:
                    if item.item_props['prank_type'] == ewcfg.prank_type_instantuse:
                        item_action, response, use_mention_displayname, side_effect = await prank_utils.prank_item_effect_instantuse(cmd, item)
                        if side_effect != "":
                            response += await itm_utils.perform_prank_item_side_effect(side_effect, cmd=cmd)

                    elif item.item_props['prank_type'] == ewcfg.prank_type_response:
                        item_action, response, use_mention_displayname, side_effect = await prank_utils.prank_item_effect_response(cmd, item)
                        if side_effect != "":
                            response += await itm_utils.perform_prank_item_side_effect(side_effect, cmd=cmd)

                    elif item.item_props['prank_type'] == ewcfg.prank_type_trap:
                        item_action, response, use_mention_displayname, side_effect = await prank_utils.prank_item_effect_trap(cmd, item)

                    if item_action == "delete":
                        bknd_item.item_delete(item.id_item)
                        # prank_feed_channel = fe_utils.get_channel(cmd.guild, ewcfg.channel_prankfeed)
                        # await fe_utils.send_message(cmd.client, prank_feed_channel, fe_utils.formatMessage((cmd.message.author if use_mention_displayname == False else cmd.mentions[0]), (response+"\n`-------------------------`")))

                    elif item_action == "drop":
                        bknd_item.give_item(id_user=(user_data.poi + '_trap'), id_server=item.id_server, id_item=item.id_item)
                        # print(item.item_props)
            # elif context == "swordofseething":
            #
            # 	bknd_item.item_delete(item.id_item)
            # 	await ewdebug.begin_cataclysm(user_data)
            #
            # 	response = ewdebug.last_words

            elif context == "prankcapsule":
                response = itm_utils.popcapsule(id_user=author, id_server=server, item=item)
            
            elif context == 'partypopper':
                response = "***:tada:POP!!!:tada:*** Confetti flies all throughout the air, filling the area with a sense of celebration! :confetti_ball::confetti_ball::confetti_ball:"
                if item.soulbound is not True:
                    bknd_item.item_delete(item.id_item)

            elif context == 'milk':
                response = "After struggling with the milk cap, you eventually manage to force it off with your bare hands. Now holding the open gallon jug out, you pour all of its contents onto the ground until you're left with an empty carton."
            
            elif context == "revive":
                response = "You try to \"revive\" your fallen Slimeoid. Too bad this ain't a video game, or it might have worked!"

            elif context == "thedroplet":
                response = "You stole Slimernalia, you scrooge! What do you have to say for yourself?"



        if response is not None: resp_ctn.add_channel_response(cmd.message.channel, fe_utils.formatMessage((cmd.message.author if use_mention_displayname == False else cmd.mentions[0]), response))
        for resp in responses: resp_ctn.add_channel_response(cmd.message.channel, resp)
        await resp_ctn.post()

    else:
        if item_search:  # if they didnt forget to specify an item and it just wasn't found
            response = "You don't have one."
        else:
            response = "Use which item? (check **!inventory**)"

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    return


async def manually_edit_item_properties(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    if cmd.tokens_count == 4:
        item_id = cmd.tokens[1]
        column_name = cmd.tokens[2]
        column_value = cmd.tokens[3]

        target_item = EwItem(id_item=item_id)
        target_item.item_props[column_name] = column_value
        target_item.persist()

        response = "Edited item with ID {}. It's {} value has been set to {}.".format(item_id, column_name, column_value)

    else:
        response = 'Invalid number of options entered.\nProper usage is: !editprop [item ID] [name] [value], where [value] is in quotation marks if it is longer than one word.'

    await fe_utils.send_message(cmd.client, cmd.message.channel, response)


"""
    Command that lets players !give others items
"""


async def give(cmd):
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    author = cmd.message.author
    server = cmd.guild

    if cmd.mentions:  # if they're not empty
        recipient = cmd.mentions[0]
    elif cmd.tokens_count > 2:
        if cmd.tokens[2] == 'vendor':
            isVendor = True
        else:
            isVendor = False
        user_data = EwUser(member=author)
        newenemysearch = ewutils.flattenTokenListToString(cmd.tokens[1])
        newitemsearch = ewutils.flattenTokenListToString(cmd.tokens[2:])
        found_enemy = cmbt_utils.find_enemy(enemy_search=newenemysearch, user_data=user_data)
        item_sought = bknd_item.find_item(item_search=newitemsearch, id_user=author.id, id_server=server.id)

        if found_enemy and item_sought:
            if user_data.weaponmarried and user_data.weapon == item_sought.get('id_item'):
                response = "Your cuckoldry is appreciated, but your {} will always remain faithful to you.".format(item_sought.get('name'))
            elif item_sought.get('soulbound') and EwItem(id_item=item_sought.get('id_item')).item_props.get("context") != "housekey":
                response = "You can't just give away soulbound items."
            elif found_enemy.enemytype != 'npc':
                response = "Quit trying to barter with the free EXP and just gank em. For all of our sakes."
            else:
                npc_obj = static_npc.active_npcs_map.get(found_enemy.enemyclass)
                return await npc_obj.func_ai(keyword='give', enemy=found_enemy, channel=cmd.message.channel, item = item_sought)
        elif found_enemy:
            response = "You don't have that item."
        elif isVendor:
            pass #add command for vendors receiving items
            response = ""
        else:
            response = "Wait, who? I don't see anybody."
        return await fe_utils.send_message(cmd.client, cmd.message.channel,  fe_utils.formatMessage(cmd.message.author, response))
    else:
        response = "You have to specify the recipient of the item."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    user_data = EwUser(member=author)
    recipient_data = EwUser(member=recipient)

    if user_data.poi != recipient_data.poi:
        response = "You must be in the same location as the person you want to gift your item to, bitch."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # Check if the player is giving an item to themselves
    if user_data.id_user == recipient_data.id_user:
        response = "You can't give yourself something you already have, headass. You literally **already have it.**"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_sought = bknd_item.find_item(item_search=item_search, id_user=author.id, id_server=server.id)

    if item_sought:  # if an item was found


        # Slimernalia gifting

        if item_sought.get('item_type') == ewcfg.it_item and ewcfg.slimernalia_active:
            item_data = EwItem(id_item = item_sought.get('id_item'))


            # Fuck everything, TRIPLE nested if statement
            if item_data.item_props.get('id_item') == 'gift':
                if item_data.item_props.get('giftee_id') == recipient_data.id_user and item_data.item_props.get("gifter_id") == user_data.id_user:
                    if item_data.item_props.get("gifted") == "false":
                        item_data.item_props['gifted'] = "true"
                        item_data.persist()
                        ewstats.change_stat(id_server=cmd.guild.id, id_user=user_data.id_user, metric=ewcfg.stat_festivity, n=int(item_data.item_props.get("gift_value")))
                        user_data.persist()



        inv_response = bknd_item.check_inv_capacity(user_data=recipient_data, item_type=item_sought.get('item_type'), return_strings=True, pronoun="They")
        #don't let people give others food when they shouldn't be able to carry more food items
        if inv_response != "":
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, inv_response))


        if item_sought.get('item_type') == ewcfg.it_weapon:

            if user_data.weaponmarried and user_data.weapon == item_sought.get('id_item'):
                response = "Your cuckoldry is appreciated, but your {} will always remain faithful to you.".format(item_sought.get('name'))
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            elif recipient_data.life_state == ewcfg.life_state_corpse:
                response = "Ghosts can't hold weapons."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        if item_sought.get('item_type') == ewcfg.it_cosmetic:
            item_data = EwItem(id_item=item_sought.get('id_item'))
            item_data.item_props["adorned"] = 'false'
            item_data.item_props["slimeoid"] = 'false'
            item_data.persist()

        if item_sought.get('soulbound') and EwItem(id_item=item_sought.get('id_item')).item_props.get("context") != "housekey":
            response = "You can't just give away soulbound items."
        else:
            bknd_item.give_item(
                member=recipient,
                id_item=item_sought.get('id_item')
            )

            response = "You gave {recipient} a {item}".format(
                recipient=recipient.display_name,
                item=item_sought.get('name')
            )

            if item_sought.get('id_item') == user_data.weapon:
                user_data.weapon = -1
                user_data.persist()
            elif item_sought.get('id_item') == user_data.sidearm:
                user_data.sidearm = -1
                user_data.persist()

            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        if item_search:  # if they didnt forget to specify an item and it just wasn't found
            response = "You don't have one."
        else:
            response = "Give which item? (check **!inventory**)"

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Throw away an item
"""


async def discard(cmd):
    user_data = EwUser(member=cmd.message.author)
    response = ""

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)

    if item_sought:
        item = EwItem(id_item=item_sought.get("id_item"))

        if not item.soulbound:
            if item.item_type == ewcfg.it_weapon and user_data.weapon >= 0 and item.id_item == user_data.weapon:
                if user_data.weaponmarried and item.item_props.get('married') == user_data.id_user:
                    weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))
                    response = "As much as it would be satisfying to just chuck your {} down an alley and be done with it, here in civilization we deal with things *maturely.* You’ll have to speak to the guy that got you into this mess in the first place, or at least the guy that allowed you to make the inane decision in the first place. Luckily for you, they’re the same person, and he’s at the Dojo.".format(
                        weapon.str_weapon)
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                else:
                    user_data.weapon = -1
                    user_data.persist()


            elif item.item_type == ewcfg.it_weapon and user_data.sidearm >= 0 and item.id_item == user_data.sidearm:
                if user_data.weaponmarried and item.item_props.get('married') == user_data.id_user:
                    weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))
                    response = "As much as it would be satisfying to just chuck your {} down an alley and be done with it, here in civilization we deal with things *maturely.* You’ll have to speak to the guy that got you into this mess in the first place, or at least the guy that allowed you to make the inane decision in the first place. Luckily for you, they’re the same person, and he’s at the Dojo.".format(
                        weapon.str_weapon)
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                else:
                    user_data.sidearm = -1
                    user_data.persist()

            # elif item.item_type == ewcfg.it_cosmetic:
            # 	# Prevent the item from being dropped if it is adorned
            # 	if item_sought.get("adorned") == 'true':
            # 		response = "You need to !dedorn your {} first, before you can throw it away.".format(item_sought.get("name"))
            # 		return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            response = "You throw away your " + item_sought.get("name")
            itm_utils.item_drop(id_item=item.id_item)

            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

        else:
            response = "You can't throw away soulbound items."
    else:
        if item_search:
            response = "You don't have one"
        else:
            response = "Discard which item? (check **!inventory**)"

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Deletes a food item instead of dropping
"""


async def trash(cmd):
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    author = cmd.message.author
    server = cmd.guild

    item_sought = bknd_item.find_item(item_search=item_search, id_user=author.id, id_server=server.id)

    if item_sought:
        # Load the user before the item so that the right item props are used
        user_data = EwUser(member=author)

        item = EwItem(id_item=item_sought.get('id_item'))

        response = "You can't !trash an item that isn't food. Try **!drop**ing it instead."  # if it's not overwritten

        if item.item_type == ewcfg.it_food:
            response = "You throw away your {} into a nearby trash can.".format(item.item_props.get("food_name"))
            bknd_item.item_delete(item.id_item)
    else:
        response = "Are you sure you have that item?"

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def zuck(cmd):
    user_data = EwUser(member=cmd.message.author)

    tokens = ewutils.flattenTokenListToString(cmd.tokens[1:])

    syr_item = bknd_item.find_item(item_search="zuckerberg", id_user=cmd.message.author.id, id_server=cmd.guild.id)

    if syr_item:
        response = "The syringe is all rusted out. It's a shame you zucked the only person capable of maintainting it."
    else:
        response = "You'll need a corpse and the zuck syringe before you can do that."

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def makecostume(cmd):
    costumekit = bknd_item.find_item(item_search="costumekit", id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None, item_type_filter=ewcfg.it_item)

    user_data = EwUser(member=cmd.message.author)

    id_user = user_data.id_user
    id_server = user_data.id_server

    if not costumekit:
        response = "You don't know how to make one, bitch."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if len(cmd.tokens) != 3:
        response = 'Usage: !makecostume "[name]" "[description]".\nExample: !makecostume "Ghost Costume" "A bedsheet with holes for eyes."'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    bknd_item.item_delete(id_item=costumekit.get('id_item'))

    item_name = cmd.tokens[1]
    item_desc = cmd.tokens[2]

    item_props = {
        "id_cosmetic" : 'dhcostume',
        "cosmetic_name": item_name,
        "cosmetic_desc": item_desc,
        "adorned": "false",
        "rarity": "Plebeian",
        "context": "costume",
        'attack': 6,
        'defense': 6,
        'speed': 6,
        'size': 3,
        'durability': ewcfg.soul_durability,
        'fashion_style': ewcfg.style_cool,
        'freshness': 10,
        'ability': None,
        'str_onadorn': ewcfg.str_generic_onadorn,
        'str_unadorn': ewcfg.str_generic_unadorn,
        'str_onbreak': ewcfg.str_generic_onbreak
    }

    new_item_id = bknd_item.item_create(
        id_server=id_server,
        id_user=id_user,
        item_type=ewcfg.it_cosmetic,
        item_props=item_props
    )

    response = "You fashion your **{}** Double Halloween costume using the creation kit.".format(item_name)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def flowerpot(cmd):
    # Now just a command to weed out
    rand1 = random.randrange(100)
    rand2 = random.randrange(5)
    response = ""
    if rand1 > 80:
        response = "**"
    for x in range(rand2 + 1):
        response += "Y"
    for x in range(rand2 + 1):
        response += "E"
    for x in range(rand2 + 1):
        response += "A"
    for x in range(rand2 + 1):
        response += "H"
    response += " BRO!"
    if rand1 > 80:
        response += "**"

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def unpot(cmd):
    playermodel = EwPlayer(id_user=cmd.message.author.id)
    usermodel = EwUser(id_user=cmd.message.author.id, id_server=playermodel.id_server)
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=playermodel.id_server)
    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_type == ewcfg.it_furniture:
            if item.item_props.get('id_furniture') == "flowerpot" and item.item_props.get('acquisition') != ewcfg.acquisition_smelting:
                if bknd_item.give_item(id_item=item.item_props.get('acquisition'), id_user=cmd.message.author.id, id_server=cmd.guild.id):
                    response = "You yank the foliage out of the pot."
                    bknd_item.item_delete(id_item=item_sought.get('id_item'))
                else:
                    response = "You try to yank at the foliage, but your hands are already full of food!"
            else:
                response = "Get the pot before you unpot it."
        else:
            response = "Get the pot before you unpot it."
    else:
        response = "Are you sure you have that plant?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def propstand(cmd):
    playermodel = EwPlayer(id_user=cmd.message.author.id)
    usermodel = EwUser(id_server=playermodel.id_server, id_user=cmd.message.author.id)

    check_poi = poi_static.id_to_poi.get(usermodel.poi)
    if not (check_poi.is_apartment and (cmd.message.guild is None or check_poi.channel == cmd.message.channel.name)):
        return await apt_utils.lobbywarning(cmd)

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=playermodel.id_server)

    if not bknd_item.check_inv_capacity(user_data=usermodel, item_type=ewcfg.it_furniture):
        response = "You don't have room for any more furniture items."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_type == ewcfg.it_furniture:
            if item.item_props.get('id_furniture') == "propstand":
                response = "It's already on a prop stand."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        if item.soulbound:
            response = "Cool idea, but no. If you tried to mount a soulbound item above the fireplace you'd be stuck there too."
        elif item.item_type == ewcfg.it_relic or item.item_props.get('aquisition') == 'relic':
            response = "Hey, can't help but notice that you don't run a museum. Only people that run a museum are allowed to stick priceless artifacts on pedestals. Think you can handle that, bitch?"
        else:
            if item.item_type == ewcfg.it_weapon and usermodel.weapon >= 0 and item.id_item == usermodel.weapon:
                if usermodel.weaponmarried:
                    weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))
                    response = "Your dearly beloved? Put on a propstand? At least have the decency to get a divorce at the dojo first, you cretin.".format(weapon.str_weapon)
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                else:
                    usermodel.weapon = -1
                    usermodel.persist()
            elif item.item_type == ewcfg.it_cosmetic:
                item.item_props["adorned"] = "false"
                item.item_props["slimeoid"] = 'false'
                item.persist()

            fname = "{} stand".format(item_sought.get('name'))
            response = "You affix the {} to a wooden mount. You know this priceless trophy will last thousands of years, so you spray it down with formaldehyde to preserve it forever. Or at least until you decide to remove it.".format(item_sought.get('name'))
            lookdesc = "A {} is mounted on the wall.".format(item_sought.get('name'))
            placedesc = "You mount the {} on the wall. God damn magnificent.".format(item_sought.get('name'))
            fdesc = static_items.item_def_map.get(item_sought.get('item_type')).str_desc
            if fdesc.find('{') >= 0:
                fdesc = fdesc.format_map(item.item_props)

                if fdesc.find('{') >= 0:
                    fdesc = fdesc.format_map(item.item_props)
            fdesc += " It's preserved on a mount."

            bknd_item.item_create(
                id_user=cmd.message.author.id,
                id_server=cmd.guild.id,
                item_type=ewcfg.it_furniture,
                item_props={
                    'furniture_name': fname,
                    'id_furniture': "propstand",
                    'furniture_desc': fdesc,
                    'rarity': ewcfg.rarity_plebeian,
                    'acquisition': "{}".format(item_sought.get('id_item')),
                    'furniture_place_desc': placedesc,
                    'furniture_look_desc': lookdesc
                }
            )
            bknd_item.give_item(id_item=item_sought.get('id_item'), id_user=str(cmd.message.author.id) + "stand", id_server=cmd.guild.id)
    # bknd_item.item_delete(id_item=item_sought.get('id_item'))

    else:
        if item_search == "" or item_search == None:
            response = "Specify the item you want to put on the stand."
        else:
            response = "Are you sure you have that item?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def releaseprop(cmd):
    playermodel = EwPlayer(id_user=cmd.message.author.id)
    user_data = EwUser(id_user=cmd.message.author.id, id_server=playermodel.id_server)

    if user_data.poi != ewcfg.poi_id_bazaar:
        response = "You need to see a specialist at The Bazaar to do that."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=playermodel.id_server)
    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_type == ewcfg.it_furniture:
            if item.item_props.get('id_furniture') == "propstand" and item.item_props.get('acquisition') != ewcfg.acquisition_smelting:
                if bknd_item.give_item(id_item=item.item_props.get('acquisition'), id_user=cmd.message.author.id, id_server=cmd.guild.id):
                    response = "After a bit of tugging, you and the mysterious individual running the prop release stall pry the item of its stand."
                    bknd_item.item_delete(id_item=item_sought.get('id_item'))
                else:
                    stood_item = EwItem(id_item=item.item_props.get('acquisition'))
                    response = "You can't carry any more {}s, so this is staying on the stand.".format(stood_item.item_type)
            elif item.item_props.get('acquisition') == ewcfg.acquisition_smelting:
                response = "Uh oh. This one's not coming out. "
            else:
                response = "Don't try to unstand that which is not a stand."
        else:
            response = "Don't try to unstand that which is not a stand."
    else:
        response = "Are you sure you have that item?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def aquarium(cmd):
    # Removed
    response = "You can plop fish in an aquarium with !collect. You can purchase aquariums at the Museum."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def releasefish(cmd):
    playermodel = EwPlayer(id_user=cmd.message.author.id)
    usermodel = EwUser(id_user=cmd.message.author.id, id_server=playermodel.id_server)

    if usermodel.poi != ewcfg.poi_id_bazaar:
        response = "You need to see a specialist at The Bazaar to do that."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=playermodel.id_server)
    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_type == ewcfg.it_furniture:
            if item.item_props.get('id_furniture') == "aquarium" and item.item_props.get('acquisition') != ewcfg.acquisition_smelting:
                if bknd_item.give_item(id_item=item.item_props.get('acquisition'), id_user=cmd.message.author.id, id_server=cmd.guild.id):
                    response = "The mysterious individual running the fish luring stall helps you coax the fish out of its tank."
                    bknd_item.item_delete(id_item=item_sought.get('id_item'))
                else:
                    response = "The individual running the fish luring stall coaxes the fish out of the tank, but you can't hold it, so they put it back and berate you for wasting their time."
            elif item.item_props.get('acquisition') == ewcfg.acquisition_smelting:
                response = "Uh oh. This one's not coming out. "
            else:
                response = "Don't try to conjure a fish out of just anything. Find an aquarium."
        else:
            response = "Don't try to conjure a fish out of just anything. Find an aquarium."
    else:
        response = "Are you sure you have that fish?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def store_item(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    if poi.community_chest != None:
        return await faction.factioncmds.store(cmd)
    elif poi.is_apartment:
        return await apt.aptcmds.store_item(cmd)
    # response = "Try that in a DM to ENDLESS WAR."
    else:
        response = "There is no storage here, public or private."
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def remove_item(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    if poi.community_chest != None:
        return await faction.factioncmds.take(cmd)
    elif poi.is_apartment:
        return await apt.aptcmds.remove_item(cmd)
    # response = "Try that in a DM to ENDLESS WAR."
    else:
        response = "There is no storage here, public or private."
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def unwrap(cmd):
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id)
    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_type == ewcfg.it_item:
            if item.item_props.get('id_item') == "gift":
                if bknd_item.give_item(id_item=item.item_props.get('acquisition'), id_user=cmd.message.author.id, id_server=cmd.guild.id):
                    gifted_item = EwItem(id_item=item.item_props.get('acquisition'))

                    gift_name_type = ''
                    if gifted_item.item_type == ewcfg.it_item:
                        gift_name_type = 'item_name'
                    elif gifted_item.item_type == ewcfg.it_medal:
                        gift_name_type = 'medal_name'
                    elif gifted_item.item_type == ewcfg.it_questitem:
                        gift_name_type = 'qitem_name'
                    elif gifted_item.item_type == ewcfg.it_food:
                        gift_name_type = 'food_name'
                    elif gifted_item.item_type == ewcfg.it_weapon:
                        gift_name_type = 'weapon_name'
                    elif gifted_item.item_type == ewcfg.it_cosmetic:
                        gift_name_type = 'cosmetic_name'
                    elif gifted_item.item_type == ewcfg.it_furniture:
                        gift_name_type = 'furniture_name'
                    elif gifted_item.item_type == ewcfg.it_book:
                        gift_name_type = 'title'

                    gifted_item_name = gifted_item.item_props.get('{}'.format(gift_name_type))
                    
                    # Specifically for weapons, if the weapon doesn't have a name, then use it's type
                    if (not gifted_item_name) and gifted_item.item_type == ewcfg.it_weapon:
                        weapon_type = gifted_item.item_props.get("weapon_type")
                        weapon_data = static_weapons.weapon_map.get(weapon_type)
                        gifted_item_name = weapon_data.str_name
                    
                    gifted_item_message = item.item_props.get('context')


                    if ewcfg.slimernalia_active:
                        giftee_data = EwUser(member=cmd.message.author)
                        # Make sure the player is not opening their own gift before applying festivity
                        if giftee_data.id_user != item.item_props.get("gifter_id"):
                            ewstats.change_stat(id_server=cmd.guild.id, id_user=cmd.message.author.id, metric=ewcfg.stat_festivity, n=ewcfg.festivity_gift_wrap)

                    response = "You shred through the packaging formalities to reveal a {}!\nThere is a note attached: '{}'.".format(gifted_item_name, gifted_item_message)
                    bknd_item.item_delete(id_item=item_sought.get('id_item'))
                else:
                    response = "Whatever's inside, you can't hold anymore!"
            else:
                response = "You can't unwrap something that isn't a gift, bitch."
        else:
            response = "You can't unwrap something that isn't a gift, bitch."
    else:
        response = "Are you sure you have that item?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def add_message(cmd):
    if cmd.tokens_count == 1:
        response = "Scrawl what? Do you even know what that means?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif cmd.tokens_count == 2:
        response = "Try !scrawl <item> <description>."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1])
    outofspace = False
    message_text = ' '.join(word for word in cmd.tokens[2:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)


    if len(message_text) > 1000:
        outofspace = True
        message_text = message_text[:1000]

    if item_sought:
        item_obj = EwItem(id_item=item_sought.get('id_item'))
        has_message = item_obj.item_props.get('item_message')
        item_obj.item_props['item_message'] = message_text
        item_obj.persist()
        if has_message == None or has_message == "":
            response = "You scrawl out a little note and put it on the {}.\n\n{}".format(item_sought.get('name'), message_text)
        else:
            response = "You rip out the old message and scrawl another one on the {}.\n\n{}".format(item_sought.get('name'), message_text)
        if outofspace is True:
            response += "\nOh. Shit, looks like you ran out of space."
    else:
        response = "Are you sure you have that item?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def strip_message(cmd):
    if cmd.tokens_count == 1:
        response = "You heard 'em. *Strip.*"
        user_data = EwUser(member=cmd.message.author)
        user_data.change_crime(n=1) #indecent exposure
        user_data.persist()
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)

    if item_sought:
        item_obj = EwItem(id_item=item_sought.get('id_item'))
        has_message = item_obj.item_props.get('item_message')

        if has_message == None or has_message == "":
            response = "There is no message. Quit reading into everything."
        else:
            item_obj.item_props['item_message'] = ""
            item_obj.persist()
            response = "You rip out the old message. Nobody will ever know what they wrote here."
    else:
        response = "Are you sure you have that item?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" 
    DEBUG COMMANDS
"""


async def forge_master_poudrin(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    if cmd.mentions_count == 1:
        member = cmd.mentions[0]
        user_data = EwUser(member=member)
    else:
        return

    item_props = {
        "cosmetic_name": (ewcfg.emote_masterpoudrin + " Master Poudrin " + ewcfg.emote_masterpoudrin),
        "cosmetic_desc": "One poudrin to rule them all... or something like that. It's wrapped in twine, fit to wear as a necklace. There's a fuck ton of slime on the inside, but you're not nearly powerful enough on your own to !crush it.",
        "adorned": "false",
        "rarity": "princeps",
        "context": user_data.slimes,
        "id_cosmetic": "masterpoudrin",
    }

    new_item_id = bknd_item.item_create(
        id_server=cmd.guild.id,
        id_user=user_data.id_user,
        item_type=ewcfg.it_cosmetic,
        item_props=item_props,
        soulbound=True
    )

    ewutils.logMsg("Master poudrin created. Slime stored: {}, Cosmetic ID = {}".format(user_data.slimes, new_item_id))

    user_data.slimes = 0
    user_data.persist()

    response = "A pillar of light envelops {}! All of their slime is condensed into one, all-powerful Master Poudrin!\nDon't !crush it all in one place, kiddo.".format(
        member.display_name)
    await fe_utils.send_message(cmd.client, cmd.message.channel, response)


# A debug function designed to generate almost any kind of item within the game. Can be used to give items to users.
async def create_item(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    if len(cmd.tokens) > 1:
        value = cmd.tokens[1]
    else:
        return

    item_recipient = None
    if cmd.mentions_count == 1:
        item_recipient = cmd.mentions[0]
    else:
        item_recipient = cmd.message.author

    # The proper usage is !createitem [item id] [recipient]. The opposite order is invalid.
    if '<@' in value:  # Triggers if the 2nd command token is a mention
        response = "Proper usage of !createitem: **!createitem [item id] [recipient]**."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

    item = static_items.item_map.get(value)

    item_type = ewcfg.it_item
    if item != None:
        item_id = item.id_item
        name = item.str_name

    # Finds the item if it's an EwFood item.
    if item == None:
        item = static_food.food_map.get(value)
        item_type = ewcfg.it_food
        if item != None:
            item_id = item.id_food
            name = item.str_name

    # Finds the item if it's an EwCosmeticItem.
    if item == None:
        item = cosmetics.cosmetic_map.get(value)
        item_type = ewcfg.it_cosmetic
        if item != None:
            item_id = item.id_cosmetic
            name = item.str_name

    if item == None:
        item = static_items.furniture_map.get(value)
        item_type = ewcfg.it_furniture
        if item != None:
            item_id = item.id_furniture
            name = item.str_name
            if item_id in static_items.furniture_pony:
                item.vendors = [ewcfg.vendor_bazaar]

    if item == None:
        item = static_weapons.weapon_map.get(value)
        item_type = ewcfg.it_weapon
        if item != None:
            item_id = item.id_weapon
            name = item.str_weapon

    if item == None:
        item = static_fish.fish_map.get(value)
        item_type = ewcfg.it_food
        if item != None:
            item_id = item.id_fish
            name = item.str_name

    if item == None:
        item = static_relic.relic_map.get(value)
        item_type = ewcfg.it_relic
        if item != None:
            item_id = item.id_relic
            name = item.str_name

    if item != None:

        item_props = itm_utils.gen_item_props(item)

        generated_item_id = bknd_item.item_create(
            item_type=item_type,
            id_user=item_recipient.id,
            id_server=cmd.guild.id,
            stack_max=-1,
            stack_size=0,
            item_props=item_props
        )
        if generated_item_id is not None:
            response = "Created item **{}** with id **{}** for **{}**".format(name, generated_item_id, item_recipient)
        else:
            response = "Could not create item."
    else:
        response = "Could not find item."

    await fe_utils.send_message(cmd.client, cmd.message.channel, response)


async def create_multi(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    if len(cmd.tokens) > 2:
        number = int(cmd.tokens[1])
        value = cmd.tokens[2]
    else:
        return

    item_recipient = None
    if cmd.mentions_count == 1:
        item_recipient = cmd.mentions[0]
    else:
        item_recipient = cmd.message.author

    # The proper usage is !createitem [item id] [recipient]. The opposite order is invalid.
    if '<@' in value:  # Triggers if the 2nd command token is a mention
        response = "Proper usage of !createitem: **!createitem [item id] [recipient]**."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

    item = static_items.item_map.get(value)

    item_type = ewcfg.it_item
    if item != None:
        item_id = item.id_item
        name = item.str_name

    # Finds the item if it's an EwFood item.
    if item == None:
        item = static_food.food_map.get(value)
        item_type = ewcfg.it_food
        if item != None:
            item_id = item.id_food
            name = item.str_name

    # Finds the item if it's an EwCosmeticItem.
    if item == None:
        item = cosmetics.cosmetic_map.get(value)
        item_type = ewcfg.it_cosmetic
        if item != None:
            item_id = item.id_cosmetic
            name = item.str_name

    if item == None:
        item = static_items.furniture_map.get(value)
        item_type = ewcfg.it_furniture
        if item != None:
            item_id = item.id_furniture
            name = item.str_name
            if item_id in static_items.furniture_pony:
                item.vendors = [ewcfg.vendor_bazaar]

    if item == None:
        item = static_weapons.weapon_map.get(value)
        item_type = ewcfg.it_weapon
        if item != None:
            item_id = item.id_weapon
            name = item.str_weapon

    if item == None:
        item = static_fish.fish_map.get(value)
        item_type = ewcfg.it_food
        if item != None:
            item_id = item.id_fish
            name = item.str_name

    if item != None:

        for x in range(number):
            item_props = itm_utils.gen_item_props(item)

            generated_item_id = bknd_item.item_create(
                item_type=item_type,
                id_user=item_recipient.id,
                id_server=cmd.guild.id,
                stack_max=-1,
                stack_size=0,
                item_props=item_props
            )

        response = "Created {} items **{}** for **{}**".format(number, name, item_recipient)
    else:
        response = "Could not find item."

    await fe_utils.send_message(cmd.client, cmd.message.channel, response)




# Debug
async def manual_soulbind(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    if len(cmd.tokens) > 1:
        id_item = cmd.tokens[1]
    else:
        return

    item = EwItem(id_item=id_item)

    if item != None:
        item.soulbound = True
        item.persist()

        response = "Soulbound item **{}**.".format(id_item)
        await fe_utils.send_message(cmd.client, cmd.message.channel, response)
    else:
        return


async def create_all(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    # The proper usage is !createitem [item id] [recipient]. The opposite order is invalid.
    if '<@' in cmd.tokens[1]:  # Triggers if the 2nd command token is a mention
        response = "Proper usage of !createall: **!createall [Number of copies] [recipient]**."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

    try:
        num_target = int(cmd.tokens[1])
    except:
        num_target = 1

    number_created = 0

    if cmd.mentions_count == 1:
        item_recipient = cmd.mentions[0]
    else:
        item_recipient = cmd.message.author

    list_all = static_items.item_list + static_items.furniture_list
    list_all += static_food.food_list
    list_all += static_fish.fish_list
    list_all += static_weapons.weapon_list
    list_all += cosmetics.cosmetic_items_list

    for item in list_all:

        if item != None:
            number_of_each = 0
            while number_of_each < num_target:
                item_props = itm_utils.gen_item_props(item)

                bknd_item.item_create(
                    item_type=item.item_type,
                    id_user=item_recipient.id,
                    id_server=cmd.guild.id,
                    stack_max=-1,
                    stack_size=0,
                    item_props=item_props
                )

                number_created += 1
                number_of_each += 1

    response = "Created {} items for **{}**.".format(number_created, item_recipient)

    await fe_utils.send_message(cmd.client, cmd.message.channel, response)


async def manual_transfer(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return
    item_id = cmd.tokens[1]
    destination = cmd.tokens[2]
    if cmd.mentions_count == 1:
        target = EwUser(member=cmd.mentions[0])
        destination = str(target.id_user)
    item_sought = EwItem(id_item=item_id)

    if item_sought:
        item_sought.id_owner = destination
        response = "OK, item moved."
        item_sought.persist()
    else:
        response = "Can't move that. It's !moveitem <item id> <destination>"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def collect(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)
    item_sought_col = None

    if cmd.tokens_count != 3:
        response = "You need to specify the item and the collection. Try !collect \"collection\" \"item\"."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    collection_seek = cmd.tokens[1]
    # Check for collection in apartment's decorate inventory
    if (poi.is_apartment and user_data.visiting == ewcfg.location_id_empty):
        item_sought_col = bknd_item.find_item(item_search=collection_seek, id_user="{}{}".format(user_data.id_user, "decorate"),id_server=user_data.id_server)
    # If user has packrat or is in their apartment, check their actual inventory
    if item_sought_col is None and ((ewcfg.mutation_id_packrat in user_data.get_mutations()) or (poi.is_apartment and user_data.visiting == ewcfg.location_id_empty)):
        item_sought_col = bknd_item.find_item(item_search=collection_seek, id_user=user_data.id_user, id_server=user_data.id_server)

    item_seek = cmd.tokens[2]
    item_sought_item = bknd_item.find_item(item_search=item_seek, id_user=user_data.id_user, id_server=user_data.id_server)

    # Stop the command if a variety of things
    if (user_data.visiting != ewcfg.location_id_empty or not poi.is_apartment) and ewcfg.mutation_id_packrat not in user_data.get_mutations():
        response = "Nobody can know about your shameful hoarding habits. Add to your collections in your apartment."
    elif not item_sought_col:
        response = "You don't have that collection either here, or in your inventory."
    elif not item_sought_item:
        response = "Ah, a collector of imaginary objects. Too bad your brain is one of them. Pick a real item."
    elif not collection_seek:
        response = "You must specify a collection item."
    elif item_sought_item.get('soulbound') == True:
        response = "That's bound to your soul. You can't collect it any harder if you wanted to."
    elif item_sought_item.get('item_type') == ewcfg.it_relic:
        response = "Only some sort of CURATOR can pull hyjinks like that, besides that you have a feeling someone will swipe the relic under your nose when you try to get it out anyways."
    else:
        furn_list = static_items.furniture_map
        item = EwItem(id_item=item_sought_item.get('id_item'))
        collection = EwItem(id_item=item_sought_col.get('id_item'))
        collectiontype = collection.item_props.get('id_furniture')
        collect_map = furn_list.get(collectiontype)

        collection_inventory = bknd_item.inventory(id_user='{}collection'.format(item_sought_col.get('id_item')), id_server=cmd.guild.id)

        # Make sure collection is the corresponding type of item.
        if collect_map is None or collect_map.furn_set != 'collection':
            response = "You can't just shove anything into anything. A {} isn't gonna fit in a {}.".format(item_sought_item.get('name'), item_sought_col.get('name'))
        elif ((collectiontype == 'weaponchest' and item.item_type != ewcfg.it_weapon) or 
              (collectiontype == 'soulcylinder' and item.item_props.get('id_cosmetic') != 'soul') or 
              (collectiontype == 'scalpcollection' and item.item_props.get('id_cosmetic') != 'scalp') or 
              (collectiontype == 'largeaquarium' and item.item_props.get('acquisition') != ewcfg.acquisition_fishing) or 
              (collectiontype == 'portablegreenhouse' and item.item_props.get('id_food') not in static_food.vegetable_ids_list) or
              (item.item_props.get('id_furniture') in static_items.furniture_collection) 
              ):

            response = "You've got the wrong item type. It's a {}, try and guess what it's for.".format(item_sought_col.get('name'))

        # Make sure collection isn't full
        elif len(collection_inventory) >= 50 or (len(collection_inventory) >= 10 and collectiontype=='generalcollection'):
            response= "You collection's full. You really stuffed that sucker, goddamn."
        elif item.soulbound:
            response = "If you try to collect a soulbound item you'll basically be collecting yourself. You decide not to trap yourself in the {}.".format(item.item_props.get('str_name'))
        else:
            # Unequip weapons
            if item.item_type == ewcfg.it_weapon:
                if user_data.weapon == item.id_item:
                    if user_data.weaponmarried:
                        response = "If only it were that easy. But you can't just shove your lover in a {}.".format()
                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                    user_data.weapon = -1
                    user_data.persist()
                elif user_data.sidearm == item.id_item:
                    user_data.sidearm = -1
                    user_data.persist()
            # Dedorn cosmetics
            elif item.item_type == ewcfg.it_cosmetic:
                item.item_props["adorned"] = 'false'
                item.item_props["slimeoid"] = 'false'
                item.persist()

            response = "You drop the {} into the {}.".format(item_sought_item.get('name'), item_sought_col.get('name'))
            bknd_item.give_item(id_user="{}collection".format(collection.id_item), id_server=item.id_server, id_item=item.id_item)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def remove_from_collection(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)
    price = 100000
    extract_all = False

    if user_data.poi != ewcfg.poi_id_bazaar:
        response = "You don't actually know how to get stuff out of this. Better find a specialist in the Bazaar."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif cmd.tokens_count != 3:
        response = "You need to specify the item and the collection. Try \"!extract <collection> <item>\"."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    collection_seek = ewutils.flattenTokenListToString(cmd.tokens[1])
    item_sought_col = bknd_item.find_item(item_search=collection_seek, id_user=user_data.id_user, id_server=user_data.id_server)
    if not item_sought_col:
        response = "That's not a real collection. Remember, it's \"!extract <collection> <item>\"."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_seek = cmd.tokens[2]
    item_sought_item = bknd_item.find_item(item_search=item_seek, id_user='{}collection'.format(item_sought_col.get('id_item')), id_server=user_data.id_server)

    if not item_sought_item:
        response = "Wait, that's not in this collection. That's not even a real thing."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    furnlist = static_items.furniture_map
    collection = EwItem(id_item=item_sought_col.get('id_item'))
    collectiontype = collection.item_props.get('id_furniture')
    item = EwItem(id_item=item_sought_item.get('id_item'))
    collection_list = furnlist.get(collection.item_props.get('id_furniture'))

    if collectiontype == "portablegreenhouse":
        price = 1000

    if collection_list is None or collection_list.furn_set != 'collection':
        response = "Trying to pull shit out of random objects? Yeah, I did meth once too."
    elif 'collection' != item.id_owner[-10:]:
        response = "That's not in your collection. Can't remove what isn't there."
    elif user_data.slimes < int(price):
        response = "These fucking prices... The removal fee is {price} slime.".format(price = price)
    else:
        bknd_item.give_item(id_user=user_data.id_user, id_server=int(item.id_server), id_item=item_sought_item.get('id_item'))
        user_data.change_slimes(n=-price, source=ewcfg.source_spending)
        user_data.persist()
        response = "You somehow find a specialist in the smoky kiosks that can get your precious belongings out of the {} you forced them into. You hand over {:,} slime, and he walks into the tent behind his stall. \n\nBefore you can figure you what it is he's doing, {}. Eventually, you find your way back to the stall. The specialist hands you the item and collection, fully separated. Maybe someday you'll figure out how to do it...".format(item_sought_col.get('name'), price, random.choice(comm_cfg.bazaar_distractions))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def rename_collection(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    # Requires at least 3 tokens
    if cmd.tokens_count < 3:
        response = "You need to specify a collection to rename and the name you wish to ascribe to it."
    else:
        item_sought = cmd.tokens[1]
        collection_sought = bknd_item.find_item(item_search=item_sought, id_user=user_data.id_user, id_server=user_data.id_server)

        if collection_sought is None and poi.is_apartment and user_data.visiting == "empty":
            collection_sought = bknd_item.find_item(item_search=item_sought, id_user="{}decorate".format(user_data.id_user), id_server=user_data.id_server)

        if not collection_sought:
            response = "You don't have that collection in your inventory."
        else:
            # Get the collection name, max 32 characters
            collection_name_draft = ' '.join(word for word in cmd.tokens[2:])
            if len(collection_name_draft) > 32:
                collection_name_draft = collection_name_draft[:32]

            collection = EwItem(id_item=collection_sought.get('id_item'))

            collection.item_props['furniture_name'] = collection_name_draft
            collection.persist()

            response = "You write on the collection with a stray marker. It is now known as a \"{}\"!".format(collection_name_draft)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def bury(cmd):
    user_data = EwUser(member = cmd.message.author)
    if user_data.weapon >= 0:
        weapon_item = EwItem(id_item=user_data.weapon)
        # Make sure user is carrying a shovel
        if weapon_item.template != 'shovel':
            response = "You'll need a shovel to bury shit."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        elif cmd.tokens_count <= 2:
            response = "That's not going to work. Try !bury <coordinates> <item>"
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        coords = cmd.tokens[1]
        coords = coords.replace(':', '')
        if '-' in coords:
            response = "The coordinates have a hyphen in them. It'll go into the ground all lopsided."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
     # Look for item to bury

        item_seek = ewutils.flattenTokenListToString(cmd.tokens[2:])
        item_sought = bknd_item.find_item(item_search=item_seek, id_user=cmd.message.author.id, id_server=cmd.guild.id)
        if item_sought:
            if item_sought.get('soulbound'):
                response = "You can't bury that. It's bound to your essence, stupid."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            # Format the string that'll be used as the id_user for the item.
            ground_recipient = "{}-{}-{}".format('bury', user_data.poi, coords.lower())

            # Set the item's id_user to the formatted string
            bknd_item.give_item(id_item=item_sought.get('id_item'), id_server=cmd.guild.id, id_user=ground_recipient)
            response = "You bury the {} at coordinates {}.".format(item_sought.get('name'), coords.upper())
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response), delete_after=10)
        else:
            response = "You don't have that."
    else:
        response = "You're not even carrying a stick, let alone a shovel."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def unearth(cmd):
    user_data = EwUser(member = cmd.message.author)

    # Flatten coords to an undercase string with no spaces or punctuation
    coords = ewutils.flattenTokenListToString(cmd.tokens[1:]).lower()
    coords = coords.replace(':', '')
    if '-' in coords:
        response = "No hyphens, buddy. Don't be so negative."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    lookup = 'bury-{}-{}'.format(user_data.poi, coords)

    # Check if there's any items with the id_user of formatted string
    burial_finding = bknd_item.inventory(id_user=lookup, id_server=cmd.guild.id)
    if len(burial_finding) == 0:
        response = "There's nothing in there."
    else:
        # If there are any items with the id_user of formatted string, and the user has space, give them one.
        item = burial_finding[0]
        if not bknd_item.check_inv_capacity(user_data, item.get('item_type')):
            response = "There's something down there, but you don't have room for it."
        else:
            response = "You unearthed a {}!".format(item.get('name'))
            bknd_item.give_item(member=cmd.message.author, id_item=item.get('id_item'))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def huff(cmd):
    user_data = EwUser(member = cmd.message.author)
    status = user_data.getStatusEffects()
    item_sought = bknd_item.find_item(item_search=ewcfg.weapon_id_thinnerbomb, id_user=cmd.message.author.id, id_server=cmd.guild.id, item_type_filter=ewcfg.it_weapon) or bknd_item.find_item(item_search=ewcfg.weapon_id_spraycan, id_user=cmd.message.author.id, id_server=cmd.guild.id, item_type_filter=ewcfg.it_weapon)

    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))


        if ewcfg.status_thinned_id in status or ewcfg.status_huffed_id in status:
            response = "Don't OD now, bro. You're fucked out as it is."
        elif not item_sought:

            response = "You don't have any paint thinner or spraycans."
        elif item.template != ewcfg.weapon_id_thinnerbomb and item.template != ewcfg.weapon_id_spraycan:
            response = "Nice try, dumpass. Them's fake drugs."
        else:
            if item.template == ewcfg.weapon_id_spraycan:
                response = "Time to see some stars. You unload the entire aerosol can of spraypaint on your teeth. The can now useless as you stumple around, but suddenly the world looks so vivid."
                bknd_item.item_delete(id_item=item.id_item)
                user_data.applyStatus(id_status=ewcfg.status_huffed_id)
            else:
                response = "Time to see some stars. You take a huge whiff out of one of your thinnerbombs. It breaks as you stumble around, but suddenly the world looks so vivid."
                bknd_item.item_delete(id_item=item.id_item)
                user_data.applyStatus(id_status=ewcfg.status_thinned_id)
            
            
    else:
        response = "You can't get high on your own farts, at least not yet. Get a thinnerbomb or spraycan and we'll talk."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


