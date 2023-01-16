import asyncio
from ew.static import npc as static_npc
from ew.utils import frontend as fe_utils
import random
from ew.static import poi as poi_static
from ew.static import cfg as ewcfg
from ew.static import items as static_items
from ew.static import food as static_food
from ew.static import cosmetics as static_cosmetics
from ew.static import weapons as static_weapons

import ew.backend.core as bknd_core
from ew.backend.item import EwItem
import ew.utils.combat as ewcombat
import ew.utils.hunting as ewhunting
import ew.backend.item as bknd_item
from ew.backend.dungeons import EwGamestate
from ew.backend.player import EwPlayer
from ew.backend import hunting as bknd_hunting
import time
import ew.utils.combat as util_combat
from ew.backend.status import EwEnemyStatusEffect
import ew.utils.core as ewutils
import ew.utils.item as itm_utils

#from ew.utils.combat import EwEnemy
#move: enemy move action
#talk: action on a !talk
#act: action every 3 seconds
#die: action when the enemy dies
#hit: action when the enemy gets hit

async def generic_npc_action(keyword = '', enemy = None, channel = None, npc_obj = None, item = None, user_data = None):
    if npc_obj is None:
        npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'move':
        return await generic_move(enemy=enemy, npc_obj=npc_obj)
    elif keyword == 'act':
        return await generic_act(channel=channel, npc_obj=npc_obj, enemy=enemy)
    elif keyword == 'talk':
        return await generic_talk(channel=channel, npc_obj=npc_obj, enemy = enemy, user_data=user_data)
    elif keyword == 'hit':
        return await generic_hit(npc_obj=npc_obj, channel=channel, enemy=enemy)
    elif keyword == 'die':
        drop_held_items(enemy=enemy)
        await fe_utils.send_message(None, channel, "{} is dead!".format(npc_obj.str_name))
        return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='die', enemy = enemy, user_data=user_data)
    elif keyword == 'give':
        return await generic_give(channel=channel, npc_obj=npc_obj, enemy=enemy, item=item)

async def chatty_npc_action(keyword = '', enemy = None, channel = None, item = None, user_data = None): #similar to the generic npc, but with loopable dialogue
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'act':
        if random.randint(1, 20) == 2:
            return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='loop', enemy = enemy, user_data=user_data)
    elif keyword == 'talk':
        return await generic_talk(channel=channel, npc_obj=npc_obj, enemy = enemy, user_data=user_data)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)

async def police_npc_action(keyword = '', enemy = None, channel = None, item = None, user_data = None): #similar to the generic npc, but with loopable dialogue
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'act':
        return await conditional_act(channel=channel, npc_obj=npc_obj, enemy=enemy)
    elif keyword == 'die':
        return await police_die(channel=channel, npc_obj=npc_obj, keyword_override='die', enemy = enemy)
    elif keyword == 'move':
        return await generic_move(enemy=enemy, npc_obj=npc_obj, move_override=30)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)

async def police_chief_npc_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)
    #run the police set of actions, except for on death
    if keyword == 'die':
        return await chief_die(channel=channel, npc_obj=npc_obj, keyword_override='die', enemy = enemy)
    else:
        return await police_npc_action(keyword = keyword, enemy = enemy, channel = channel, item=item)


async def condition_hostile_action (keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'act':
        return await conditional_act(channel=channel, npc_obj=npc_obj, enemy=enemy)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)


async def juvieman_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)
    if keyword == 'act':
        return await conditional_act(channel=channel, npc_obj=npc_obj, enemy=enemy)
    elif keyword == 'die':
        return await juvieman_die(channel=channel, npc_obj=npc_obj, enemy=enemy)
    elif keyword == 'hit':
        return await generic_talk(channel=channel, npc_obj=npc_obj, enemy = enemy, keyword_override='hit', user_data=user_data)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)


async def marty_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'give':
        return await marty_give(channel = channel, npc_obj = npc_obj, enemy = enemy, item = item)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)

async def candidate_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)

    if keyword == 'give':
        return await candidate_give(channel = channel, npc_obj = npc_obj, enemy = enemy, item = item)
    elif keyword == 'die':
        return await candidate_die(channel=channel, npc_obj=npc_obj, enemy=enemy, item=item)
    else:
        return await chatty_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)


async def mozz_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)
    if keyword == 'give':
        return await mozz_give(enemy=enemy, channel=channel, item=item, npc_obj=npc_obj)
    elif keyword == 'move':
        return await mozz_move(npc_obj=npc_obj, channel=channel, enemy=enemy)
    elif keyword == 'talk':
        return await attack_talk(npc_obj=npc_obj, channel=channel, enemy=enemy)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)


async def slox_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)
    if keyword == 'die':
        return await warpath_die(channel=channel, npc_obj=npc_obj, enemy=enemy)
    elif keyword == 'give':
        return await feeder_give(enemy=enemy, channel=channel, item=item, npc_obj=npc_obj)
    elif keyword == 'move':
        pass
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)

async def dojomaster_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)
    if keyword == 'hit':
        return await dojomaster_hit(npc_obj=npc_obj, channel=channel, enemy=enemy, user_data = user_data)
    if keyword == 'act':
        await generic_act(channel=channel, npc_obj=npc_obj, enemy=enemy) #this fucker's the fastest in the west, i mean east
        await asyncio.sleep(1)
        await generic_act(channel=channel, npc_obj=npc_obj, enemy=enemy)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)

async def needy_npc_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    npc_obj = static_npc.active_npcs_map.get(enemy.enemyclass)
    if keyword == 'talk':
        return await needy_talk(channel=channel, npc_obj=npc_obj, keyword_override='loop', enemy = enemy, user_data=user_data)
    elif keyword == 'move':
        return await needy_move(enemy=enemy, npc_obj=npc_obj)
    elif keyword == 'act':
        return await needy_act(channel=channel, npc_obj=npc_obj, enemy=enemy)
    elif keyword == 'give':
        return await needy_give(channel=channel, npc_obj=npc_obj, enemy=enemy, item=item)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)


async def drinkster_npc_action(keyword = '', enemy = None, channel = None, item = None, user_data = None):
    drink = find_drink(id_server=enemy.id_server, user_data=user_data, item=item)

    if drink is not None and keyword in ['talk', 'give']:
        return await crush_drink(channel=channel, id_item=drink)
    else:
        return await generic_npc_action(keyword=keyword, enemy=enemy, channel=channel, item=item)

#top level functions here
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#specific reaction functions here




async def generic_talk(channel, npc_obj, keyword_override = 'talk', enemy = None, user_data = None): #sends npc dialogue, including context specific and rare variants
    delete_after = None
    if 'loop' in keyword_override:
        delete_after = 30
    if ewutils.is_district_empty(poi=enemy.poi):
        return

    rare_keyword = "rare{}".format(keyword_override)
    location_keyword = '{}{}'.format(enemy.poi, keyword_override)

    player = None if user_data is None else EwPlayer(id_user=user_data.id_user)

    if rare_keyword in npc_obj.dialogue.keys() and random.randint(1, 20) == 2:
        keyword_override = rare_keyword #rare dialogue has a 1 in 20 chance of firing

    potential_dialogue = npc_obj.dialogue.get(keyword_override)

    if location_keyword in npc_obj.dialogue.keys() and 'rare' not in keyword_override:
        potential_dialogue += npc_obj.dialogue.get(location_keyword)

    if potential_dialogue is not None:
        response = random.choice(potential_dialogue).format(player_name= "" if player is None else player.display_name)
    else:
        response = None


    if response is not None:
        if response[:2] == '()':  # for exposition that doesn't use a talk bubble
            response = response[2:]
            return await fe_utils.send_message(None, channel, response)

        name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
        return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel, delete_after=delete_after)




async def generic_move(enemy = None, npc_obj = None, move_override = 120): #moves within boundaries every 20 seconds or so
    if enemy.life_state == ewcfg.enemy_lifestate_alive:
        if random.randrange(move_override) == 0:
            resp_cont = enemy.move()
            if resp_cont != None:
                if len(resp_cont.channel_responses) > 0:
                    channel = list(resp_cont.channel_responses.keys())[0]
                    await resp_cont.post(delete_after=120)
                    if npc_obj.dialogue.get('enter') is not None:
                        return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='enter')
                    elif npc_obj.dialogue.get('loop') is not None:
                        return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='loop')


async def generic_act(channel, npc_obj, enemy): #attacks when hostile. otherwise, if act or talk dialogue is available, the NPC will use it every so often.
    enemy_statuses = enemy.getStatusEffects()
    poi = poi_static.id_to_poi.get(enemy.poi)

    if ewcfg.status_enemy_hostile_id in enemy_statuses and poi.pvp:
        if any([ewcfg.status_evasive_id, ewcfg.status_aiming_id]) not in enemy_statuses and random.randrange(10) == 0:
            resp_cont = random.choice([enemy.dodge, enemy.taunt, enemy.aim])()
        else:
            resp_cont = await enemy.kill()

        if resp_cont is not None:
            await resp_cont.post()

    elif random.randrange(35) == 0 and not ewutils.is_district_empty(poi=enemy.poi):
        if npc_obj.dialogue.get('loop') is not None:
            return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='loop')
        elif npc_obj.dialogue.get('talk') is not None:
            return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='talk')




async def generic_hit(channel, npc_obj, enemy, territorial = True, probability = 1): #territorial enemy that attacks when you do. if a line is prepared for it, talkbubble that line
    if ewcfg.status_enemy_hostile_id not in enemy.getStatusEffects() and territorial:
        enemy.applyStatus(id_status=ewcfg.status_enemy_hostile_id)
        await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='hit', enemy=enemy)
    else:
        if random.randint(1, probability) == 1:
            await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='hit', enemy=enemy)



async def generic_give(channel, npc_obj, enemy, item):

    if item.get('item_type') == ewcfg.it_cosmetic:
        item_data = EwItem(id_item=item.get('id_item'))
        item_data.item_props["adorned"] = 'false'
        item_data.persist()
    bknd_item.give_item(id_item=item.get('id_item'), id_user="npcinv{}".format(enemy.enemyclass), id_server=enemy.id_server)

    response = "?"
    if npc_obj.dialogue.get('give') is not None:
        return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='give', enemy=enemy)

    name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
    return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel)



async def conditional_act(channel, npc_obj, enemy): #attacks when hostile. otherwise, if act or talk dialogue is available, the NPC will use it every so often.
    enemy_statuses = enemy.getStatusEffects()

    if random.randrange(25) == 0 and not ewutils.is_district_empty(poi=enemy.poi): #one in 25 chance to talk in addition to attacking. attacks are based on a condition
        if npc_obj.dialogue.get('loop') is not None:
            return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='loop', enemy=enemy)
        elif npc_obj.dialogue.get('talk') is not None:
            return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='talk', enemy=enemy)
        else:
            response = "..."
            name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
            return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel, delete_after=30)

    poi = poi_static.id_to_poi.get(enemy.poi)
    resp_cont = None
    if poi.pvp:
        resp_cont = await enemy.kill(condition = npc_obj.condition)

    if resp_cont is not None:
        await resp_cont.post()

async def police_die(channel, npc_obj, keyword_override = 'die', enemy = None):
    potential_dialogue = npc_obj.dialogue.get(keyword_override)
    drop_held_items(enemy=enemy)
    response = random.choice(potential_dialogue)
    await fe_utils.send_message(None, channel, response)
    name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
    await fe_utils.send_message(None, channel, "{} is dead!".format(npc_obj.str_name))
    if response is not None:
        await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel)


    timewait = random.randint(15, 45)
    await asyncio.sleep(timewait)

    numcops = random.randint(2, 7)

    for x in range(numcops):
        ewhunting.spawn_enemy(id_server=enemy.id_server, pre_chosen_type='policeofficer', pre_chosen_poi=enemy.poi)

    response = "Oh shit, cop car! There's {} of those bitches in there!".format(numcops)
    return await fe_utils.send_message(None, channel, response)


async def chief_die(channel, npc_obj, keyword_override = 'die', enemy = None):
    potential_dialogue = npc_obj.dialogue.get(keyword_override)
    drop_held_items(enemy=enemy)
    response = random.choice(potential_dialogue)
    name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
    await fe_utils.send_message(None, channel, "{} is dead!".format(npc_obj.str_name))
    if response is not None:
        await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel)


    await asyncio.sleep(10)

    numcops = random.randint(2, 7)

    ewhunting.spawn_enemy(id_server=enemy.id_server, pre_chosen_type='npc', pre_chosen_poi=enemy.poi, pre_chosen_npc='riot')
    ewhunting.spawn_enemy(id_server=enemy.id_server, pre_chosen_type='npc', pre_chosen_poi=enemy.poi, pre_chosen_npc='sleuth')
    ewhunting.spawn_enemy(id_server=enemy.id_server, pre_chosen_type='npc', pre_chosen_poi=enemy.poi, pre_chosen_npc='pork')
    for x in range(numcops):
        ewhunting.spawn_enemy(id_server=enemy.id_server, pre_chosen_type='policeofficer', pre_chosen_poi=enemy.poi)

    results = bknd_core.execute_sql_query("select id_enemy from enemies where life_state = 1 and enemyclass in('riot', 'pork', 'sleuth')")

    for result in results:
        backup_obj = ewcombat.EwEnemy(id_enemy=result, id_server=enemy.id_server)
        backup_obj.applyStatus(id_status=ewcfg.status_enemy_hostile_id)

    response = "Oh shit, cop car! There's {} of those bitches in there!\n\nWait...Oh no...".format(numcops + 3)
    await fe_utils.send_message(None, channel, response)



def drop_held_items(enemy):
    owner_id = "npcinv{}".format(enemy.enemyclass)
    items_list = bknd_item.inventory(id_server=enemy.id_server, id_user=owner_id)

    items_to_drop = []

    for item in items_list:
        items_to_drop.append(item.get('id_item'))
    if len(items_to_drop) > 0:
        bknd_item.give_item_multi(id_list=items_to_drop, destination=enemy.poi)


async def juvieman_die(channel, npc_obj, enemy = None):
    drop_held_items(enemy=enemy)
    new_poi = random.choice(poi_static.capturable_districts)
    ewhunting.spawn_enemy(id_server=enemy.id_server, pre_chosen_type='npc', pre_chosen_poi=new_poi, pre_chosen_npc='juvieman')
    return await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='die', enemy=enemy)

async def marty_give(channel, npc_obj, enemy, item):
    gamestate_items = EwGamestate(id_server=enemy.id_server, id_state='martyitems')

    gamestate_project = EwGamestate(id_server=enemy.id_server, id_state='constructionprogress')

    currentitemnumber = gamestate_items.number
    items_list = gamestate_items.value.split()

    item_obj = EwItem(id_item=item.get('id_item'))

    if gamestate_project.number >= int(gamestate_project.value):
        response = "*You're too late.* You didn't make it. We have these materials already!"
    elif item_obj.id_item < currentitemnumber and item_obj.template in items_list:
        response = "Just what I needed!"
        gamestate_project.number += 1
        gamestate_project.persist()
        bknd_item.item_delete(item_obj.id_item)

        if gamestate_project.number >= int(gamestate_project.value):
            response += " Oh boy! We've got the materials for this project now! Time to get to work!"
        else:
            response += " Thanks for the donation!"
    elif item_obj.id_item >= currentitemnumber:
        response = "That item's too *old* to let us build here, stupid! The government wants us to use recycled materials because they're *grandstanding commie bastards!*"
    else:
        response = "Thanks, but we don't need this item right now. Worthless. Disposable. *Worthless.*"

    if response is not None:
        await fe_utils.talk_bubble(response=response, name='**__MARTY__**', image=npc_obj.image_profile, channel=channel)


async def candidate_give(channel, npc_obj, enemy, item):
    statename = npc_obj.id_npc + "morale"
    gamestate = EwGamestate(id_state=statename, id_server=enemy.id_server)
    gamestate.number += 10
    gamestate.persist()


    item_obj = EwItem(id_item=item.get('id_item'))
    usermodel = util_combat.EwUser(id_user=item_obj.id_owner, id_server=enemy.id_server)

    if item_obj.soulbound or item_obj.item_type == ewcfg.it_weapon and usermodel.weapon >= 0 and item_obj.id_item == usermodel.weapon:
        response = "You can't do that. Isn't that important?"
        return await fe_utils.send_message(None, channel, response)
    if item_obj.item_type in([ewcfg.it_questitem, item_obj.item_type == ewcfg.it_medal, ewcfg.it_relic])  or item_obj.item_props.get('rarity') == ewcfg.rarity_princeps or item_obj.item_props.get('id_cosmetic') == "soul" or item_obj.item_props.get('id_furniture') == "propstand" or item_obj.item_props.get('id_furniture') in static_items.furniture_collection or item_obj.item_props.get('acquisition') == 'relic':
        if item.get('item_type') == ewcfg.it_cosmetic:
            item_data = EwItem(id_item=item.get('id_item'))
            item_data.item_props["adorned"] = 'false'
            item_data.persist()
        bknd_item.give_item(id_item=item.get('id_item'), id_user="npcinv{}".format(enemy.enemyclass), id_server=enemy.id_server)
    else:
        bknd_item.item_delete(item.get('id_item'))
    response = "!!"
    if npc_obj.dialogue.get('give') is not None:
        response = random.choice(npc_obj.dialogue.get('give'))

    name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
    return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel)

async def candidate_die(channel, npc_obj, enemy, item):
    statename = npc_obj.id_npc + "morale"
    gamestate = EwGamestate(id_state=statename, id_server=enemy.id_server)
    gamestate.number -= 100
    gamestate.persist()
    drop_held_items(enemy=enemy)
    response = "!!"

    if npc_obj.dialogue.get('die') is not None:
        response = random.choice(npc_obj.dialogue.get('die'))
    await fe_utils.send_message(None, channel, "{} is dead!".format(npc_obj.str_name))
    name = "{}{}{}".format('**__', npc_obj.str_name.upper(), '__**')
    return await fe_utils.talk_bubble(response=response, name=name, image=npc_obj.image_profile, channel=channel)


async def attack_talk(channel, npc_obj, enemy, territorial = True): #territorial enemy that attacks when you do. if a line is prepared for it, talkbubble that line
    if ewcfg.status_enemy_hostile_id not in enemy.getStatusEffects() and territorial:
        enemy.applyStatus(id_status=ewcfg.status_enemy_hostile_id)

    await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='talk', enemy=enemy)


async def mozz_give(channel, npc_obj, enemy, item):
    item_data = EwItem(id_item=item.get('id_item'))
    item_has_expired = float(getattr(item_data, "time_expir", 0)) < time.time()
    if item_data.item_type == ewcfg.it_food and item_has_expired:
        resp_cont = enemy.move()
        await resp_cont.post()
        if ewcfg.status_enemy_hostile_id in enemy.getStatusEffects():
            enemy.clear_status(id_status=ewcfg.status_enemy_hostile_id)
        bknd_item.item_delete(item.get('id_item'))
        if random.randrange(5) == 0:
            enemy.level += 1
        enemy.persist()
        await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='give', enemy=enemy)

    else:
        await attack_talk(channel, npc_obj, enemy, territorial = True)

async def mozz_move(channel, npc_obj, enemy):
    if random.randrange(30) == 0 or ewutils.DEBUG_OPTIONS.get('alternate_talk') == True:
        resp_cont = enemy.move()
        await resp_cont.post()
        if resp_cont != None:
            channel = list(resp_cont.channel_responses.keys())[0]
            enemy = util_combat.EwEnemy(id_server=enemy.id_server, id_enemy=enemy.id_enemy)
            items_in_poi = bknd_item.inventory(id_user=enemy.poi if not ewutils.DEBUG else ewcfg.poi_id_southsleezeborough, id_server=enemy.id_server,  item_sorting_method='id', item_type_filter=ewcfg.it_food)
            max_food_items = 15
            for item_thing in items_in_poi:
                item = EwItem(id_item = item_thing.get('id_item'))
                item_has_expired = float(getattr(item, "time_expir", 0)) < time.time()
                if item_has_expired:
                    max_food_items -= 1
                    bknd_item.item_delete(item_thing.get('id_item'))

                    if random.randrange(5) == 0:
                        enemy.level += 1
                    if max_food_items <= 0:
                        break
            enemy.persist()
            if npc_obj.dialogue.get('enter') is not None:
                return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='enter')
            elif npc_obj.dialogue.get('loop') is not None:
                return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='loop')


async def warpath_die(channel, npc_obj, enemy):

    enemydata = bknd_core.execute_sql_query(
        "SELECT {id_enemy} FROM enemies WHERE {display_name} = %s AND {life_state} = 1 AND {id_server} = %s".format(
            id_enemy=ewcfg.col_id_enemy,
            display_name=ewcfg.col_enemy_class,
            life_state=ewcfg.col_enemy_life_state,
            id_server=ewcfg.col_id_server
        ), (
            enemy.enemyclass,
            enemy.id_server
        ))

    for enemy_id in enemydata:
        sim_enemy = util_combat.EwEnemy(id_server=enemy.id_server, id_enemy=enemy_id[0])
        if enemy.life_state == ewcfg.enemy_lifestate_alive:
            sim_enemy.applyStatus(id_status=ewcfg.status_enemy_hostile_id)
            sim_enemy.level += 50
            sim_enemy.slimes += 5000000
            sim_enemy.persist()
    await fe_utils.send_message(None, channel, "{} is dead!".format(npc_obj.str_name))
    await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='hit')


async def feeder_give(channel, npc_obj, enemy, item, willEatExpired = False):
    item_data = EwItem(id_item=item.get('id_item'))
    item_has_expired = float(getattr(item_data, "time_expir", 0)) < time.time()
    if item_data.item_type == ewcfg.it_food and (willEatExpired or not item_has_expired):
        await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='give')
        bknd_item.item_delete(item.get('id_item'))
    else:
        response = "{} turns their nose at your offer."
        return await fe_utils.send_message(None, channel, response)


async def dojomaster_hit(channel, npc_obj, enemy, territorial = True, probability = 3, user_data = None):
    if ewcfg.status_enemy_hostile_id not in enemy.getStatusEffects() and territorial:
        enemy.applyStatus(id_status=ewcfg.status_enemy_hostile_id)
        await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='hit', enemy=enemy)
    else:
        if random.randint(1, probability) == 1:
            await generic_talk(channel=channel, npc_obj=npc_obj, keyword_override='hit', enemy=enemy)

    if user_data.weapon != -1:
        user_data = ewcombat.EwUser(id_user=user_data.id_user, id_server=user_data.id_server)
        weapon_item = EwItem(id_item=user_data.weapon)
        itemtype = weapon_item.template
        user_data.add_weaponskill(n=1, weapon_type = itemtype)
        user_data.persist()

async def needy_talk(channel, npc_obj, keyword_override = 'talk', enemy = None, user_data = None):
    status = enemy.getStatusEffects() #talking to this NPC once triggers their undying affection
    if ewcfg.status_enemy_following_id in status:
        enemy.clear_status(id_status=ewcfg.status_enemy_hostile_id)
    enemy.applyStatus(id_status=ewcfg.status_enemy_following_id, id_target=user_data.id_user)

    return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='talk', user_data=user_data)

async def needy_act(channel, npc_obj, enemy, probability = 1):
    status = enemy.getStatusEffects() #if the follower has a target they'll pester them constantly
    if ewcfg.status_enemy_following_id in status:
        status_obj = EwEnemyStatusEffect(id_enemy=enemy.id_enemy, id_server=enemy.id_server, id_status=ewcfg.status_enemy_following_id)
        user_data = util_combat.EwUser(id_server=enemy.id_server, id_user=status_obj.id_target)
        if random.randint(1, probability) == 1 and user_data.poi == enemy.poi:
            return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='loop', user_data=user_data)

async def needy_give(channel, npc_obj, enemy, item):
    status = enemy.getStatusEffects()  # give me a horse, and I will be yours forever. -andrew hussie
    if ewcfg.status_enemy_following_id in status:
        enemy.clear_status(id_status=ewcfg.status_enemy_hostile_id)
    item_obj = EwItem(id_item=item.get('id_item'))
    enemy.applyStatus(id_status=ewcfg.status_enemy_following_id, id_target=item_obj.id_owner)

    return await generic_give(channel, npc_obj, enemy, item)

async def needy_move(enemy = None, npc_obj = None):
    if enemy.life_state == ewcfg.enemy_lifestate_alive:
        pre_chosen_poi = None
        move_probability = 120
        status = enemy.getStatusEffects()  # if the follower has a target they'll pester them constantly
        if ewcfg.status_enemy_following_id in status:
            status_obj = EwEnemyStatusEffect(enemy_data=enemy, id_status=ewcfg.status_enemy_following_id)
            user_data = util_combat.EwUser(id_server=enemy.id_server, id_user=status_obj.id_target)
            if user_data.poi not in[ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown, ewcfg.poi_id_juviesrow, ewcfg.poi_id_thesewers] and user_data.poi[:3] != 'apt' and user_data.poi != enemy.poi:
                pre_chosen_poi = user_data.poi
                move_probability = 1
            else:
                return

        if random.randint(1, move_probability) == 1:
            resp_cont = enemy.move(pre_chosen_poi=pre_chosen_poi)
            if resp_cont != None:
                channel = list(resp_cont.channel_responses.keys())[0]
                await resp_cont.post(delete_after=120)
                if npc_obj.dialogue.get('enter') is not None:
                    return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='enter')
                elif npc_obj.dialogue.get('loop') is not None:
                    return await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='loop')


def find_drinkster(user_data, isDrink):
    enemydata = bknd_core.execute_sql_query(
        "SELECT {id_enemy}, {poi} FROM enemies WHERE {enemyclass} = %s AND {life_state} = 1 AND {id_server} = %s".format(
            id_enemy=ewcfg.col_id_enemy,
            poi=ewcfg.col_poi,
            enemyclass=ewcfg.col_enemy_class,
            life_state=ewcfg.col_enemy_life_state,
            id_server=ewcfg.col_id_server
        ), (
            'thedrinkster',
            user_data.id_server
        ))
    for enemy in enemydata:
        poi = poi_static.id_to_poi.get(enemy[1])
        if user_data.poi in poi.neighbors.keys():
            enemy_obj = ewcombat.EwEnemy(id_enemy=enemy[0], id_server=user_data.id_server)
            if isDrink and user_data.poi not in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown, ewcfg.poi_id_juviesrow, ewcfg.poi_id_thesewers]:
                enemy_obj.poi = user_data.poi
                enemy.persist()
                return True
        elif isDrink and user_data.poi == poi.id_poi:
            return True
    return False

def find_drink(id_server, user_data = None, item = None):
    if item is not None:
        item_obj = EwItem(id_item=item.get('id_item'))
        if item_obj.template in static_food.drinks:
            return item_obj.id_item
    elif user_data is not None:
        inv = bknd_item.inventory(id_user=user_data.id_user, id_server=id_server, item_type_filter=ewcfg.it_food)
        for itm in inv:
            item_obj = EwItem(id_item=itm.get('id_item'))
            if item_obj.template in static_food.drinks:
                return item_obj.id_item
    return None

async def crush_drink(channel = None, id_item = None):
    response = "https://rfck.app/npc/drinksterdance.gif\nThe Drinkster went and crushed your drink! Damn it, that guy just won't leave you alone..."
    bknd_item.item_delete(id_item)
    return await fe_utils.send_message(None, channel, response)


async def trade_give(channel, npc_obj, enemy, item): #thus far is an unused npc trade system
    if item is not None:
        item_obj = EwItem(id_item=item.get('id_item'))
        id_user = item_obj.id_owner
        dialogue = npc_obj.dialogue
        direct = dialogue.get('trade' + item_obj.template)
        if direct == None:
            direct = dialogue.get('trade' + item_obj.item_type)
            if direct == None:
                direct = dialogue.get('traderandom')

        if direct is not None:
            item_received = random.choice(direct)
            if item_received != 'nothing':
                item = static_items.item_map.get(item_received)

                item_type = ewcfg.it_item
                if item != None:
                    item_id = item.id_item
                    name = item.str_name

                # Finds the item if it's an EwFood item.
                if item == None:
                    item = static_food.food_map.get(item_received)
                    item_type = ewcfg.it_food
                    if item != None:
                        item_id = item.id_food
                        name = item.str_name

                # Finds the item if it's an EwCosmeticItem.
                if item == None:
                    item = static_cosmetics.cosmetic_map.get(item_received)
                    item_type = ewcfg.it_cosmetic
                    if item != None:
                        item_id = item.id_cosmetic
                        name = item.str_name

                if item == None:
                    item = static_items.furniture_map.get(item_received)
                    item_type = ewcfg.it_furniture
                    if item != None:
                        item_id = item.id_furniture
                        name = item.str_name
                        if item_id in static_items.furniture_pony:
                            item.vendors = [ewcfg.vendor_bazaar]

                if item == None:
                    item = static_weapons.weapon_map.get(item_received)
                    item_type = ewcfg.it_weapon
                    if item != None:
                        item_id = item.id_weapon
                        name = item.str_weapon

                item_props = itm_utils.gen_item_props(item)

                bknd_item.item_create(
                    item_type=item_type,
                    id_user=id_user,
                    id_server=item_obj.id_server,
                    item_props=item_props
                )

        bknd_item.item_delete(item_obj.id_item)
        await generic_talk(channel=channel, npc_obj=npc_obj, enemy=enemy, keyword_override='give')
