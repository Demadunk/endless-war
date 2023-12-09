import asyncio
import discord
import random
import sys
import time
import datetime

from ew.backend import core as bknd_core
from ew.backend import item as bknd_item
from ew.backend import worldevent as bknd_worldevent

from ew.backend.apt import EwApartment

from ew.backend.item import EwItem
from ew.backend.market import EwMarket
from ew.backend.status import EwEnemyStatusEffect
from ew.backend.status import EwStatusEffect
from ew.backend.worldevent import EwWorldEvent
from ew.backend.mutation import EwMutation
from ew.backend.dungeons import EwGamestate
from ew.backend.questrecords import fetch_quest_records

from ew.utils.transport import EwTransport

from ew.static import cfg as ewcfg
from ew.static import community_cfg as comm_cfg
from ew.static import hue as hue_static
from ew.static import items as static_items
from ew.static import mutations as static_mutations
from ew.static import poi as poi_static
from ew.static import status as se_static
from ew.static import vendors
from ew.static import cosmetics as static_cosmetics
from ew.static import npc as npcutils
from ew.backend.player import EwPlayer

from ew.static import weapons as static_weapons
from ew.utils import cmd as cmd_utils
from ew.utils import combat as cmbt_utils
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import item as itm_utils
from ew.utils import leaderboard as bknd_leaderboard
from ew.utils import prank as prank_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils import stats as ewstats
from ew.utils import weather as weather_utils
from ew.utils.combat import EwUser
from ew.utils.cmd import EwCmd
from ew.utils.district import EwDistrict
from ew.utils.frontend import EwResponseContainer
from ew.utils.slimeoid import EwSlimeoid
from .cmdsutils import gen_score_text
from .cmdsutils import get_user_shares_str
from .cmdsutils import item_commands
from .cmdsutils import item_off
from .cmdsutils import location_commands
from .cmdsutils import mutation_commands
from ew.cmd.juviecmd import juviecmdutils
from ew.backend.goonscapestats import EwGoonScapeStat
from .cmdsutils import holiday_commands
from .. import item as ewitem
from ..apt import aptcmds as apt_cmds
from ..faction import factioncmds as faction_cmds
from ..wep import wepcmds as wep_cmds
try:
    from ..debug import debug24
    from ew.static import rstatic as relic_static
except:
    from ..debug_dummy import debug24
    from ew.static import rstatic_dummy as relic_static

""" show player's slime score """


async def score(cmd: cmd_utils.EwCmd):
    user_data = None
    member = None
    response = ""


    slime_alias = ewutils.flattenTokenListToString(cmd.tokens[0])
    if len(cmd.mention_ids) == 0:
        if ewrolemgr.check_clearance(cmd.message.author) <= 3 and cmd.tokens_count > 1:
            target_type = "district"
        else:
            target_type = "self"
    else:
        target_type = ewutils.mention_type(cmd, cmd.mention_ids[0])

    # :slimeepic:
    if slime_alias == "<slimeepic973836637777825864>":
        slime_alias = ewcfg.emote_slimeepic

    # endless war slime check
    if target_type == "ew":
        # get total amount of player slime and total amount of district ground slime
        totalplayerslime = bknd_core.execute_sql_query("SELECT SUM(slimes) FROM users WHERE slimes > 0 AND id_server = '{}'".format(cmd.guild.id))
        totalgroundslime = bknd_core.execute_sql_query("SELECT SUM(slimes) FROM districts WHERE slimes > 0 AND id_server = '{}'".format(cmd.guild.id))

        # add those two numbers together
        totalslimes = totalplayerslime[0][0] + totalgroundslime[0][0]
        response = "ENDLESS WAR has amassed {:,} {}.".format(totalslimes, slime_alias)

    # self slime check
    elif target_type == "self":
        user_data = EwUser(ew_id=cmd.author_id)
        poudrin_amount = bknd_item.find_poudrin(id_user=cmd.message.author.id, id_server=cmd.guild.id)

        # return my score
        response = "You currently have {:,} {}{}.".format(user_data.slimes, slime_alias, (" and {} {} poudrin{}".format(poudrin_amount, slime_alias, ("" if poudrin_amount == 1 else "s")) if poudrin_amount > 0 else ""))

    elif target_type == "district":
        district_search = cmd.tokens[1:]
        district_search = ewutils.flattenTokenListToString(district_search)
        found_district = poi_static.id_to_poi.get(district_search)
        if found_district:
            district_search = found_district.id_poi # use this to clean up the search, so we always specific get the right name for the db call
            district = EwDistrict(cmd.guild.id, district_search)
            response = "There's currently {:,} {} in {}.".format(district.slimes, slime_alias, district_search)
        else:
            response = "That's not a district. Hit the books, dweeb."

    # other user slime check
    else:
        member = cmd.mentions[0]  # for ewrolemgr
        response = gen_score_text(ew_id=cmd.mention_ids[0], slime_alias=slime_alias)

    time_now_msg_start = int(time.time())
    # Send the response to the player.
    await fe_utils.send_response(response, cmd)
    time_now_msg_end = int(time.time())

    time_now_role_start = int(time.time())
    if member != None:  # update roles on other user slime check
        await ewrolemgr.updateRoles(client=cmd.client, member=member)
    time_now_role_end = int(time.time())

    time_now_cmd_end = int(time.time())


# ewutils.logMsg('send_response took {} seconds.'.format(time_now_msg_end - time_now_msg_start))
# ewutils.logMsg('updateRoles took {} seconds.'.format(time_now_role_end - time_now_role_start))
# ewutils.logMsg('total command time took {} seconds.'.format(time_now_cmd_end - time_now_cmd_start))

""" show player information and description """


async def data(cmd):
    member = None
    response = ""

    if len(cmd.mention_ids) == 0:
        target_type = "self"
    else:
        target_type = ewutils.mention_type(cmd, cmd.mention_ids[0])

    # enemy data check
    if len(cmd.tokens) > 1 and cmd.mentions_count == 0 and len(cmd.mention_ids) == 0:
        user_data = EwUser(member=cmd.message.author)
        soughtenemy = " ".join(cmd.tokens[1:]).lower()
        enemy = cmbt_utils.find_enemy(soughtenemy, user_data)
        if enemy != None:

            description = ewcfg.enemy_data_table[enemy.enemytype].get("raredescription") if enemy.rare_status else ewcfg.enemy_data_table[enemy.enemytype].get("description")
            # Try for arctic variant description
            if description is not None and ewcfg.enemy_data_table[enemy.enemytype].get("arcticvariant") == enemy.display_name:
                description = ewcfg.enemy_data_table[enemy.enemytype].get("arcticdescription")
            description = "" if description == None else description

            if enemy.enemytype == 'npc':
                npc_obj = npcutils.active_npcs_map.get(enemy.enemyclass)
                response = "{}\n{}\n{}\n{} is level {}. They have {:,} slime. ".format(npc_obj.image_profile, npc_obj.str_name, npc_obj.description, npc_obj.str_name, enemy.level, enemy.slimes)
            elif enemy.attacktype != ewcfg.enemy_attacktype_unarmed:
                response = "{} is a level {} enemy. They have {:,} slime and attack with their {}. {}".format(enemy.display_name, enemy.level, enemy.slimes, enemy.attacktype, description)
            else:
                response = "{} is a level {} enemy. They have {:,} slime. {}".format(enemy.display_name, enemy.level, enemy.slimes, description)  # , enemy.hardened_sap)

            statuses = enemy.getStatusEffects()

            for status in statuses:
                status_effect = EwEnemyStatusEffect(id_status=status, enemy_data=enemy)
                if status_effect.time_expire > time.time() or status_effect.time_expire == -1:
                    status_flavor = se_static.status_effects_def_map.get(status)

                    severity = ""
                    try:
                        value_int = int(status_effect.value)
                        if value_int < 3:
                            severity = "lightly injured."
                        elif value_int < 7:
                            severity = "battered and bruised."
                        elif value_int < 11:
                            severity = "severely damaged."
                        else:
                            severity = "completely fucked up, holy shit!"
                    except:
                        pass

                    format_status = {'severity': severity}

                    if status_flavor is not None:
                        response += status_flavor.str_describe.format_map(format_status) + " "

            if enemy.enemytype in ewcfg.slimeoid_trainers:
                enemy_slimeoid = EwSlimeoid(id_user=enemy.id_enemy, id_server=cmd.message.guild.id)
                if enemy_slimeoid.level > 0:
                    response += "\n\nThey are accompanied by {}, a {}-foot-tall Slimeoid. ".format(enemy_slimeoid.name, str(enemy_slimeoid.level))

        else:
            response = "ENDLESS WAR didn't understand that name."


    elif target_type == "ew":
        response = "ENDLESS WAR is a level 666 ancient obelisk. He is wielding THE BONE HURTING BEAM. He is a rank 111 bone hurter. He has been weathered by months of bicarbonate rain. He has millions of confirmed kills."


    # self data check
    elif target_type == "self":

        user_data = EwUser(member=cmd.message.author)
        slimeoid = EwSlimeoid(member=cmd.message.author)

        cosmetics = bknd_item.inventory(
            id_user=cmd.message.author.id,
            id_server=cmd.guild.id,
            item_type_filter=ewcfg.it_cosmetic
        )
        adorned_cosmetics = []

        # A list of all adorned cosmetics' ids
        cosmetic_id_list = []

        for cosmetic in cosmetics:
            cos = EwItem(id_item=cosmetic.get('id_item'))
            if cos.item_props['adorned'] == 'true':
                hue = hue_static.hue_map.get(cos.item_props.get('hue'))
                hue2 = cos.item_props.get('hue2')
                pattern = cos.item_props.get('pattern')
                adorned_cosmetics.append(((hue.str_name if hue is not None else "") + ('/' + hue2 if hue2 is not None else '') + (' ' + pattern + ' ' if pattern is not None else '') + (' ' if hue != None and hue2 == None else '') + cosmetic.get('name')))
                cosmetic_id_list.append(cos.item_props['id_cosmetic'])




        #get race flavor text
        player_race = ewcfg.defined_races.get(user_data.race)
        if player_race != None:
            race_prefix = player_race.get("race_prefix", "")
            race_suffix = player_race.get("race_suffix", "")
        else:
            race_prefix = ""
            race_suffix = ""

        if user_data.life_state == ewcfg.life_state_corpse:
            title = "{}dead{}".format(race_suffix, user_data.gender).capitalize()
        else:
            title = "{}slime{}".format(race_suffix, user_data.gender)
        response = "You are a LV{} {}{}.\n".format(user_data.slimelevel, race_prefix, title)

        poi = poi_static.id_to_poi.get(user_data.poi)

        if user_data.hunger > 0:
            hungerblock = "You are {}% hungry. ".format(
                round(user_data.hunger * 100.0 / user_data.get_hunger_max(), 1)
            )
        else:
            hungerblock = ""

        if poi != None:
            response += "You find yourself {} {}. {}\n".format(poi.str_in, poi.str_name, hungerblock)



        coinbounty = int(user_data.bounty / ewcfg.slimecoin_exchangerate)

        weapon_item = EwItem(id_item=user_data.weapon)
        weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))

        if weapon != None:
            response += "{} {}{}.".format(
                ewcfg.str_weapon_married_self if user_data.weaponmarried == True else ewcfg.str_weapon_wielding_self, (
                    "" if len(weapon_item.item_props.get("weapon_name")) == 0 else "{}, ".format(
                        weapon_item.item_props.get("weapon_name"))), weapon.str_weapon)
            if user_data.weaponskill >= 5:
                response += " {}".format(weapon.str_weaponmaster_self.format(rank=(user_data.weaponskill - 4), title="master"))
            else:
                response += " {}".format(weapon.str_weaponmaster_self.format(rank=(user_data.weaponskill), title="rookie"))

        trauma = se_static.trauma_map.get(user_data.trauma)

        sidearm_item = EwItem(id_item=user_data.sidearm)
        sidearm = static_weapons.weapon_map.get(sidearm_item.item_props.get("weapon_type"))

        if sidearm != None:
            if weapon == None:
                response += "You have sidearmed {}{}.".format((
                    "" if len(sidearm_item.item_props.get("weapon_name")) == 0 else "{}, ".format(
                        sidearm_item.item_props.get("weapon_name"))), sidearm.str_weapon)
            else:
                response += " You have sidearmed {}{}.".format((
                    "" if len(sidearm_item.item_props.get("weapon_name")) == 0 else "{}, ".format(
                        sidearm_item.item_props.get("weapon_name"))), sidearm.str_weapon)

        if trauma != None:
            if weapon != None or sidearm != None:
                response += " {}".format(trauma.str_trauma_self)
            else:
                response += "{}".format(trauma.str_trauma_self)
    
        response_block = ""

        #user_kills = ewstats.get_stat(user=user_data, metric=ewcfg.stat_kills)
        #enemy_kills = ewstats.get_stat(user=user_data, metric=ewcfg.stat_pve_kills)

        #response_block += "{}{}".format(cmd_utils.get_crime_level(num=user_data.crime, forYou=1), ' ')


        #if user_kills > 0 and enemy_kills > 0:
        #    response_block += "You have {:,} confirmed kills, and {:,} confirmed hunts. ".format(user_kills,
        #                                                                                         enemy_kills)
        #elif user_kills > 0:
        #    response_block += "You have {:,} confirmed kills. ".format(user_kills)
        #elif enemy_kills > 0:
        #    response_block += "You have {:,} confirmed hunts. ".format(enemy_kills)

        #if coinbounty != 0:
            #response_block += "SlimeCorp offers a bounty of {:,} SlimeCoin for your death. ".format(coinbounty)


            # Otherwise, generate response text for freshness and style.
            #elif outfit_map is not None:
                #response_block += itm_utils.get_style_freshness_rating(user_data=user_data, dominant_style=outfit_map['dominant_style']) + " "

        statuses = user_data.getStatusEffects()
        if user_data.has_soul == 0:
            response_block += " You have no soul."

        for status in statuses:
            status_effect = EwStatusEffect(id_status=status, user_data=user_data)
            if status_effect.time_expire > time.time() or status_effect.time_expire == -1:
                status_flavor = se_static.status_effects_def_map.get(status)

                severity = ""
                try:
                    value_int = int(status_effect.value)
                    if value_int < 3:
                        severity = "lightly injured."
                    elif value_int < 7:
                        severity = "battered and bruised."
                    elif value_int < 11:
                        severity = "severely damaged."
                    else:
                        severity = "completely fucked up, holy shit!"
                except:
                    pass

                format_status = {'severity': severity}

                if status_flavor is not None:
                    response_block += status_flavor.str_describe_self.format_map(format_status) + " "

        if (slimeoid.life_state == ewcfg.slimeoid_state_active):
            # If the user isn't a corpse
            if user_data.life_state != ewcfg.life_state_corpse:
                response_block += "You are accompanied by {}, a {}-foot-tall Slimeoid. ".format(slimeoid.name, str(slimeoid.level))
            # If the user is a corpse, but has a negaslimeoid
            elif slimeoid.sltype == ewcfg.sltype_nega:
                response_block += "You are accompanied by {}, a {}-foot-tall Negaslimeoid. ".format(slimeoid.name, str(slimeoid.level))

        server = ewutils.get_client().get_guild(user_data.id_server)
        if user_data.life_state == ewcfg.life_state_corpse:
            inhabitee_id = user_data.get_inhabitee()
            if inhabitee_id:
                inhabitee_name = (await fe_utils.get_member(server, inhabitee_id)).display_name
                possession = user_data.get_possession()
                if possession:
                    if possession[3] == 'weapon':
                        response_block += "You are currently possessing {}'s weapon. ".format(inhabitee_name)
                    elif possession[3] == 'rod':
                        response_block += "You are currently possessing {}'s fishing rod. ".format(inhabitee_name)
                else:
                    response_block += "You are currently inhabiting the body of {}. ".format(inhabitee_name)
        else:
            inhabitant_ids = user_data.get_inhabitants()
            if inhabitant_ids:
                inhabitant_names = []
                for inhabitant_id in inhabitant_ids:
                    inhabitant_names.append((await fe_utils.get_member(server, inhabitant_id)).display_name)

                possession = user_data.get_possession()
                if possession is not None:
                    ghost_in_weapon = possession[0]
                    possession_type = 'fishing rod' if possession[3] == 'rod' else possession[3]

                if len(inhabitant_names) == 1:
                    response_block += "You are inhabited by the ghost of {}{}. ".format(inhabitant_names[0], ', who is possessing your ' + possession_type if possession else '')
                else:
                    response_block += "You are inhabited by the ghosts of {}{} and {}. ".format(
                        ", ".join(inhabitant_names[:-1]),
                        "" if len(inhabitant_names) == 2 else ",",
                        inhabitant_names[-1]
                    )
                    if possession:
                        response_block += "{} is also possessing your {}. ".format((await fe_utils.get_member(server, ghost_in_weapon)).display_name, possession_type)

        if len(adorned_cosmetics) > 0:
            response_block += "\n\nYou have a {} adorned. ".format(ewutils.formatNiceList(adorned_cosmetics, 'and'))

            #outfit_map = itm_utils.get_outfit_info(id_user=cmd.message.author.id, id_server=cmd.guild.id)
            user_data.persist()

            # If user is wearing all pieces of the a costume set, add text
            if all(elem in cosmetic_id_list for elem in static_cosmetics.cosmetic_nmsmascot):
                response_block += "You're dressed like a fucking airplane with tits, dude. "
            elif all(elem in cosmetic_id_list for elem in static_cosmetics.cosmetic_hatealiens):
                response_block += "Your taste in clothes is a symbol of hatred to illegal aliens everywhere."

        # if user_data.swear_jar >= 500:
        # 	response_block += "You're going to The Underworld for the things you've said."
        # elif user_data.swear_jar >= 100:
        # 	response_block += "You swear like a sailor!"
        # elif user_data.swear_jar >= 50:
        # 	response_block += "You have quite a profane vocabulary."
        # elif user_data.swear_jar >= 10:
        # 	response_block += "You've said some naughty things in the past."
        # elif user_data.swear_jar >= 5:
        # 	response_block += "You've cussed a handful of times here and there."
        # elif user_data.swear_jar > 0:
        # 	response_block += "You've sworn only a few times."
        # else:
        # 	response_block += "Your mouth is clean as a whistle."

        if len(response_block) > 0:
            response += "\n" + response_block

        response += "\n\nhttps://rfck.app/stats/player.html?pl={}".format(user_data.id_user)

    # other data check
    else:
        member = cmd.mentions[0]
        response = cmd_utils.gen_data_text(
            id_user=member.id,
            id_server=member.guild.id,
            display_name=member.display_name,
        )

        response += "\n\nhttps://rfck.app/stats/player.html?pl={}".format(member.id)

    # Send the response to the player.
    await fe_utils.send_response(response, cmd)

    await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
    if member != None:
        await ewrolemgr.updateRoles(client=cmd.client, member=member)


""" Finally, separates mutations from !data """


async def mutations(cmd):
    response = ""
    total_levels = 0

    if "level" in cmd.tokens:
        response += "\n"

    if cmd.mentions_count == 0:
        user_data = EwUser(member=cmd.message.author)
        mutations = user_data.get_mutations()




        if ewcfg.mutation_id_gay in mutations:
            # PRESENT DAY
            # PRESENT TIME
            the_month = datetime.datetime.now().month
            if the_month != 6: # If it's not pride month, sorry bucko.
                resp_cont = EwResponseContainer(client=cmd.client, id_server=user_data.id_server)
                die_resp = user_data.die(cause=ewcfg.cause_gay)
                resp_cont.add_response_container(die_resp)
                return await resp_cont.post()


        for mutation in mutations:
            mutation_flavor = static_mutations.mutations_map[mutation]
            total_levels += mutation_flavor.tier
            if "level" in cmd.tokens:
                # Get the object each mutation is from.
                mutation_obj = EwMutation(id_mutation=mutation, id_user=user_data.id_user, id_server=cmd.message.guild.id)
                
                # If a mutation is artificial on self-check, have it be labelled as grafted
                if mutation_obj.artificial == 1:
                    response += "**LEVEL {}**:{} *Grafted*. \n".format(mutation_flavor.tier, mutation_flavor.str_describe_self)
                else:
                    response += "**LEVEL {}**:{} \n".format(mutation_flavor.tier, mutation_flavor.str_describe_self)
            else:
                response += "{} ".format(mutation_flavor.str_describe_self)
        if len(mutations) == 0:
            response = "You are miraculously unmodified from your normal genetic code!"
        elif "level" in cmd.tokens:
            response += "Total Levels: {}/50\nMutation Levels Added: {}/{}".format(user_data.slimelevel, total_levels, min(50, user_data.slimelevel))

    else:
        member = cmd.mentions[0]
        user_data = EwUser(
            id_user=member.id,
            id_server=member.guild.id
        )


        mutations = user_data.get_mutations()
        for mutation in mutations:
            mutation_flavor = static_mutations.mutations_map[mutation]
            total_levels += mutation_flavor.tier
            if "level" in cmd.tokens:
                response += "**LEVEL {}**:{} \n".format(mutation_flavor.tier, mutation_flavor.str_describe_other)
            else:
                response += "{} ".format(mutation_flavor.str_describe_other)
        if len(mutations) == 0:
            response = "They are miraculously unmodified from their normal genetic code!"
        elif "level" in cmd.tokens:
            response += "Total Levels: {}/50\nMutation Levels Added: {}/{}".format(user_data.slimelevel, total_levels, min(50, user_data.slimelevel))
    await fe_utils.send_response(response, cmd)


""" Check how hungry you are. """


async def hunger(cmd):
    user_data = EwUser(member=cmd.message.author)
    response = ""

    if user_data.hunger > 0:
        response = "You are {}% hungry. ".format(
            round(user_data.hunger * 100.0 / user_data.get_hunger_max(), 1)
        )
    else:
        response = "You aren't hungry at all."

    return await fe_utils.send_response(response, cmd)


""" time and weather information """


async def weather(cmd):
    market_data = EwMarket(id_server=cmd.guild.id)
    response = ewutils.weather_txt(market_data)

    time_current = market_data.clock
    #if 3 <= time_current <= 10:
        #response += "\n\nThe police are probably all asleep, the lazy fucks. It's a good time for painting the town!"

    world_events = bknd_worldevent.get_world_events(id_server=cmd.guild.id, active_only=True)
    for id_event in world_events:
        # If there's a world event in NLACakaNM with corresponding alert
        if world_events.get(id_event) in ewcfg.poi_events:
            event_data = bknd_worldevent.EwWorldEvent(id_event=id_event)

            if event_data.event_props.get('alert') == "gangbase":
                event_def = poi_static.event_type_to_def.get(event_data.event_type)
                event_poi = poi_static.id_to_poi.get(event_data.event_props.get('poi'))

                response += "\n\n{}{}.".format(event_def.str_check_text, event_poi.str_name)
            else:
                response += "\n\nThere's a phenomenon occurring somewhere in NLACakaNM."

    # Send the response to the player.
    await fe_utils.send_response(response, cmd)


async def forecast(cmd):
    # Decide whether to use the mobile-friendly squashed response, or the desktop-friendly wide response
    resp_type = "long"
    if str(cmd.message.author.mobile_status) != "offline":
        resp_type = "short"
    # If the user specified a length, use that
    if cmd.tokens_count > 1:
        if cmd.tokens[1].lower() in ["short", "mobile", "m", "phone", "shortened", "iphone"]:
            resp_type = "short"
        elif cmd.tokens[1].lower() in ["long", "pc", "computer", "com", "full", "web", "desktop"]:
            resp_type = "long"

    # Get forecast from weather_utils
    forecast_response = weather_utils.forecast_txt(id_server=cmd.guild.id, resp_type=resp_type)

    # Format response
    response = "The weather forecast is:\n{}".format(forecast_response)
    if resp_type == "short":
        response = "The squashed weather forecast is:\n{}".format(forecast_response)

    # Send response
    await fe_utils.send_response(response, cmd)


"""
    Killers DAB
"""


async def dab(cmd):
    user_data = EwUser(member=cmd.message.author)

    if (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_killers:
        response = '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_slime1 + ewcfg.emote_slime3 + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime1 + ewcfg.emote_ck + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime1 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + '\n' + "{emote}" + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime1 + ewcfg.emote_slime1 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + "{emote}" + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime1 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_ck + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_ck + ewcfg.emote_slime3 + ewcfg.emote_slime1 + ewcfg.emote_slime1 + ewcfg.emote_slime3 + ewcfg.emote_ck + ewcfg.emote_slime1 + ewcfg.emote_ck + ewcfg.emote_ck + ewcfg.emote_slime1 + ewcfg.emote_ck
        final_response = response.format(emote=random.choice(ewcfg.dab_emotes))
        
    #Other factions being dumb
    elif (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_rowdys:
        final_response = "The fuck you think you're doing, bustah?"
    else:
        final_response = "You're too much of a coward to !dab, dumbass."

    await fe_utils.send_response(final_response, cmd)

"""
    Rowdys THRASH
"""


async def thrash(cmd):
    user_data = EwUser(member=cmd.message.author)

    if (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_rowdys:
        response = '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_rf + ewcfg.emote_slime3 + ewcfg.emote_slime1 + ewcfg.emote_slime3 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_slime1 + ewcfg.emote_slime1 + ewcfg.emote_slime3 + ewcfg.emote_slime1 + ewcfg.emote_rf + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_slime3 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + '\n' + "{emote}" + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_slime3 + ewcfg.emote_slime1 + ewcfg.emote_slime3 + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_slime3 + ewcfg.emote_slime1 + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + "{emote}" + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_slime3 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_slime3 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_rf + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_slime1 + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf + ewcfg.emote_rf
        final_response = response.format(emote=random.choice(ewcfg.thrash_emotes))
        
    #Other factions being dumb	
    elif (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_killers:
        final_response = "EXCUSE ME <@177731019322032128> WE GOT A TRAITOR HERE" # Yeah it @s Ben Saint lol
    else:
        final_response = "You're too much of a coward to !thrash, dumbass."

    await fe_utils.send_response(final_response, cmd, format_ats=False)

"""
    Ghosts BOO
"""


async def boo(cmd):
    user_data = EwUser(member=cmd.message.author)
    resp_cont = EwResponseContainer(id_server=user_data.id_server)
    if user_data.life_state == ewcfg.life_state_corpse or user_data.life_state == ewcfg.life_state_grandfoe:
        response = '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_staydead + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + '\n' + "{emote}" + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + "{emote}" + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead
        final_response = response.format(emote=random.choice(ewcfg.boo_emotes))

    #Other factions being dumb
    else:
        final_response = "Why would you want to lower yourself to the level of a filthy ghost?"
    
    #await fe_utils.send_response(final_response, cmd)
    resp_cont.add_channel_response(cmd.message.channel.name, final_response)
    # if user_data.life_state == ewcfg.life_state_corpse or user_data.life_state == ewcfg.life_state_grandfoe:
    await resp_cont.post()


# await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_blank + ewcfg.emote_blank + '\n' + ewcfg.emote_ghost + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_srs + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_ghost + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_blank + ewcfg.emote_blank + '\n' + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_negaslime + ewcfg.emote_srs + ewcfg.emote_negaslime + ewcfg.emote_staydead + ewcfg.emote_staydead + ewcfg.emote_blank + ewcfg.emote_blank + ewcfg.emote_blank))


async def spook(cmd):
    # user_data = EwUser(member=cmd.message.author)
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, '\n' "***SPOOKED YA!***" + '\n' + "https://www.youtube.com/watch?v=T-dtcIXZo4s"))


"""
    Juvies DANCE
"""


async def dance(cmd):
    user_data = EwUser(ew_id=cmd.author_id)

    if user_data.life_state == ewcfg.life_state_juvenile:
        response = random.choice(comm_cfg.dance_responses).format(cmd.author_id.display_name)
        response = "{} {} {}".format(ewcfg.emote_slime3, response, ewcfg.emote_slime3)
    
    #Other factions being dumb
    else:
        response = "You don't feel groovy enough to dance right now."

    await fe_utils.send_response(response, cmd, format_name=False)

"""
    Slimecorp PROPAGANDIZES
"""


async def propaganda(cmd):
    user_data = EwUser(ew_id=cmd.author_id)

    if (user_data.life_state == ewcfg.life_state_enlisted and user_data.faction == ewcfg.faction_slimecorp) or user_data.life_state == ewcfg.life_state_executive:
        response = random.choice("ur bad")
        await fe_utils.send_response(response, cmd)


"""
    Terezi Gang FLIP COINS
"""


async def coinflip(cmd):
    user_data = EwUser(member=cmd.message.author)
    response = ""

    if fe_utils.check_user_has_role(cmd.guild, cmd.message.author, ewcfg.role_donor_proper):

        if user_data.slimecoin <= 1:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "YOU DON'T H4V3 4NY SL1M3CO1N TO FL1P >:["))
        else:
            user_data.change_slimecoin(n=-1, coinsource=ewcfg.coinsource_spending)
            user_data.persist()

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "YOU FL1P ON3 SL1M3CO1N R1GHT 1N TH3 41R!\nhttps://cdn.discordapp.com/attachments/431240644464214017/652341405129375794/Terezi_Hussnasty_coinflip.gif"))
        await asyncio.sleep(2)
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "..."))
        await asyncio.sleep(3)

        flipnum = random.randrange(2)

        if flipnum == 0:
            response = "H34DS!\nhttps://www.homestuck.com/images/storyfiles/hs2/02045_3.gif"
        else:
            response = "T41LS!\nhttps://66.media.tumblr.com/tumblr_m6gdpg4qOg1r6ajb6.gif"

        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Bass wielders JAM OUT
"""


async def jam(cmd):
    # def leppard and pearl jam? meet def jam. this is what the refrance, fuck yeah.
    item_found = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_found, id_user=cmd.message.author.id, id_server=cmd.guild.id)

    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_props.get("id_furniture") in static_items.furniture_instrument or item.item_props.get("weapon_type") in [ewcfg.weapon_id_bass, ewcfg.weapon_id_slimeoidwhistle]:
            cycle = random.randrange(20)
            response = ""
            if random.randint(0, 10) == 0:
                if item.item_props.get("id_furniture") == None:
                    if item.item_props.get("weapon_type") != ewcfg.weapon_id_slimeoidwhistle:
                        item_key = "bass"
                    else:
                        item_key = "whistle"
                else:
                    item_key = item.item_props.get("id_furniture")
                response = random.choice(comm_cfg.jam_tunes[item_key])
            else:
                for x in range(1, cycle):
                    response += random.choice([":musical_note:", ":notes:"])

            await debug24(cmd)

        else:
            response = "You place your mouth on the {} but it makes no noise. Either that's not an instrument or you aren't good enough.".format(item_sought.get('name'))
    else:
        response = "Are you sure you have that item?"

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Dice wielders can DIE    
"""


async def rolldie(cmd):
    validroll = False
    
    # Look for die
    item_found = ewutils.flattenTokenListToString("die")
    item_sought = bknd_item.find_item(item_search=item_found, id_user=cmd.message.author.id, id_server=cmd.guild.id)

    # Check for if the user has either a die OR is Terezi Gang
    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_props.get("id_furniture") == "die":
            validroll = True
    elif fe_utils.check_user_has_role(cmd.guild, cmd.message.author, ewcfg.role_donor_proper):
        validroll = True
    
    # If the user *can* roll
    if validroll:
        # Send a dice rolling message
        response = "{}".format(ewcfg.emote_dice_rolling)
        sent_message = await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    
        await asyncio.sleep(4)  # WAIT

        # Roll dice, edit esponse
        dieroll = random.randint(1, 6)
        return await fe_utils.edit_message(cmd.client, sent_message, fe_utils.formatMessage(cmd.message.author, "{}".format(ewcfg.emotes_dice[dieroll - 1])))
    
    else:
        response = "You're not feeling dicey enough to do that."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def stunt(cmd):
    user_data = EwUser(member=cmd.message.author)
    item = None
    item_wanted = ""
    item_sought = None

    # Find the player's item
    item_wanted = ewutils.flattenTokenListToString(cmd.tokens[1:])

    # If the player listed nothing, assume they want their equipped weapon, sidearmed weapon, or a skateboard (hopefully a skateboard)
    if item_wanted == "":
        # Get the user's weapon. Check if it's a skateboard.
        item = EwItem(id_item=user_data.weapon)
        if item.item_props.get("weapon_type") not in [ewcfg.weapon_id_skateboard]:
            # If it's not a skateboard, get their sidearmed weapon.
            item = EwItem(id_item=user_data.sidearm)
            if item.item_props.get("weapon_type") not in [ewcfg.weapon_id_skateboard]:
                # If it's not a skateboard, default to name search for "skateboard"
                item_wanted = "skateboard"
                item = None

    # If the player isn't holding or sidearming a skateboard
    if item == None:
        item_sought = bknd_item.find_item(item_search=item_wanted, id_user=cmd.message.author.id, id_server=cmd.guild.id)
        if item_sought != None:
            item = EwItem(id_item=item_sought.get('id_item'))

    # If the player has an item that was sought
    if item != None:
        # If it's a skateboard
        if item.item_props.get("weapon_type") in [ewcfg.weapon_id_skateboard]:
            response = ''

            # Give the user some CRIME for ILLEGAL SKATING
            user_data.change_crime(n=ewcfg.cr_unlawful_stunting)
            user_data.persist()

            # Take a random response from Tricks
            response = random.choice(comm_cfg.skatetricks)

            # If it's not a skateboard
        else:
            response = "How would you trick with a {}?".format(item_sought.get('name'))

    else:
        response = "You need a skateboard to do tricks. C'mon!"

    # Send the response
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def endlesswar(cmd):
    total = bknd_core.execute_sql_query("SELECT SUM(slimes) FROM users WHERE slimes > 0 AND id_server = '{}'".format(cmd.guild.id))
    totalslimes = total[0][0]
    response = "ENDLESS WAR has amassed {:,} slime.".format(totalslimes)
    return await fe_utils.send_response(response, cmd)


async def slimefest(cmd):
    market_data = EwMarket(id_server=cmd.guild.id)

    response = "Soon..."
    # if market_data.winner == ewcfg.faction_killers:
    #	response = "Killers are winning Slimefest."
    # elif market_data.winner == ewcfg.faction_rowdys:
    #	response = "Rowdys are winning Slimefest."

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def swearjar(cmd):
    market_data = EwMarket(id_server=cmd.guild.id)
    total_swears = market_data.global_swear_jar

    response = "The swear jar has reached: **{}**".format(total_swears)

    if total_swears < 1000:
        pass
    elif total_swears < 10000:
        response += "\nThings are starting to get nasty."
    elif total_swears < 100000:
        response += "\nSwears? In *my* free Text-Based MMORPG playable entirely within my browser? It's more likely than you think."
    elif total_swears < 1000000:
        response += "\nGod help us all..."
    else:
        response = "\nThe city is rife with mischief and vulgarity, though that's hardly a surprise when it's inhabited by lowlifes and sinners across the board."

    return await fe_utils.send_response(response, cmd)


async def toss_off_cliff(cmd):
    user_data = EwUser(member=cmd.message.author)
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=user_data.id_server)

    if cmd.message.channel.name != ewcfg.channel_slimesendcliffs:
        if item_sought:
            if item_sought.get('name') == "brick" and cmd.mentions_count > 0:
                if ewutils.global_brick_counter > 60:
                    return
                else:
                    ewutils.global_brick_counter += 1

                item = EwItem(id_item=item_sought.get('id_item'))
                target = EwUser(member=cmd.mentions[0])
                target_apt = EwApartment(id_user=target.id_user, id_server=cmd.guild.id)
                if target_apt.poi == user_data.poi:
                    item.id_owner = str(cmd.mentions[0].id) + ewcfg.compartment_id_decorate
                    item.persist()
                    response = "You throw a brick through {}'s window. Oh shit! Quick, scatter before they see you!".format(cmd.mentions[0].display_name)
                    user_data.change_crime(n=1)
                    user_data.persist()

                    if poi_static.id_to_poi.get(target.poi).is_apartment and target.visiting == ewcfg.location_id_empty:
                        try:
                            await fe_utils.send_message(cmd.client, cmd.mentions[0], fe_utils.formatMessage(cmd.mentions[0], "SMAAASH! A brick flies through your window!"))
                        except Exception as e:
                            ewutils.logMsg("failed to send brick message to user {}:{}".format(target.id_user, e))
                elif target.poi == user_data.poi:
                    if target.life_state == ewcfg.life_state_corpse:
                        response = "You reel back and chuck the brick at a ghost. As much as we both would like to teach the dirty staydead a lesson, the brick passes right through."
                        item.id_owner = target.poi
                        item.persist()
                    elif target.life_state == ewcfg.life_state_kingpin:
                        response = "The brick is hurtling toward the kingpin's head, but they've long since gotten used to bricks to the head. It bounces off like nothing."
                        item.id_owner = target.poi
                        item.persist()
                    else:
                        response = ":bricks::boom: BONK! The brick slams against {}'s head!".format(cmd.mentions[0].display_name)
                        item.id_owner = target.poi
                        item.persist()

                        user_data.change_crime(n=1)
                        user_data.persist()

                        try:
                            await fe_utils.send_message(cmd.client, cmd.mentions[0], fe_utils.formatMessage(cmd.mentions[0], random.choice(["!!!!!!", "BRICK!", "FUCK", "SHIT", "?!?!?!?!?", "BONK!", "F'TAAAAANG!", "SPLAT!", "SPLAPP!", "WHACK"])))
                        except Exception as e:
                            ewutils.logMsg("failed to send brick message to user {}:{}".format(target.id_user, e))
                else:
                    response = "There's nobody here."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            else:
                return await ewitem.itemcmds.discard(cmd=cmd)
        else:
            response = "You don't have that item."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif item_sought:
        item_obj = EwItem(id_item=item_sought.get('id_item'))
        if item_obj.soulbound == True:
            response = "That's soulbound. You can't get rid of it just because you're in a more dramatic looking place."

        elif item_obj.item_type == ewcfg.it_weapon and user_data.weapon >= 0 and item_obj.id_item == user_data.weapon:
            if user_data.weaponmarried:
                weapon = static_weapons.weapon_map.get(item_obj.item_props.get("weapon_type"))
                response = "You decide not to chuck your betrothed off the cliff because you care about them very very much. See {}? I'm not going to hurt you. You don't have to call that social worker again.".format(weapon.str_weapon)
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            else:
                response = item_off(item_sought.get('id_item'), user_data.id_server, item_sought.get('name'))
                user_data.change_crime(n=ewcfg.cr_littering_points)
                user_data.persist()
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:
            response = item_off(item_sought.get('id_item'), user_data.id_server, item_sought.get('name'))
            user_data.change_crime(n=ewcfg.cr_littering_points)
            user_data.persist()

        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    else:
        response = "You don't have that item."
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def jump(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)
    died = False

    # If the player is in any of the mines
    if user_data.poi in juviecmdutils.mines_map:
        response = "You bonk your head on the shaft's ceiling."
        # if voidhole world event is valid, move the guy to the void and post a message
        # else, post something about them bonking their heads
        world_events = bknd_worldevent.get_world_events(id_server=cmd.guild.id)
        for id_event in world_events:
            if world_events.get(id_event) == ewcfg.event_type_voidhole:
                event_data = EwWorldEvent(id_event=id_event)
                if int(event_data.event_props.get('id_user')) == user_data.id_user and event_data.event_props.get('poi') == user_data.poi:
                    response = "You jump in!"
                    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                    await asyncio.sleep(1)

                    user_data.poi = ewcfg.poi_id_thevoid
                    user_data.time_lastenter = int(time.time())
                    user_data.persist()
                    await user_data.move_inhabitants(id_poi=ewcfg.poi_id_thevoid)
                    await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

                    void_poi = poi_static.id_to_poi.get(ewcfg.poi_id_thevoid)
                    wafflehouse_poi = poi_static.id_to_poi.get(ewcfg.poi_id_thevoid)
                    response = "You do a backflip on the way down, bounce on the trampoline a few times to reduce your momentum, and climb down a ladder from the roof, down to the ground. You find yourself standing next to {}, in {}.".format(wafflehouse_poi.str_name, void_poi.str_name)
                    await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, void_poi.channel), fe_utils.formatMessage(cmd.message.author, response), 20)

                    return

    # If a poi has a jump destination specificied, go there.
    elif poi.jump_dest != '':
        resp_cont = EwResponseContainer(client=cmd.client, id_server=user_data.id_server)

        user_data.poi = poi.jump_dest
        poi_dest = poi_static.id_to_poi.get(poi.jump_dest)
        # The blimp's jump destination - becomes wherever the blimp is.
        if user_data.poi == 'blimpland':
            blimp_obj = EwTransport(id_server=user_data.id_server, poi = poi.id_poi)
            user_data.poi = blimp_obj.current_stop
            poi_dest = poi_static.id_to_poi.get(blimp_obj.current_stop)

        # Kill the player if they don't have laaf
        if ewcfg.mutation_id_lightasafeather not in user_data.get_mutations():
            user_data.trauma = ewcfg.trauma_id_environment
            die_resp = await user_data.die(cause=ewcfg.cause_falling)
            died = True
            resp_cont.add_response_container(die_resp)
            response_dest = "SPLAT! A body collides with the asphalt with such force, that it is utterly annihilated, covering bystanders in blood and slime and guts."
        else:
            response_dest = "{} floats in from above!".format(cmd.message.author.display_name)
        user_data.persist()
        response = ewcfg.jump_responses.get(poi.id_poi).format(cmd.message.author.display_name)

        # Secnd messages to channels
        resp_cont.add_channel_response(channel=poi.channel, response=response)
        resp_cont.add_channel_response(channel=poi_dest.channel, response=response_dest)
        if not died:
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
        return await resp_cont.post()
            
    # If the user has Stiltwalker
    elif ewcfg.mutation_id_stiltwalker in user_data.get_mutations():
        blimp_obj = EwTransport(id_server=user_data.id_server, poi = ewcfg.poi_id_blimp)
        # If the user is under the blimp, put them on the blimp.
        if user_data.poi == blimp_obj.current_stop:

            jump_response = "STR-EEEEETCHHHH!!!!"
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, jump_response))
            await asyncio.sleep(1)

            response = "{} steps up from the city streets below. MF built like a pole, swear to god.".format(cmd.message.author.display_name)
            # Change their POI
            user_data.poi = ewcfg.poi_id_blimp
            blimp_poi = poi_static.id_to_poi.get(ewcfg.poi_id_blimp)
            user_data.time_lastenter = int(time.time())
            user_data.persist()
            # Move ghosts, update roles, send messages.
            await user_data.move_inhabitants(id_poi=ewcfg.poi_id_blimp)
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
            await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, blimp_poi.channel), fe_utils.formatMessage(cmd.message.author, response))

            return

        # If the user is in the Waffle House, put them in a random mine.
        elif user_data.poi == ewcfg.poi_id_wafflehouse:

            jump_response = "STR-EEEEETCHHHH!!!!"
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, jump_response))
            await asyncio.sleep(1)
  
            # Choose a random mine
            jump_poi_id = random.choice([ewcfg.poi_id_mine, ewcfg.poi_id_mine_sweeper, ewcfg.poi_id_mine_bubble, ewcfg.poi_id_tt_mines,
                                        ewcfg.poi_id_tt_mines_sweeper, ewcfg.poi_id_tt_mines_bubble, ewcfg.poi_id_cv_mines,
                                        ewcfg.poi_id_cv_mines_sweeper, ewcfg.poi_id_cv_mines_bubble])
            jump_poi = poi_static.id_to_poi.get(jump_poi_id)
            response = "{} steps up from the ever-ethereal Waffle House, a creature of the night emerging from utter nothingness. MF built like Slenderman, swear to god.".format(cmd.message.author.display_name)
            # Change their POI, do all POI-moving checks.
            user_data.poi = jump_poi_id
            user_data.time_lastenter = int(time.time())
            user_data.persist()
            await user_data.move_inhabitants(id_poi=jump_poi_id)
            await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
            await fe_utils.send_message(cmd.client, fe_utils.get_channel(cmd.guild, jump_poi.channel), fe_utils.formatMessage(cmd.message.author, response))

            return

        # Unique flavor for the slime's end cliffs, can't kill self.
        elif user_data.poi == ewcfg.poi_id_slimesendcliffs:
            response = "You take a step into the Slime Sea. Heh, it tickles! You're feeling your legs getting dissolved, dumbass. You take a step out."

        # Otherwise, unique !jump flavor.
        else:
            response = random.choice(comm_cfg.stiltwalker_jump_response)

    # If you're NOT at the cliffs.
    elif cmd.message.channel.name != ewcfg.channel_slimesendcliffs:
        roll = random.randrange(25)
        # Small chance to do parkour
        if roll == 0:
            response = "You start running and taking the momentum to then make the fucking highest jump you've ever done. When you reach the ground, you somehow manage to land a backflip. Damn, guess you were good at parkour in the end!"
        # Bigger chance to fuck up
        if roll >= 1 and roll <=4:
            response = "You start running and taking the momentum to then make the fucking highest jump you've ever done. You fuck up midair and end up landing face first, breaking your teeth. What did you expect?"
        else:
            response = "You jump. Nope. Still not good at parkour."
    
    # Jump off the cliffs
    else:
    # Ghosts and kingpins can't jump
        if user_data.life_state == ewcfg.life_state_corpse:
            response = "You're already dead. You'd just hover above the drop."
        elif user_data.life_state == ewcfg.life_state_kingpin:
            response = "You try to end things right here. Sadly, the gangster sycophants that kiss the ground you walk on grab your ankles in desperation and prevent you from suicide. Oh, the price of fame."

    # Everyone else fucking dies
        else:
            response = "Hmm. The cliff looks safe enough. You imagine, with the proper diving posture, you'll be able to land in the slime unharmed. You steel yourself for the fall, run along the cliff, and swan dive off its steep edge. Of course, you forgot that the Slime Sea is highly corrosive, there are several krakens there, and you can't swim. Welp, time to die."

            # Take all of the player's items
            cliff_inventory = bknd_item.inventory(id_server=cmd.guild.id, id_user=user_data.id_user)
            for item in cliff_inventory:
                item_object = EwItem(id_item=item.get('id_item'))
                # Don't put soulbound items in the sea.
                if item.get('soulbound'):
                    pass

                # If a weapon is equipped or sidearmed, put it directly in the sea's inventory.
                if item_object.item_type == ewcfg.it_weapon:
                    if item.get('id_item') == user_data.weapon or item.get('id_item') == user_data.sidearm:
                        bknd_item.give_item(id_item=item_object.id_item, id_user=ewcfg.poi_id_slimesea, id_server=cmd.guild.id)
                    # Otherwise goes through regular cliff !toss checks.
                    else:
                        item_off(id_item=item.get('id_item'),  item_name=item.get('name'), id_server=cmd.guild.id)

                # If an item is adorned, put it directly into the sea's inventory.
                elif item_object.item_props.get('adorned') == 'true':
                    bknd_item.give_item(id_item=item_object.id_item, id_user=ewcfg.poi_id_slimesea, id_server=cmd.guild.id)

                # Otherwise goes through regular cliff !toss checks.
                else:
                    item_off(id_item=item.get('id_item'),  item_name=item.get('name'), id_server=cmd.guild.id)

        # Kill the player
        user_data.trauma = ewcfg.trauma_id_environment
        die_resp = await user_data.die(cause=ewcfg.cause_cliff)
        if die_resp != EwResponseContainer(id_server=cmd.guild.id):
            await die_resp.post()
    return await fe_utils.send_response(response, cmd)


async def push(cmd):
    user_data = EwUser(member=cmd.message.author)
    districtmodel = EwDistrict(id_server=cmd.guild.id, district=ewcfg.poi_id_slimesendcliffs)

    if cmd.mentions_count == 0:
        response = "You try to push a nearby building. Nope, still not strong enough to move it."
        return await fe_utils.send_response(response, cmd)
    elif cmd.mentions_count >= 2:
        response = "You can't push more than one person at a time."
        return await fe_utils.send_response(response, cmd)

    target = cmd.mentions[0]
    targetmodel = EwUser(member=target)
    target_mutations = targetmodel.get_mutations()
    user_mutations = user_data.get_mutations()

    if targetmodel.poi != user_data.poi:
        response = "You can't {} them because they aren't here.".format(cmd.tokens[0])

    elif cmd.message.channel.name != ewcfg.channel_slimesendcliffs:
        response = random.choice(ewcfg.bully_responses)

        formatMap = {}
        formatMap["target_name"] = target.display_name

        slimeoid_model = EwSlimeoid(id_server=cmd.guild.id, id_user=targetmodel.id_user)
        if slimeoid_model.name != "":
            slimeoid_model = slimeoid_model.name
        else:
            slimeoid_model = ""

        cosmetics = bknd_item.inventory(id_user=targetmodel.id_user, id_server=targetmodel.id_server, item_type_filter=ewcfg.it_cosmetic)
        selected_cos = None
        for cosmetic in cosmetics:
            cosmetic_item = EwItem(id_item=cosmetic.get('id_item'))
            if cosmetic_item.item_props.get('adorned') == "true":
                selected_cos = cosmetic
                break

        if selected_cos is None:
            selected_cos = "PANTS"
        else:
            selected_cos = id_item = selected_cos.get('name')

        formatMap["cosmetic"] = selected_cos.upper()

        if "{slimeoid}" in response:
            if slimeoid_model != "":
                formatMap["slimeoid"] = slimeoid_model
            elif slimeoid_model == "":
                response = "You push {target_name} into a puddle of sludge, laughing at how hopelessly dirty they are."

        response = response.format_map(formatMap)

    elif targetmodel.id_user == user_data.id_user:
        response = "You can't push yourself you FUCKING IDIOT!"

    elif user_data.life_state == ewcfg.life_state_corpse:
        response = "You attempt to push {} off the cliff, but your hand passes through them. If you're going to push someone, make sure you're corporeal.".format(target.display_name)

    elif targetmodel.life_state == ewcfg.life_state_corpse:
        response = "You try to give ol' {} a shove, but they're a bit too dead to be taking up physical space.".format(target.display_name)

    elif (ewcfg.mutation_id_bigbones in target_mutations or ewcfg.mutation_id_fatchance in target_mutations) and (ewcfg.mutation_id_lightasafeather not in target_mutations and ewcfg.mutation_id_airlock not in target_mutations):
        response = "You try to push {}, but they're way too heavy. It's always fat people, constantly trying to prevent your murderous schemes.".format(target.display_name)

    elif targetmodel.life_state == ewcfg.life_state_kingpin:
        response = "You sneak behind the kingpin and prepare to push. The crime you're about to commit is so heinous that you start snickering to yourself, and {} catches you in the act. Shit, mission failed.".format(target.display_name)

    elif ewcfg.mutation_id_lightasafeather in user_mutations or ewcfg.mutation_id_airlock in user_mutations:
        response = "You strain to push {} off the cliff, but your light frame gives you no lifting power.".format(target.display_name)

    else:
        response = "You push {} off the cliff and watch them scream in agony as they fall. Sea monsters frenzy on their body before they even land, gnawing them to jagged ribbons and gushing slime back to the clifftop.".format(target.display_name)

        if ewcfg.mutation_id_lightasafeather in target_mutations or ewcfg.mutation_id_airlock in target_mutations:
            response = "You pick {} up with your thumb and index finger, and gently toss them off the cliff. Wow. That was easy.".format(target.display_name)

        slimetotal = targetmodel.slimes * 0.75
        districtmodel.change_slimes(n=slimetotal)
        districtmodel.persist()

        cliff_inventory = bknd_item.inventory(id_server=cmd.guild.id, id_user=targetmodel.id_user)
        for item in cliff_inventory:
            item_object = EwItem(id_item=item.get('id_item'))
            if item.get('soulbound'):
                pass

            elif item_object.item_type == ewcfg.it_weapon:
                if item.get('id_item') == targetmodel.weapon:
                    bknd_item.give_item(id_item=item_object.id_item, id_user=ewcfg.poi_id_slimesea, id_server=cmd.guild.id)

                else:
                    item_off(id_item=item.get('id_item'), item_name=item.get('name'), id_server=cmd.guild.id)

            elif item_object.item_props.get('adorned'):
                if "slimeoid" in item_object.item_props and item_object.item_props.get("slimeoid"):
                    pass
                else:
                    if "adorned" in item_object.item_props:
                        item_object.item_props["adorned"] = "false"
                    

                    item_object.persist()
                    bknd_item.give_item(id_item=item_object.id_item, id_user=ewcfg.poi_id_slimesea, id_server=cmd.guild.id)

            else:
                item_off(id_item=item.get('id_item'), item_name=item.get('name'), id_server=cmd.guild.id)

        targetmodel.trauma = ewcfg.trauma_id_environment
        die_resp = await targetmodel.die(cause=ewcfg.cause_cliff)

        await die_resp.post()

    return await fe_utils.send_response(response, cmd)


async def purify(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.poi == ewcfg.poi_id_sodafountain:

        if user_data.life_state == ewcfg.life_state_corpse:
            response = "You're too ghastly for something like that. Besides, you couldn't even touch the water if you wanted to, it would just phase right through your ghostly form."
        else:
            if user_data.slimelevel < 50:
                response = "You're not big enough in slime levels to be worthy of purification"
            else:
                response = "You close your eyes and hold out your hands to the gentle waters of the bicarbonate soda fountain..."

                user_data.slimelevel = 1
                user_data.slimes = 0
                # user_data.hardened_sap = 0

                new_weaponskill = int(user_data.weaponskill * 0.75)

                ewutils.weaponskills_clear(id_server=user_data.id_server, id_user=user_data.id_user, weaponskill=new_weaponskill)

                user_data.persist()

                response += "\n\nYou have purified yourself and are now a level 1 slime{}.\nThe bond you've forged with your weapon has grown weaker as a result.".format(user_data.gender)
    else:
        response = "Purify yourself how? With what? Your own piss?"

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def store_item(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    if poi.community_chest != None:
        return await faction_cmds.store(cmd)
    elif poi.is_apartment:
        return await apt_cmds.store_item(cmd)
    # response = "Try that in a DM to ENDLESS WAR."
    else:
        response = "There is no storage here, public or private."
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def crime(cmd):
    user_data = EwUser(member=cmd.message.author)
    forYou = 1
    if cmd.mentions_count > 0:
        forYou = 0
        target_data = EwUser(member = cmd.mentions[0])
        crimestring = cmd_utils.get_crime_level(num=target_data.crime, forYou=forYou)
        response = "{} has commited {} crime. {}".format(cmd.mentions[0].display_name, target_data.crime, crimestring)
    else:
        crimestring = cmd_utils.get_crime_level(num=user_data.crime, forYou=forYou)
        response = "You have commited {} crime. {}".format(user_data.crime, crimestring)

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def remove_item(cmd):
    user_data = EwUser(member=cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    if poi.community_chest != None:
        return await faction_cmds.take(cmd)
    elif poi.is_apartment:
        return await apt_cmds.remove_item(cmd)
    # response = "Try that in a DM to ENDLESS WAR."
    else:
        response = "There is no storage here, public or private."
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def check_flag(cmd):
    response = "https://img.booru.org/rfck//images/2/5c00b9d105d2435546ff6d3d9f545b05650d6631.png"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, response)


""" Accept a russian roulette challenge """


async def accept(cmd):
    user = EwUser(member=cmd.message.author)
    if (ewutils.active_target_map.get(user.id_user) != None and ewutils.active_target_map.get(user.id_user) != ""):
        challenger = EwUser(id_user=ewutils.active_target_map[user.id_user], id_server=user.id_server)
        if (ewutils.active_target_map.get(user.id_user) != user.id_user and ewutils.active_target_map.get(challenger.id_user) != user.id_user):
            ewutils.active_target_map[challenger.id_user] = user.id_user
            slimeoid_data = EwSlimeoid(member=cmd.message.author)
            response = ""
            if user.poi == ewcfg.poi_id_arena and ewutils.active_slimeoidbattles.get(slimeoid_data.id_slimeoid):
                response = "You accept the challenge! Both of your Slimeoids ready themselves for combat!"
            elif user.poi == ewcfg.poi_id_thecasino and ewutils.active_restrictions[challenger.id_user] == 1:
                response = "You accept the challenge! Both of you head out back behind the casino and load a bullet into the gun."

            if len(response) > 0:
                await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Refuse a russian roulette challenge """


async def refuse(cmd):
    user = EwUser(member=cmd.message.author)

    if (ewutils.active_target_map.get(user.id_user) != None and ewutils.active_target_map.get(user.id_user) != ""):
        challenger = EwUser(id_user=ewutils.active_target_map[user.id_user], id_server=user.id_server)

        ewutils.active_target_map[user.id_user] = ""
        ewutils.active_restrictions[user.id_user] = 0

        if (ewutils.active_target_map.get(user.id_user) != user.id_user and ewutils.active_target_map.get(challenger.id_user) != user.id_user):
            response = "You refuse the challenge, but not before leaving a large puddle of urine beneath you."
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:
            ewutils.active_target_map[challenger.id_user] = ""
            ewutils.active_restrictions[challenger.id_user] = 0


async def confirm(cmd):
    return


async def cancel(cmd):
    return


"""
    Link to the world map.
"""


async def map(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, 'Online world map: https://rfck.app/map/'))


"""
    Link to the subway map
"""


async def transportmap(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Map of the subway: https://cdn.discordapp.com/attachments/431237299137675297/1021140587572887653/slimemapfinal.png"))



""" Check your outfit. """

freshseed = random.Random()
async def fashion(cmd):
    if cmd.mentions_count == 0:
        user_data = EwUser(member=cmd.message.author, data_level=2)

        cosmetic_items = bknd_item.inventory(
            id_user=cmd.message.author.id,
            id_server=cmd.guild.id,
            item_type_filter=ewcfg.it_cosmetic
        )

        adorned_cosmetics = []
        adorned_ids = []

        adorned_styles = []

        stats_breakdown = {}

        space_adorned = 0
        market_data = EwMarket(id_server=user_data.id_server)
        freshseed.seed(user_data.fashion_seed + market_data.day)
        bonus_freshness = freshseed.randint(-20, 20)
        if bonus_freshness < -10:
            bonus_response = "You're really having a shit day, and your baggy-ass eyes make you look 5 years older."
        elif bonus_freshness < 0:
            bonus_response = "You're not feeling very photogenic right now."
        elif bonus_freshness < 10:
            bonus_response = "You're feeling well rested, by gangster standards anyway."
        else:
            bonus_response = "You look fantastic. You can smell the followers before you even take a picture."

        for cosmetic in cosmetic_items:
            c = EwItem(id_item=cosmetic.get('id_item'))

            if c.item_props['adorned'] == 'true':

                hue = hue_static.hue_map.get(c.item_props.get('hue'))
                hue2 = c.item_props.get('hue2') # hue2 and pattern hold no importance in the cosmetic's calculation, so no need to go through the hue map for it.
                pattern = c.item_props.get('pattern')
                adorned_styles.append(c.item_props.get('fashion_style'))

                if c.item_props['id_cosmetic'] not in adorned_ids:
                    if any(stat in c.item_props.keys() for stat in ewcfg.playerstats_list):
                        for stat in ewcfg.playerstats_list:
                            if abs(int(c.item_props[stat])) > 0:
                                stats_breakdown[stat] = stats_breakdown.get(stat, 0) + int(c.item_props[stat])

                space_adorned += int(c.item_props['size'])

                adorned_ids.append(c.item_props['id_cosmetic'])
                adorned_cosmetics.append(((hue.str_name if hue is not None else "") + ('/' + hue2 if hue2 is not None else '') + (' ' + pattern + ' ' if pattern is not None else '') + (' ' if hue != None and hue2 == None else '') + cosmetic.get('name'))) # Throws as "red/white striped felinehat if all are not none, throws red felinehat if dye2 and pattern is none."

        # show all the cosmetics that you have adorned.
        if len(adorned_cosmetics) > 0:
            response = "You whip out your smartphone and reverse your camera around to thoroughly analyze yourself.\n\n"
            response += "{} You have a {} adorned. ".format(bonus_response, ewutils.formatNiceList(adorned_cosmetics, 'and'))

            # fashion outfit, freshness rating.
            if len(adorned_cosmetics) >= 2:
                response += "\n\n"

                outfit_map = itm_utils.get_outfit_info(id_user=cmd.message.author.id, id_server=cmd.guild.id)
                user_data.persist()
                
                # If user is wearing all pieces of the a costume set, add text 
                if all(elem in adorned_ids for elem in static_cosmetics.cosmetic_nmsmascot):
                    response += "You're dressed like a fucking airplane with tits, dude."
                elif all(elem in adorned_ids for elem in static_cosmetics.cosmetic_hatealiens):
                    response += "Your taste in clothes is a symbol of hatred to illegal aliens everywhere."
                
                elif outfit_map is not None:
                    response += itm_utils.get_style_freshness_rating(user_data=user_data, dominant_style=outfit_map['dominant_style'])

            response += " Your total freshness rating is {}.\n\n".format(user_data.freshness)

            space_remaining = ewutils.max_adornspace_bylevel(user_data.slimelevel) - space_adorned

            if space_remaining == 0:
                response += "You don't have cosmetic space left."
            else:
                response += "You have about {amount} adornable space.".format(amount=space_remaining)

            # 1/3 chance of slimeoid also being included in the fashion check. No extra flavor text is generated if the slimeoid isn't wearing clothes.
            if random.randint(0, 2) == 0 and user_data.active_slimeoid != -1:
                # Get the slimeoid
                slimeoid = EwSlimeoid(member=cmd.message.author)
                slimeoid_adorned_cosmetics = []

                # Get the slimeoid's adorned cosmetics
                for cosmetic in cosmetic_items:
                    c = EwItem(id_item=cosmetic.get('id_item'))
                    if c.item_props.get('slimeoid') == 'true':
                        slimeoid_hue = hue_static.hue_map.get(c.item_props.get('hue'))
                        slimeoid_adorned_cosmetics.append((slimeoid_hue.str_name + " colored " if slimeoid_hue != None else "") + c.item_props.get('cosmetic_name'))

                # If the slimeoid has adorned cosmetics, generate flavor text.
                if len(slimeoid_adorned_cosmetics) > 0:
                    response += "\n\n{} butts in to the camera view! It has a {} adorned.".format(slimeoid.name, ewutils.formatNiceList(slimeoid_adorned_cosmetics, "and"))

                    # If the slimeoid has more than one adorned cosmetic, give it a freshness rating.
                    if len(slimeoid_adorned_cosmetics) >= 2:
                        outfit_map = itm_utils.get_outfit_info(id_user=cmd.message.author.id, id_server=cmd.guild.id, slimeoid = True)

                        if outfit_map is not None:
                            response += " Its total freshness rating is a {} {}.".format(outfit_map['dominant_style'], outfit_map['total_freshness'])


        else:
            response = "You aren't wearing anything!"

    else:
        member = cmd.mentions[0]
        user_data = EwUser(member=member, data_level=2)

        cosmetic_items = bknd_item.inventory(
            id_user=member.id,
            id_server=cmd.guild.id,
            item_type_filter=ewcfg.it_cosmetic
        )

        adorned_cosmetics = []
        adorned_ids = []

        adorned_styles = []

        stats_breakdown = {}

        space_adorned = 0

        for cosmetic in cosmetic_items:
            c = EwItem(id_item=cosmetic.get('id_item'))

            if c.item_props['adorned'] == 'true':

                hue = hue_static.hue_map.get(c.item_props.get('hue'))
                hue2 = c.item_props.get('hue2')
                pattern = c.item_props.get('pattern')
                adorned_styles.append(c.item_props.get('fashion_style'))

                if c.item_props['id_cosmetic'] not in adorned_ids:
                    if any(stat in c.item_props.keys() for stat in ewcfg.playerstats_list):
                        for stat in ewcfg.playerstats_list:
                            if abs(int(c.item_props[stat])) > 0:
                                stats_breakdown[stat] = stats_breakdown.get(stat, 0) + int(c.item_props[stat])

                space_adorned += int(c.item_props['size'])

                adorned_ids.append(c.item_props['id_cosmetic'])
                adorned_cosmetics.append(((hue.str_name if hue is not None else "") + ('/' + hue2 if hue2 is not None else '') + (' ' + pattern + ' ' if pattern is not None else '') + (' ' if hue != None and hue2 == None else '') + cosmetic.get('name')))

        # show all the cosmetics that you have adorned.
        if len(adorned_cosmetics) > 0:
            response = "You take out your smartphone and tab back over to {}'s Instagrime account to obsessively analyze their latest outfit with a mixture of unearned superiority and unbridled jealousy.\n\n".format(member.display_name)
            response += "They have a {} adorned. ".format(ewutils.formatNiceList(adorned_cosmetics, 'and'))

            # fashion outfit, freshness rating.
            if len(adorned_cosmetics) >= 2:
                response += "\n\n"

                # If user is wearing all pieces of a costume set, add text 
                if all(elem in adorned_ids for elem in static_cosmetics.cosmetic_nmsmascot):
                    response += "They're dressed like a fucking airplane with tits, dude."
                elif all(elem in adorned_ids for elem in static_cosmetics.cosmetic_hatealiens):
                    response += "Their taste in clothes is a symbol of hatred to illegal aliens everywhere."
                elif user_data.freshness < ewcfg.freshnesslevel_1:
                    response += "Their outfit is starting to look pretty fresh, but They’ve got a long way to go if they wanna be NLACakaNM’s next top model."
                elif user_data.freshness < ewcfg.freshnesslevel_2:
                    response += "Their outfit is low-key on point, not gonna lie. They’re goin’ places, kid."
                elif user_data.freshness < ewcfg.freshnesslevel_3:
                    response += "Their outfit is lookin’ fresh as hell, goddamn! They shop so much they can probably speak Italian."
                elif user_data.freshness < ewcfg.freshnesslevel_4:
                    response += "Their outfit is straight up **GOALS!** Like, honestly. I’m being, like, totally sincere right now. Their Instragrime has attracted a small following."
                else:
                    response += "Holy shit! Their outfit is downright, positively, without a doubt, 100% **ON FLEEK!!** They’ve blown up on Instragrime, and they’ve got modeling gigs with fashion labels all across the city."

            response += " Their total freshness rating is {}.\n\n".format(user_data.freshness)

            # gameplay relvant stuff, inspect order

            response += "All told, their outfit "

            stat_responses = []

            for stat in ewcfg.playerstats_list:

                if stat in stats_breakdown.keys():
                    if abs(int(stats_breakdown[stat])) > 0:

                        if int(stats_breakdown[stat]) > 0:
                            stat_response = "increases their "
                        else:
                            stat_response = "decreases their "

                        stat_response += "{stat} by {amount} ".format(stat=stat, amount=int(stats_breakdown[stat]))

                        stat_responses.append(stat_response)  # bye bye

            # Commented out for now. Doesn't do anything except exist
            # if len(stat_responses) == 0:
            #     response += "doesn't affect their stats at all. "
            # else:
            #     response += ewutils.formatNiceList(names=stat_responses, conjunction="and") + ". \n\n"

            space_remaining = ewutils.max_adornspace_bylevel(user_data.slimelevel) - space_adorned

            if space_remaining == 0:
                response += "They don't have cosmetic space left."
            else:
                response += "They have about {amount} adornable space.".format(amount=space_remaining)

            # 1/3 chance of slimeoid also being included in the fashion check. No extra flavor text is generated if the slimeoid isn't wearing clothes.
            if random.randint(0, 2) == 0 and user_data.active_slimeoid != -1:
                # Get the slimeoid
                slimeoid = EwSlimeoid(member=member)
                slimeoid_adorned_cosmetics = []

                # Get the cosmetics worn by the slimeoid
                for cosmetic in cosmetic_items:
                    c = EwItem(id_item=cosmetic.get('id_item'))
                    if c.item_props.get('slimeoid') == 'true':
                        slimeoid_hue = hue_static.hue_map.get(c.item_props.get('hue'))
                        slimeoid_adorned_cosmetics.append((slimeoid_hue.str_name + " colored " if slimeoid_hue != None else "") + c.item_props.get('cosmetic_name'))

                # Create flavor text if the slimeoid is wearing clothes
                if len(slimeoid_adorned_cosmetics) > 0:
                    response += "\n\nThey've also recently posted with their {} {} in the background. It has a {} adorned.".format("Slimeoid" if slimeoid.sltype == ewcfg.sltype_lab else "Negaslimeoid", slimeoid.name, ewutils.formatNiceList(slimeoid_adorned_cosmetics, "and"))

                    # Give the slimeoid a freshness rating if it's wearing more than 1 article of clothing.
                    if len(slimeoid_adorned_cosmetics) >= 2:
                        outfit_map = itm_utils.get_outfit_info(id_user=user_data.id_user, id_server=cmd.guild.id, slimeoid = True)

                        if outfit_map is not None:
                            response += " Its total freshness rating is a {} {}.".format(outfit_map['dominant_style'], outfit_map['total_freshness'])

        else:
            response = "...But they aren't wearing anything!"

    return await fe_utils.send_response(response, cmd)


"""recycle your trash at the SlimeCorp Recycling plant"""


async def recycle(cmd):
    user_data = EwUser(member=cmd.message.author)
    response = ""

    if user_data.poi != ewcfg.poi_id_recyclingplant:
        response = "You can only {} your trash at the Recycling Plant in Smogsburg.".format(cmd.tokens[0])
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)

    if item_sought:
        item = EwItem(id_item=item_sought.get("id_item"))

        if not item.soulbound:
            if item.item_type == ewcfg.it_weapon and user_data.weapon >= 0 and item.id_item == user_data.weapon:
                if user_data.weaponmarried:
                    weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))
                    response = "Woah, wow, hold on there! Domestic violence is one thing, but how could you just throw your faithful {} into a glorified incinerator? Look, we all have bad days, but that's no way to treat a weapon. At least get a proper divorce first, you animal.".format(weapon.str_weapon)
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                else:
                    #user_data.weapon = -1
                    #user_data.persist()
                    response = "Your hard-bitten criminal instincts prevent you from loosening grip on your weapon. Unequip it before trying to recycle it."
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            elif item.item_type == ewcfg.it_weapon and user_data.sidearm >= 0 and item.id_item == user_data.sidearm:
                #user_data.sidearm = -1
                #user_data.persist()
                weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))
                response = "Your hard-bitten criminal instincts prevent you from relaxing your ass cheeks, and you can't get {} out of your back pocket. Get it out of your sidearm slot!".format(weapon.str_weapon)
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            #elif item.item_type == ewcfg.it_relic: i need to learn to let things go and adapt.
            #    relic_mapped = rstatic.relic_map.get(item.item_props.get('id_relic'))
            #    if relic_mapped.has_effect or item.item_props.get('donated') is None or item.item_props.get('donated') == 0:
            #        response = "You reach into your pocket to dispose of this sacrosanct piece of history, but you can't find it! Damn, you've been pickpocketed!"
            #        bknd_item.give_item(id_server=cmd.guild.id, id_user='slimesea', id_item=item.id_item)
            #        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            bknd_item.item_delete(id_item=item.id_item)

            pay = int(random.random() * 10 ** random.randrange(2, 6))
            
            if item.item_props.get('id_furniture') == 'sord':
                response = "You jam the jpeg artifact into the recycling bin. It churns and sputters, desperately trying to turn it into anything of value. Needless to say, it fails. \"get a load of this hornses ass.\" a robotic voice informs you"

                if user_data.slimecoin >= 1:
                    response += ", nabbing 1 SlimeCoin from you out of spite."
                    user_data.change_slimecoin(n=-1, coinsource=ewcfg.coinsource_recycle)
                    user_data.persist()
                else:
                    response += "."
            elif pay == 0:
                item_reward = random.choice(vendors.mine_results)

                item_props = itm_utils.gen_item_props(item_reward)

                bknd_item.item_create(
                    item_type=item_reward.item_type,
                    id_user=cmd.message.author.id,
                    id_server=cmd.guild.id,
                    item_props=item_props
                )

                ewstats.change_stat(user=user_data, metric=ewcfg.stat_lifetime_poudrins, n=1)

                response += "\n\nYou receive a {}!".format(item_reward.str_name)
            elif random.randint(0,99) == 99 and item.item_props.get('id_furniture') != 'sord':
                bknd_item.item_create(
                        item_type=ewcfg.it_item,
                        id_user=cmd.message.author.id,
                        id_server=cmd.guild.id,
                        item_props={
                            'id_item': ewcfg.item_id_discontinuedscrap,
                            'item_name': "Discontinued Scrap",
                            'item_desc': "An unintelligible scrap of material. Completely useless on its own, meant as an ingredient to smelt previously discontinued items from previous or current deadbeat developers.",
                            'context': "discontinuedscrap"
                        }
                    )
                response = "You put your {} into the designated opening. **CRUSH! Splat!** *hiss...* and it's gone. \"Thanks for keeping the city clean.\" a robotic voice informs you.\nOh, and you swindle away something from the recycling plant while nobody is looking.".format(item_sought.get("name"))
                user_data.change_slimecoin(n=pay, coinsource=ewcfg.coinsource_recycle)
                user_data.persist()
            else:
                user_data.change_slimecoin(n=pay, coinsource=ewcfg.coinsource_recycle)
                user_data.persist()

                response += "\n\nYou receive {:,} SlimeCoin.".format(pay)

        else:
            response = "You can't {} soulbound items.".format(cmd.tokens[0])
    else:
        if item_search:
            response = "You don't have one"
        else:
            response = "{} which item? (check **!inventory**)".format(cmd.tokens[0])

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def windowshop(cmd):
    user_data = EwUser(member = cmd.message.author)
    poi = poi_static.id_to_poi.get(user_data.poi)

    if cmd.tokens_count <= 1:
        response = "What are you wistfully gazing at?"
    else:
        value = ewutils.flattenTokenListToString(cmd.tokens[1:]).lower()
        item = static_cosmetics.cosmetic_map.get(value)
        if item is None:
            response = "Whatever that is, it's not in the clothing aisle."
        else:
            market = EwMarket(id_server=cmd.guild.id)

            freshness = bknd_item.get_base_freshness(seed=user_data.fashion_seed, mapkey=value)

            if 'bazaar' in poi.vendors and item.id_cosmetic not in market.bazaar_wares.values():
                response = "They don't sell that here. Not right now, anyway."
            elif 'bazaar' not in poi.vendors and len(set(item.vendors).intersection(poi.vendors)) == 0:
                response = "They don't sell that here."
            elif freshness <= 3:
                response = "Ugh, who decided to start selling {} here? Low key gross, ngl. You could barely squeeze {} freshness out of that garbage.".format(item.str_name, freshness)
            elif freshness <= 6:
                response = "Hard to flex in that, but you do you I guess. Wearing a {} around only nets you {} freshness.".format(item.str_name, freshness)
            elif freshness <= 9:
                response = "That {}'s pretty bussin, ngl ngl. It'll win you {} freshness, maybe not worthy of your socials but it's something.".format(item.str_name, freshness)
            else:
                response = "THAT {} SLAAAAAYS QUEEN! GET THAT {} FRESHNESS, THAT IS FIRE!! 🤯😳😭".format(item.str_name.upper(), freshness)

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    advertise help services
"""


async def help(cmd):
    response = ""
    topic = None
    user_data = EwUser(member=cmd.message.author)
    resp_cont = EwResponseContainer(id_server=cmd.guild.id)



    # help only checks for districts while in game channels

    # checks if user is in a college or if they have a game guide
    gameguide = bknd_item.find_item(item_search="gameguide", id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None, item_type_filter=ewcfg.it_item)

    if user_data.poi == ewcfg.poi_id_neomilwaukeestate or user_data.poi == ewcfg.poi_id_nlacu or gameguide:
        if not len(cmd.tokens) > 1:
            # list off help topics to player at college
            response = "(Use !help [topic] to learn about a topic. Example: \"!help basics\")\n\nWhat would you like to learn about? Topics include: \n"

            # display the list of topics in grouped format
            groups = ewcfg.help_response_group_map
            for group in groups:
                # Get list of topics in group
                group_list = groups[group].copy()

                # Add beginning of response and first topic, remove first topic from list.
                response += "**{}**:  {}".format(group.upper(), group_list[0])
                group_list.pop(0)

                # Add each topic after the first
                if group_list != []:
                    for topic in group_list:
                        response += ", {}".format(topic)
                
                # New line
                response += "\n"

            channel_topics = cmd_utils.channel_help_topics(channel=poi_static.id_to_poi.get(user_data.poi).channel)

            if channel_topics != []:
                response += "\n*Based on your location, you may want to read up on **{}.***\n".format(ewutils.formatNiceList(names=channel_topics, conjunction="**and**"))
            
            response += '\nFor the list of weapons, as well as topics for weapon types, use "!help weapons".'

            resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        else:

            if cmd.tokens[1] == 'juvieman':
                poi = poi_static.id_to_poi.get(user_data.poi)
                if user_data.life_state != ewcfg.life_state_juvenile:
                    response = "No answer. Guess he only responds to juvies."
                elif poi.pvp == False:
                    response = "You're not in danger, dumbass."
                else:
                    enemy = cmbt_utils.find_npc(npcsearch='juvieman', id_server=user_data.id_server)
                    if not enemy:
                        response = "But nobody came. Guess Juvieman's busy."
                    else:
                        enemy.poi = user_data.poi
                        enemy.applyStatus(id_status=ewcfg.status_enemy_hostile_id)
                        enemy.persist()
                        response = "DID SOMEBODY SAY... JUVIEMAN!?"
                        name = "{}{}{}".format('**__', "JUVIEMAN", '__**')
                        return await fe_utils.talk_bubble(response=response, name=name,
                                                          image="https://cdn.discordapp.com/attachments/982703096616599602/996615981407408249/unknown.png",
                                                          channel=cmd.message.channel)
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            topic = ewutils.flattenTokenListToString(cmd.tokens[1:])
            
            # List all weapons and weapon types
            if topic in ["weapon", "weapons"]:
                
                # Initial response
                response = "(Use !help [weapon] to learn about a specific weapon, or !help [weapon type] to learn about the weapon type. Example: \"!help revolver\" / \"!help normal\")\n\nWhat weapon would you like to learn about? All current weapons include:\n"
                
                # Display the list of topics in grouped format
                groups = ewcfg.weapon_response_group_map
                for group in groups:
                    # Get list of topics in group
                    group_list = groups[group].copy()

                    # Add beginning of response and first topic, remove first topic from list.
                    response += "**{}**:  {}".format(group.upper(), group_list[0])
                    group_list.pop(0)

                    # Add each topic after the first
                    if group_list != []:
                        for topic in group_list:
                            response += ", {}".format(topic)
                    
                    # New line
                    response += "\n"

                resp_cont.add_channel_response(cmd.message.channel, response)

            # Manage specifying any response
            elif topic in ewcfg.help_responses:
                # Create and send the response
                response = ewcfg.help_responses[topic]
                resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                
                # Handle Mymutations
                if topic == 'mymutations':
                    mutations = user_data.get_mutations()
                    if len(mutations) == 0:
                        response = "\nWait... you don't have any!"
                        resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                    else:
                        for mutation in mutations:
                            mutation_name = static_mutations.mutations_map[mutation].str_name

                            response = "**{}**: {}".format(mutation_name, ewcfg.mutation_descriptions[mutation])
                            resp_cont.add_channel_response(cmd.message.channel, response)

            else:
                response = 'ENDLESS WAR questions your belief in the existence of such a topic. Try referring to the topics list again by using just !help.'
                resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # User doesn't have a game guide
    else:
        if cmd.tokens_count >= 2 and cmd.tokens[1] == 'juvieman':
            poi = poi_static.id_to_poi.get(user_data.poi)
            if user_data.life_state != ewcfg.life_state_juvenile:
                response = "No answer. Guess he only responds to juvies."
            elif poi.pvp == False:
                response = "You're not in danger, dumbass."
            else:
                enemy = cmbt_utils.find_npc(npcsearch='juvieman', id_server=user_data.id_server)
                if not enemy:
                    response = "But nobody came. Guess Juvieman's busy."
                else:
                    enemy.poi = user_data.poi
                    enemy.applyStatus(id_status=ewcfg.status_enemy_hostile_id)
                    enemy.persist()
                    response = "DID SOMEBODY SAY... JUVIEMAN!?"
                    name = "{}{}{}".format('**__', "JUVIEMAN", '__**')
                    return await fe_utils.talk_bubble(response=response, name=name, image="https://cdn.discordapp.com/attachments/982703096616599602/996615981407408249/unknown.png",  channel=cmd.message.channel)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


        poi = poi_static.id_to_poi.get(user_data.poi)

        # Get topics associated with said channel
        channel_topics = cmd_utils.channel_help_topics(channel=poi.channel, poi=poi)

        if channel_topics != []:
            # Choose a random topic, in case there are > 1
            topic = random.choice(channel_topics)

            # Generate the silly page number for fun
            page_random_class = random.Random(topic)
            page_number = page_random_class.randint(1, 1337)

            # Create a response with a part about the topic name and a reminder about game guides.
            response = "Excerpt from the Game Guide, page {}, on **{}**:\n\n".format(page_number, topic) + ewcfg.help_responses[topic] + "\n\nDon't forget - portable, fully-featured Game Guides can be purchased at Neo Milwaukee State or NLACU for 10,000 slime!"

        else:
            response = ewcfg.generic_help_response

        resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # Send the response to the player.
    await resp_cont.post()


# await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def commands(cmd):
    user_data = EwUser(member=cmd.message.author)
    response = ""
    category = ewutils.flattenTokenListToString(tokens=cmd.tokens[1:])

    # if cmd.tokens_count == 1:
    #     response += "Look up basic commands with **!commands basic**, or a full list with **!commands categories**.\n"

    #     response += location_commands(cmd)
    #     response += mutation_commands(cmd)
    #     response += item_commands(cmd)
    #     response += holiday_commands()
        
    #     return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if "categories" in category or cmd.tokens_count == 1:
        response += "Categories are: \n\n**Basic**: Bread-and-butter commands.\n"\
                                    "**Player Info**: Commands that tell you some of your statistics.\n"\
                                    "**My Items** / **My Location** / **My Mutations** / **My Faction** / **My Race**: Commands for things pertaining to you.\n"\
                                    "**Outside Links**: Links to things such as the map and wiki.\n"\
                                    "**Items**: Show item-related commands.\n"\
                                    "**Combat**: Combat-based commands.\n"\
                                    "**Juvies** / **Enlisted** / **Corpses**: Commands for each life state.\n"\
                                    "**Smelting**: Smelting-related commands.\n"\
                                    "**Cosmetics and Dyes**: Display information on cosmetics and dyes.\n"\
                                    "**Apartments**: Commands for apartments and commands for collections.\n"\
                                    "**Slimeoids**: Slimeoid-related commands.\n"\
                                    "**Trading**: Trading-related commands.\n"\
                                    "**Quadrants**: Quadrant related commands.\n"\
                                    "**Misc**: Miscellaneous commands.\n"\
                                    "**Flavor**: Other shitpost-y type commands.\n"\
                                    "**All Items** / **All Mutations**: All commands for items or mutations.\n"\
                                    "**Holiday**: If an event is going on, display the commands for it.\n\n"\
                                    "You can also check the commands of a specific location using !commands location <district>."

        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if "basic" in category:
        response += "Commands:\n" + ewcfg.basic_commands

    elif ewutils.flattenTokenListToString(tokens=cmd.tokens[1]) == 'location':
        poi_look = ewutils.flattenTokenListToString(tokens=cmd.tokens[2:]) if cmd.tokens_count >= 3 else user_data.poi
        poi_sought = poi_static.id_to_poi.get(poi_look, None)
        if poi_sought:
            command_output = location_commands(cmd=cmd, search_poi=poi_sought.id_poi)
            if command_output != "":
                response += command_output
            else:
                response = "No commands for that region."
        else:
            response = "Not a real place."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif "myitems" in category:
        response += "" + item_commands(cmd)
    elif "mylocation" in category:
        response += "" + location_commands(cmd)
    elif "mymutations" in category:
        response += "" + mutation_commands(cmd)
    elif "myfaction" in category:
        if user_data.life_state == ewcfg.life_state_juvenile:
            response += "Commands:\n" + ewcfg.juvenile_commands
        elif user_data.life_state == ewcfg.life_state_corpse:
            response += "Commands:\n" + ewcfg.corpse_commands
        else:
            if user_data.faction == 'rowdys':
                response += "Commands:\n" + "!thrash: Thrashing is a rowdy's fucking lifeblood.\n"
            elif user_data.faction == 'killers':
                response += "Commands:\n" + "!dab: To dab on some haters.\n"
            response += ewcfg.enlisted_commands
    elif "juvies" in category:
        response += "Commands:\n" + ewcfg.juvenile_commands
    elif "corpses" in category:
        response += "Commands:\n" + ewcfg.corpse_commands
    elif "enlisted" in category:
        response += "Commands:\n" + ewcfg.enlisted_commands
    elif "myrace" in category:
        race = user_data.race
        if ewcfg.race_unique_commands.get(race) is not None:
            response += "Commands:\n" + ewcfg.race_unique_commands.get(race)
        else:
            response += "No racial commands found."
    elif "doublehalloween" in category:
        response += "Commands:\n" + ewcfg.holidaycommands.get("doublehalloween")
    elif "holiday" in category:
        response += "Commands:\n" + holiday_commands(header = False)
    elif "combat" in category:
        response += "Commands:\n" + ewcfg.combat_commands
    #elif "capping" in category:
        #response += "Commands:\n" + ewcfg.capping_commands
    elif "playerinfo" in category:
        response += "Commands:\n" + ewcfg.player_info_commands
    elif "outsidelinks" in category:
        response += "Commands:\n" + ewcfg.external_link_commands
    elif "items" in category and "allitems" not in category:
        response += "Commands:\n" + ewcfg.item_commands
    elif "cosmeticsanddyes" in category:
        response += "Commands:\n" + ewcfg.cosmetics_dyes_commands
    elif "slimeoids" in category:
        response += "Commands:\n" + ewcfg.slimeoid_commands
    elif "smelting" in category:
        response += "Commands:\n" + ewcfg.smelting_commands
    elif "trading" in category:
        response += "Commands:\n" + ewcfg.trading_commands
    elif "quadrants" in category:
        response += "Commands:\n" + ewcfg.quadrant_commands
    elif "misc" in category:
        response += "Commands:\n" + ewcfg.miscellaneous_commands
    elif "flavor" in category:
        response += "Commands:\n" + ewcfg.flavor_commands
    elif "farming" in category:
        response += "Commands:\n" + ewcfg.farm_commands
    elif "apartments" in category:
        response += "Commands:\n" + ewcfg.apartment_commands
    elif "allitems" in category:
        response += "Commands:\n"
        for item in ewcfg.item_unique_commands.keys():
            if item not in relic_static.relic_map.keys():
                response += "\n" + ewcfg.item_unique_commands.get(item)
    elif "allmutations" in category:
        response += "Commands:\n"
        for item in ewcfg.mutation_unique_commands.keys():
            response += "\n" + ewcfg.mutation_unique_commands.get(item)
    elif response == "" or '!' not in response:
        response = "No commands found."

    messageArray = ewutils.messagesplit(stringIn=response)

    for message in messageArray:
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, message))


# return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

""" pure flavor command, howls """


async def cmd_howl(cmd):
    user_data = EwUser(member=cmd.message.author)
    slimeoid = EwSlimeoid(member=cmd.message.author)
    response = ewcfg.howls[random.randrange(len(ewcfg.howls))]

    if (slimeoid.life_state == ewcfg.slimeoid_state_active) and (user_data.life_state != ewcfg.life_state_corpse):
        response += "\n{} howls along with you! {}".format(str(slimeoid.name), ewcfg.howls[random.randrange(len(ewcfg.howls))])
    elif (slimeoid.sltype == ewcfg.sltype_nega) and (user_data.life_state == ewcfg.life_state_corpse):
        response += "\n{} howls along with you! {}".format(str(slimeoid.name), ewcfg.howls[random.randrange(len(ewcfg.howls))])

    await fe_utils.send_response(response, cmd)


async def cmd_moan(cmd):
    user_data = EwUser(member=cmd.message.author)
    slimeoid = EwSlimeoid(member=cmd.message.author)
    response = ewcfg.moans[random.randrange(len(ewcfg.moans))]

    if user_data.race != ewcfg.race_shambler:
        response = "You're not really feeling it... Maybe if you lacked cognitive function, you'd be more inclined to moan, about brains, perhaps."
        return await fe_utils.send_response(response, cmd)

    if (slimeoid.life_state == ewcfg.slimeoid_state_active):
        response += "\n{} moans along with you! {}".format(str(slimeoid.name), ewcfg.moans[random.randrange(len(ewcfg.moans))])

    await fe_utils.send_response(response, cmd)


"""
    Harvest is not and has never been a command.
    (Krak made it a command once you fool)
"""


async def harvest(cmd):
    response = '**HARVEST IS NOT A COMMAND YOU FUCKING IDIOT**'
    await fe_utils.send_response(response, cmd)


"""
    Salute the NLACakaNM flag.
"""


async def salute(cmd):
    response = 'http://165.227.192.207/img/nlacakanm_flag.gif'
    await fe_utils.send_response(response, cmd)


"""
    Burn the NLACakaNM flag.
"""


async def unsalute(cmd):
    response = 'http://165.227.192.207/img/nlacakanm_flag_burning.gif'
    await fe_utils.send_response(response, cmd)


"""
    TFAAAP HURL GIF
"""


async def hurl(cmd):
    response = 'http://165.227.192.207/img/tfaaap-hurl.gif'
    await fe_utils.send_response(response, cmd)


"""
    advertise patch notes
"""


async def patchnotes(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, 'Look for the latest patchnotes on the news page: https://rfck.app/news/'))


"""
    Link to the RFCK wiki.
"""


async def wiki(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, 'Rowdy Fuckers Cop Killers Wiki: https://rfck.miraheze.org/wiki/Main_Page'))


"""
    Link to the fan art booru.
"""


async def booru(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, 'Rowdy Fuckers Cop Killers Booru: http://rfck.booru.org/'))


"""
    Link to the RFCK bandcamp.
"""


async def bandcamp(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, 'Rowdy Fuckers Cop Killers Bandcamp: https://rowdyfuckerscopkillers.bandcamp.com/releases'))


"""
    Link to the Gameplay category in the RFCK wiki
"""


async def tutorial(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, 'In-depth tutorial of all the gameplay mechanics in the Endless War: https://rfck.miraheze.org/wiki/Category:Gameplay'))


"""
    Link to the leaderboards on rfck.app.
"""


async def leaderboard(cmd):
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, 'Live leaderboards: https://rfck.app/stats/'))


async def lol(cmd):
    response = 'You laugh out loud!'
    await fe_utils.send_response(response, cmd)




async def pray(cmd):
    user_data = EwUser(member=cmd.message.author)

    if cmd.message.channel.name != ewcfg.channel_endlesswar:
        response = "You must be in the presence of your lord if you wish to pray to him."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if len(cmd.mention_ids) == 0:
        target_type = "ew"
    else:
        target_type = ewutils.mention_type(cmd, cmd.mention_ids[0])

    # endless war disapoves of praying to others and has a high chance to kill
    if target_type != "ew":
        probabilityofdeath = 20
        diceroll = random.randint(1, 100)

        # don't kill kingpins
        if user_data.life_state != ewcfg.life_state_kingpin and diceroll < probabilityofdeath:
            response = "ENDLESS WAR doesn’t respond. You squint, looking directly into his eye, and think you begin to see particle effects begin to accumulate..."
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            await asyncio.sleep(3)

            user_data = EwUser(member=cmd.message.author)
            user_data.trauma = ewcfg.trauma_id_environment
            die_resp = await user_data.die(cause=ewcfg.cause_praying)
            await die_resp.post()

            response = "ENDLESS WAR completely and utterly obliterates you with a bone-hurting beam."
        else:
            response = "ENDLESS WAR disapproves of this idolatry."
    else:
        if user_data.life_state == ewcfg.life_state_kingpin:

            # kingpins don't die or get poudrins
            responses_list = comm_cfg.pray_responses_list

            if user_data.slimes > 1000000:
                responses_list = responses_list + ["ENDLESS WAR is impressed by your vast amounts of slime."]
            else:
                responses_list = responses_list + ["ENDLESS WAR can’t help but laugh at how little slime you have."]

            response = random.choice(responses_list)
        else:
            # Generates a random integer from 1 to 100. If it is below the prob of poudrin, the player gets a poudrin.
            # If the random integer is above prob of poudrin but below probofpoud+probofdeath, then the player dies. Else,
            # the player is blessed with a response from EW.
            probabilityofpoudrin = 10
            probabilityofdeath = 10
            diceroll = random.randint(1, 100)

            # Redeem the player for their sins.
            market_data = EwMarket(id_server=cmd.guild.id)
            market_data.global_swear_jar = max(0, market_data.global_swear_jar - 3)
            market_data.persist()
            user_data.persist()

            if diceroll < probabilityofpoudrin:  # Player gets a poudrin.
                item = random.choice(vendors.mine_results)

                item_props = itm_utils.gen_item_props(item)

                bknd_item.item_create(
                    item_type=item.item_type,
                    id_user=cmd.message.author.id,
                    id_server=cmd.guild.id,
                    item_props=item_props
                )

                response = "ENDLESS WAR takes pity on you, and with a minor tremor he materializes a {} in your pocket.".format(item.str_name)

            elif diceroll < (probabilityofpoudrin + probabilityofdeath):  # Player gets a face full of bone-hurting beam.
                response = "ENDLESS WAR doesn’t respond. You squint, looking directly into his eye, and think you begin to see particle effects begin to accumulate..."
                await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                await asyncio.sleep(3)

                user_data = EwUser(member=cmd.message.author)
                user_data.trauma = ewcfg.trauma_id_environment
                die_resp = await user_data.die(cause=ewcfg.cause_praying)
                await die_resp.post()

                response = "ENDLESS WAR completely and utterly obliterates you with a bone-hurting beam."

            else:
                responses_list = comm_cfg.pray_responses_list

                if user_data.slimes > 1000000:
                    responses_list = responses_list + ["ENDLESS WAR is impressed by your vast amounts of slime."]
                else:
                    responses_list = responses_list + ["ENDLESS WAR can’t help but laugh at how little slime you have."]

                response = random.choice(responses_list)

    await fe_utils.send_response(response, cmd)


async def check_mastery(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.weapon != -1:
        weapon_item = EwItem(user_data.weapon)
        equipped_type = weapon_item.item_props.get("weapon_type")
    else:
        equipped_type = "unarmed"

    message = "\nYou close your eyes for a moment, recalling your masteries: \n"
    if cmd.mentions_count > 0:
        response = "You can only recall your own weapon masteries!"
    else:
        wepskills = ewutils.weaponskills_get(member=cmd.message.author)
        for skill in wepskills:
            # Now actually grabs the mastery string! Rejoice!
            # In case someone somehow got a fucked up weapon, just skip it and don't think about it
            if static_weapons.weapon_map.get(skill) is None:
                continue
            master_weapon_response = (static_weapons.weapon_map[skill]).str_weaponmaster_self + '\n'
            if master_weapon_response == "\n":
                continue
            # Prints masteries above the mastery threshold as "master" skills, whereas those below are "rookie" skills
            if wepskills[skill] >= 5:
                message += master_weapon_response.format(rank=wepskills[skill] - 4, title="master")
            if wepskills[skill] < 5 and (wepskills[skill] > 0 or skill == equipped_type):
                message += master_weapon_response.format(rank=wepskills[skill], title="rookie")
        response = message

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    SLIMERNALIA COMMANDS
"""


async def festivity(cmd: EwCmd):
    """ Show a player's festivity """
    if len(cmd.mention_ids) == 0:
        target_type = "self"
    else:
        target_type = ewutils.mention_type(cmd, cmd.mention_ids[0])

    if target_type == "ew":
        global_festivity = ewstats.get_stat(id_server=cmd.guild.id, id_user=-1, metric=ewcfg.stat_festivity_global)
        response = "ENDLESS WAR has amassed {:,} festivity. @everyone Yo, Slimernalia!".format(global_festivity)
        # This one has to exit early because it specifically allows @s
        return await fe_utils.send_response(response, cmd, allow_everyone=True, format_ats=False)

    elif target_type == "self":
        user_data = EwUser(member=cmd.message.author)
        response = "You currently have {:,} festivity.".format(user_data.get_festivity())

    elif target_type == "other":
        member = cmd.mentions[0]
        user_data = EwUser(member=member)
        if user_data.id_user == 177731019322032128: #Ben Saint's discord id
            global_festivity = ewstats.get_stat(id_server=cmd.guild.id, id_user=-1, metric=ewcfg.stat_festivity_global)
            response = "Deep in the catacombs beneath Cop Killtown, {}'s holiday hostility grows as he observes the party taking place in the city above. He is filled with {} festivity.".format(member.display_name, -global_festivity)
        else:
            response = "{} currently has {:,} festivity.".format(member.display_name, user_data.get_festivity())

    else:
        response = "Your ceaseless Slimernalia cheer has confused ENDLESS WAR. Try again."

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def wrap(cmd: EwCmd):
    """ Wrap a gift for another player. """
    if cmd.tokens_count != 4:
        response = 'To !wrap a gift, you need to specify a recipient, message, and item, like so:\n```!wrap @munchy#6443 "Sample text." chickenbucket```'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

    if cmd.mentions_count == 0:
        response = "Who exactly are you giving your gift to?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count > 1:
        response = "Back it up man, the rules are one gift for one person!"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    recipient = cmd.mentions[0]
    recipient_data = EwUser(member=recipient)

    member = cmd.message.author
    user_data = EwUser(member=cmd.message.author)

    if recipient_data.id_user == user_data.id_user:
        response = "C'mon man, you got friends, don't you? Try and give a gift to someone other than yourself."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    paper_sought = bknd_item.find_item(item_search="wrappingpaper", id_user=cmd.message.author.id, id_server=cmd.guild.id, item_type_filter=ewcfg.it_item)

    if paper_sought:
        paper_item = EwItem(id_item=paper_sought.get('id_item'))

    if paper_sought and paper_item.item_props.get('context') == ewcfg.context_wrappingpaper:
        paper_name = paper_sought.get('name')
    else:
        response = "How are you going to wrap a gift without any wrapping paper?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    gift_message = cmd.tokens[2]

    item_search = ewutils.flattenTokenListToString(cmd.tokens[3:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id)

    if item_sought:
        item = EwItem(id_item=item_sought.get('id_item'))
        if item.item_type == ewcfg.it_item:
            if item.item_props.get('id_item') == "gift":
                response = "It's already wrapped."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        if item.soulbound:
            response = "It's a nice gesture, but trying to gift someone a Soulbound item is going a bit too far, don't you think?"
        # Check if the item has been gifted before
        elif item.item_props.get('gifted') == "true":
            response = "Alas, regifting is considered a grave sin from Phoebus themselves. Enjoy your gift, or else. {}".format(ewcfg.emote_slimeheart)
        elif not bknd_item.check_inv_capacity(user_data=user_data, item_type=ewcfg.it_item):
            response = ewcfg.str_generic_inv_limit.format(ewcfg.it_item)
        else:
            gift_name = "Gift"

            gift_address = 'To {}, {}. From, {}'.format(recipient.display_name, gift_message, member.display_name, )

            gift_desc = "A gift wrapped in {}. Wonder what's inside?\nThe front of the tag reads '{}'\nOn the back of the tag, an ID number reads **({})**.".format(paper_name, gift_address, item.id_item)

            response = "You shroud your {} in {} and slap on a premade bow. Onto it, you attach a note containing the following text: '{}'.\nThis small act of kindness manages to endow you with Slimernalia spirit, if only a little.".format(item_sought.get('name'), paper_name, gift_address)

            # Make the gifted item marked as gifted so that it can't be regifted once it's gifted
            item.item_props['gifted'] = "true"
            item.persist()

            festivity_value = ewcfg.festivity_gift_base
            bonus = 0
            # Calculate the festivity value of the gift - this changes depending on the type of item wrapped
            # Cosmetic-specific bonuses
            if item.item_type == ewcfg.it_cosmetic:
                gift_freshness = int(item.item_props.get("freshness"))

                bonus += gift_freshness * ewcfg.festivity_gift_cosmetic
                if item.item_props.get("hue"):
                    bonus += ewcfg.festivity_dye_bonus
            # Weapon-specific bonuses
            elif item.item_type == ewcfg.it_weapon:
                gift_kills = int(item.item_props.get("totalkills"))
                gift_type = item.item_props.get("weapon_type")
                gift_wtype = static_weapons.weapon_map.get(gift_type)

                if gift_wtype.acquisition == ewcfg.acquisition_smelting:
                    bonus += ewcfg.festivity_smelt_bonus

                bonus = gift_kills * ewcfg.festivity_gift_weapon

                if item.item_props.get("weapon_name"):
                    bonus += ewcfg.festivity_name_bonus
            # Food-specific bonuses
            elif item.item_type == ewcfg.it_food:
                gift_hunger = int(item.item_props.get("recover_hunger"))
                gift_expiry = float(item.item_props.get("time_expir"))

                if gift_expiry <= time.time():
                    bonus -= ewcfg.festivity_expired_penalty

                bonus += (gift_hunger / 10) * ewcfg.festivity_gift_food
            # Furniture-specific bonuses
            elif item.item_type == ewcfg.it_furniture:
                gift_rarity = item.item_props.get("rarity")
                gift_acquisition = item.item_props.get('acquisition')

                if gift_acquisition == ewcfg.acquisition_smelting:
                    bonus += ewcfg.festivity_smelt_bonus

                if gift_rarity == ewcfg.rarity_plebeian:
                    bonus += ewcfg.festivity_pleb_bonus
                elif gift_rarity == ewcfg.rarity_patrician:
                    bonus += ewcfg.festivity_patr_bonus
                else:
                    bonus += ewcfg.festivity_othr_bonus
            # Phoebus isn't so sure about anything else
            else:
                festivity_value -= ewcfg.festivity_generic_penality

            # Generic bonus
            if item.item_props.get("item_message"):
                bonus += ewcfg.festivity_scrawl_bonus

            festivity_value += bonus

            # Gifts cannot be negative festivity, and gifts cannot go above a max
            festivity_value = max(festivity_value, 1)
            festivity_value = min(festivity_value, ewcfg.festivity_gift_max)

            bknd_item.item_create(
                id_user=cmd.message.author.id,
                id_server=cmd.guild.id,
                item_type=ewcfg.it_item,
                item_props={
                    'item_name': gift_name,
                    'id_item': "gift",
                    'item_desc': gift_desc,
                    'context': gift_address,
                    'acquisition': "{}".format(item_sought.get('id_item')),
                    # flag indicating if the gift has already been given once so as to not have people farming festivity through !giving
                    'gifted': "false",
                    'gift_value': festivity_value,
                    'giftee_id': recipient_data.id_user,
                    'gifter_id': user_data.id_user,
                    'gifter_server': user_data.id_server
                }
            )

            bknd_item.give_item(id_item=item_sought.get('id_item'), id_user=str(cmd.message.author.id) + "gift", id_server=cmd.guild.id)
            bknd_item.item_delete(id_item=paper_item.id_item)


            ewstats.change_stat(id_server=cmd.guild.id, id_user=user_data.id_user, metric=ewcfg.stat_festivity, n=ewcfg.festivity_gift_wrap)


    else:
        if item_search == "" or item_search == None:
            response = "Specify the item you want to wrap."
        else:
            response = "Are you sure you have that item?"
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def eventstage(cmd: EwCmd):
    """ Returns the current event stage. """
    return await fe_utils.send_response(f"Event is currently at Stage {ewcfg.event_stage}.", cmd)

async def yoslimernalia(cmd: EwCmd):
    """ Yo, Slimernalia! """
    ewstats.increment_stat(id_server=cmd.guild.id, id_user=cmd.message.author.id, metric=ewcfg.stat_festivity)
    await fe_utils.send_message(cmd.client, cmd.message.channel, '@everyone Yo, Slimernalia!', filter_everyone=False)

# Admin commands
async def announceeventstage(cmd: EwCmd):
    """ Announces the patch notes for the current/past slimernalia event stages. """
    if not cmd.message.author.guild_permissions.administrator:
        return
    # Unpack tokens, if 'all' is anywhere after the main commad print everything up to where we are currently at
    # e.g. !announcefestivestage when you're at stage 4 will just announce stage 4
    # ! announcefestivestage all when you're at stage 4 will announce stages 1, 2, 3 & 4
    print_all = False
    if "all" in cmd.tokens:
        print_all = True

    await fe_utils.announce_event_stage_increase(cmd.client, cmd.guild, print_all)

    return await fe_utils.send_response("Announced them there stages for ya, sonny!", cmd)


async def seteventstage(cmd):
    """ Allows an admin to set the event stage manually. """
    if not cmd.message.author.guild_permissions.administrator:
        return

    # Verify what the user sent
    if len(cmd.tokens) > 1 and str.isnumeric(cmd.tokens[1]):
        if int(cmd.tokens[1]) <= len(ewcfg.event_stage_announcements):
            ewcfg.event_stage = int(cmd.tokens[1])
            response = f"Set event stage to {ewcfg.event_stage}"
        else:
            response = f"Wuh? There's only {len(ewcfg.event_stage_announcements)} stages."
    else:
        response = "It's !seteventstage <int>."

    return await fe_utils.send_response(response, cmd)


async def slimecoin(cmd):
    """ Show player's slimecoin balance """
    if cmd.mentions_count == 0:
        user_data = EwUser(member=cmd.message.author)
        coins = user_data.slimecoin
        response = "You have {:,} SlimeCoin.".format(coins)


    else:
        member = cmd.mentions[0]
        user_data = EwUser(member=member)
        coins = user_data.slimecoin
        response = "{} has {:,} SlimeCoin.".format(member.display_name, coins)

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" show player's shares in a stock """


async def shares(cmd):
    user_data = EwUser(member=cmd.message.author)

    stock = ""
    response = ""

    if cmd.tokens_count > 0:
        stock = ewutils.flattenTokenListToString(cmd.tokens[1:])

    if stock in ewcfg.stocks:
        response = get_user_shares_str(id_server=user_data.id_server, id_user=user_data.id_user, stock=stock)

    elif stock == "":
        for stock in ewcfg.stocks:
            response += "\n"
            response += get_user_shares_str(id_server=user_data.id_server, id_user=user_data.id_user, stock=stock)

    else:
        response = "That's not a valid stock name, please use a proper one, you cunt: {}".format(ewutils.formatNiceList(ewcfg.stocks))

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    SWILLDERMUK COMMANDS
"""


async def prank(cmd):
    # User must have the Janus Mask adorned, and must use the command in a capturable district's channel
    user_data = EwUser(member=cmd.message.author)

    if (ewutils.channel_name_is_poi(cmd.message.channel.name) == False):  # or (user_data.poi not in poi_static.capturable_districts):
        response = "The powers of the mask don't really resonate with you here."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    mentions_user = False
    use_mention_displayname = False
    if cmd.mentions_count > 0:
        mentions_user = True

    cosmetics = bknd_item.inventory(
        id_user=user_data.id_user,
        id_server=user_data.id_server,
        item_type_filter=ewcfg.it_cosmetic
    )
    adorned_cosmetics = []

    response = "You aren't funny enough to do that. Please be funnier."  # If it's not overwritten

    for cosmetic in cosmetics:
        cos = EwItem(id_item=cosmetic.get('id_item'))
        if cos.item_props['adorned'] == 'true':
            if cos.item_props['rarity'] == 'Swilldermuk':
                # print('success')

                item_action = ""
                use_mention_displayname = False
                reroll = True
                item = None

                while reroll:
                    rarity_roll = random.randrange(10)

                    if rarity_roll > 3:
                        prank_item = random.choice(static_items.prank_items_heinous)
                    elif rarity_roll > 0:
                        prank_item = random.choice(static_items.prank_items_scandalous)
                    else:
                        prank_item = random.choice(static_items.prank_items_forbidden)

                    item_props = itm_utils.gen_item_props(prank_item)

                    # Set the user ID to 0 so it can't be given, looted, etc, before it gets deleted.
                    prank_item_id = bknd_item.item_create(
                        item_type=prank_item.item_type,
                        id_user=0,
                        id_server=user_data.id_server,
                        item_props=item_props
                    )

                    item = EwItem(id_item=prank_item_id)

                    if (item.item_props['prank_type'] != ewcfg.prank_type_trap and mentions_user) or (item.item_props['prank_type'] == ewcfg.prank_type_trap and not mentions_user):
                        # Don't reroll the item choice.
                        reroll = False

                response = ''
                pluck_response = "With the power of the Janus Mask, {} plucks a prank item from the ether!\n".format(cmd.message.author.display_name)

                if item.item_props['prank_type'] == ewcfg.prank_type_instantuse:
                    item_action, response, use_mention_displayname, side_effect = await prank_utils.prank_item_effect_instantuse(cmd, item)
                    if side_effect != "":
                        response += await itm_utils.perform_prank_item_side_effect(side_effect, cmd=cmd)

                    response = pluck_response + response

                elif item.item_props['prank_type'] == ewcfg.prank_type_response:
                    item_action, response, use_mention_displayname, side_effect = await prank_utils.prank_item_effect_response(cmd, item)
                    if side_effect != "":
                        response += await itm_utils.perform_prank_item_side_effect(side_effect, cmd=cmd)
                    
                    response = pluck_response + response

                elif item.item_props['prank_type'] == ewcfg.prank_type_trap:
                    item_action, response, use_mention_displayname, side_effect = await prank_utils.prank_item_effect_trap(cmd, item)

                    response = pluck_response + response

                if item_action == "delete":
                    bknd_item.item_delete(item.id_item)
                # prank_feed_channel = fe_utils.get_channel(cmd.guild, ewcfg.channel_prankfeed)
                # await fe_utils.send_message(cmd.client, prank_feed_channel, fe_utils.formatMessage((cmd.message.author if use_mention_displayname == False else cmd.mentions[0]), (response + "\n`-------------------------`")))

                elif item_action == "drop":
                    bknd_item.give_item(id_user=(user_data.poi + '_trap'), id_server=item.id_server, id_item=item.id_item)

                break

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage((cmd.message.author if use_mention_displayname == False else cmd.mentions[0]), response))


"""
    ENCYCLOPEDIC COMMANDS
"""

# Gaiaslimeoids and Shamblers
async def almanac(cmd):
    if not cmd.tokens_count > 1:
        enemy_counter = 0
        enemy_total = 0
        # list off help topics to player at college
        response = "(Use !almanac [enemy] to learn about a shambler/gaiaslimeoid. Example: '!almanac defaultshambler')\nWhat would you like to learn about? Topics include: \n\n"

        # display the list of topics in order
        enemies = ewcfg.gvs_almanac

        response += "------------------------------GAIASLIMEOIDS-------------------------------\n"

        # enemies = ewcfg.cmd_gvs_almanac.keys()
        for enemy in enemies:
            enemy_counter += 1
            enemy_total += 1
            response += "**{}**".format(enemy)
            if enemy_total != len(enemies):
                response += ", "

            if enemy_counter == 5:
                response += "\n"
            elif 5 < enemy_counter < 21 and (enemy_counter + 3) % 4 == 0:
                response += "\n"
            elif enemy_counter == 21:
                response +="\n--------------------------------SHAMBLERS----------------------------------\n"
            elif enemy_counter > 21 and (enemy_counter + 3) % 4 == 0:
                response +="\n"

    else:
        enemytype = ewutils.flattenTokenListToString(cmd.tokens[1:])
        if enemytype in ewcfg.gvs_almanac:
            response = ewcfg.gvs_almanac[enemytype]
        else:
            response = 'ENDLESS WAR questions your belief in the existence of such a shambler or gaiaslimeoid. Try referring to the ones in the list again by using just !almanac.'

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    
"""
    DEBUG COMMANDS
"""


# Debug
async def set_slime(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    response = ""
    target = None

    if cmd.mentions_count != 1:
        # If no user is @'d, try for a POI.
        poi = poi_static.id_to_poi.get(cmd.tokens[1])
        # Can't match to a POI
        if poi == None:
            response = "Invalid use of command. Example: !setslime @player 100"
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:
            # Get district data & number entered
            district_data = EwDistrict(id_server=cmd.guild.id, district=poi.id_poi)
            new_slime = ewutils.getIntToken(tokens=cmd.tokens, allow_all=True)
            if new_slime == None:
                response = "Invalid number entered."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))            
            district_data.slimes = new_slime
            district_data.persist()
            # Send message
            response = "Set {}'s slime to {:,}.".format(poi.str_name, new_slime)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        target = cmd.mentions[0]

    target_user_data = EwUser(id_user=target.id, id_server=cmd.guild.id)

    if len(cmd.tokens) > 2:
        new_slime = ewutils.getIntToken(tokens=cmd.tokens, allow_all=True)
        if new_slime == None:
            response = "Invalid number entered."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        new_slime -= target_user_data.slimes

        if len(cmd.tokens) > 3: # Give negative slime if anything after the int. lazy
            new_slime = -ewutils.getIntToken(tokens=cmd.tokens, allow_all=True)
            new_slime -= target_user_data.slimes

    else:
        return

    if target_user_data != None:

        user_initial_level = target_user_data.slimelevel
        levelup_response = target_user_data.change_slimes(n=new_slime)

        was_levelup = True if user_initial_level < target_user_data.slimelevel else False

        if was_levelup:
            response += " {}".format(levelup_response)
        target_user_data.persist()

        response = "Set {}'s slime to {:,}.".format(target.display_name, target_user_data.slimes)
    else:
        return

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


# Debug
async def check_stats(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    response = ""

    if cmd.mentions_count != 1:
        response = "Invalid use of command. Example: !checkstats @player "
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        target = cmd.mentions[0]

    target_user_data = EwUser(id_user=target.id, id_server=cmd.guild.id, data_level=2)

    if target_user_data != None:
        response = "They have {} attack, {}  defense, and {} speed.".format(target_user_data.attack, target_user_data.defense, target_user_data.speed)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


# Give Brimstone Programmer role to a member
async def make_bp(cmd):
    #return
    if EwUser(member=cmd.message.author).life_state != ewcfg.life_state_kingpin and not cmd.author_id.admin:
        return

    if  cmd.mentions_count > 0 and cmd.mentions[0].id != 324283333984911361:
        response = 'We were only going to give admin to Danny this time around.'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif cmd.mentions_count > 0:
        recipient = cmd.mentions[0]
    else:
        response = 'who?'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    bp_role = None
    for role in cmd.guild.roles:
        if role.name == "Brimstone Programmer":
            bp_role = role
            break

    if bp_role:
        await recipient.add_roles(bp_role)
    else:
        ewutils.logMsg("Could not find Brimstone Programmer role.")


# pings user
async def ping_me(cmd):
    author = cmd.message.author
    user_data = EwUser(member=author)

    if not (ewutils.DEBUG or author.guild_permissions.administrator or user_data.life_state == ewcfg.life_state_kingpin):
        return

    try:
        requested_channel = cmd.tokens[1]
    except:
        return

    pinged_poi = poi_static.id_to_poi.get(requested_channel)
    channel = fe_utils.get_channel(cmd.guild, pinged_poi.channel)

    if pinged_poi != None:
        response = user_data.get_mention()
        return await fe_utils.send_message(cmd.client, channel, response)


async def shut_down_bot(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return await wep_cmds.suicide(cmd=cmd)

    ewutils.logMsg('Goodbye!')
    await asyncio.sleep(2)

    while True:
        sys.exit()

async def set_debug_option(cmd):
    response = ""
    if ewutils.DEBUG == True:
        if len(cmd.tokens) == 3:
            option = cmd.tokens[1].lower()
            value = cmd.tokens[2].lower()

            ewutils.DEBUG_OPTIONS.get(option)
            if option != None:
                if value == 'true':
                    ewutils.DEBUG_OPTIONS[option] = True
                    response = "{option} = {value}".format(option=option, value=value)

                elif value == 'false':
                    ewutils.DEBUG_OPTIONS[option] = False
                    response = "{option} = {value}".format(option=option, value=value)

                else:
                    response = "State whether debug option should be true or false."
            else:
                response = "Invalid debug option."
        else:
            response = "Command format: {} [option] [true/false]".format(ewcfg.cmd_set_debug_option)
    else:
        response = "ENDLESS WAR pays you no mind."

    return await fe_utils.send_response(response, cmd)





async def check_bot(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return
    ewutils.logMsg('TERMINATE is currently: {}'.format(ewutils.TERMINATE))

    return
    sys.exit()


"""
    Ban a player from participating in the game
"""


async def arrest(cmd):
    author = cmd.message.author


    if not 0 < ewrolemgr.check_clearance(member=author) < 4:
        return await cmd_utils.fake_failed_command(cmd)
    market = EwMarket(id_server=cmd.guild.id)
    time_done = ""



    if cmd.mentions_count == 1:
        member = cmd.mentions[0]
        if 0 < ewrolemgr.check_clearance(member=member) < 4:
            response = "I'm sorry, {}. I can't let you do that.".format(cmd.message.author)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        if cmd.tokens_count == 3 and cmd.tokens[2].isnumeric():
            length = int(cmd.tokens[2])
            time_done = " for {} days. They'll be released on Day {}, RFCK Standard Time".format(length, market.day + (length * 4))
        else:
            length = 9999


        user_data = EwUser(member=member)
        user_data.arrested = market.day + (length * 4)

        user_data.poi = ewcfg.poi_id_thesphere
        user_data.change_slimes(n=- user_data.slimes)
        user_data.persist()

        response = "{} is thrown into one of the Juvenile Detention Center's high security solitary confinement spheres{}.".format(member.display_name, time_done)
        await ewrolemgr.updateRoles(client=cmd.client, member=member)
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        leak_channel = fe_utils.get_channel(server=cmd.guild, channel_name='squickyleaks')
        await fe_utils.send_message(cmd.client, leak_channel, "<@!{}>: Arrested {}{}.".format(cmd.message.author.id, member.display_name, time_done), filter_everyone=False)



"""
    Allow a player to participate in the game again
"""


async def release(cmd):

    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        return await cmd_utils.fake_failed_command(cmd)

    if cmd.mentions_count == 1:
        member = cmd.mentions[0]
        user_data = EwUser(member=member)
        user_data.arrested = 0

        user_data.poi = ewcfg.poi_id_juviesrow
        user_data.persist()

        response = "{} is released. But beware, the cops will be keeping an eye on you.".format(member.display_name)
        await ewrolemgr.updateRoles(client=cmd.client, member=member)
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        leak_channel = fe_utils.get_channel(server=cmd.guild, channel_name='squickyleaks')
        await fe_utils.send_message(cmd.client, leak_channel, "<@!{}>: Released {}.".format(cmd.message.author.id, member.display_name), filter_everyone=False)


async def dual_key_ban(cmd):
    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        return await cmd_utils.fake_failed_command(cmd)
    final_ban_text = ""

    player = None
    member = None

    if cmd.mentions_count == 1:
        # Raw mentions so we can even grab the funny ones
        mention_id = cmd.message.raw_mentions[0]
        member = await fe_utils.get_member(cmd.message.guild, mention_id)

    if len(cmd.tokens) >= 2 and str.isnumeric(cmd.tokens[1]):
        mention_id = cmd.tokens[1]
        member = await fe_utils.get_member(cmd.message.guild, mention_id)

    if member is not None:
        # If the person you're trying to dualkey is also a mod/admin/etc.
        if 0 < ewrolemgr.check_clearance(member=member) < 4:
            response = f"I'm sorry, {cmd.message.author.display_name}. I can't let you do that."
            return await fe_utils.send_response(response, cmd)
        player = EwPlayer(id_user=member.id, id_server=cmd.message.guild.id)

    if player is not None:
        target_data = EwUser(id_user=player.id_user, id_server=player.id_server)

        bannedalready = False
        for ban in target_data.get_bans():
            if 'dualkey' in ban:
                if int(ban[7:]) == cmd.message.author.id:
                    bannedalready =True
                else:
                    yourban = "dualkey{}".format(cmd.message.author.id)
                    if yourban not in target_data.get_bans():
                        target_data.ban(faction="dualkey{}".format(cmd.message.author.id))
                    response = "You banish {} into the torturous depths of somewhere else. They're in a better place now. What a shame.".format(member.display_name)
                    final_ban_text = "{} is now banned.".format(member.display_name)
                    try:
                        await member.ban(reason="Dual key banned.")
                    except:
                        response = "Ban failed. Were they out of the server? Either way, your key's in."
                        leak_channel = fe_utils.get_channel(server=cmd.guild, channel_name='squickyleaks')

                        await fe_utils.send_message(cmd.client, leak_channel, "{} has turned their key to ban {}, but they left the server already.".format(cmd.message.author.display_name, member.display_name, final_ban_text))

                        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

                    leak_channel = fe_utils.get_channel(server=cmd.guild, channel_name='squickyleaks')
                    await fe_utils.send_message(cmd.client, leak_channel, "<@!{}> has turned their key to ban {}. They are now banned.".format(cmd.message.author.id, member.display_name, final_ban_text), filter_everyone=False)

                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        if bannedalready:
            response = "You already banned them, but nobody else has."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        target_data.ban(faction="dualkey{}".format(cmd.message.author.id))

        leak_channel = fe_utils.get_channel(server=cmd.guild, channel_name='squickyleaks')
        await fe_utils.send_message(cmd.client, leak_channel, "{} has turned their key to ban {}.".format(cmd.message.author.display_name, member.display_name, final_ban_text))


        response = "You turn your key. {} is just one step away from banishment...".format(member.display_name)
        return await fe_utils.send_response(response, cmd)
    else:
        response = "Either your syntax is wrong or they're out of the server. It's either !dualkeyban @player or !dualkeyban <ID>."
        return await fe_utils.send_response(response, cmd)


async def dual_key_release(cmd):
    if not 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:
        return await cmd_utils.fake_failed_command(cmd)
    response = ""
    final_unban_text = ""
    player = None
    member = None

    if cmd.mentions_count == 1:
        # Raw mentions so we can even grab the funny ones
        mention_id = cmd.message.raw_mentions[0]
        member = await fe_utils.get_member(cmd.message.guild, mention_id)

    if len(cmd.tokens) >= 2 and str.isnumeric(cmd.tokens[1]):
        mention_id = cmd.tokens[1]
        member = await fe_utils.get_member(cmd.message.guild, mention_id)

    if member is not None:
        # If the person you're trying to dualkey is also a mod/admin/etc.
        if 0 < ewrolemgr.check_clearance(member=member) < 4:
            response = f"I'm sorry, {cmd.message.author.display_name}. I can't let you (un)do that."
            return await fe_utils.send_response(response, cmd)
        player = EwPlayer(id_user=member.id, id_server=cmd.message.guild.id)

    if player is not None:
        target_data = EwUser(id_user=int(player.id_user), id_server = cmd.guild.id)

        bans = target_data.get_bans()
        key = 'dualkey{}'.format(cmd.message.author.id)
        response = "You never banned them to begin with. "

        if key in bans:
            target_data.unban(faction=key)
            response = "You take your ban key out of the slot. "
            bans.remove(key)

        ban_count = 0
        for ban in bans:
            if 'dualkey' in ban:
                ban_count += 1
        if ban_count < 2:
            async for ban in cmd.guild.bans():
                if ban.user.id == player.id_user:
                    await cmd.guild.unban(ban.user)
                    final_unban_text = "{} is unbanned!".format(member.display_name)
            response += final_unban_text

        if "You never banned them to begin with." not in response:
            leak_channel = fe_utils.get_channel(server=cmd.guild, channel_name='squickyleaks')

            await fe_utils.send_message(cmd.client, leak_channel, "{} has undone their key to ban {}.{}".format(cmd.message.author.display_name, member.display_name, final_unban_text))

        return await fe_utils.send_message(cmd.client, cmd.message.channel,fe_utils.formatMessage(cmd.message.author, response))
    else:
        response = "They haven't been in the server before or your syntax is wrong. It's !dualkeyrelease @player or !dualkeyrelease <ID>."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



async def post_leaderboard(cmd):
    author = cmd.message.author
    if not author.guild_permissions.administrator:
        return
    user_data = EwUser(member=author)
    client = cmd.client
    server = client.get_guild(user_data.id_server)
    # Check for permissions
    await bknd_leaderboard.post_leaderboards(client=client, server=server)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, "Yee-haw! Just refreshed that their leaderboard for ya sonny!")


"""
    Grants executive status
"""


async def promote(cmd):
    author = cmd.message.author

    if not author.guild_permissions.administrator:
        return

    if cmd.mentions_count == 1:
        member = cmd.mentions[0]
        user_data = EwUser(member=member)
        user_data.life_state = ewcfg.life_state_executive
        user_data.faction = ewcfg.faction_slimecorp
        user_data.persist()

        await ewrolemgr.updateRoles(client=cmd.client, member=member)


async def unban_manual(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return
    if len(cmd.tokens) == 2:
        id = int(cmd.tokens[1])
        user_obj = cmd.client.get_user(id)
        await cmd.guild.unban(user_obj)
        response = "Success"
    else:
        response = "Failure {}".format(len(cmd.mentions))
    await fe_utils.send_message(cmd.client, cmd.message.channel, response)


async def assign_status_effect(cmd = None, status_name = None, user_id = None, server_id = None):
    if status_name is not None:
        user_data = EwUser(id_server=server_id, id_user=user_id)
        response = user_data.applyStatus(id_status=status_name, source=user_id, id_target=user_id)
    else:
        if not cmd.message.author.guild_permissions.administrator or cmd.mentions_count == 0:
            return await cmd_utils.fake_failed_command(cmd)
        target = cmd.mentions[0]
        status_name = ewutils.flattenTokenListToString(cmd.tokens[2:])
        user_data = EwUser(member=target)
        response = user_data.applyStatus(id_status=status_name, source=user_data.id_user, id_target=user_data.id_user)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def print_cache(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    if len(cmd.tokens) > 1:
        target_id = cmd.tokens[1]
        cache = bknd_core.get_cache("EwItem")

        if cache is not False:
            target = cache.get_entry(unique_vals={"id_item": target_id})
            if target is not False:
                ewutils.logMsg("Target Item Data: \n{}".format(target))
                return

        ewutils.logMsg("No item with specified id found.")
        return

    typelog = "*{}*: Current cache types are: \n".format(cmd.message.author.display_name)
    datalog = ""

    for cache in bknd_core.caches:
        typelog += "    {} with {} entries\n".format(cache.entry_type, len(cache.entries))
        datalog += "\n{} Cache contains:\n".format(cache.entry_type)

        if len(cache.entries) < 5000:
            entry_iter = 0
            for entry_id, entry in cache.entries.items():
                datalog += "    Identifier: {}, Data: {}\n".format(entry_id, entry)
                entry_iter += 1
                if entry_iter % 1000 == 0:
                    ewutils.logMsg("Building string for cache, this may take a bit...")
        else:
            datalog += "    Over 5000 entries. Please specify one.\n"

    ewutils.logMsg(typelog)
    ewutils.logMsg(datalog)


async def toggle_cache(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    response = "Command is used as follows: **!togglecache [1 or 0] [Name of cached object type]**"
    # Ensure correct token count
    if len(cmd.tokens) == 3:
        # Dont break if they pass incorrect arguments
        try:
            # Extract arguments
            desired_status = int(cmd.tokens[1])
            target_cache = cmd.tokens[2]

            # If they want the cache enabled
            if desired_status:
                # If the cache is allowed and not already enabled, initialize it
                if (target_cache in ewcfg.cacheable_types) and (target_cache not in bknd_core.enabled_caches):
                    bknd_core.enabled_caches.append(target_cache)
                    response = "Caching of {}s has been enabled.\n".format(target_cache)

                    bknd_core.ObjCache(ew_obj_type=target_cache)
                    response += "{} cache has been initialized.\n".format(target_cache)
                # If the cache is already enabled, tell them
                elif (target_cache in ewcfg.cacheable_types):
                    response = "Caching of {}s was already enabled.\n".format(target_cache)
                # Dont allow caching on non-configured types
                else:
                    response = "Caching of {}s is disabled in cfg. Cannot be enabled.\n".format(target_cache)

            else:
                # disable if it is enabled
                if target_cache in bknd_core.enabled_caches:
                    bknd_core.enabled_caches.remove(target_cache)
                    response = "Caching of {}s has been disabled.\n".format(target_cache)

                # remove the object from the list and delete it
                for potential_victim in bknd_core.caches:
                    if potential_victim.entry_type == target_cache:
                        bknd_core.caches.remove(potential_victim)
                        del potential_victim
                        response += "{} cache has been deleted.\n".format(target_cache)

        # Uh-oh, someone used the command wrong. teach them how
        except ValueError:
            response = "Command failed to convert str to int."
            response += " Structure of command is !togglecache (1 for on or 0 for off) (name of object type)."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def verify_cache(cmd):
    # Only allow admins to use this
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    # Get items how find_item would
    server_id = cmd.guild.id
    server_items = bknd_item.inventory(id_server=server_id)

    # Iterate through all items
    for item_data in server_items:
        # log the ID and data if it fails where find_item would
        try:
            flat_name = ewutils.flattenTokenListToString(item_data.get("name"))
        except:
            ewutils.logMsg("Item {}'s name failed flattening. Data: \n{}".format(item_data.get("id_item"), item_data))

    return


"""
    Admin-only commands to create or control world events
"""
async def manual_poi_event_create(cmd):
    # Only allow admins to use this
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    pre_chosen_event = None
    pre_chosen_poi = None
    pre_chosen_buffer = None
    pre_chosen_length = None

    if len(cmd.tokens) > 1:
        pre_chosen_event = cmd.tokens[1]
        if pre_chosen_event == "random":
            pre_chosen_event = None
    else:
        response = "Invalid use of command. Correct format is \"!createpoievent <event> [id_poi] [buffer] [length]\". A correct example would be *\"!createpoievent tornado downtown 24 4\"*. \nEvent can be specified as \"random\"."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if len(cmd.tokens) > 2:
        pre_chosen_poi = cmd.tokens[2]

        if len(cmd.tokens) > 3:
            if cmd.tokens[3] == "true":
                pre_chosen_buffer = 0
            else:
                pre_chosen_buffer = int(cmd.tokens[3])
        
            if len(cmd.tokens) > 4:
                pre_chosen_length = cmd.tokens[4]

    await weather_utils.create_poi_event(id_server=cmd.guild.id, pre_chosen_event=pre_chosen_event, pre_chosen_poi=pre_chosen_poi, pre_chosen_buffer=pre_chosen_buffer, pre_chosen_length=pre_chosen_length)

    response = "POI event created."
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def list_worldevents(cmd):
    # Only allow admins to use this
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    activeonly = True
    response = "The current world events are:\n"

    # Allow one to see inactive worldevents as well
    if len(cmd.tokens) > 1:
        inactive = cmd.tokens[1]
        if inactive in ["inactive", "all", "1", "true"]:
            activeonly = False
            response = "Current time is {}.\nAll world events in the database:\n".format(int(time.time()))

    world_events = bknd_worldevent.get_world_events(id_server=cmd.guild.id, active_only=activeonly)
    for id_event in world_events:
        event_data = bknd_worldevent.EwWorldEvent(id_event=id_event)
        poi = ""

        if 'poi' in event_data.event_props:
            poi = ", POI is {}".format(event_data.event_props.get('poi'))

        if not activeonly:
            # Get the activation and expiry time
            try:
                poi += ", time_activate is {}, time_expir is {}".format(event_data.time_activate, event_data.time_expir)
            except:
                poi += ", error with time_activate and/or time_expir"

        response += "\n{}: Event type is {}{}.".format(id_event, event_data.event_type, poi)
    
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def end_worldevent(cmd):
    # Admins only creep (weirdo)
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    event_end_id = cmd.tokens[1]
    event_data = bknd_worldevent.EwWorldEvent(id_event=event_end_id)

    event_data.time_expir = 10

    event_data.persist()

    response = "Worldevent {} has been ended.".format(event_end_id)
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
    Admin only command to force the bot to double check for a member
"""
async def user_search(cmd):
    # Only allow admins to use this
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    # Set response for incorrect usage
    response = fe_utils.formatMessage(cmd.message.author, "Incorrect Usage. Please try `{cm} <user snowflake>` or `{cm} <user mention>`.".format(cm=cmd.tokens[0]))

    # Ensure correct terms are sent
    if len(cmd.mentions) != 1 and len(cmd.tokens) != 2:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

    # Parse search terms
    if len(cmd.mentions) == 1:
        target_id = cmd.mentions[0].id
    else:
        # Convert id without mention to integer, tell correct usage if incorrect
        try:
            target_id = int(cmd.tokens[1])
        except ValueError:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

    # Actually commit the search
    found = await fe_utils.get_member(cmd.guild, target_id)

    # Create and send response based on what was returned
    if found is None:
        response = "Failed to find user with id **{}**.".format(target_id)
    else:
        response = "Found user **{}** from id **{}**.".format(found.display_name, target_id)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def cockdraw(cmd):
    user_data = EwUser(member=cmd.message.author)
    command_used = str(cmd.tokens[0])
    cosmetics = bknd_item.inventory(id_user=user_data.id_user, id_server=cmd.guild.id, item_type_filter=ewcfg.it_cosmetic)
    protected = False
    action = 'measure the'
    object = ''
    for cosmetic in cosmetics:
        cosmetic_data = EwItem(id_item=cosmetic.get('id_item'))
        if cosmetic_data.item_props.get('id_cosmetic') == 'chastitybelt':
            if cosmetic_data.item_props.get('adorned') == 'true':
                protected = True


    if len(command_used[8:]) > 0:
        object = command_used[8:]
    elif cmd.tokens_count > 1:
        object = message_text = ' '.join(word for word in cmd.tokens[1:])
    else:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "Measure what?"))

    if cmd.tokens[0] in ['!cockdraw', '!measurecock']:
        user_data.change_crime(n=1)
        user_data.persist()

        object = 'dick'
        action = 'whip out your'
        if protected:

            response = "You reach for your pants, only to be blocked by your chastity belt. The Lord has once again thwarted your degeneracy."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        size = float(user_data.rand_seed % 110)/10

        if size >= 10:
            size = user_data.rand_seed % 1000
    else:
        # Create a seeded random class for !measure, as to not overwrite the global random seed
        measure_random_class = random.Random(object)

        size = float((measure_random_class.randint(1, 100000) + user_data.rand_seed) % 110) / 10

        if size >= 10:
            size = (measure_random_class.randint(1, 100000) + user_data.rand_seed) % 1000

    if cmd.tokens[0] == '!cockdraw':
        response = "You slowly stick your hand in your pants..."
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        await asyncio.sleep(1)
        response = "**3!**"
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        await asyncio.sleep(1)
        response = "**2!**"
        await fe_utils.send_message(cmd.client, cmd.message.channel,fe_utils.formatMessage(cmd.message.author, response))
        await asyncio.sleep(1)
        response = "**1!**"
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        await asyncio.sleep(1)

    response = "You {} {}! It's {} inches long!".format(action, object, size)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def fun(cmd):
    response = "Nah, you can't do that. They removed fun from the game, remember?"

    """user_data = EwUser(member=cmd.message.author)

    item_sought = bknd_item.find_item(item_search='funpizza', item_type_filter=ewcfg.it_food, id_server=cmd.guild.id,
                                      id_user=cmd.message.author.id)

    if not item_sought:
        response = "What? Fuck you. You don't even have any fun pizza."
        await user_data.die(cause=ewcfg.cause_suicide)
        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)

    else:
        ewcfg.cmd_prefix = 'fun'
        response = "OH SHIT CHECK IT OUT!"
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        await asyncio.sleep(1)
        response = "WE'RE HAVING FUN HOLY SHIT!"
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        await asyncio.sleep(1)
        response = "THE PIZZA IS FUN THE PREFIX IS FUN YEAH YEAH YEAH!"
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        for x in range(6):
            await asyncio.sleep(3)
            if ewcfg.cmd_prefix == '!':
                ewcfg.cmd_prefix = 'fun'

        ewcfg.cmd_prefix = '!'

        response = 'You stop having fun.'"""

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def display_goonscape_stats(cmd):
    response = "\n```ini\n" # Use markdown formatting
    normal = True
    hidden = False

    if cmd.mentions_count > 0:
        target_id = cmd.mentions[0].id
    else:
        target_id = cmd.message.author.id

    # Handle user specification
    if cmd.tokens_count > 1:
        if cmd.tokens[1].lower() in ["all", "a"]:
            hidden = True
        elif cmd.tokens[1].lower() in ["legacy", "hidden", "l", "h"]:
            normal = False
            hidden = True

    # List all normal stats
    if normal:
        for stat_name in [ewcfg.goonscape_mine_stat, ewcfg.goonscape_farm_stat, ewcfg.goonscape_fish_stat, ewcfg.goonscape_eat_stat, ewcfg.goonscape_clout_stat]:

            stat = EwGoonScapeStat(target_id, cmd.guild.id, stat_name)

            response += "{stat:>10}] {level:>2}/{level:>2} ;{xp} xp\n".format(stat= "[" + stat.stat.capitalize(), level= stat.level , xp=stat.xp)
    # List hidden stats
    if hidden:
        for stat_name in [ewcfg.goonscape_halloweening_stat, ewcfg.goonscape_pee_stat]:

            stat = EwGoonScapeStat(target_id, cmd.guild.id, stat_name)

            # Format usual response, with explanation of the stat's origin.
            origin = ewcfg.legacy_stat_dict.get(stat_name)
            response += "{stat:>10}] {level:>2}/{level:>2} ;{xp} xp {origin}\n".format(stat= "[" + stat.stat.capitalize(), level= stat.level , xp=stat.xp, origin=("- "+origin if origin is not None else ""))

    response += "```"

    
    await fe_utils.send_response(response, cmd)

async def clear_zero_stats(cmd):
    """Admin command to clear redundant 0 value stats from the database."""
    # Only allow admins to use this
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    await fe_utils.send_response("Attempting to remove all 0 value stats from the database, this may take a while...", cmd)

    result = ewstats.clean_stats(cmd.guild.id)

    if result is not None:
        return await fe_utils.send_response(f"Successfully cleaned the database of {result} redundant stats. Nice!", cmd)

async def loop_diagnostic(cmd):
    if 0 < ewrolemgr.check_clearance(member=cmd.message.author) < 4:

        response = "Tick loop progress:\n"
        time_now = int(time.time())

        for timestamp in ewutils.last_loop.keys():
            response += "{} loop: {} seconds ago\n".format(timestamp, time_now - ewutils.last_loop.get(timestamp))

        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

