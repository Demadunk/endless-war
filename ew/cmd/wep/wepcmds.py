import asyncio
import math
import random
import time

from ew.backend import item as bknd_item
from ew.backend import worldevent as bknd_worldevent
from ew.backend.item import EwItem
from ew.backend.market import EwMarket
from ew.backend.player import EwPlayer
from ew.backend.worldevent import EwWorldEvent
from ew.static import cfg as ewcfg
from ew.static import poi as poi_static
from ew.static import slimeoid as sl_static
from ew.static import weapons as static_weapons
from ew.utils import combat as cmbt_utils
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import item as itm_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils import stats as ewstats
try:
    from ew.utils.rutils import debug16
    from ew.utils.rutils import debug17
    from ew.utils.rutils import debug114
    from ew.utils.rutils import debug_var_1
except:
    from ew.utils.rutils_dummy import debug16
    from ew.utils.rutils_dummy import debug17
    from ew.utils.rutils_dummy import debug114
    from ew.utils.rutils_dummy import debug_var_1
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.frontend import EwResponseContainer
from ew.utils.slimeoid import EwSlimeoid
from ew.utils.user import add_xp
from .weputils import EwEffectContainer
from .weputils import attackEnemy
from .weputils import apply_status_bystanders
from .weputils import canAttack
from .weputils import canCap
from .weputils import fulfill_ghost_weapon_contract
from .weputils import weapon_explosion
from .weputils import apply_attack_modifiers

""" Player attacks a target """


async def attack(cmd):
    resp_ctn = EwResponseContainer(id_server=cmd.guild.id)
    kf_ctn = None
    start_time = time.time()
    attacker_member = cmd.message.author
    attacker = EwUser(member=attacker_member, data_level=2)
    attacker_mutations = attacker.get_mutations()

    check_resp = canAttack(cmd)
    weaponCheckDeb = False
    if check_resp == "":
        """ 
            The block for running calculations of an actual attack
        """
        # Retrive necessary values for an attack
        attacker_weapon_item = attacker.get_weapon_item()
        attacker_weapon = static_weapons.weapon_map.get(attacker_weapon_item.template)
        attacker_slimeoid = EwSlimeoid(member=attacker_member)
        target_member = cmd.mentions[0]
        target = EwUser(member=target_member, data_level=2)
        target_mutations = target.get_mutations()
        target_weapon_item = EwItem(id_item=target.weapon) if target.weapon > 0 else None
        target_weapon = static_weapons.weapon_map.get(target_weapon_item.template) if target.weapon > 0 else None
        market_data = EwMarket(id_server=cmd.guild.id)
        district_data = EwDistrict(district=attacker.poi, id_server=cmd.guild.id)

        # Setup flavortext variables
        # this is disgusting, who wrote this?
        response, mass_status, wep_explode, napalm, hit_msg, bkf_msg, rel_warn, new_cap, slimeoid_resp, bounty_resp, contract_resp, lvl_resp = "", None, None, "", "", "", "", "", "", "", "", ""
        target_killed = False
        bounty = 0

        """ Attack Calculation """

        if attacker_weapon_item.template == ewcfg.weapon_id_slimeoidwhistle: # abstract this at some point
            _lvl = attacker_slimeoid.level if attacker_slimeoid.life_state != ewcfg.slimeoid_state_none else -1
            attacker_weapon.fn_effect = static_weapons.slimeoid_weapon_type_convert.get(_lvl)

        # Calculate some base values
        skill_mult = (0.05 * attacker.weaponskill) + 1
        base_cost = ((max(35, attacker.slimelevel) ** 4) / 30) if attacker_weapon.is_tool else ((attacker.slimelevel ** 4) / 30) * float(ewcfg.global_damage_multiplier_dt[attacker.id_server])
        base_dmg = 5 * base_cost * skill_mult

        # Generate some random values
        hitzone = cmbt_utils.get_hitzone()
        randombodypart = random.choice(hitzone.aliases) if random.random() < 0.5 else hitzone.name

        # Build a container so multiple values can be easily passed  to modifying functions
        ctn = EwEffectContainer(
            slimes_spent=base_cost,
            slimes_damage=base_dmg,
            user_data=attacker,
            shootee_data=target,
            weapon_item=attacker_weapon_item,
            time_now=int(start_time),
            market_data=market_data
        )

        # general purpose abstraction to ensure they are all applied in one place at the same time
        apply_attack_modifiers(ctn, hitzone, attacker_mutations, target_mutations, target_weapon, district_data)

        # Do the calculations for the weapon now
        attacker_weapon.fn_effect(ctn)

        # Ensure the attacker can cover the cost in slime before wasting any more time here
        if ctn.slimes_spent > attacker.slimes:
            resp = "You don't have enough slime to attack. ({:,}/{:,})".format(attacker.slimes, ctn.slimes_spent)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(attacker_member, resp))

        # Lord forgive me for branching again, but if you missed, none of this is necessary
        if not ctn.miss:

            """ Misc. effects """

            # Garrote attacks may be able to just return now
            if attacker_weapon_item.template == ewcfg.weapon_id_garrote:
                # Send the waiting message
                resp = "You wrap your wire around {}'s neck...".format(target_member.display_name)
                await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(attacker_member, resp))

                # Wait for a response, return if received. wait_for will throw an exception if it times out
                try:
                    garrote_resp_msg = await cmd.client.wait_for('message', timeout=5, check=lambda msg: msg.author == target_member)
                    return
                except asyncio.TimeoutError:
                    garrote_resp_msg = None
                
                # Refresh data
                attacker = EwUser(member=attacker_member)
                target = EwUser(member=target_member)

                # stop attack if either user died, or if they are no longer in the same zone
                if ewcfg.life_state_corpse in [attacker.life_state, target.life_state] or target.poi != attacker.poi:
                    return
                else:
                    # This status should be automatically removed, but just in case, get rid of it before continuing
                    target.clear_status(ewcfg.status_strangled_id)

            # apply targeted statuses to target
            for status_id, value in ctn.apply_status.items():
                stat_resp = target.applyStatus(id_status=status_id, value=value, source=attacker.id_user)

                # This assumes all Targeted burning is napalm snot. will require a rework if a weapon is given this
                if status_id == ewcfg.status_burning_id:
                    napalm = "**HCK-PTOOO!** " + stat_resp.format(name_player=target_member.display_name)

            # Apply mass burn from incendiary weapons
            if ctn.mass_apply_status == ewcfg.status_burning_id:
                mass_status = await apply_status_bystanders(
                    user_data=attacker, status=ewcfg.status_burning_id,
                    value=ctn.bystander_damage, life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile, ewcfg.life_state_executive, ewcfg.life_state_vigilante],
                    factions=["", target.faction], district_data=district_data
                )

            # Set up explosion from Death From Above if grenades aren't being used
            if (ewcfg.mutation_id_deathfromabove in attacker_mutations or ewcfg.mutation_id_airlock in attacker_mutations) and market_data.weather == ewcfg.weather_lightning and not ctn.explode:
                ctn.explode = True
                ctn.bystander_damage = ctn.slimes_damage / 10

        """ Slime & Coin Distribution """  # Still calc'd on miss because backfiring :D

        # Setup variables for slime distribution
        target_killed = ctn.slimes_damage > target.slimes - target.bleed_storage
        to_sewer, to_attacker, to_bleed, to_district, to_kingpin = 0, ctn.slimes_spent * -1, 0, 0, 0

        # Determine how slime will be distributed
        if target_killed:

            # attacker gets half slime and half is drained on teamkill, otherwise attacker gets all
            if target.life_state == ewcfg.life_state_enlisted and target.faction == attacker.faction:
                to_sewer = target.slimes/2
                to_attacker += target.slimes/2
            else:
                to_attacker += target.slimes

            # Transfer bounty
            bounty = int(target.bounty / ewcfg.slimecoin_exchangerate)
            attacker.change_slimecoin(n=bounty, coinsource=ewcfg.coinsource_bounty)
        else:
            if target.life_state in [ewcfg.life_state_juvenile]:
                # attacking juvies sends half to bleed and half to splatter
                to_bleed = ctn.slimes_damage/2
                to_district = ctn.slimes_damage/2
            elif target.life_state == ewcfg.life_state_enlisted and target.faction == attacker.faction:
                # attacking enlisted teammates sends half to sewers, 1/4 to bleed, and 1/4 to splatter
                to_sewer = ctn.slimes_damage/2
                to_bleed = ctn.slimes_damage/4
                to_district = ctn.slimes_damage/4
            else:
                # Attacking other combatants sends half to kingpin, 1/4 to bleed, and 1/4 to splatter
                to_kingpin = ctn.slimes_damage/2
                to_bleed = ctn.slimes_damage/4
                to_district = ctn.slimes_damage/4

        # nosferatu gives attacker 60% of splatter
        if to_district > 0 and ewcfg.mutation_id_nosferatu in attacker_mutations and (20 <= market_data.clock or market_data.clock < 6):
            to_attacker += to_district * 0.6
            to_district *= 0.4

        # Slurps Up or Airlock give attacker 50% of remaining splatter in rain 
        if to_district > 0 and (ewcfg.mutation_id_slurpsup in attacker_mutations or ewcfg.mutation_id_airlock in attacker_mutations) and market_data.weather == ewcfg.weather_rainy:
            to_attacker += to_district * 0.5
            to_district *= 0.5
                
        # Have backfire effect considered with slime gained from the kill already theirs
        attacker_killed = ctn.backfire_damage > attacker.slimes + to_attacker - attacker.bleed_storage
        if attacker_killed:
            # Distribution for enlisted gangsters attacking enlisted rival gangsters
            if attacker.life_state == ewcfg.life_state_enlisted and attacker.faction != target.faction:
                to_sewer += (attacker.slimes + to_attacker) / 2
                to_kingpin += (attacker.slimes + to_attacker) / 2
            # Distribution for Juvies
            else:
                to_sewer += attacker.slimes + to_attacker

            to_attacker = 0  # Don't give their ghost slime
        else:
            # Distribution for enlisted gangsters attacking enlisted rival gangsters
            if attacker.life_state == ewcfg.life_state_enlisted and attacker.faction != target.faction:
                to_district += ctn.backfire_damage / 2
                to_kingpin += ctn.backfire_damage / 2
            # Distribution for Juvie attackers and juvie/ally targets
            else:
                to_sewer += ctn.backfire_damage

            to_attacker -= ctn.backfire_damage  # Why add another line to the actual distribution?

        # Handyman gives kingpin twice as much slime when attacking with a tool
        if to_kingpin > 0 and ewcfg.mutation_id_handyman in attacker_mutations and attacker_weapon.is_tool:
            to_kingpin *= 2

        # Actually distribute slime now
        if attacker.faction not in [ewcfg.faction_slimecorp, target.faction] and attacker.life_state not in [ewcfg.life_state_juvenile] and to_kingpin > 0:
            # Kingpin only gets slime if not a teamkill or shill, or juvie, or shambler attacking
            kingpin = fe_utils.find_kingpin(id_server=cmd.guild.id, kingpin_role=ewcfg.role_rowdyfucker if attacker.faction == ewcfg.faction_rowdys else ewcfg.role_copkiller)
            if kingpin:
                kingpin = EwUser(id_server=cmd.guild.id, id_user=kingpin.id_user)
                kingpin.change_slimes(n=int(to_kingpin))
                kingpin.persist() # THIS ONLY GETS PERSISTED HERE BECAUSE THIS IS THE ONLY PLACE IT WILL EVER BE USED

        if (not target_killed) and (ctn.slimes_damage >= 0):
            # only take away slime if they survived to care
            target.change_slimes(n=-1 * (ctn.slimes_damage - to_bleed), source=ewcfg.source_damage)
            target.bleed_storage += to_bleed

        if (not attacker_killed) and (to_attacker != 0):
            # Distribution is calculated assuming they only get/lose any slime if they survive
            lvl_resp = attacker.change_slimes(n=int(to_attacker), source=ewcfg.source_killing if to_attacker >= 0 else ewcfg.source_self_damage)

        if to_sewer > 0:
            sewer_data = EwDistrict(district=ewcfg.poi_id_thesewers, id_server=cmd.guild.id)
            sewer_data.change_slimes(n=int(to_sewer))
            sewer_data.persist()  # this is the ONLY exception to "persist everything at the end" (aside from kingpin) because it is SOLELY used here

        if to_district > 0:
            district_data.change_slimes(n=int(to_district), source=ewcfg.source_killing)

        """ Misc. Value Changes & Stat Changes"""

        # Value changes on all attempted attacks
        attacker_weapon_item.item_props["time_lastattack"] = start_time
        if ewcfg.weapon_class_ammo in attacker_weapon.classes:
            attacker_weapon_item.item_props["ammo"] = int(attacker_weapon_item.item_props.get("ammo", attacker_weapon.clip_size)) - 1
        if ewcfg.weapon_class_captcha in attacker_weapon.classes:
            attacker_weapon_item.item_props["captcha"] = ewutils.generate_captcha(length=attacker_weapon.captcha_length, user_data=attacker)
        attacker.hunger += ewcfg.hunger_pershot * ewutils.hunger_cost_mod(attacker.slimelevel)

        # Values changed on backfire
        if ctn.backfire_damage > 0:
            # Weapon Data Changes
            attacker_weapon_item.item_props["consecutive_hits"] = 0  # we'll do this before the increment, to be nice

            # User Data Changes
            attacker.time_lasthit = int(start_time)

            # If ya did an oopsie
            if attacker_killed:
                # Weapon Data Changes
                attacker_weapon_item.item_props["totalsuicides"] = 1 + int(attacker_weapon_item.item_props.get("totalsuicides", 0))

                # User Data Changes
                attacker.trauma = ewcfg.trauma_id_backfire
                attacker.id_killer = attacker.id_user
                attacker.divide_weaponskill(fraction=math.inf, weapon_type=attacker_weapon.id_weapon)

        if ctn.miss:
            # Value Changes on misses
            attacker_weapon_item.item_props["consecutive_hits"] = 0
        else:
            # Value Changes on successful hits
            if target_weapon_item is not None: target_weapon_item.item_props["consecutive_hits"] = 0
            target.time_lasthit = int(start_time)
            attacker_weapon_item.item_props["consecutive_hits"] = 1 + int(attacker_weapon_item.item_props.get("consecutive_hits", 0))

            # Stat Changes on successful hits
            ewstats.track_maximum(user=attacker, metric=ewcfg.stat_max_hitdealt, value=ctn.slimes_damage)
            ewstats.change_stat(user=attacker, metric=ewcfg.stat_lifetime_damagedealt, n=ctn.slimes_damage)

            # For Fatal Blows Only
            if target_killed:
                # Value Changes
                attacker.hunger = 0 if ewcfg.mutation_id_fungalfeaster in attacker_mutations else attacker.hunger
                if attacker_weapon_item.template == ewcfg.weapon_id_molotov:
                    attacker.change_crime(n=ewcfg.cr_arson_points)
                else:
                    attacker.change_crime(n=ewcfg.cr_murder_points)


                attacker_weapon_item.item_props["kills"] = 1 + int(attacker_weapon_item.item_props.get("kills", 0))
                attacker_weapon_item.item_props["totalkills"] = 1 + int(attacker_weapon_item.item_props.get("totalkills", 0))
                attacker.add_bounty(n=(target.bounty/2) + (target.totaldamage + target.slimes)/4)
                if attacker.weaponskill <= target.slimelevel >= attacker.slimelevel:
                    attacker.add_weaponskill(n=1, weapon_type=attacker_weapon.id_weapon)
                if attacker.faction == target.faction and attacker.faction != "":
                    target.trauma = ewcfg.trauma_id_betrayal
                else:
                    target.trauma = attacker_weapon.id_weapon

                target.id_killer = attacker.id_user


                # Stat Updates
                debug16(attacker_weapon_item, attacker, target)
                ewstats.increment_stat(user=attacker, metric=ewcfg.stat_kills)
                ewstats.track_maximum(user=attacker, metric=ewcfg.stat_biggest_kill, value=target.totaldamage + target.slimes)
                ewstats.increment_stat(user=attacker, metric=attacker_weapon.stat)
                if attacker.slimelevel > target.slimelevel:
                    ewstats.increment_stat(user=attacker, metric=ewcfg.stat_lifetime_ganks)
                elif attacker.slimelevel < target.slimelevel:
                    ewstats.increment_stat(user=attacker, metric=ewcfg.stat_lifetime_takedowns)
                if ewcfg.slimernalia_active and attacker.life_state == ewcfg.life_state_juvenile:
                    ewstats.change_stat(id_server=attacker.id_server, id_user=attacker.id_user, metric=ewcfg.stat_festivity, n=ewcfg.festivity_kill_bonus)

            else:
                attacker.change_crime(n=ewcfg.cr_assault_points)

                if to_kingpin > 0:
                    ewstats.change_stat(user=attacker, metric=ewcfg.stat_lifetime_kingpin_slimes, n=to_kingpin)


        """ Flavortext Generation """

        # Generate slimeoid based flavor for the whistle, and get possession status
        possession = attacker.get_possession('weapon')
        slimeoid_name, slimeoid_kill, slimeoid_crit, slimeoid_dmg = "", "", "", ""
        if attacker_weapon.id_weapon == ewcfg.weapon_id_slimeoidwhistle:
            if attacker_slimeoid.life_state == ewcfg.slimeoid_state_none:
                slimeoid_name = cmd.message.author.display_name
                slimeoid_kill = 'goes full child gorilla and tears their victim to hideous chunks, before wailing a ferocious battle cry!'
                slimeoid_crit = 'a full speed donkey kick'
                slimeoid_dmg = 'knocked upside the head'
            else:
                slimeoid_name = attacker_slimeoid.name
                slimeoid_kill = static_weapons.slimeoid_kill_text.get(attacker_slimeoid.weapon)
                slimeoid_crit = static_weapons.slimeoid_crit_text.get(attacker_slimeoid.special)
                slimeoid_dmg = static_weapons.slimeoid_dmg_text.get(attacker_slimeoid.weapon)

        # Generate flavortext for all attempted attacks
        if ewcfg.weapon_class_ammo in attacker_weapon.classes and attacker_weapon_item.item_props["ammo"] == 0:
            rel_warn += "\n" + attacker_weapon.str_reload_warning.format(name_player=attacker_member.display_name)

        if ewcfg.weapon_class_captcha in attacker_weapon.classes:
            new_cap += "\nNew security code: **{}**".format(ewutils.text_to_regional_indicator(attacker_weapon_item.item_props.get("captcha")))

        bonus1 = debug17(attacker_weapon_item)

        if target_killed:
            # Flavortext for fatal blows only
            chosen_kill_str = random.choice(attacker_weapon.str_kill)
            hit_msg = "\n\n{}".format(chosen_kill_str.format(
                name_player=attacker_member.display_name,
                name_target=target_member.display_name,
                emote_skull=ewcfg.emote_slimeskull,
                slimeoid_name=slimeoid_name,
                slimeoid_kill=slimeoid_kill,
                bonus1 = bonus1
            ))
            if attacker_weapon.id_weapon == debug_var_1:
                weaponCheckDeb = True

            if attacker_slimeoid.life_state == ewcfg.slimeoid_state_active:
                slimeoid_resp += "\n\n" + sl_static.brain_map.get(attacker_slimeoid.ai).str_kill.format(slimeoid_name=attacker_slimeoid.name)

            target_slimeoid = EwSlimeoid(member=target_member)
            if target_slimeoid.life_state == ewcfg.slimeoid_state_active:
                slimeoid_resp += "\n\n" + sl_static.brain_map.get(target_slimeoid.ai).str_death.format(slimeoid_name=target_slimeoid.name)

            if bounty > 0:
                bounty_resp = "\n\n SlimeCorp transfers {:,} SlimeCoin to {}\'s account.".format(bounty, attacker_member.display_name)

            if possession:
                ghost_name = (await fe_utils.get_member(cmd.guild, possession[0])).display_name
                contract_resp = "\n\n {} winces in pain as their slime is corrupted into negaslime. {}'s contract has been fulfilled.".format(attacker_member.display_name, ghost_name)

            if random.randint(0, 99) == 0 and target.gender != 'gorl':
                foreskin = True
            else:
                foreskin = False

            


            # Lets throw a little scalp and/or foreskin creation in here
            if ewcfg.slimernalia_active:
                bknd_item.item_create(
                    item_type=ewcfg.it_furniture,
                    id_user=attacker_member.id,
                    id_server=cmd.guild.id,
                    item_props={
                        'id_furniture': ewcfg.item_id_sigillaria,
                        'furniture_name': "{}'s sigillaria".format(target_member.display_name),
                        'furniture_desc': "A sigillaria of {}.".format(target_member.display_name),
                        'rarity': ewcfg.rarity_patrician,
                        'furniture_place_desc': "You place the figurine, filling your apartment with Slimernalia cheer.",
                        'furniture_look_desc': "There's a sigillaria of {}.".format(target_member.display_name),
                    }
                )
                if bounty >= 1000000 or ctn.slimes_spent >= 1000000 or random.randint(0,9) == 9 and target.slimelevel >= 35: # Prevents gooners spawncamping victims for gaining the system -- hello gooners reading this!
                    bknd_item.item_create(
                        item_type=ewcfg.it_item,
                        id_user=attacker_member.id,
                        id_server=cmd.guild.id,
                        item_props={
                            'id_item': ewcfg.item_id_discontinuedscrap,
                            'item_name': "Discontinued Scrap",
                            'item_desc': "An unintelligible scrap of material. Completely useless on its own, meant as an ingredient to smelt discontinued items from previous or current deadbeat developers.",
                            'context': "discontinuedscrap"
                        }
                    )
            elif foreskin:
                bknd_item.item_create(
                    item_type=ewcfg.it_cosmetic,
                    id_user=attacker_member.id,
                    id_server=cmd.guild.id,
                    item_props={
                        'id_cosmetic': 'foreskin',
                        'cosmetic_name': "{}'s foreskin".format(target_member.display_name),
                        'cosmetic_desc': "A foreskin.{}".format(attacker_weapon.str_scalp),
                        'str_onadorn': ewcfg.str_generic_onadorn,
                        'str_unadorn': ewcfg.str_generic_unadorn,
                        'str_onbreak': ewcfg.str_generic_onbreak,
                        'rarity': ewcfg.rarity_patrician,
                        'attack': 0,
                        'defense': 0,
                        'speed': 3,
                        'ability': None,
                        'durability': int(ewutils.slime_bylevel(target.slimelevel) / 4),
                        'original_durability': int(ewutils.slime_bylevel(target.slimelevel) / 4),
                        'size': 1,
                        'fashion_style': ewcfg.style_tough,
                        'freshness': 10,
                        'adorned': 'false'
                    }
                )
            else:
                bknd_item.item_create(
                    item_type=ewcfg.it_cosmetic,
                    id_user=attacker_member.id,
                    id_server=cmd.guild.id,
                    item_props={
                        'id_cosmetic': 'scalp',
                        'cosmetic_name': "{}'s scalp".format(target_member.display_name),
                        'cosmetic_desc': "A scalp.{}".format(attacker_weapon.str_scalp),
                        'str_onadorn': ewcfg.str_generic_onadorn,
                        'str_unadorn': ewcfg.str_generic_unadorn,
                        'str_onbreak': ewcfg.str_generic_onbreak,
                        'rarity': ewcfg.rarity_patrician,
                        'attack': 1,
                        'defense': 0,
                        'speed': 0,
                        'ability': None,
                        'durability': int(ewutils.slime_bylevel(target.slimelevel) / 4),
                        'original_durability': int(ewutils.slime_bylevel(target.slimelevel) / 4),
                        'size': 1,
                        'fashion_style': ewcfg.style_cool,
                        'freshness': 10,
                        'adorned': 'false'
                    }
                )

        elif not ctn.miss:
            # Flavor for non fatal blows only
            hit_msg = attacker_weapon.str_damage.format(
                name_player=attacker_member.display_name,
                name_target=target_member.display_name,
                hitzone=randombodypart,
                slimeoid_name=slimeoid_name,
                slimeoid_dmg=slimeoid_dmg,
                bonus1 = bonus1
            )

            if ctn.crit:
                hit_msg += " " + attacker_weapon.str_crit.format(
                    name_player=attacker_member.display_name,
                    name_target=target_member.display_name,
                    hitzone=randombodypart,
                    slimeoid_name=slimeoid_name,
                    slimeoid_crit=slimeoid_crit,
                    bonus1 = bonus1
                )

            hit_msg += " {target_name} loses {damage:,} slime!".format(target_name=target_member.display_name, damage=ctn.slimes_damage)

        else:
            # flavor for misses only
            hit_msg = attacker_weapon.str_miss.format(
                name_player=attacker_member.display_name,
                name_target=target_member.display_name,
                slimeoid_name=slimeoid_name,
                bonus1 = bonus1
            )

        if ctn.backfire_damage > 0:
            # Flavor from backfires
            bkf_msg = "\n\n" + attacker_weapon.str_backfire.format(
                name_player=attacker_member.display_name,
                name_target=target_member.display_name,
                hitzone=randombodypart,
            )
            if attacker_killed:
                bkf_msg += "\nYou have been destroyed by your own stupidity."
            else:
                bkf_msg += "\nYou bled {} slime!\n".format(ctn.backfire_damage)

        """ Final Operations """

        # Fulfill possession if necessary
        if possession: await fulfill_ghost_weapon_contract(possession, market_data, attacker, attacker_member.display_name)

        # Persist everything that may have been changed. RIP function completion time
        if not possession: district_data.persist() # this is changed and persisted within fulfillment, no need to do it twice
        attacker.persist()
        target.persist()
        attacker_weapon_item.persist()
        if target_weapon_item is not None: target_weapon_item.persist()

        # Now we're allowed to run explosions.
        die_resp = None
        bkf_resp = None
        if target_killed and EwUser(member=target_member).life_state != ewcfg.life_state_corpse:
            # This MUST be run before weapon explosions, in case the weapon explosion triggers a spontaneous combustion
            # That case could kill the target, and running this afterward would kill the target twice, dropping items x2
            die_resp = await target.die(cause=ewcfg.cause_killing)
        if ctn.explode:
            wep_explode = await weapon_explosion(user_data=EwUser(member=attacker_member), shootee_data=EwUser(member=target_member),
                                           district_data=EwDistrict(id_server=cmd.guild.id, district=attacker.poi),
                                           market_data=EwMarket(id_server=cmd.guild.id),
                                           life_states=[ewcfg.life_state_enlisted, ewcfg.life_state_juvenile, ewcfg.life_state_executive, ewcfg.life_state_vigilante],
                                           factions=["", target.faction],
                                           slimes_damage=ctn.bystander_damage, time_now=start_time, target_enemy=False)
        if (EwUser(member=attacker_member).life_state != ewcfg.life_state_corpse) and attacker_killed:
            # Funny enough, this must be run AFTER the weapon explosion, as explosions can reward slime to the attacker,
            # which we can't have happening for a ghost, and it needs the attacker's weapon. Chance of slimegain is too low for me to factor it into whether they die or not though
            bkf_resp = await attacker.die(cause=ewcfg.cause_backfire)

        # build final response
        if mass_status is not None: resp_ctn.add_response_container(mass_status)
        if wep_explode is not None: resp_ctn.add_response_container(wep_explode)
        if napalm != "": resp_ctn.add_channel_response(cmd.message.channel, napalm)
        if die_resp is not None: resp_ctn.add_response_container(die_resp)
        if bkf_resp is not None: resp_ctn.add_response_container(bkf_resp)
        response = hit_msg + bkf_msg + rel_warn + new_cap + slimeoid_resp + bounty_resp + contract_resp
        resp_ctn.add_channel_response(cmd.message.channel, response)
        if lvl_resp != "": resp_ctn.add_channel_response(cmd.message.channel, "\n" + lvl_resp)

        # Now copy for the killfeed if necessary
        if target_killed or attacker_killed:
            kf_ctn = EwResponseContainer(id_server=cmd.guild.id)
            resps = resp_ctn.channel_responses.get(cmd.message.channel, []) + resp_ctn.channel_responses.get(cmd.message.channel.name, [])
            for msg in resps:
                kf_ctn.add_channel_response(ewcfg.channel_killfeed, msg)
            kf_ctn.format_channel_response(ewcfg.channel_killfeed, attacker_member)
            kf_ctn.add_channel_response(ewcfg.channel_killfeed, "`-------------------------`")
            if target_killed: resp_ctn.add_member_to_update(target_member)
            if attacker_killed: resp_ctn.add_member_to_update(attacker_member)

    elif check_resp == ewcfg.ghost_busting_string:
        """
            The block for running calculations of a ghostbusting
        """
        # Get variables
        target_member = cmd.mentions[0]
        target = EwUser(member=target_member)
        bounty = int(target.bounty / ewcfg.slimecoin_exchangerate)

        # Change values
        target.id_killer = attacker.id_user
        attacker.change_slimecoin(n=bounty, coinsource=ewcfg.coinsource_bounty)


        # Generate Flavortext
        response = "{name_target}\'s ghost has been **BUSTED**!!".format(name_target=target_member.display_name)
        if bounty > 0: response += "\n\n SlimeCorp transfers {:,} SlimeCoin to {}\'s account.".format(bounty, attacker_member.display_name)

        # Kill and persist
        bust_ctn = await target.die(cause=ewcfg.cause_busted) # This persists the target, no need to do it again

        # Build final response
        resp_ctn.add_response_container(bust_ctn)
        resp_ctn.add_channel_response(cmd.message.channel, response)

    elif check_resp == ewcfg.enemy_targeted_string:
        """
            This function will run the code for attacking an enemy
            Hopefully with the NPC rework enemies can be handled like players
        """
        return await attackEnemy(cmd)

    else:
        resp_ctn.add_channel_response(cmd.message.channel, check_resp)

    # format and post the response container
    resp_ctn.format_channel_response(cmd.message.channel.name, attacker_member)
    resp_ctn.format_channel_response(cmd.message.channel, attacker_member)
    await resp_ctn.post()
    if weaponCheckDeb:
        kf_ctn = await debug114(cmd=cmd, kf_ctn = kf_ctn)

    # Post to killfeed if necessary
    if kf_ctn is not None:
        if ewcfg.mutation_id_amnesia in attacker_mutations:
            await asyncio.sleep(60)
        await kf_ctn.post()

    return


""" Reload ammo based weapons """


async def reload(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    
    response = ""
    reload_mismatch = True
    bonus = 0

    # Give magic bullet theory bonus bullet
    if ewcfg.mutation_id_magicbullettheory in mutations:
        bonus += 1

    # If the user has a weapon equipped and it's an ammo-type weapon.
    if user_data.weapon > 0:
        weapon_item = EwItem(id_item=user_data.weapon)
        weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))

        if ewcfg.weapon_class_ammo in weapon.classes:
            if weapon.id_weapon == ewcfg.weapon_id_harpoon:
                # Because this takes so long, we check a couple times if the player has died
                response = "You start frantically reloading the harpoon gun..."
                await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                await asyncio.sleep(2)
                if user_data.life_state == ewcfg.life_state_corpse:
                    return
                response = "...oh god oh fuck oh fuck oh god oh fuck oh shit..."
                await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                await asyncio.sleep(3)
                if user_data.life_state == ewcfg.life_state_corpse:
                    return

            weapon_item.item_props["ammo"] = weapon.clip_size + bonus
            weapon_item.persist()
            response = weapon.str_reload
            reload_mismatch = False

    # If the user has a weapon sidearmed and it's an ammo-type weapon.
    if user_data.sidearm > 0:
        sidearm_item = EwItem(id_item=user_data.sidearm)
        sidearm = static_weapons.weapon_map.get(sidearm_item.item_props.get("weapon_type"))
        # Harpoon excluded
        if ewcfg.weapon_class_ammo in sidearm.classes and sidearm.id_weapon != ewcfg.weapon_id_harpoon:
            sidearm_item.item_props["ammo"] = sidearm.clip_size + bonus
            sidearm_item.persist()
            if response != "":
                response += "\n"
            response += sidearm.str_reload
            reload_mismatch = False

    if user_data.weapon == -1 and user_data.sidearm == -1:
        response = "What are you expecting to reload, dumbass? {} a weapon first!".format(ewcfg.cmd_equip)
    elif reload_mismatch:
        response = "What do you think you're going to be reloading with that?"

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Set active weapon """


async def equip(cmd):
    user_data = EwUser(member=cmd.message.author)

    time_now = int(time.time())

    if user_data.time_lastenlist > time_now:
        response = "You've enlisted way too recently! You can't equip any weapons just yet."

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)

    if item_sought:
        item = EwItem(id_item=item_sought.get("id_item"))

        if item.item_type == ewcfg.it_weapon:
            weapon = static_weapons.weapon_map.get(item.item_props.get("weapon_type"))
            # if weapon.is_tool == 1 and (user_data.sidearm < 0 or user_data.weapon >= 0):
            #	return await sidearm(cmd =cmd)

            item.item_props['roomba'] = ""
            response = user_data.equip(item)
            user_data.persist()
            item.persist()
        else:
            response = "Not a weapon, you ignorant juvenile."
    else:
        response = "You don't have one."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Set sidearm slot """


async def sidearm(cmd):
    user_data = EwUser(member=cmd.message.author)

    time_now = int(time.time())

    if user_data.time_lastenlist > time_now:
        response = "You've enlisted way too recently! You can't sidearm any weapons just yet."

    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)

    if item_sought:
        item = EwItem(id_item=item_sought.get("id_item"))

        if item.item_type == ewcfg.it_weapon:
            item.item_props['roomba'] = ""
            response = user_data.equip_sidearm(sidearm_item=item)
            user_data.persist()
            item.persist()

        else:
            response = "Not a tool, you ignorant juvenile."
    else:
        response = "You don't have one."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Player kills themselves """


async def suicide(cmd):
    response = ""

    resp_cont = EwResponseContainer(id_server=cmd.guild.id)

    # Only allowed in the combat zone.
    if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        response = "You must go into the city to commit {}.".format(cmd.tokens[0][1:])
    else:
        # Get the user data.
        user_data = EwUser(member=cmd.message.author)
        mutations = user_data.get_mutations()

        user_iskillers = user_data.life_state == ewcfg.life_state_enlisted and user_data.faction == ewcfg.faction_killers
        user_isrowdys = user_data.life_state == ewcfg.life_state_enlisted and user_data.faction == ewcfg.faction_rowdys
        user_isslimecorp = user_data.life_state == ewcfg.life_state_enlisted and user_data.faction == ewcfg.faction_slimecorp
        user_isgeneral = user_data.life_state == ewcfg.life_state_kingpin
        user_isjuvenile = user_data.life_state == ewcfg.life_state_juvenile
        user_isdead = user_data.life_state == ewcfg.life_state_corpse
        user_isexecutive = user_data.life_state == ewcfg.life_state_executive
        user_islucky = user_data.life_state == ewcfg.life_state_lucky

        if user_isdead:
            response = "Too late for that."
        elif user_isjuvenile and ewcfg.mutation_id_nervesofsteel not in mutations:
            response = "Juveniles are too cowardly for suicide."
        elif user_isgeneral:
            response = "\*click* Alas, your gun has jammed."
        elif user_iskillers or user_isrowdys or user_isexecutive or user_islucky or user_isjuvenile or user_isslimecorp:
            if ewutils.active_restrictions.get(user_data.id_user) != None and ewutils.active_restrictions.get(user_data.id_user) > 0:
                response = "You can't do that right now."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

            slimes_total = user_data.slimes
            slimes_drained = int(slimes_total * 0.1)
            slimes_todistrict = slimes_total - slimes_drained

            sewer_data = EwDistrict(district=ewcfg.poi_id_thesewers, id_server=user_data.id_server)
            sewer_data.change_slimes(n=slimes_drained)
            sewer_data.persist()

            district_data = EwDistrict(district=user_data.poi, id_server=cmd.guild.id)
            district_data.change_slimes(n=slimes_todistrict, source=ewcfg.source_killing)
            district_data.persist()

            # Set the id_killer to the player himself, remove his slime and slime poudrins.
            user_data.id_killer = cmd.message.author.id
            user_data.trauma = ewcfg.trauma_id_suicide
            user_data.visiting = ewcfg.location_id_empty
            die_resp = await user_data.die(cause=ewcfg.cause_suicide)
            resp_cont.add_response_container(die_resp)

            if user_data.has_soul == 1:
                response = '{} has willingly returned to the slime. {}'.format(cmd.message.author.display_name, ewcfg.emote_slimeskull)
            else:
                response = "Ahh. As it should be. {}".format(ewcfg.emote_slimeskull)

        else:
            # This should never happen. We handled all the role cases. Just in case.
            response = "\*click* Alas, your gun has jammed."

    # Send the response to the player.
    resp_cont.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    await resp_cont.post()


async def brandish(cmd):
    user_data = EwUser(member=cmd.message.author)
    if user_data.weapon > 0:
        weapon = EwItem(id_item=user_data.weapon)
        weapon_obj = static_weapons.weapon_map.get(weapon.item_props.get("weapon_type"))
        if len(weapon.item_props.get('weapon_name')) <= 0:
            weapon_name = "{}{}".format('their ', weapon_obj.str_name)
        else:
            weapon_name = weapon.item_props.get('weapon_name')

        response = random.choice(weapon_obj.str_brandish).format(weapon=weapon_name, name = cmd.message.author.display_name, tag = user_data.spray)
    else:
        response = "{} flips the bird!".format(cmd.message.author.display_name)
    return await fe_utils.send_message(cmd.client, cmd.message.channel,fe_utils.formatMessage(cmd.message.author, response))


""" Player spars with a friendly player to gain slime. """


async def spar(cmd):
    time_now = int(time.time())
    response = ""

    if cmd.message.channel.name != ewcfg.channel_dojo:
        response = "You must go to the dojo to spar."

    elif cmd.mentions_count > 1:
        response = "One sparring partner at a time!"

    elif cmd.mentions_count == 1:
        member = cmd.mentions[0]

        if (member.id == cmd.message.author.id):
            response = "How do you expect to spar with yourself?"
        else:
            # Get killing player's info.
            user_data = EwUser(member=cmd.message.author)
            weapon_item = EwItem(id_item=user_data.weapon)

            # Get target's info.
            sparred_data = EwUser(member=member)
            sparred_weapon_item = EwItem(id_item=sparred_data.weapon)

            user_iskillers = user_data.life_state == ewcfg.life_state_enlisted and user_data.faction == ewcfg.faction_killers
            user_isrowdys = user_data.life_state == ewcfg.life_state_enlisted and user_data.faction == ewcfg.faction_rowdys
            user_isslimecorp = user_data.life_state == ewcfg.life_state_enlisted and user_data.faction == ewcfg.faction_slimecorp
            user_isexecutive = user_data.life_state in [ewcfg.life_state_lucky, ewcfg.life_state_executive]
            user_isdead = user_data.life_state == ewcfg.life_state_corpse

            if user_data.hunger >= user_data.get_hunger_max():
                response = "You are too exhausted to train right now. Go get some grub!"
            elif user_data.poi != ewcfg.poi_id_dojo or sparred_data.poi != ewcfg.poi_id_dojo:
                response = "Both players need to be in the dojo to spar."
            elif sparred_data.hunger >= user_data.get_hunger_max():
                response = "{} is too exhausted to train right now. They need a snack!".format(member.display_name)
            elif user_isdead == True:
                response = "The dead think they're too cool for conventional combat. Pricks."
            elif (user_iskillers == False and user_isrowdys == False and user_isexecutive == False and user_isslimecorp == False) or user_data.life_state == ewcfg.life_state_corpse:
                # Only killers, rowdys, the cop killer, and the rowdy fucker can spar
                response = "Juveniles lack the backbone necessary for combat."
            elif user_data.weapon <= 0 or sparred_data.weapon <= 0:
                response = "You both need WEAPONs to master your WEAPONs, dumbasses."
            else:
                was_juvenile = False
                was_sparred = False
                was_dead = False
                was_player_tired = False
                was_target_tired = False
                was_enemy = False
                duel = False

                # Determine if the !spar is a duel:
                weapon = None
                if weapon_item.item_props.get("weapon_type") == sparred_weapon_item.item_props.get("weapon_type"):
                    weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
                    duel = True

                if sparred_data.life_state == ewcfg.life_state_corpse:
                    # Target is already dead.
                    was_dead = True
                elif (user_data.time_lastspar + ewcfg.cd_spar) > time_now:
                    # player sparred too recently
                    was_player_tired = True
                    timeuntil_player_spar = ewcfg.cd_spar - (time_now - user_data.time_lastspar)
                elif (sparred_data.time_lastspar + ewcfg.cd_spar) > time_now:
                    # taret sparred too recently
                    was_target_tired = True
                    timeuntil_target_spar = ewcfg.cd_spar - (time_now - sparred_data.time_lastspar)
                elif sparred_data.life_state == ewcfg.life_state_juvenile:
                    # Target is a juvenile.
                    was_juvenile = True
                elif (user_iskillers and (sparred_data.life_state == ewcfg.life_state_enlisted and sparred_data.faction == ewcfg.faction_killers)) or (user_isrowdys and (sparred_data.life_state == ewcfg.life_state_enlisted and sparred_data.faction == ewcfg.faction_rowdys)) or (
                        user_isslimecorp and (sparred_data.life_state == ewcfg.life_state_enlisted and sparred_data.faction == ewcfg.faction_slimecorp)):
                    # User can be sparred.
                    was_sparred = True
                elif (user_iskillers and (sparred_data.life_state == ewcfg.life_state_enlisted and sparred_data.faction != ewcfg.faction_killers)) or (user_isrowdys and (sparred_data.life_state == ewcfg.life_state_enlisted and sparred_data.faction != ewcfg.faction_rowdys)) or (
                        user_isslimecorp and (sparred_data.life_state == ewcfg.life_state_enlisted and sparred_data.faction != ewcfg.faction_slimecorp)):
                    # Target is a member of the opposing faction.
                    was_enemy = True

                # if the duel is successful
                if was_sparred:
                    weaker_player = sparred_data if sparred_data.slimes < user_data.slimes else user_data
                    stronger_player = sparred_data if user_data is weaker_player else user_data

                    # Weaker player gains slime based on the slime of the stronger player.
                    possiblegain = int(ewcfg.slimes_perspar_base * (2.2 ** weaker_player.slimelevel))
                    slimegain = min(possiblegain, stronger_player.slimes / 20)
                    weaker_player.change_slimes(n=slimegain)

                    # hunger drain for both players
                    user_data.hunger += ewcfg.hunger_perspar * ewutils.hunger_cost_mod(user_data.slimelevel)
                    sparred_data.hunger += ewcfg.hunger_perspar * ewutils.hunger_cost_mod(sparred_data.slimelevel)

                    if weapon.id_weapon in [ewcfg.weapon_id_bat, ewcfg.weapon_id_spraycan, ewcfg.weapon_id_paintroller]:
                        weaker_player.change_crime(n=ewcfg.cr_dojo_crime_points)
                        stronger_player.change_crime(n=ewcfg.cr_dojo_crime_points)


                    # Bonus 50% slime to both players in a duel.
                    if duel:
                        weaker_player.change_slimes(n=slimegain / 2)
                        stronger_player.change_slimes(n=slimegain / 2)

                        if weaker_player.weaponskill < 5 or (weaker_player.weaponskill + 2) < stronger_player.weaponskill:
                            weaker_player.add_weaponskill(n=1, weapon_type=weapon.id_weapon)

                        if stronger_player.weaponskill < 5 or (stronger_player.weaponskill + 2) < weaker_player.weaponskill:
                            stronger_player.add_weaponskill(n=1, weapon_type=weapon.id_weapon)

                    weaker_player.time_lastspar = time_now

                    user_data.persist()
                    sparred_data.persist()
                    # await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)

                    # player was sparred with
                    if duel and weapon != None:
                        response = weapon.str_duel.format(name_player=cmd.message.author.display_name, name_target=member.display_name)
                    else:
                        response = '{} parries the attack. :knife: {}'.format(member.display_name, ewcfg.emote_slime5)

                    # Notify if max skill is reached
                    if weapon != None:
                        if user_data.weaponskill >= 5:
                            response += ' {} is a master of the {}.'.format(cmd.message.author.display_name, weapon.id_weapon)
                        if sparred_data.weaponskill >= 5:
                            response += ' {} is a master of the {}.'.format(member.display_name, weapon.id_weapon)

                else:
                    if was_dead:
                        # target is already dead
                        response = '{} is already dead.'.format(member.display_name)
                    elif was_target_tired:
                        # target has sparred too recently
                        response = '{} is too tired to spar right now. They\'ll be ready in {} seconds.'.format(member.display_name, int(timeuntil_target_spar))
                    elif was_player_tired:
                        # player has sparred too recently
                        response = 'You are too tired to spar right now. Try again in {} seconds'.format(int(timeuntil_player_spar))
                    elif was_enemy:
                        # target and player are different factions
                        response = "You cannot spar with your enemies."
                    else:
                        # otherwise unkillable
                        response = '{} cannot spar now.'.format(member.display_name)
    else:
        response = 'Your fighting spirit is appreciated, but ENDLESS WAR didn\'t understand that name.'

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" name a weapon using a slime poudrin """


async def annoint(cmd):
    response = ""
    user_data = EwUser(member=cmd.message.author)
    weapon_item = EwItem(id_item=user_data.weapon)

    # Make sure user has a weapon equipped before all else
    if user_data.weapon <= 0:
        response = "Equip a weapon first."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # Grab the wanted name
    if cmd.tokens_count < 2:
        annoint_name = weapon_item.name
    else:
        annoint_name = cmd.message.content[(len(ewcfg.cmd_annoint)):].strip() 

    # See if the player has a poudrin
    poudrin = bknd_item.find_item(item_search="slimepoudrin", id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None, item_type_filter=ewcfg.it_item)

    # Checks for name too long, poudrin, and slime
    if len(annoint_name) > 32:
        response = "That name is too long.({:,}/32)".format(len(annoint_name))
    elif poudrin is None:
        response = "You need a slime poudrin."
    elif user_data.slimes < 100:
        response = "You need more slime."
    # Change weapon properties
    else:
        newname = 0

        # Make sure name is original
        all_weapons = bknd_item.inventory(
            id_server=cmd.guild.id,
            item_type_filter=ewcfg.it_weapon
        )
        for weapon in all_weapons:
            if weapon.get("name") == annoint_name and weapon.get("id_item") != user_data.weapon:
                response = "**ORIGINAL WEAPON NAME DO NOT STEAL.**"
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            
        # Change weapon's name if needed
        if weapon_item.item_props.get("weapon_name", "") != annoint_name:
            newname = 1
            weapon_item.item_props["weapon_name"] = annoint_name

        # Change user
        user_data.change_slimes(n=-100, source=ewcfg.source_spending)

        if user_data.weaponskill < 10:
            user_data.add_weaponskill(n=1, weapon_type=weapon_item.item_props.get("weapon_type"))

        # delete a slime poudrin from the player's inventory
        bknd_item.item_delete(id_item=poudrin.get('id_item'))

        # Persist user & weapon
        user_data.persist()
        weapon_item.persist()

        # Make response
        if newname == 1:
            naming_text = "It is now known as {}!\n\nThe name draws you closer to your weapon. ".format(annoint_name)
        else:
            naming_text = ""

        response = "You place your weapon atop the poudrin and annoint it with slime. {}The poudrin was destroyed in the process.".format(naming_text)

    # Send the response to the player.
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Bind player to active weapon, slightly increase mastery """


async def marry(cmd):
    user_data = EwUser(member=cmd.message.author)
    world_events = bknd_worldevent.get_world_events(id_server=user_data.id_server)
    already_getting_married = False
    mutations = user_data.get_mutations()

    for event_id, etype in world_events.items():
        if etype == ewcfg.event_type_marriageceremony:
            world_event = EwWorldEvent(id_event=event_id)
            if int(world_event.event_props.get("user_id")) == user_data.id_user:
                already_getting_married = True
                break

    weapon_item = EwItem(id_item=user_data.weapon)
    weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
    display_name = cmd.message.author.display_name
    if weapon != None:
        weapon_name = weapon_item.item_props.get("weapon_name") if len(weapon_item.item_props.get("weapon_name")) > 0 else weapon.str_weapon

    # Checks to make sure you're in the dojo.
    if user_data.poi != ewcfg.poi_id_dojo:
        response = "Do you really expect to just get married on the side of the street in this war torn concrete jungle? No way, you need to see a specialist for this type of thing, someone who can empathize with a man’s love for his arsenal. Maybe someone in the Dojo can help, *hint hint*."
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif already_getting_married:
        response = "You're already getting married, hold your metaphorical horses. Just sit back and enjoy the ceremony."
        await fe_utils.send_response(response, cmd)
    # Informs you that you cannot marry other juvies.
    elif cmd.mentions_count > 0:
        response = "Ewww, gross! You can’t marry another juvenile! That’s just degeneracy, pure and simple. What happened to the old days, where you could put a bullet in someone’s brain for receiving a hug? You people have gone soft on me, I tells ya."
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    # Makes sure you have a weapon to marry.
    elif weapon is None:
        response = "How do you plan to get married to your weapon if you aren’t holding any weapon? Goddamn, think these things through, I have to spell out everything for you."
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    # Makes sure you have a displayed rank 4 or higher weapon.
    elif user_data.weaponskill < 8:
        response = "Slow down, Casanova. You do not nearly have a close enough bond with your {} to engage in holy matrimony with it. You’ll need to reach rank 4 mastery or higher to get married.".format(weapon_name)
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    # Makes sure you aren't trying to farm the extra weapon mastery ranks by marrying over and over again.
    elif user_data.weaponmarried == True:
        response = "Ah, to recapture the magic of the first nights together… Sadly, those days are far behind you now. You’ve already had your special day, now it’s time to have the same boring days forever. Aren’t you glad you got married??"
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:

        marriage_line = 0
        time_now = int(time.time())
        props = {"user_id": user_data.id_user}
        marriage_world_event = bknd_worldevent.create_world_event(id_server = user_data.id_server, event_type = ewcfg.event_type_marriageceremony, time_activate = time_now, time_expir= time_now + 300, event_props = props)

        # Update world events again in case something changed in these split seconds
        world_events = bknd_worldevent.get_world_events(user_data.id_server)

        while world_events.get(marriage_world_event) != None and marriage_line != len(ewcfg.marriage_ceremony_text):
            response = ewcfg.marriage_ceremony_text[marriage_line]
            response = response.format(weapon_name = weapon_name, display_name = display_name, weapon_type = weapon.str_weapon)
            await fe_utils.send_response(response, cmd)
            await asyncio.sleep(6)
            marriage_line += 1
            world_events = bknd_worldevent.get_world_events(user_data.id_server)

        bknd_worldevent.delete_world_event(marriage_world_event)
        user_data = EwUser(member=cmd.message.author)
        if user_data.poi == ewcfg.poi_id_dojo:
            user_data.weaponmarried = True
            user_data.persist()

            # Sets their weaponmarried table to true, so that "you are married to" appears instead of "you are wielding" intheir !data, you get an extra two mastery levels, and you can't change your weapon.
            weapon_item.item_props["married"] = user_data.id_user
            weapon_item.persist()

            user_data = EwUser(member=cmd.message.author)
            user_data.add_weaponskill(n=2, weapon_type=weapon.id_weapon)
        else:
            if ewcfg.mutation_id_amnesia in mutations:
                display_name = "?????"
            else:
                display_name = cmd.author_id.display_name
            response = "The Dojo Master looks around confused. Looks like {} fled the scene of the marriage!".format(display_name)
            return await fe_utils.send_response(response, cmd.author_id.displayname)
        
        user_data.persist()
        return

""" Object to a marriage-in-progress. Can be done by other players, or by the player being married."""

async def object(cmd):
    user_data = EwUser(member=cmd.message.author)
    world_events = bknd_worldevent.get_world_events(id_server = user_data.id_server)
    found_ceremony = False
    objection_type = "self"
    objectee = user_data

    if cmd.mentions_count == 0:
        objection_type = "self"
    elif cmd.mentions_count == 1:
        objection_type = "other"
        objectee = EwUser(member=cmd.mentions[0])
        if objectee.poi != user_data.poi:
            return await fe_utils.send_response(response_text="How do you plan on doing that? You're not even in the same place as them.", cmd=cmd)
    else:
        return await fe_utils.send_response(response_text="You can only object to one marriage at once, buddy!", cmd=cmd)
    
    for event_id in world_events:
        if world_events.get(event_id) == ewcfg.event_type_marriageceremony:
            world_event = EwWorldEvent(event_id)
            ewutils.logMsg("Found marriage ceremony {ceremony_id} for player {player_id}".format(ceremony_id = event_id, player_id = world_event.event_props.get("user_id")))
            if world_event.event_props.get("user_id") == str(objectee.id_user):
                bknd_worldevent.delete_world_event(event_id)
                found_ceremony = True
                break
    
    if found_ceremony:
        if objection_type == "self":
            response = "You get cold feet and want out of this doomed marriage-to-be. You protest to the Dojo Master who just shrugs and stops the ceremony. Maybe you'll find love next time?"
        else:
            response = "\"STOP THE CEREMONY!\" you shout at the top of your lungs. The Dojo Master looks fed up with this shit and stops the ceremony."
    else:
        if objection_type == "self":
            response = "Object to what? It's not like you're currently getting married or anything."
        else:
            response = "Object to what? It's not like they're currently getting married or anything."
    
    return await fe_utils.send_response(response_text = response, cmd=cmd)

""" Destroy Spouse, ending the marriage """


async def divorce(cmd):
    user_data = EwUser(member=cmd.message.author)

    weapon_item = EwItem(id_item=user_data.weapon)
    weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))

    if weapon is None:
        response = "Divorce what? You ain't even holding a weapon, buddy."
    # Makes sure you have a partner to divorce.
    elif user_data.weaponmarried == False:
        response = "I appreciate your forward thinking attitude, but how do you expect to get a divorce when you haven’t even gotten married yet? Throw your life away first, then we can talk."
    # Checks to make sure you're in the dojo.
    elif user_data.poi != ewcfg.poi_id_dojo:
        response = "As much as it would be satisfying to just chuck your {} down an alley and be done with it, here in civilization we deal with things *maturely.* You’ll have to speak to the guy that got you into this mess in the first place, or at least the guy that allowed you to make the inane decision in the first place. Luckily for you, they’re the same person, and he’s at the Dojo.".format(
            weapon.str_weapon)
    elif user_data.life_state == ewcfg.life_state_juvenile:
        response = "The Dojo Master offers annulment services to paying customers only. Enlist in a gang and he'll consider removing you from your hellish facade of a relationship."
    else:
        weapon_name = weapon_item.item_props.get("weapon_name") if len(weapon_item.item_props.get("weapon_name")) > 0 else weapon.str_weapon

        response = "Are you sure you want to divorce {}? The Dojo Master will take back weapon after the proceedings and it will be gone. **Forever**. Oh yeah, and the divorce courts around here are pretty harsh so expect to kiss at least half of your slimecoin goodbye.\n**!accept to continue, or !refuse to back out**".format(weapon.str_weapon)
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        try:
            accepted = False
            message = await cmd.client.wait_for('message', timeout=30, check=lambda message: message.author == cmd.message.author and message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])

            if message != None:
                if message.content.lower() == ewcfg.cmd_accept:
                    accepted = True
                if message.content.lower() == ewcfg.cmd_refuse:
                    accepted = False
        except:
            accepted = False
        
        if not accepted:
            response = "You hastily decide that maybe this dumpster fire of a relationship is worth saving after all. Probably. Maybe."
        else:
            # Unpreform the ceremony
            response = "You decide it’s finally time to end the frankly obviously inane farce that is your marriage with your {}. Things were good at first, you both wanted the same things out of life. But, that was then and this is now. You reflect briefly on your myriad of woes; the constant bickering, the mundanity of your everyday routine, the total lack of communication. You’re a slave. But, a slave you will be no longer! You know what you must do." \
                        "\nYou approach the Dojo Master yet again, and explain to him your troubles. He solemnly nods along to every beat of your explanation. Luckily, he has a quick solution. He rips apart the marriage paperwork he forged last flavor text, and just like that you’re divorced from {}. It receives half of your SlimeCoin in the settlement, a small price to pay for your freedom. You hand over what used to be your most beloved possession and partner to the old man, probably to be pawned off to whatever bumfuck juvie waddles into the Dojo next. You don’t care, you just don’t want it in your data. " \
                        "So, yeah. You’re divorced. Damn, that sucks.".format(weapon.str_weapon, weapon_name)

            # You divorce your weapon, discard it, lose it's rank, and loose half your SlimeCoin in the aftermath.
            user_data.weaponmarried = False
            user_data.weapon = -1
            ewutils.weaponskills_set(member=cmd.message.author, weapon=weapon_item.item_props.get("weapon_type"), weaponskill=0)

            fee = (user_data.slimecoin / 2)
            user_data.change_slimecoin(n=-fee, coinsource=ewcfg.coinsource_revival)

            user_data.persist()

            # delete weapon item
            bknd_item.item_delete(id_item=weapon_item.id_item)

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def taunt(cmd):
    user_data = EwUser(member=cmd.message.author)

    response = ""

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "A bit late for that, don't you think?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count > 1:
        response = "You can only focus on taunting one person at a time."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count == 1:
        target = cmd.mentions[0]
        target_data = EwUser(member=target)
    else:
        huntedenemy = " ".join(cmd.tokens[1:]).lower()
        target_data = target = cmbt_utils.find_enemy(enemy_search=huntedenemy, user_data=user_data)

    if target_data == None:
        response = "ENDLESS WAR didn't understand that name."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if target_data.poi != user_data.poi:
        response = "You can't {} someone, who's not even here.".format(cmd.tokens[0])
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    id_status = ewcfg.status_taunted_id

    target_statuses = target_data.getStatusEffects()

    if id_status in target_statuses:
        response = "{} has already been taunted.".format(target.display_name)
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    target_data.applyStatus(id_status=id_status, source=cmd.message.author.id, id_target=cmd.message.author.id)

    user_data.persist()

    response = "You taunt {} into attacking you.".format(target.display_name)
    await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def aim(cmd):
    user_data = EwUser(member=cmd.message.author)

    response = ""

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "A bit late for that, don't you think?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count > 1:
        response = "You can only focus on aiming at one person at a time."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count == 1:
        target = cmd.mentions[0]
        target_data = EwUser(member=target)
    else:
        huntedenemy = " ".join(cmd.tokens[1:]).lower()
        target_data = target = cmbt_utils.find_enemy(enemy_search=huntedenemy, user_data=user_data)

    if target_data == None:
        response = "ENDLESS WAR didn't understand that name."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if target_data.poi != user_data.poi:
        response = "You can't {} at someone, who's not even here.".format(cmd.tokens[0])
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    id_status = ewcfg.status_aiming_id

    user_data.clear_status(id_status=id_status)

    user_data.applyStatus(id_status=id_status, source=cmd.message.author.id, id_target=(target.id if target_data.combatant_type == "player" else target_data.id_enemy))

    user_data.persist()

    response = "You aim at {}'s weak spot.".format(target.display_name)
    await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def dodge(cmd):
    user_data = EwUser(member=cmd.message.author)

    response = ""

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "A bit late for that, don't you think?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count > 1:
        response = "You can only focus on dodging one person at a time."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if cmd.mentions_count == 1:
        target = cmd.mentions[0]
        target_data = EwUser(member=target)
    else:
        huntedenemy = " ".join(cmd.tokens[1:]).lower()
        target_data = target = cmbt_utils.find_enemy(enemy_search=huntedenemy, user_data=user_data)

    if target_data == None:
        response = "ENDLESS WAR didn't understand that name."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if target_data.poi != user_data.poi:
        response = "You can't {} someone, who's not even here.".format(cmd.tokens[0])
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    id_status = ewcfg.status_evasive_id

    user_data.clear_status(id_status=id_status)

    user_data.applyStatus(id_status=id_status, source=cmd.message.author.id, id_target=(target.id if target_data.combatant_type == "player" else target_data.id_enemy))

    user_data.persist()

    response = "You focus on dodging {}'s attacks.".format(target.display_name)
    await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Attack the control of a district, or buff your team's control """


async def spray(cmd):
    roomba_loop = 0
    while True:
        # Get user data, then flag for PVP
        user_data = EwUser(id_user=cmd.message.author.id, id_server=cmd.guild.id)

        market_data = EwMarket(id_server=cmd.guild.id)
        time_current = market_data.clock

        time_now_float = time.time()
        time_now = int(time_now_float)

        # Get shooting player's info
        weapon = None
        weapon_item = None
        sidearm_viable = 0
        user_mutations = user_data.get_mutations()

        # if user_data.sidearm >= 0:
        #	weapon_item = EwItem(id_item=user_data.sidearm)
        #	weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
        #	captcha = weapon_item.item_props.get('captcha')
        #	if ewcfg.weapon_class_paint in weapon.classes:
        #		sidearm_viable = 1

        if user_data.weapon >= 0 and sidearm_viable == 0:
            weapon_item = EwItem(id_item=user_data.weapon)
            weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
            captcha = weapon_item.item_props.get('captcha')

        if weapon_item is not None and roomba_loop == 0:
            if weapon_item.item_props.get("weapon_type") == 'roomba':
                if weapon_item.item_props.get("roomba") == user_data.poi:
                    weapon_item.item_props['roomba'] = ""
                    weapon_item.persist()
                    response = "You pick the roomba back up and have it stop spraying down the floor."
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                else:
                    weapon_item.item_props['roomba'] = user_data.poi
                    weapon_item.persist()

        response = canCap(cmd, "spray", roomba_loop)

        if response == "":
            if user_data.slimelevel <= 0:
                user_data.slimelevel = 1
                user_data.persist()

            # Get district data
            poi = poi_static.id_to_poi.get(user_data.poi)
            district_data = EwDistrict(id_server=cmd.guild.id, district=poi.id_poi)

            gangsters_in_district = district_data.get_players_in_district(min_slimes=ewcfg.min_slime_to_cap, life_states=[ewcfg.life_state_enlisted], ignore_offline=True)

            miss = False
            crit = False
            bystander_damage = 0
            hit_chance_mod = 0
            crit_mod = 0
            dmg_mod = 0
            # sap_damage = 0
            # sap_ignored = 0

            weapon.fn_effect = static_weapons.weapon_type_convert.get(weapon.id_weapon)

            shooter_status_mods = cmbt_utils.get_shooter_status_mods(user_data, None, None)

            hit_chance_mod += shooter_status_mods['hit_chance']
            crit_mod += shooter_status_mods['crit']
            dmg_mod *= shooter_status_mods['dmg']

            slimes_spent = int(ewutils.slime_bylevel(user_data.slimelevel) / 300)
            slimes_damage = int((50000 + slimes_spent * 10) * (100 + (user_data.weaponskill * 5)) / 100.0)
            slimes_spent = round(slimes_spent * .1125)
            statuses = user_data.getStatusEffects()

            if weapon is None:
                slimes_damage /= 2  # penalty for not using a weapon, otherwise fists would be on par with other weapons

            slimes_damage += int(slimes_damage * dmg_mod)
            # user_data.hunger += ewcfg.hunger_pershot * ewutils.hunger_cost_mod(user_data.slimelevel)

            if weapon != None and weapon.fn_effect != None:
                # Build effect container
                ctn = EwEffectContainer(
                    miss=miss,
                    crit=crit,
                    slimes_damage=slimes_damage,
                    slimes_spent=slimes_spent,
                    user_data=user_data,
                    weapon_item=weapon_item,
                    shootee_data=None,
                    time_now=time_now,
                    bystander_damage=bystander_damage,
                    hit_chance_mod=hit_chance_mod,
                    crit_mod=crit_mod,
                    market_data=market_data,
                    # sap_damage=sap_damage,
                    # sap_ignored=sap_ignored,
                )

                # Make adjustments

                weapon.fn_effect(ctn)

                # Apply effects for non-reference values
                resp_cont = EwResponseContainer(id_server=cmd.guild.id)
                miss = ctn.miss
                crit = ctn.crit
                slimes_damage = ctn.slimes_damage
                slimes_spent = ctn.slimes_spent
                # sap_damage = ctn.sap_damage

                if miss is True and random.randint(0, 1) == 0:
                    miss = False

                if (slimes_spent > user_data.slimes):
                    # Not enough slime to shoot.
                    response = "You don't have enough slime to cap. ({:,}/{:,})".format(user_data.slimes, slimes_spent)
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

                weapon_item.item_props['time_lastattack'] = time_now_float
                weapon_item.persist()
                user_data.change_slimes(n=(-user_data.slimes if slimes_spent >= user_data.slimes else -slimes_spent), source=ewcfg.source_spending)
                user_data.persist()

                # Remove a bullet from the weapon
                if ewcfg.weapon_class_ammo in weapon.classes:
                    weapon_item.item_props['ammo'] = int(weapon_item.item_props.get("ammo")) - 1

                if miss:
                    slimes_damage = 0

                    weapon_item.item_props["consecutive_hits"] = 0
                    crit = False
                weapon_item.persist()
                # Remove !revive invulnerability.
                user_data.time_lastrevive = 0
                market_data = EwMarket(id_server=cmd.guild.id)
                # apply attacker damage mods
                slimes_damage *= cmbt_utils.damage_mod_cap(
                    user_data=user_data,
                    user_mutations=user_mutations,
                    market_data=market_data,
                    district_data=district_data,
                    weapon=weapon
                )

                if weapon.id_weapon == ewcfg.weapon_id_watercolors:
                    if not miss:
                        slimes_damage = ewcfg.min_garotte
                # if (user_data.faction != district_data.controlling_faction and (user_data.faction is None or user_data.faction == '')) and district_data.capture_points > ewcfg.limit_influence[district_data.property_class]:
                #	slimes_damage = round(slimes_damage / 5)
                #	pass
                if weapon != None:
                    if miss:
                        response = weapon.tool_props[0].get('miss_spray')
                    else:

                        response = weapon.tool_props[0].get('reg_spray').format(gang=user_data.faction[:-1].capitalize(), curse=random.choice(list(ewcfg.curse_words.keys())))
                        response += " You got {:,} influence for the {}!".format(int(abs(slimes_damage)), user_data.faction.capitalize())

                        if (user_data.faction != district_data.cap_side and district_data.cap_side != "") and (user_data.faction is not None or user_data.faction != ''):
                            slimes_damage = round(slimes_damage * -.8)
                        # district_data.change_capture_points()

                        district_data.change_capture_points(progress=slimes_damage, actor=user_data.faction)

                        if crit and weapon.id_weapon == ewcfg.weapon_id_watercolors:
                            district_data.change_capture_points(progress=-district_data.capture_points, actor=user_data.faction)

                        district_data.persist()

                        district_data = EwDistrict(district=district_data.name, id_server=district_data.id_server)
                        # district_data.capture_points += slimes_damage
                        # if district_data.capture_points < 0:
                        #	district_data.controlling_faction = user_data.faction
                        #	district_data.capture_points *= -1
                        # district_data.persist()
                        # response = weapon.str_damage.format(
                        #	name_player=cmd.message.author.display_name,
                        #	name_target=enemy_data.display_name,
                        #	hitzone=randombodypart,
                        #	strikes=strikes
                        # )

                        if crit:
                            if user_data.faction == ewcfg.faction_rowdys:
                                color = "pink"
                            elif user_data.faction == "slimecorp":
                                color = "Slimecorp propaganda"
                            else:
                                color = "purple"
                            response = user_data.spray + "\n\n"
                            response += weapon.tool_props[0].get('crit_spray').format(color=color)
                            response += " It gets you {:,} influence!".format(abs(slimes_damage))
                    # response += " {}".format(weapon.str_crit.format(
                    #	name_player=cmd.message.author.display_name,
                    #	name_target=enemy_data.display_name,
                    #	hitzone=randombodypart,
                    # ))

                    if ewcfg.weapon_class_ammo in weapon.classes and weapon_item.item_props.get("ammo") == 0:
                        response += "\n" + weapon.str_reload_warning.format(
                            name_player=cmd.message.author.display_name)

                    if (ewcfg.weapon_class_captcha in weapon.classes) and roomba_loop == 0:
                        if weapon.id_weapon != ewcfg.weapon_id_paintgun:
                            new_captcha_low = ewutils.generate_captcha(length=weapon.captcha_length, user_data=user_data)
                            new_captcha = ewutils.text_to_regional_indicator(new_captcha_low)
                            # new_loc = new_loc.replace(new_captcha_low, new_captcha)
                            response += "\nNew captcha is {}.".format(new_captcha)
                            weapon_item.item_props['captcha'] = new_captcha_low
                        # new_captcha = ewutils.generate_captcha(length = weapon.captcha_length)
                        else:
                            riflearray = ewcfg.riflecap
                            direction = str(random.choice(riflearray))
                            weapon_item.item_props['captcha'] = direction
                            new_captcha_gun = ewutils.text_to_regional_indicator(direction)
                            response += "\nNext target is {}.".format(new_captcha_gun)
                        weapon_item.persist()

                    if district_data.controlling_faction == user_data.faction and abs(district_data.capture_points) >= ewcfg.max_capture_points[poi.property_class]:
                        if user_data.faction == ewcfg.faction_rowdys:
                            color = "pink"
                        elif user_data.faction == "slimecorp":
                            color = "Slimecorp propaganda"
                        else:
                            color = "purple"
                        response += "\nThe street is awash in a sea of {}. It's hard to imagine where else you could spray down.".format(color)
                    elif district_data.controlling_faction == user_data.faction and abs(district_data.capture_points) >= (ewcfg.max_capture_points[poi.property_class] / 2):
                        response += "\nThe {} are developing a decent grip on this district.".format(user_data.faction)
                    #elif district_data.controlling_faction == user_data.faction and abs(district_data.capture_points) > ewcfg.min_influence[poi.property_class]:
                        #response += "\nThe {} have developed a loose grip on this district.".format(user_data.faction)
            else:
                if miss:
                    response = "You spray something so obscure nobody notices."
                else:
                    response = "Nice vandalism! You get {damage} influence out of it!".format(
                        damage=abs(slimes_damage)
                    )
        else:
            if weapon_item is not None:
                weapon_item.item_props['roomba'] = ""
                weapon_item.persist()
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        user_data = EwUser(member=cmd.message.author)
        if user_data.weapon >= 0:
            weapon_item = EwItem(id_item=user_data.weapon)
            if weapon_item.item_props.get('roomba') == user_data.poi:
                await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                await asyncio.sleep(7)
                roomba_loop = 1
            else:
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" Switch to set sidearm """


async def switch_weapon(cmd):
    user_data = EwUser(member=cmd.message.author)

    if user_data.weaponmarried:
        response = "You don't have the heart to cheat on your wife with your side ho. Not right in front of her. Not like this."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    weapon_holder = user_data.weapon
    user_data.weapon = user_data.sidearm
    user_data.sidearm = weapon_holder
    user_data.persist()

    if user_data.weapon == -1 and user_data.sidearm == -1:
        response = "You switch your nothing for nothing. What a notable exchange."
    elif user_data.weapon == -1 and user_data.sidearm:
        response = "You put your weapon away."
    elif user_data.weapon >= 0:
        weapon_item = EwItem(id_item=user_data.weapon)
        weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
        response = "**FWIP-CLICK!** You whip out your {}.".format(weapon_item.item_props.get("weapon_name") if weapon_item.item_props.get("weapon_name") != "" else weapon.str_name)
        if ewcfg.weapon_class_captcha in weapon.classes:
            newcaptcha = ewutils.text_to_regional_indicator(weapon_item.item_props.get('captcha'))
            response += " New captcha is {}.".format(newcaptcha)
    else:
        response = ""
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def null_cmd(cmd):
    return


async def duel(cmd):
    time_now = int(time.time())
    author = cmd.message.author

    challenger = EwUser(member=author)

    if challenger.poi == 'hangemsquare' and cmd.mentions_count == 0 and ewutils.square_duel == 0:
        channel = fe_utils.get_channel(server=cmd.guild, channel_name='hang-em-square')
        response = "OK, cowpokes, this whole field will be live in 60 seconds. Git ready!"
        ewutils.square_duel = 1
        await fe_utils.send_message(cmd.client, channel, fe_utils.formatMessage(author, response))
        await asyncio.sleep(55)
        for x in range(5):
            response = "**{}**".format(5 - x)
            await fe_utils.send_message(cmd.client, channel, fe_utils.formatMessage(author, response))
        response = "DRAW!"
        ewutils.square_duel = 2
        await fe_utils.send_message(cmd.client, channel, fe_utils.formatMessage(author, response))
        await asyncio.sleep(120)
        ewutils.square_duel = 0
        response = "Gee whillicers! The show's over, nothing to see here."
        return await fe_utils.send_message(cmd.client, channel, fe_utils.formatMessage(cmd.message.author, response))
    elif ewutils.square_duel in [1, 2] and challenger.poi == 'hangemsquare':
        response = "A duel's happening now, hold your horses."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif cmd.mentions_count != 1:
        # Must mention only one player
        response = "Mention the player you want to challenge."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))



    member = cmd.mentions[0]
    challengee = EwUser(member=member)

    if author.id == member.id:
        response = "You might be looking for !suicide."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))



    challenger_poi = poi_static.id_to_poi.get(challenger.poi)
    challengee_poi = poi_static.id_to_poi.get(challengee.poi)
    if (not challenger_poi.is_district or not challengee_poi.is_district) and challenger.poi != 'hangemsquare':
        response = "Both participants need to be in a district zone."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    # Players have been challenged
    if ewutils.active_target_map.get(challenger.id_user) != None and ewutils.active_target_map.get(challenger.id_user) != "":
        response = "You are already in the middle of a challenge."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))

    if ewutils.active_target_map.get(challengee.id_user) != None and ewutils.active_target_map.get(challengee.id_user) != "":
        response = "{} is already in the middle of a challenge.".format(member.display_name).replace("@", "\{at\}")
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))

    if challenger.poi != challengee.poi:
        response = "Both duelers must be in the same location."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))

    # Players have to be enlisted
    playable_life_states = [ewcfg.life_state_enlisted, ewcfg.life_state_lucky, ewcfg.life_state_executive]
    if challenger.life_state not in playable_life_states or challengee.life_state not in playable_life_states:
        if challenger.life_state == ewcfg.life_state_corpse:
            response = "Ghosts can't duel people. Alas, they can only watch from afar and !haunt."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))
        elif challengee.life_state == ewcfg.life_state_corpse:
            response = "Ghosts can't duel people. Alas, they can only watch from afar and !haunt."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))
        elif challenger.life_state == ewcfg.life_state_kingpin:
            response = "Throwing all of your gang's hard earned slime on the line strikes you as a bad idea..."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))
        elif challengee.life_state == ewcfg.life_state_kingpin:
            response = "They think about accepting for a moment, but then back away, remembering all the hard work their gangsters have put forth. Bummer..."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))
    # else:
    # 	response = "Juveniles are too cowardly to throw their lives away in a duel."
    # 	return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))

    # Assign a challenger so players can't be challenged
    ewutils.active_target_map[challenger.id_user] = challengee.id_user
    ewutils.active_target_map[challengee.id_user] = challenger.id_user

    # Apply restrictions to prevent movement, !tp, etc. This also lets the !accept command differentiate RR from duels.
    ewutils.active_restrictions[challenger.id_user] = 2
    ewutils.active_restrictions[challengee.id_user] = 2

    response = "You have been challenged by {} to a duel. Do you !accept or !refuse?".format(author.display_name).replace("@", "\{at\}")
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(member, response))

    # Wait for an answer
    accepted = False
    try:
        msg = await cmd.client.wait_for('message', timeout=30, check=lambda message: message.author == member and
                                                                                     message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])

        if msg != None:
            if msg.content == ewcfg.cmd_accept:
                accepted = True
    except:
        accepted = False

    # Start game
    if accepted == 1:
        challenger = EwUser(member=author)
        challengee = EwUser(member=member)

        # Start the countdown. Set restriction level to 3, which causes either user to die if they type during the countdown.
        ewutils.active_restrictions[challenger.id_user] = 3
        ewutils.active_restrictions[challengee.id_user] = 3

        countdown = 10

        while countdown != 0:
            # check if either user has had their restriction level set back to 0, indicating a death.
            if ewutils.active_restrictions[challenger.id_user] == 0 or ewutils.active_restrictions[challengee.id_user] == 0:
                ewutils.active_target_map[challenger.id_user] = ""
                ewutils.active_target_map[challengee.id_user] = ""

                ewutils.active_restrictions[challenger.id_user] = 0
                ewutils.active_restrictions[challengee.id_user] = 0

                response = "The duel is over before it even began."
                return await fe_utils.send_message(cmd.client, cmd.message.channel, response)

            if countdown > 8:
                text_mod = ""
            elif countdown > 6:
                text_mod = "*"
            elif countdown > 3:
                text_mod = "**"
            else:
                text_mod = "***"

            if countdown == 10:
                countdown_resp = "ENDLESS WAR begins to count down. Don't try anything funny...\n{}{}{}".format(text_mod, countdown, text_mod)
            else:
                countdown_resp = "{}{}{}".format(text_mod, countdown, text_mod)

            countdown -= 1
            await fe_utils.send_message(cmd.client, cmd.message.channel, countdown_resp)
            await asyncio.sleep(1)
            challenger = EwUser(member=author)
            challengee = EwUser(member=member)
            challenger.applyStatus(id_status=ewcfg.status_dueling)
            challengee.applyStatus(id_status=ewcfg.status_dueling)

        ewutils.active_restrictions[challenger.id_user] = 2
        ewutils.active_restrictions[challengee.id_user] = 2

        response = "{}***DRAW!***{}".format(ewcfg.emote_slimegun, ewcfg.emote_slimegun)
        await fe_utils.send_message(cmd.client, cmd.message.channel, response)

        await ewrolemgr.updateRoles(client=cmd.client, member=author)
        await ewrolemgr.updateRoles(client=cmd.client, member=member)
        challenger = EwUser(member=author)
        challengee = EwUser(member=member)

        duel_timer = ewcfg.time_pvp_duel

        challenger_slimes = challenger.slimes
        challengee_slimes = challengee.slimes

        while challenger_slimes > 0 and challengee_slimes > 0 and duel_timer > 0:
            # count down from 3 minutes, the max possible time a duel should last
            duel_timer -= 1
            await asyncio.sleep(1)

            # re-grab slime counts from both duelers
            challenger = EwUser(member=author)
            challengee = EwUser(member=member)
            challenger_slimes = challenger.slimes
            challengee_slimes = challengee.slimes

        challengee.clear_status(id_status=ewcfg.status_dueling)
        challenger.clear_status(id_status=ewcfg.status_dueling)

        if challenger.slimes <= 0:
            # challenger lost
            response = "**{} has won the duel!!**".format(member.display_name).replace("@", "\{at\}")
            await fe_utils.send_message(cmd.client, cmd.message.channel, response)
            challengee = EwUser(member=member)

        elif challengee.slimes <= 0:
            # challengee lost
            response = "**{} has won the duel!!**".format(author.display_name).replace("@", "\{at\}")
            await fe_utils.send_message(cmd.client, cmd.message.channel, response)
            challenger = EwUser(member=author)

        else:
            # timer stall
            response = "**Neither dueler was bloodthirsty enough to finish the job in time! The duel is over!**"
            await fe_utils.send_message(cmd.client, cmd.message.channel, response)

        await ewrolemgr.updateRoles(client=cmd.client, member=author)
        await ewrolemgr.updateRoles(client=cmd.client, member=member)


    # Or cancel the challenge
    else:
        response = "{} was too cowardly to accept your challenge.".format(member.display_name).replace("@", "\{at\}")
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(author, response))

    challenger = EwUser(member=author)
    challengee = EwUser(member=member)

    ewutils.active_target_map[challenger.id_user] = ""
    ewutils.active_target_map[challengee.id_user] = ""

    ewutils.active_restrictions[challenger.id_user] = 0
    ewutils.active_restrictions[challengee.id_user] = 0

    challenger.persist()
    challengee.persist()

    return
