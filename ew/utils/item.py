import collections
import random
import time
import traceback
import sys

from . import core as ewutils
from . import frontend as fe_utils
from . import stats as ewstats
from ..backend import core as bknd_core
from ..backend import item as bknd_item
try:
    from ew.utils import rutils as relic_utils
except:
    from ew.utils import rutils_dummy as relic_utils
from ..backend.item import EwItem
from ..backend.player import EwPlayer
from ..backend.user import EwUserBase as EwUser
from ..static import cfg as ewcfg
from ..static import community_cfg as comm_cfg
from ..static import hue as hue_static
from ..static import items as static_items
from ..static import weapons as static_weapons
from ..static import poi as static_poi
try:
    from ..static.rstatic import relic_list
    from ..static.rstatic import dontfilter_relics
except:
    from ..static.rstatic_dummy import relic_list
    from ..static.rstatic_dummy import dontfilter_relics


def item_dropsome(id_server=None, id_user=None, item_type_filter=None, fraction=None, rigor=False, ambidextrous=False) -> list:
    """ Return a list of some of a user's non-exempt items to drop. """
    try:
        user_data = EwUser(id_server=id_server, id_user=id_user)
        items = bknd_item.inventory(id_user=id_user, id_server=id_server, item_type_filter=item_type_filter)
        mastery = ewutils.weaponskills_get(id_server=id_server, id_user=id_user)

        drop_candidates = []
        end_drops = []

        # Filter out Soulbound items.
        for item in items:
            item_props = item.get('item_props')
            if item_props.get('context') in ["corpse", "droppable"]:
                bknd_item.give_item(id_user=user_data.poi, id_server=id_server, id_item=item.get('id_item'))
            if not item.get('soulbound') and not (rigor and item_props.get('preserved') == user_data.id_user) and item_props.get('context') != 'gellphone' and item_props.get('id_item') != 'gameguide':
                drop_candidates.append(item)

        filtered_items = []

        if item_type_filter == ewcfg.it_item or item_type_filter == ewcfg.it_food:
            filtered_items = drop_candidates
        if item_type_filter == ewcfg.it_cosmetic:
            for item in drop_candidates:
                cosmetic_id = item.get('id_item')
                cosmetic_item = EwItem(id_item=cosmetic_id)
                if cosmetic_item.item_props.get('id_cosmetic') == "dogtag": # Dog Tags always drop on death
                    end_drops.append(item.get('id_item'))
                elif cosmetic_item.item_props.get('adorned') != "true" and cosmetic_item.item_props.get('slimeoid') != "true":
                    filtered_items.append(item)

        if item_type_filter == ewcfg.it_weapon:
            for item in drop_candidates:
                # Weapons with over 7 mastery are excluded for ambidextrous users
                if ambidextrous:
                    weapon = EwItem(id_item=item.get('id_item'))
                    weapon_type = weapon.item_props.get('weapon_type')
                    if weapon_type in mastery:
                        if int(mastery[weapon_type]) >= 7:
                            continue
                        
                if item.get('id_item') != user_data.weapon and item.get('id_item') != user_data.sidearm:
                    filtered_items.append(item)

        number_of_filtered_items = len(filtered_items)

        number_of_items_to_drop = int(number_of_filtered_items / fraction)

        if number_of_items_to_drop >= 2:
            random.shuffle(filtered_items)
            for drop in range(number_of_items_to_drop):
                for item in filtered_items:
                    id_item = item.get('id_item')
                    end_drops.append(id_item)
                    filtered_items.pop(0)
                    break
        return end_drops
    except Exception as e:
        ewutils.logMsg('Failed to drop some items for user with id {}: {}'.format(id_user, e))
        return []


def die_dropall(user_data, item_type, kill_method='') -> list:
    """ Return a list of all of a user's non-exempt items to drop. """
    end_list = []
    if item_type != '':
        type_filter = 'and item_type = \'{}\''.format(item_type)
    else:
        type_filter = ''

    try:
        if kill_method != ewcfg.cause_suicide and item_type == ewcfg.it_relic:
            item_cache = bknd_core.get_cache(obj_type="EwItem")
            if item_cache:
                search_criteria = {
                    'id_owner': user_data.id_user,
                    'id_server': user_data.id_server,
                    'soulbound': False
                }
                if item_type != '':
                    search_criteria.update({'item_type': item_type})
                result = item_cache.find_entries(criteria=search_criteria)
                result = list(map(lambda dat: [dat.get('id_item')], result))
            else:
                result = bknd_core.execute_sql_query(
                    "select id_item from items WHERE id_user = %s AND id_server = %s and soulbound = 0 {}".format(
                        type_filter), (
                        user_data.id_user,
                        user_data.id_server
                    ))
        else:
            item_cache = bknd_core.get_cache(obj_type="EwItem")
            if item_cache:
                search_criteria = {
                    'id_owner': user_data.id_user,
                    'id_server': user_data.id_server,
                    'soulbound': False,
                    'item_props': {'preserved': user_data.id_user}
                }
                if item_type != '':
                    search_criteria.update({'item_type': item_type})
                result = item_cache.find_entries(criteria=search_criteria)
                result = list(map(lambda dat: [dat.get('id_item')], result))
            else:
                result = bknd_core.execute_sql_query(  # this query excludes preserved items
                    "select it.id_item from items it left join items_prop ip on it.id_item = ip.id_item and ip.name = 'preserved' and ip.value = %s WHERE id_user = %s AND id_server = %s and soulbound = 0 and ip.name IS NULL {}".format(
                        type_filter), (
                        user_data.id_user,
                        user_data.poi,
                        user_data.id_user,
                        user_data.id_server
                    ))
        if result is not None:
            for id in result:
                end_list.append(id[0])
    except Exception as e:
        ewutils.logMsg('Failed to drop all items for user with id {}: {}'.format(user_data.id_user, e))
        return []
    return end_list


def get_cosmetic_abilities(id_user, id_server):
    active_abilities = []

    cosmetic_items = bknd_item.inventory(
        id_user=id_user,
        id_server=id_server,
        item_type_filter=ewcfg.it_cosmetic
    )

    for item in cosmetic_items:
        i = item.get('item_props')
        if i['adorned'] == "true" and i['ability'] is not None:
            active_abilities.append(i['ability'])
        else:
            pass

    return active_abilities


def get_outfit_info(id_user, id_server, wanted_info = None, slimeoid = False):
    cosmetic_items = bknd_item.inventory(
        id_user=id_user,
        id_server=id_server,
        item_type_filter=ewcfg.it_cosmetic

    )

    adorned_cosmetics = []
    adorned_ids = []

    adorned_styles = []
    dominant_style = None

    adorned_hues = []

    total_freshness = 0

    for cosmetic in cosmetic_items:
        item_props = cosmetic.get('item_props')

        if slimeoid == False:
            if item_props['adorned'] == 'true':
                adorned_styles.append(item_props.get('fashion_style'))

                hue = hue_static.hue_map.get(item_props.get('hue'))
                adorned_hues.append(item_props.get('hue'))

                if item_props['id_cosmetic'] not in adorned_ids:
                    total_freshness += int(item_props.get('freshness'))

                adorned_ids.append(item_props['id_cosmetic'])
                adorned_cosmetics.append((hue.str_name + " " if hue != None else "") + cosmetic.get('name'))
        else:
            if item_props.get('slimeoid') == 'true':
                adorned_styles.append(item_props.get('fashion_style'))

                hue = hue_static.hue_map.get(item_props.get('hue'))
                adorned_hues.append(item_props.get('hue'))

                if item_props['id_cosmetic'] not in adorned_ids:
                    total_freshness += int(item_props.get('freshness'))

                adorned_ids.append(item_props['id_cosmetic'])
                adorned_cosmetics.append((hue.str_name + " " if hue != None else "") + cosmetic.get('name'))

    if len(adorned_cosmetics) != 0:
        # Assess if there's a cohesive style
        if len(adorned_styles) != 0:
            counted_styles = collections.Counter(adorned_styles)

            dominant_style = max(counted_styles, key=counted_styles.get)

            relative_style_amount = round(int(counted_styles.get(dominant_style) / len(adorned_cosmetics) * 100))
            # If the outfit has a dominant style
            if relative_style_amount >= 60:

                total_freshness *= int(relative_style_amount / 10)  # If relative amount is 60 --> multiply by 6. 70 --> 7, 80 --> 8, etc. Rounds down, so 69 --> 6.

    if wanted_info is not None and wanted_info == "dominant_style" and dominant_style is not None:
        return dominant_style
    elif wanted_info is not None and wanted_info == "total_freshness":
        return total_freshness
    else:
        outfit_map = {
            'dominant_style': dominant_style,
            'total_freshness': total_freshness
        }
        return outfit_map


def get_style_freshness_rating(user_data, dominant_style = None):
    if dominant_style == None:
        dominant_style = "fresh"

    if user_data.freshness < ewcfg.freshnesslevel_1:
        response = "Your outfit is starting to look pretty fresh, but you’ve got a long way to go if you wanna be NLACakaNM’s next top model."
    else:
        if user_data.freshness < ewcfg.freshnesslevel_2:
            response = "Your outfit is low-key on point, not gonna lie. You’re goin’ places, kid."
        elif user_data.freshness < ewcfg.freshnesslevel_3:
            response = "Your outfit is lookin’ fresh as hell, goddamn! You shop so much you can probably speak Italian."
        elif user_data.freshness < ewcfg.freshnesslevel_4:
            response = "Your outfit is straight up **GOALS!** Like, honestly. I’m being, like, totally sincere right now. Your Instragrime has attracted a small following."
        else:
            response = "Holy shit! Your outfit is downright, positively, without a doubt, 100% **ON FLEEK!!** You’ve blown up on Instragrime, and you’ve got modeling gigs with fashion labels all across the city."

        if dominant_style == ewcfg.style_cool:
            if user_data.freshness < ewcfg.freshnesslevel_4:
                response += " You’re lookin’ wicked cool, dude. Like, straight up radical, man. For real, like, ta-haaa, seriously? Damn, bro. Sick."
            else:
                response += " Hey, kids, the world just got cooler. You’re the swingingest thing from coast-to-coast, and that ain’t no boast. You’re every slimegirl’s dream, you know what I mean? You’re where it’s at, and a far-out-happenin’ cat to boot. Man, it must hurt to be this hip."
        elif dominant_style == ewcfg.style_tough:
            if user_data.freshness < ewcfg.freshnesslevel_4:
                response += " You’re lookin’ tough as hell. Juveniles of all affiliations are starting to act nervous around you."
            else:
                response += " You’re just about the toughest-lookin' juveniledelinquent in the whole detention center. Ain’t nobody gonna pick a fight with you anymore, goddamn."
        elif dominant_style == ewcfg.style_smart:
            if user_data.freshness < ewcfg.freshnesslevel_4:
                response += " You’re starting to look like a real hipster, wearing all these smartypants garments. You love it, the people around you hate it."
            else:
                response += " You know extensive facts about bands that are so underground they’ve released their albums through long-since-expired Vocaroo links. You’re a leading hashtag warrior on various internet forums, and your opinions are well known by everyone who has spoken to you for more than five minutes. Everyone wants to knock your lights out, but… you’re just too fresh. "
        elif dominant_style == ewcfg.style_beautiful:
            if user_data.freshness < ewcfg.freshnesslevel_4:
                response += " You’re looking extremely handsome in all of those beautiful garments. If only this refined, elegant look reflected in your manners when cracking into a Arizonian Kingpin Crab."
            else:
                response += " You’re the belle of the ball at every ball you attend, which has never happened. But, if you *were* to ever attend one, your beautiful outfit would surely distinguish you from the crowd. Who knows, you might even find TRUE LOVE because of it and get MARRIED. That is, if you weren’t already married to slime."
        elif dominant_style == ewcfg.style_cute:
            if user_data.freshness < ewcfg.freshnesslevel_4:
                response += " Awwwhhh, look at you! You’re sooo cute~, oh my gosh. I could just eat you up, and then vomit you back up after I read back the previous line I’ve just written."
            else:
                response += " It is almost kowai how kawaii you are right now. Your legions of fans slobber all over each new post on Instragrime and leave very strange comments. You’re stopped for autographs in public now, and there hasn’t been a selfie taken with you that hasn’t featured a hover hand."
        elif dominant_style == ewcfg.style_evil:
            if user_data.freshness < ewcfg.freshnesslevel_4:
                response += " You're starting to make your relatives and friends worry about what you'll do next. Somewhere along the lines you've started to be led astray from society accepting your fashion norms. Is it a phase? That's an astounding HELL NO, hypothetical dad! You're evil and that's final!"
            else:
                response += " You've been barred from entry to most public schools, libraries, city hall, anywhere the city that the local NLACakaNM government can as a preventive measure to make sure you don't destroy it all, and all of your instagrime followers are edgy teenagers and actual goths who watch your every post for inspiration. Everyone else can't help but shudder and flinch while you walk past them on the streets. Your clothes is a mirror of your mental state, and you can't wait to make everyone shocked at your devious plans."
        elif dominant_style == ewcfg.style_skill:
            if user_data.freshness < ewcfg.freshnesslevel_4:
                response += " You're skilling the fashion game so hard, google searches of any kind struggle to not show your face."
            else:
                response += " You've solved fashion."
    return response


def gen_item_props(item):
    item_props = {}
    if not hasattr(item, "item_type"):
        return item_props
    if item.item_type == ewcfg.it_food and hasattr(item, 'id_fish'):
        item_props = {
            'id_food': item.id_fish,
            'food_name': item.str_name,
            'food_desc': item.str_desc,
            'recover_hunger': 20,
            'str_eat': ewcfg.str_eat_raw_material.format(item.str_name),
            'rarity': item.rarity,
            'size': ewcfg.fish_size_average,
            'time_expir': time.time() + ewcfg.std_food_expir,
            'time_fridged': 0,
            'acquisition': ewcfg.acquisition_fishing,
            'value': 3,
            'noslime': 'false'
        }
    elif item.item_type == ewcfg.it_food:
        item_props = {
            'id_food': item.id_food,
            'food_name': item.str_name,
            'food_desc': item.str_desc,
            'recover_hunger': item.recover_hunger,
            'inebriation': item.inebriation,
            'str_eat': item.str_eat,
            'time_expir': int(time.time()) + item.time_expir,
            'time_fridged': item.time_fridged,
            'perishable': item.perishable,
        }
    elif item.item_type == ewcfg.it_relic:
        item_props = {
            'id_relic': item.id_relic,
            'relic_name': item.str_name,
            'relic_desc': item.str_desc,
            'acquisition': item.acquisition
        }
    elif item.item_type == ewcfg.it_item:
        item_props = {
            'id_item': item.id_item,
            'context': item.context,
            'item_name': item.str_name,
            'item_desc': item.str_desc,
            'ingredients': item.ingredients if type(item.ingredients) == str else item.ingredients[0],
            'acquisition': item.acquisition,
        }
        if item.context == ewcfg.context_slimeoidfood:
            item_props["increase"] = item.increase
            item_props["decrease"] = item.decrease
        if item.context == ewcfg.context_prankitem:
            item_props["prank_type"] = item.prank_type
            item_props["prank_desc"] = item.prank_desc
            item_props["rarity"] = item.rarity
            item_props["gambit"] = item.gambit
            # Response items
            item_props["response_command"] = item.response_command
            item_props["response_desc_1"] = item.response_desc_1
            item_props["response_desc_2"] = item.response_desc_2
            item_props["response_desc_3"] = item.response_desc_3
            item_props["response_desc_4"] = item.response_desc_4
            # Trap items
            item_props["trap_chance"] = item.trap_chance
            item_props["trap_stored_credence"] = item.trap_stored_credence
            item_props["trap_user_id"] = item.trap_user_id
            # Some prank items have nifty side effects
            item_props["side_effect"] = item.side_effect

        try:
            item_props["durability"] = item.durability
        except:
            pass


    elif item.item_type == ewcfg.it_weapon:
        captcha = ""
        if ewcfg.weapon_class_captcha in item.classes:
            captcha = ewutils.generate_captcha(length=item.captcha_length)

        item_props = {
            "weapon_type": item.id_weapon,
            "weapon_name": "",
            "weapon_desc": item.str_description,
            "married": "",
            "ammo": item.clip_size,
            "captcha": captcha,
            "is_tool": item.is_tool
        }

    elif item.item_type == ewcfg.it_cosmetic:
        item_props = {
            'id_cosmetic': item.id_cosmetic,
            'cosmetic_name': item.str_name,
            'cosmetic_desc': item.str_desc,
            'str_onadorn': item.str_onadorn if item.str_onadorn else ewcfg.str_generic_onadorn,
            'str_unadorn': item.str_unadorn if item.str_unadorn else ewcfg.str_generic_unadorn,
            'str_onbreak': item.str_onbreak if item.str_onbreak else ewcfg.str_generic_onbreak,
            'rarity': item.rarity if item.rarity else ewcfg.rarity_plebeian,
            'attack': item.stats[ewcfg.stat_attack] if ewcfg.stat_attack in item.stats.keys() else 0,
            'defense': item.stats[ewcfg.stat_defense] if ewcfg.stat_defense in item.stats.keys() else 0,
            'speed': item.stats[ewcfg.stat_speed] if ewcfg.stat_speed in item.stats.keys() else 0,
            'ability': item.ability if item.ability else None,
            'durability': item.durability if item.durability else ewcfg.base_durability,
            'size': item.size if item.size else 1,
            'fashion_style': item.style if item.style else ewcfg.style_cool,
            'freshness': item.freshness if item.freshness else 5,
            'adorned': 'false',
            'hue': ""
        }
    elif item.item_type == ewcfg.it_furniture:
        item_props = {
            'id_furniture': item.id_furniture,
            'furniture_name': item.str_name,
            'furniture_desc': item.str_desc,
            'rarity': item.rarity,
            'furniture_place_desc': item.furniture_place_desc,
            'furniture_look_desc': item.furniture_look_desc,
            'acquisition': item.acquisition
        }


    return item_props


# SWILLDERMUK
async def perform_prank_item_side_effect(side_effect, cmd = None, member = None):
    response = ""

    if side_effect == "bungisbeam_effect":

        target_member = cmd.mentions[0]
        client = cmd.client

        current_nickname = target_member.display_name
        new_nickname = current_nickname + ' (Bungis)'

        if len(new_nickname) > 32:
            # new nickname is too long, cut out some parts of original nickname
            new_nickname = current_nickname[:20]
            new_nickname += '... (Bungis)'

        target_member = await target_member.edit(nick=new_nickname)

        response = "\n\nYou are now known as {}!".format(target_member.display_name)

    elif side_effect == "cumjar_effect":

        target_member = cmd.mentions[0]
        target_data = EwUser(member=target_member)

        if random.randrange(2) == 0:
            figurine_id = random.choice(static_items.furniture_pony)

            # print(figurine_id)
            item = static_items.furniture_map.get(figurine_id)

            item_props = gen_item_props(item)

            # print(item_props)

            bknd_item.item_create(
                id_user=target_data.id_user,
                id_server=target_data.id_server,
                item_type=ewcfg.it_furniture,
                item_props=item_props,
            )

            response = "\n\n*{}*: What's this? It looks like a pony figurine was inside the Cum Jar all along! You stash it in your inventory quickly.".format(target_member.display_name)

    elif side_effect == "bensaintsign_effect":

        target_member = member
        client = ewutils.get_client()

        new_nickname = 'Ben Saint'

        target_member = await target_member.edit(nick=new_nickname)

        response = "\n\nYou are now Ben Saint.".format(target_member.display_name)

    elif side_effect == "bodynotifier_effect":
        target_member = cmd.mentions[0]

        direct_message = "You are now manually breathing.\nYou are now manually blinking.\nYour tounge is now uncomfortable inside your mouth.\nYou just lost THE GAME."
        try:
            await fe_utils.send_message(cmd.client, target_member, direct_message)
        except:
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(target_member, direct_message))

    elif side_effect == "usedneedle_effect":
        target_member = cmd.mentions[0]
        target_data = EwUser(member=target_member)
        
        response = "\n\n(﹁ _﹁) ~→       ԅ(¯﹃¯ԅ)"

        if random.randrange(2) == 0:
            target_data.rand_seed = random.randrange(500000)        
            target_data.persist()
            response += "\n\n*{}*: What's this? You feel a shift in your pants. You whip them open and see your cock changing in size! Unbelievable! You must've contracted {} from the used needle!".format(target_member.display_name, random.choice(comm_cfg.actual_stds))

    return response


"""
    Transfer a random item from district inventory to player inventory
"""


def item_lootrandom(user_data):
    response = ""

    try:
        # find_item() uses the inventory() function anyway, so why have custom sql here followed by what you're avoiding
        items_in_poi = bknd_item.inventory(id_user=user_data.poi, id_server=user_data.id_server)

        if len(items_in_poi) > 0:
            item_sought = random.choice(items_in_poi)

            response += "You found a {}!".format(item_sought.get('name'))

            if bknd_item.check_inv_capacity(user_data=user_data, item_type=item_sought.get('item_type')):
                bknd_item.give_item(id_user=user_data.id_user, id_server=user_data.id_server, id_item=item_sought.get("id_item"))
            else:
                response += " But you couldn't carry any more {}s, so you tossed it back.".format(item_sought.get('item_type'))

        else:
            response += "You found a... oh, nevermind, it's just a piece of trash."

    except:
        ewutils.logMsg("Failed to loot random item")

    finally:
        return response


def item_lootspecific(user_data = None, item_search = None):
    response = ""
    if user_data is not None:
        item_sought = bknd_item.find_item(
            item_search=item_search,
            id_server=user_data.id_server,
            id_user=user_data.poi
        )
        if item_sought is not None:
            item_type = item_sought.get("item_type")
            response += "You found a {}!".format(item_sought.get("name"))
            can_loot = bknd_item.check_inv_capacity(user_data=user_data, item_type=item_type)
            if can_loot:
                bknd_item.give_item(
                    id_item=item_sought.get("id_item"),
                    id_user=user_data.id_user,
                    id_server=user_data.id_server
                )
            else:
                response += " But you couldn't carry any more {}s, so you tossed it back.".format(item_type)
    return response


def soulbind(id_item):
    item = EwItem(id_item=id_item)
    item.soulbound = True
    item.persist()


"""
    Find every item matching the search in the player's inventory (returns a list of (non-EwItem) item)
"""


def find_item_all(item_search = None, id_user = None, id_server = None, item_type_filter = None, exact_search = True, search_names = False):
    items_sought = []
    props_to_search = [
        'weapon_type',
        'id_item',
        'id_food',
        'id_cosmetic',
        'id_furniture',
        'id_relic'
    ]

    if search_names == True:
        props_to_search = [
            'cosmetic_name',
            'furniture_name',
            'food_name',
            'title',
            'weapon_type',
            'weapon_name',
            'item_name',
            'id_relic'
        ]

    if item_search:
        items = bknd_item.inventory(id_user=id_user, id_server=id_server, item_type_filter=item_type_filter)

        # find the first (i.e. the oldest) item that matches the search
        for item in items:
            # item_data = EwItem(id_item=item.get('id_item'))
            for prop in props_to_search:
                if prop in item.get('item_props') and (ewutils.flattenTokenListToString(item.get('item_props')[prop]) == item_search or (exact_search == False and item_search in ewutils.flattenTokenListToString(item.get('item_props')[prop]))):
                    items_sought.append(item)
                    break

    return items_sought


def surrendersoul(giver = None, receiver = None, id_server = None):
    if giver != None and receiver != None:
        receivermodel = EwUser(id_server=id_server, id_user=receiver)
        givermodel = EwUser(id_server=id_server, id_user=giver)
        giverplayer = EwPlayer(id_user=givermodel.id_user)
        if givermodel.has_soul == 1:
            givermodel.has_soul = 0
            givermodel.persist()

            item_id = bknd_item.item_create(
                id_user=receivermodel.id_user,
                id_server=id_server,
                item_type=ewcfg.it_cosmetic,
                item_props={
                    'id_cosmetic': "soul",
                    'cosmetic_name': "{}'s soul".format(giverplayer.display_name),
                    'cosmetic_desc': "The immortal soul of {}. It dances with a vivacious energy inside its jar.\n If you listen to it closely you can hear it whispering numbers: {}.".format(
                        giverplayer.display_name, givermodel.id_user),
                    'str_onadorn': ewcfg.str_generic_onadorn,
                    'str_unadorn': ewcfg.str_generic_unadorn,
                    'str_onbreak': ewcfg.str_generic_onbreak,
                    'rarity': ewcfg.rarity_patrician,
                    'attack': 6,
                    'defense': 6,
                    'speed': 6,
                    'ability': None,
                    'durability': None,
                    'size': 6,
                    'fashion_style': ewcfg.style_cool,
                    'freshness': 10,
                    'adorned': 'false',
                    'user_id': givermodel.id_user
                }
            )

            return item_id


async def lower_durability(general_item):
    general_item_data = EwItem(id_item=general_item.get('id_item'))

    current_durability = general_item_data.item_props.get('durability')
    general_item_data.item_props['durability'] = (int(current_durability) - 1)
    general_item_data.persist()


def unwrap(id_user = None, id_server = None, item = None, repeats = 0, rarity = 1000):
    response = "You eagerly rip open a pack of Secreatures™ trading cards!!"
    bknd_item.item_delete(item.id_item)
    slimexodia = False
    slimexodia_chance = 1 / 1000



    if random.random() < slimexodia_chance:
        slimexodia = True



    if slimexodia == True:
        # If there are multiple possible products, randomly select one.
        slimexodia_item = random.choice(static_items.slimexodia_parts)

        response += " There’s a single holographic card poking out of the swathes of repeats and late edition cards..."
        response += " ***...What’s this?! It’s the legendary card {}!! If you’re able to collect the remaining pieces of Slimexodia, you might be able to smelt something incomprehensibly powerful!!***".format(slimexodia_item.str_name)

    pulls = {}

    for packs in range(repeats + 1):
        slimexodia_chance = 1 / rarity

        if random.random() < slimexodia_chance:
            slimexodia = True

        if slimexodia == True:
            
            # If there are multiple possible products, randomly select one.
            slimexodia_item = random.choice(static_items.slimexodia_parts)
            item_props = gen_item_props(slimexodia_item)
            item_type = slimexodia_item.item_type
            if pulls.get(slimexodia_item):
                pulls[slimexodia_item.str_name] += 1
            else:
                pulls[slimexodia_item.str_name] = 1

            bknd_item.item_create(
                item_type=item_type,
                id_user=id_user.id,
                id_server=id_server.id,
                item_props=item_props
            )




            bknd_item.item_create(
                item_type=item_type,
                id_user=id_user.id,
                id_server=id_server.id,
                item_props=item_props
            )
            slimexodia = False

    if len(pulls) > 1:
        response += " ***...What's this?!*** You manage to find a number of legendary cards, including:\n"
        for card in pulls:
            response += "**{}x** {}".format(pulls[card], card)
    elif len(pulls) == 1:
        response += " There’s a single holographic card poking out of the swathes of repeats and late edition cards...\n"
        response += " ***...What’s this?! It’s the legendary card {}!! If you’re able to collect the remaining pieces of Slimexodia, you might be able to smelt something incomprehensibly powerful!!***\n".format(list(pulls.keys())[0])
    elif len(pulls) == 0:
        response += " But… it’s mostly just repeats and late edition cards. You toss them away."

    return response



def popcapsule(id_user = None, id_server = None, item = None):
    rarity_roll = random.randrange(10)
    bknd_item.item_delete(item.id_item)

    if rarity_roll > 3:
        prank_item = random.choice(static_items.prank_items_heinous)
    elif rarity_roll > 0:
        prank_item = random.choice(static_items.prank_items_scandalous)
    else:
        prank_item = random.choice(static_items.prank_items_forbidden)

    item_props = gen_item_props(prank_item)

    prank_item_id = bknd_item.item_create(
        item_type=prank_item.item_type,
        id_user=id_user.id,
        id_server=id_server.id,
        item_props=item_props
    )

    response = "You pop open the Prank Capsule to reveal a {}! Whoa, sick!!".format(prank_item.str_name)

    return response


"""
    Drop item into current district.
"""


def item_drop(
        id_item = None,
        other_poi = None
):
    try:
        item_data = EwItem(id_item=id_item)
        user_data = EwUser(id_user=item_data.id_owner, id_server=item_data.id_server)
        if other_poi == None:
            dest = user_data.poi
        else:
            dest = other_poi

        if item_data.item_type == ewcfg.it_cosmetic:
            item_data.item_props["adorned"] = "false"
            if item_data.item_props.get("slimeoid") is not None:
                item_data.item_props["slimeoid"] = "false"
        item_data.persist()
        bknd_item.give_item(id_user=dest, id_server=item_data.id_server, id_item=item_data.id_item)
    except Exception as e:
        ewutils.logMsg("Failed to drop item {}: {}".format(id_item, e))



def cull_slime_sea(
        id_server = None
):
    if id_server != None:
        seainv = bknd_item.inventory(
            id_user='slimesea',
            id_server=id_server
        )
        sea_size = len(seainv)
        random.shuffle(seainv)
        #print(seainv)
        to_delete = []
        if sea_size <= 500:
            return 0
        else:
            for seaitem in seainv:
                try:
                    if sea_size <= 450:
                        break
                    elif seaitem.get('soulbound'):
                        sea_size += 1
                    elif seaitem.get('item_type') in [ewcfg.it_book, ewcfg.it_food]:
                        to_delete.append(seaitem.get('id_item'))
                    elif seaitem.get('name') in static_weapons.weapon_names and seaitem.get('item_type') == ewcfg.it_weapon: #delete non-named weapons
                        to_delete.append(seaitem.get('id_item'))
                    elif seaitem.get('item_type') == ewcfg.it_item:
                        item_obj = EwItem(seaitem.get('id_item'))
                        if item_obj.item_props.get('context') in ['prankitem', ewcfg.context_wrappingpaper, 'batterypack', 'player_bone', 'prankcapsule', 'dye', 'poudrin'] or item_obj.item_props.get('id_item') in ewcfg.slimesea_disposables:
                            to_delete.append(seaitem.get('id_item'))
                        else:
                            sea_size += 1
                    elif seaitem.get('item_type') == ewcfg.it_furniture: #non-smelted furniture with a price below 1 mega gets culled
                        item_obj = EwItem(id_item=seaitem.get('id_item'))
                        mapped = static_items.furniture_map.get(item_obj.item_props.get('id_furniture'))
                        if mapped is not None:
                            if (mapped.price < 100000 and mapped.acquisition != ewcfg.acquisition_smelting) or mapped.id_furniture in ewcfg.slimesea_disposables:
                                to_delete.append(seaitem.get('id_item'))
                            else:
                                sea_size += 1
                        else:
                            sea_size += 1
                    elif seaitem.get('item_type') == ewcfg.it_cosmetic:
                        item_obj = EwItem(seaitem.get('id_item'))
                        if item_obj.item_props.get('id_cosmetic') in ewcfg.slimesea_disposables:
                            to_delete.append(seaitem.get('id_item'))
                    else:
                        sea_size += 1
                    sea_size -= 1
                except Exception as e:
                    ewutils.logMsg("Error when trying to cull item {}: {}".format(seaitem.get('id_item'), e))

            # Make sure there's something to delete, or otherwise the bot will crash out trying to delete nothing
            if len(to_delete) > 0:    
                #delete_string = [str(element) for element in to_delete]
                drop_list = ','.join(map(str, to_delete))

                bknd_core.execute_sql_query("DELETE FROM items WHERE {id_item} IN ({drop_list})".format(id_item=ewcfg.col_id_item, drop_list=drop_list), ())

                item_cache = bknd_core.get_cache(obj_type="EwItem")
                num = len(to_delete)
                if item_cache:
                    for itemid in to_delete:
                        bknd_core.remove_entry(obj_type="EwItem", id_entry=int(itemid))
                        #item_cache.entries.pop(itemid)
                return num
            else:
                return 0

def get_root_owner(id_item):
    item = EwItem(id_item=id_item)
    if 'collection' in item.id_owner:
        root_item = EwItem(id_item=item.id_owner.replace('collection', ''))
        return root_item.id_owner
    elif 'stand' in item.id_owner:
        data = bknd_core.execute_sql_query('SELECT id_item from items_prop where name = \'acquisition\' and value = %s', (item.id_item))
        orig_item = int(data[0][0])
        orig_obj = EwItem(id_item=orig_item)
        return orig_obj.id_owner
    else:
        return item.id_owner

async def move_relics(id_server):
    relic_stash = bknd_item.inventory(
        id_server=id_server,
        item_prop_method={"acquisition": "relic"}
        )


    #this code sucks but it only runs once a day so fuck it
    owner_list = []



    for relic in relic_stash:
        relic_item = EwItem(id_item=relic.get('id_user'))
        if relic_item.id_owner == 'slimesea' and relic_item.template not in dontfilter_relics:
            relic_item.id_owner = random.choice(static_poi.capturable_districts)
            relic_item.persist()
            continue

        owner_condensed = relic_item.id_owner.replace('decorate', '').replace('fridge', '').replace('closet', '').replace('bookshelf', '')
        if 'collection' in owner_condensed or 'stand' in owner_condensed:
            owner_condensed = get_root_owner(relic_item.id_item)

        if not owner_condensed.isalpha():
            owner_list.append(owner_condensed)
    totals = len(relic_list)
    mean_relics = max(set(owner_list), key=owner_list.count)
    if owner_list.count(mean_relics) > min(totals * 0.5, 20):
        iterator = int(owner_list.count(mean_relics) * .4)
        for relic in relic_stash:
            relic_item = EwItem(id_item=relic.get('id_item'))
            if relic_item.id_owner == mean_relics:
                relic_item.id_owner = random.choice(static_poi.capturable_districts)
                relic_item.persist()
                iterator -= 1
                if iterator <= 0:
                    break
        client = ewcfg.get_client()
        server = client.get_guild(id_server)
        user = EwUser(id_server=id_server, id_user=mean_relics)
        player = EwPlayer(id_user=user.id_user, id_server=id_server)
        user_poi = static_poi.id_to_poi.get(user.poi)
        channel = fe_utils.get_channel(server=server, channel_name=user_poi.channel)

        return await fe_utils.send_message(client, channel, "Oh fuck! {} just got graverobbed! Relics have been scattered!".format(player.display_name))






