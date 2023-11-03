import asyncio
import random
import time
import datetime
import math

from ew.backend import core as bknd_core
from ew.backend import item as bknd_item
from ew.backend.item import EwItem
from ew.backend.market import EwMarket
from ew.backend.mutation import EwMutation
from ew.backend.player import EwPlayer
from ew.static import cfg as ewcfg
from ew.static import hue as hue_static
from ew.static import items as static_items
from ew.static import mutations as static_mutations
from ew.static import poi as poi_static
from ew.static import weapons as static_weapons
from ew.utils import core as ewutils
from ew.utils import frontend as fe_utils
from ew.utils import item as itm_utils
from ew.utils import move as move_utils
from ew.utils import poi as poi_utils
from ew.utils import prank as prank_utils
from ew.utils import rolemgr as ewrolemgr
from ew.utils import cmd as cmd_utils
from ew.utils import mutations as mut_utils
from ew.utils.combat import EwUser
from ew.utils.district import EwDistrict
from ew.utils.frontend import EwResponseContainer
from ew.utils.slimeoid import EwSlimeoid
from ew.utils.user import add_xp
from .mutationutils import brickeat


async def chemo(cmd):
    user_data = EwUser(member=cmd.message.author)

    if cmd.message.channel.name != ewcfg.channel_clinicofslimoplasty:
        response = "Chemotherapy doesn't just grow on trees. You'll need to go to the clinic in Crookline to get some."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif user_data.life_state == ewcfg.life_state_corpse:
        response = '"You get out of here. We don\'t serve your kind." \n\n Auntie Dusttrap threatingly flails a jar of cole slaw at you. Looks like you need a body to operate on one.'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    mutations = user_data.get_mutations()
    if len(mutations) == 0:
        response = '"I can chemo you all day long, sonny. You\'re not getting any cleaner than you are."'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif len(cmd.tokens) <= 1:
        response = '"Are you into chemo for the thrill, boy? You have to tell me what you want taken out."'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif cmd.tokens[1] == "all":
        finalprice = 0

        for mutation in mutations:
            finalprice += static_mutations.mutations_map.get(mutation).tier * 5000

        if finalprice > user_data.slimes:
            response = '"We\'re not selling gumballs here. It\'s chemotherapy. It\'ll cost at least {:,} slime, ya idjit!"'.format(finalprice)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:
            response = "\"Sure you got the slime for that, whelp? It's {:,}.\"\n**Accept** or **refuse?**".format(finalprice)
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            try:
                accepted = False
                message = await cmd.client.wait_for('message', timeout=30, check=lambda message: message.author == cmd.message.author and message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])

                if message != None:
                    if message.content.lower() == ewcfg.cmd_accept:
                        accepted = True
                    if message.content.lower() == ewcfg.cmd_refuse:
                        accepted = False

            except Exception as e:
                ewutils.logMsg(f"Failed to process chemo check for {cmd.message.author.display_name}:{e}")
                accepted = False

            if not accepted:
                response = "\"Tch. Knew you weren't good for it.\""
            else:

                for mutation in mutations:

                    price = static_mutations.mutations_map.get(mutation).tier * 5000
                    user_data.change_slimes(n=-price, source=ewcfg.source_spending)

                    mutation_obj = EwMutation(id_mutation=mutation, id_user=user_data.id_user, id_server=cmd.message.guild.id)
                    if mutation_obj.artificial == 0:
                        try:
                            bknd_core.execute_sql_query(
                                "DELETE FROM mutations WHERE {id_server} = %s AND {id_user} = %s AND {mutation} = %s".format(
                                    id_server=ewcfg.col_id_server,
                                    id_user=ewcfg.col_id_user,
                                    mutation=ewcfg.col_id_mutation
                                ), (
                                    user_data.id_server,
                                    user_data.id_user,
                                    mutation,
                                ))
                        except:
                            ewutils.logMsg("Failed to clear mutations for user {}.".format(user_data.id_user))
                user_data.persist()
                response = '"Everything, eh? All right then. This might hurt a lottle!" Auntie Dusttrap takes a specialized shop vac and sucks the slime out of you. While you\'re reeling in slimeless existential dread, she runs it through a filtration process that gets rid of the carcinogens that cause mutation. She grabs the now purified canister and haphazardly dumps it back into you. You feel pure, energized, and ready to dirty up your slime some more!'
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])
        target = ewutils.get_mutation_alias(target_name)
        mutation_obj = EwMutation(id_mutation=target, id_user=user_data.id_user, id_server=cmd.message.guild.id)

        if target == 0:
            response = '"I don\'t know what kind of gold-rush era disease that is, but I have no idea how to take it out of you."'
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        elif target not in mutations:
            response = '"Oy vey, another hypochondriac. You don\'t have that mutation, so I can\'t remove it."'
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        elif static_mutations.mutations_map.get(target).tier * 5000 > user_data.slimes:
            response = '"We\'re not selling gumballs here. It\'s chemotherapy. It\'ll cost at least {} slime, ya idjit!"'.format(static_mutations.mutations_map.get(target).tier * 5000)
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        elif mutation_obj.artificial == 1:
            response = '"Hey, didn\'t I do that to ya? Well no refunds!"\n\nGuess you can\'t get rid of artificial mutations with chemo.'
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:
            price = static_mutations.mutations_map.get(target).tier * 5000
            user_data.change_slimes(n=-price, source=ewcfg.source_spending)
            user_data.persist()

            try:
                bknd_core.execute_sql_query("DELETE FROM mutations WHERE {id_server} = %s AND {id_user} = %s AND {mutation} = %s".format(
                    id_server=ewcfg.col_id_server,
                    id_user=ewcfg.col_id_user,
                    mutation=ewcfg.col_id_mutation
                ), (
                    user_data.id_server,
                    user_data.id_user,
                    target,
                ))
            except:
                ewutils.logMsg("Failed to clear mutations for user {}.".format(user_data.id_user))
            response = '"Alright, dearie, let\'s get you purged." You enter a dingy looking operating room, with slime strewn all over the floor. Dr. Dusttrap pulls out a needle the size of your bicep and injects into odd places on your body. After a few minutes of this, you get fatigued and go under.\n\n You wake up and {} is gone. Nice! \nMutation Levels Added:{}/{}'.format(
                static_mutations.mutations_map.get(target).str_name, user_data.get_mutation_level(), min(user_data.slimelevel, 50))
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def graft(cmd):
    user_data = EwUser(member=cmd.message.author)
    # print(mut_utils.active_mutations)
    if cmd.message.channel.name != ewcfg.channel_clinicofslimoplasty:
        response = "Chemotherapy doesn't just grow on trees. You'll need to go to the clinic in Crookline to get some."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    elif user_data.life_state == ewcfg.life_state_corpse:
        response = '"You get out of here, dirty nega. We don\'t serve your kind." \n\n Auntie Dusttrap threatingly flails a jar of cole slaw at you. Looks like you need a body to mutate a body.'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    elif len(cmd.tokens) <= 1:
        response = '"What, just anything? I love a good improv surgery! I had to leave town the last one I did though, so you\'ll have to pick an actual surgical procedure. Sorry, sonny."'
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])
    target = ewutils.get_mutation_alias(target_name)

    mutations = user_data.get_mutations()
    incompatible = False

    if target == 0:
        response = '"What? My ears aren\'t what they used to be. I thought you suggested I give you {}. Only braindead squicks would say that."'.format(' '.join(cmd.tokens[1:]))
        incompatible = True
    elif target not in mut_utils.active_mutations[user_data.id_server]:
        response = '"Plumb forgot how to do that surgery, sorry kid. My Alzheimers only lets me remember the procedures in the monthly rotation. A little too convenient, if you ask me."'
        incompatible = True
    elif target in mutations:
        response = '"Nope, you already have that mutation. Hey, I thought I was supposed to be the senile one here!"'
        incompatible = True
    elif user_data.get_mutation_level() + static_mutations.mutations_map[target].tier > min([user_data.slimelevel, 50]):
        response = '"Your body\'s already full of mutations. Your sentient tumors will probably start bitin\' once I take out my scalpel."\n\nLevel:{}/50\nMutation Levels Added:{}/{}'.format(user_data.slimelevel, user_data.get_mutation_level(), min(user_data.slimelevel, 50))
        incompatible = True
    elif static_mutations.mutations_map.get(target).tier * 10000 > user_data.slimes:
        response = '"We\'re not selling gumballs here. It\'s cosmetic surgery. It\'ll cost at least {:,} slime, ya idjit!"'.format(static_mutations.mutations_map.get(target).tier * 10000)
        incompatible = True

    for mutation in mutations:
        mutation = static_mutations.mutations_map[mutation]
        if target in mutation.incompatible:
            response = mutation.incompatible[target]
            incompatible = True
            break

    if incompatible:
        return await fe_utils.send_response(response, cmd)
    else:
        price = static_mutations.mutations_map.get(target).tier * 10000
        user_data.change_slimes(n=-price, source=ewcfg.source_spending)
        user_data.persist()

        user_data.add_mutation(id_mutation=target, is_artificial=1)
        response = static_mutations.mutations_map[target].str_transplant + "\n\nMutation Levels Added:{}/{}".format(user_data.get_mutation_level(), min(user_data.slimelevel, 50))
        await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def facelift(cmd):
    user_data = EwUser(member=cmd.message.author)
    if cmd.message.channel.name != ewcfg.channel_clinicofslimoplasty:
        response = "Rhinoplasty doesn't just grow on trees. You'll need to go to the clinic in Crookline to get some."
    elif user_data.life_state == ewcfg.life_state_corpse:
        response = '"You get out of here, dirty nega. We don\'t serve your kind." \n\n Auntie Dusttrap threatingly flails a jar of cole slaw at you. Looks like you need a body to cut up a body.'
    elif user_data.slimes < 20000000:
        response = 'We\'re not selling gumballs here. It\'s cosmetic surgery. It\'ll cost at least {:,} slime, ya idjit!"'.format(20000000)
    else:
        user_data.fashion_seed = random.randrange(500000)
        user_data.change_slimes(n=-20000000, source=ewcfg.source_spending)
        user_data.persist()
        response = "You throw down 20 million slime and ask Dr. Dusttrap you want to look unrecognizable. She bursts out laughing before raising her head to say \"Be careful what you wish for, sonny.\" Before you can think twice, she shoves her hand into your face, throwing you on her operating table. As she begins to painfully cut across your nose and temples with no anaesthetic, you realize your old face is probably going in the garbage can. Though blood covers your eyes and you cant see this, she pulls out her Wheel of Faces to decide the replacement. Ooh, you landed on #{}! Dusttrap quickly peels the old features off you and pops a new set back on, stitching it closed with the crocheting skils of an actually normal old lady. Once you recover, you take the bandages off your face. Hmm. Guess you're a {}/10 now.".format(random.randint(1, 100), random.randint(0, 10))
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    #the appearance comment is purely cosmetic but i kinda like the idea of players using that

async def preserve(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    if ewcfg.mutation_id_rigormortis not in mutations:
        response = "You can't just preserve something by saying you're going to. Everything ends eventually."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=cmd.guild.id if cmd.guild is not None else None)

    if item_sought:
        item_obj = EwItem(id_item=item_sought.get('id_item'))

        if item_obj.soulbound == True:
            response = "This thing's bound to your soul. There's no need to preserve it twice."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

        preserve_id = item_obj.item_props.get('preserved')
        if preserve_id == None:
            preserve_id = 0
        else:
            preserve_id = int(preserve_id)

        if preserve_id == int(user_data.id_user):
            response = "Didn't you already preserve this? You're so paranoid."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        elif item_obj.item_props.get('preserved') == "nopreserve":
            response = "You shove it into your body but it just won't fit for some reason. That phrasing was completely intentional, by the way."
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
        else:

            rigor = EwMutation(id_user=cmd.message.author.id, id_server=cmd.message.guild.id, id_mutation=ewcfg.mutation_id_rigormortis)

            if rigor.data.isdigit() == False:
                num = 0
            else:
                num = int(rigor.data)

            if num >= 5:
                response = "Your body's dried up, it's lost its ability to preserve objects."
            else:
                response = "You take the {} and embrace it with all your might. As you squeeze, it slowly but surely begins to phase inside your body. That won't get stolen anytime soon!".format(item_sought.get('name'))
                num += 1
                rigor.data = str(num)
                item_obj.item_props['preserved'] = user_data.id_user
                rigor.persist()
                item_obj.persist()
            return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    else:
        response = "Preserve what?"
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def waft(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    if ewcfg.mutation_id_aposematicstench not in mutations:
        response = "You stink, but not that badly. Get Aposematic Stench before you try that."
    else:
        user_data.applyStatus(ewcfg.status_repelled_id)
        response = "You clench as hard as you can, and your pores excrete a mushroom cloud of pure, olive green musk. It's so caustic you might not have eyebrows anymore. You should be immune from monsters, though!"

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def track_oneeyeopen(cmd):
    user_data = EwUser(id_user=cmd.message.author.id, id_server=cmd.message.guild.id)
    if cmd.mentions_count > 0:
        target_data = EwUser(member=cmd.mentions[0])
    mutations = user_data.get_mutations()

    if ewcfg.mutation_id_oneeyeopen not in mutations:
        response = "No can do. Your third eye is feeling pretty flaccid today."
    elif cmd.mentions_count == 0:
        response = "Who are you tracking?"
    elif cmd.mentions_count > 1:
        response = "Nice try, but you're not the NSA. Limit your espionage to one poor sap."
    elif cmd.mentions[0] == cmd.message.author:
        response = "You set your third eye to track yourself. However, you are too uncomfortable with your body to keep it there. Better try something else."
    else:
        response = "Your third eye slips out of your forehead and wanders its way to {}'s location. Just a matter of time...".format(cmd.mentions[0].display_name)
        mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_oneeyeopen)
        mutation_data.data = target_data.id_user
        mutation_data.persist()

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def shakeoff(cmd):
    user_data = EwUser(member=cmd.message.author)

    if cmd.mentions_count == 0:
        statuses = user_data.getStatusEffects()
        if user_data.poi in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown, ewcfg.poi_id_juviesrow] and ewcfg.status_repelled_id in statuses:
            user_data.clear_status(ewcfg.status_repelled_id)
            response = user_data.applyStatus(ewcfg.status_repelaftereffects_id)
        else:
            response = "God knows there are like a million third eyes floating around. You'll have to specify whose you're looking for."

    elif cmd.mentions_count > 1:
        response = "You're not that good at finding private eyes. Look for one at a time."

    else:
        target_data = EwUser(member=cmd.mentions[0])
        try:
            bknd_core.execute_sql_query(
                "UPDATE mutations SET {data} = %s WHERE {id_server} = %s AND {mutation} = %s and {id_user} = %s;".format(
                    data=ewcfg.col_mutation_data,
                    id_server=ewcfg.col_id_server,
                    id_user=ewcfg.col_id_user,
                    mutation=ewcfg.col_id_mutation,
                ), (
                    "",
                    user_data.id_server,
                    ewcfg.mutation_id_oneeyeopen,
                    target_data.id_user
                ))
            response = "You search high and low for {}'s third eye, shouting a bit to give it a good scare. If it was stalking you it certainly isn't now.".format(cmd.mentions[0].display_name)
        except:
            ewutils.logMsg("Failed to undo tracking for {}.".format(user_data.id_user))
            response = ""
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def clench(cmd):
    user_data = EwUser(member=cmd.message.author)
    response = "You clench your butt cheeks together..."
    ewutils.clenched[user_data.id_user] = 1
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    await asyncio.sleep(15)
    ewutils.clenched[user_data.id_user] = 0


async def bleedout(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()

    if ewcfg.mutation_id_bleedingheart not in mutations:
        response = "You don't have an open enough wound to just gush your blood everywhere."
    elif user_data.bleed_storage == 0:
        response = "There's nothing to bleed. Sounds like someone has a persecution complex..."
    elif user_data.bleed_storage > user_data.slimes:  # don't think this is possible, but just in case
        response = "Wait, wouldn't that kill you? Better not."
    else:
        response = "You clutch your malformed heart and squeeze as hard as you can. The intense pain makes you fall to your knees, and your slime drops in spurts to the floor under you as you gasp desperately for relief. You have been bled dry."
        poi = poi_static.id_to_poi.get(user_data.poi)
        district_data = EwDistrict(id_server=cmd.message.guild.id, district=poi.id_poi)
        user_data.change_slimes(n=-user_data.bleed_storage, source=ewcfg.source_bleeding)
        district_data.change_slimes(n=user_data.bleed_storage, source=ewcfg.source_bleeding)
        user_data.bleed_storage = 0
        user_data.persist()
        district_data.persist()
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


# async def bleh(cmd):
#	user_data = EwUser(member=cmd.message.author)
#	mutations = user_data.get_mutations()
#	market_data = EwMarket(id_server=cmd.message.guild.id)
#
#
#	if ewcfg.mutation_id_nosferatu in mutations and (market_data.clock < 6 or market_data.clock >= 20):
#		eeee = random.randrange(1, 20) * "E"
#		response = "**BL{}H!**".format(eeee)
#	else:
#		response = "You can't do that. That's cringe."
#
#	return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


""" !piss """


async def piss(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    respctn = EwResponseContainer(client=cmd.client, id_server=cmd.guild.id)

    if ewcfg.mutation_id_enlargedbladder in mutations:

        user_data.change_crime(n=1)
        user_data.persist()

        cosmetics = bknd_item.inventory(id_user=user_data.id_user, id_server=cmd.guild.id,
                                        item_type_filter=ewcfg.it_cosmetic)
        protected = False
        for cosmetic in cosmetics:
            cosmetic_data = EwItem(id_item=cosmetic.get('id_item'))
            if cosmetic_data.item_props.get('id_cosmetic') == 'chastitybelt':
                if cosmetic_data.item_props.get('adorned') == 'true':
                    protected = True

        if protected == True:
            response = "Reaching for your weewee, you instead hear the desolate metal clank of your hand against a steel groincage. Damn you, chastity belt. DAMN YOU TO HELL!!! "
            
        elif cmd.mentions_count == 0:
            response = "You unzip your dick and just start pissing all over the goddamn fucking floor. God, you’ve waited so long for this moment, and it’s just as perfect as you could have possibly imagined. You love pissing so much."
            if random.randint(1, 100) < 2:
                slimeoid = EwSlimeoid(member=cmd.message.author)
                if slimeoid.life_state == ewcfg.slimeoid_state_active:
                    hue = hue_static.hue_map.get("yellow")
                    response = "CONGRATULATIONS. You suddenly lose control of your HUGE COCK and saturate your {} with your PISS. {}".format(slimeoid.name, hue.str_saturate)
                    slimeoid.hue = (hue_static.hue_map.get("yellow")).id_hue
                    slimeoid.persist()

        elif cmd.mentions_count == 1:
            target_member = cmd.mentions[0]
            target_user_data = EwUser(member=target_member)

            if user_data.id_user == target_user_data.id_user:
                response = "Your love for piss knows no bounds. You aim your urine stream sky high, causing it to land right back into your own mouth. Mmmm, tasty~!"

            elif user_data.poi == target_user_data.poi:
                if target_user_data.life_state == ewcfg.life_state_corpse:
                    response = "You piss right through them! Their ghostly form ripples as the stream of urine pours endlessly unto them."
                else:
                    response = "You piss HARD and FAST right onto {}!!".format(target_member.display_name)
           
            elif ewcfg.mutation_id_quantumlegs in mutations:
                time_now = int(time.time())
                mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_quantumlegs)
                if len(mutation_data.data) > 0:
                    time_lastuse = int(mutation_data.data)
                else:
                    time_lastuse = 0

                if time_lastuse + 60 * 60 > time_now:
                    response = "You can't do that again yet. Try again in about {} minute(s)".format(math.ceil((time_lastuse + 60 * 60 - time_now) / 60))
                else:
                    mutation_data.data = str(time_now)
                    mutation_data.persist()
                    response = "The space directly above {}'s head prolapses into a shower of piss. Slurp's up!".format(target_member.display_name)
                    respctn.add_channel_response(poi_static.id_to_poi.get(target_user_data.poi).channel, response)
                    response = "You rev up your quantum cock and piss HARD and FAST right onto {}!!".format(target_member.display_name)
            else:
                response = "You can't !piss on someone who isn't there! Moron!"

        elif cmd.mentions_count > 1:
            response = "Whoa, one water-sports fetishist at a time, pal!"

    elif user_data.life_state == ewcfg.life_state_corpse:
        if cmd.mentions_count == 0:
            response = "You grow a ghost dick, unzip it, and just start ghost pissing all over the goddamn fucking floor. God, you’ve waited so long for this moment, and it’s just as perfect as you could have possibly imagined. You love ghost pissing so much."
            if random.randint(1, 100) < 3:
                response = "You grow a gussy, unzip it, and just start ghost pissing all over the goddamn fucking floor. God, you've waited so long for this moment, and it's just as perfect as you could have possibly imagined. You love ghost pissing so much."

        elif cmd.mentions_count == 1:
            target_member = cmd.mentions[0]
            target_user_data = EwUser(member=target_member)

            if user_data.id_user == target_user_data.id_user:
                response = "Your love for negapiss knows no bounds. You aim your antiurine stream sky high, causing it to land right back into your own ghastly mouth. Mmmm, tasty~!"

            elif user_data.poi == target_user_data.poi:
                if target_user_data.life_state == ewcfg.life_state_corpse:
                    response = "You ghost piss HARD and FAST right onto {}!!".format(target_member.display_name)

                else:
                    response = "Your ghost piss passes right through them! {} seems annoyed at the negapiss you're streaming at them, but they're entirely unaffected.".format(target_member.display_name)
            else:
                response = "You can't !piss on someone who isn't there! Moron!"

        elif cmd.mentions_count > 1:
            response = "Whoa, one necrophiliac at a time, pal!"

    else:
        response = "You lack the moral fiber necessary for urination."

    respctn.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    if xp_yield != 0:
        responses = await add_xp(cmd.message.author.id, cmd.guild.id, ewcfg.goonscape_pee_stat, xp_yield)
        for resp in responses: respctn.add_channel_response(cmd.message.channel, resp)
    return await respctn.post()


"""find out how many days are left until the 31st"""


async def fursuit(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    market_data = EwMarket(id_server=cmd.guild.id)

    # gets days until full moon
    if ewcfg.mutation_id_organicfursuit in mutations:
        days_until = -market_data.day % 29
        if days_until > 15:
            days_until -= 16
        elif days_until <= 14:
            days_until += 13
        else:
            days_until = 0

        if days_until == 0:
            response = "Hair is beginning to grow on the surface of your skin rapidly. Your canine instincts will take over soon!"
        else:
            response = "With a basic hairy palm reading, you determine that you'll be particularly powerful in {} day{}.".format(days_until, "s" if days_until != 1 else "")

        # If there's an active full moon, tell the user that they have the associated buffs.
        if ewutils.check_moon_phase(market_data) == ewcfg.moon_full:
            response = "The full moon shines above! Now's your chance to strike!"

    else:
        response = "You're about as hairless as an egg, my friend."

    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


# Eating not food
async def devour(cmd):
    user_data = EwUser(member=cmd.message.author)
    item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
    item_sought = bknd_item.find_item(id_server=cmd.message.guild.id, id_user=cmd.message.author.id, item_search=item_search)
    mutations = user_data.get_mutations()
    is_brick = 0
    time_now = int(time.time())
    mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_trashmouth)
    resp_ctn = EwResponseContainer(client=cmd.client, id_server=cmd.guild.id)
    responses = []

    if len(mutation_data.data) > 0:
        time_lastuse = int(mutation_data.data)
    else:
        time_lastuse = 0


    if ewcfg.mutation_id_trashmouth not in mutations:
        response = "Wait, what? Quit trying to put everything in your mouth."
    elif item_sought:
        item_obj = EwItem(id_item=item_sought.get('id_item'))
        if time_lastuse + 60 > time_now:
            response = "You're still picking stuff out of your teeth from the last weird shit you ate. Try again in {} seconds.".format(time_lastuse + 60 - time_now)
        elif (item_obj.item_type not in [ewcfg.it_cosmetic, ewcfg.it_furniture, ewcfg.it_food] and item_obj.item_props.get('id_item') != 'slimepoudrin') or item_obj.item_props.get('id_cosmetic') in ['soul', 'snouse']:
            response = "You swallow the {} whole, but after realizing this might be a mistake, you cough it back up.".format(item_sought.get('name'))
        elif item_obj.soulbound == True:
            response = "You attempt to consume the {}, but you realize it's soulbound and that you were about to eat your own existnece. Your life flashes before your eyes, so you decide to stop.".format(item_sought.get('name'))
        else:

            str_eat = "You unhinge your gaping maw and shove the {} right down, no chewing or anything. It's about as nutritious as you'd expect.".format(item_sought.get('name'))

            if item_obj.item_type == ewcfg.it_cosmetic:
                recover_hunger = 100
            elif item_obj.item_type == ewcfg.it_furniture:
                furn = static_items.furniture_map.get(item_obj.item_props.get('id_furniture'))
                acquisition = None
                if furn is not None:
                    acquisition = furn.acquisition
                    if furn.id_furniture == 'brick':
                        brickeat(item_obj=item_obj)
                        is_brick = 1
                        recover_hunger = 50
                        response = str_eat
                    elif acquisition != ewcfg.acquisition_bazaar:
                        recover_hunger = 100
                    elif furn.price < 500:
                        recover_hunger = 0
                    elif furn.price < 5000:
                        recover_hunger = 50
                    elif furn.price < 1000000:
                        recover_hunger = 320
                    else:
                        recover_hunger = 16000
                else:
                    # This only happens in the case of propstanded items, so we just set it to the lowest possible
                    recover_hunger = 50
            elif item_obj.item_type == ewcfg.it_food:
                if item_obj.item_props.get('perishable') != None:
                    perishable_status = item_obj.item_props.get('perishable')
                    if perishable_status == 'true' or perishable_status == '1':
                        item_is_non_perishable = False
                    else:
                        item_is_non_perishable = True
                else:
                    item_is_non_perishable = False

                user_has_spoiled_appetite = ewcfg.mutation_id_spoiledappetite in mutations
                item_has_expired = float(getattr(item_obj, "time_expir", 0)) < time.time()

                if item_has_expired and not (user_has_spoiled_appetite or item_is_non_perishable):
                    response = "You realize that the {} you were trying to eat is already spoiled. Ugh, not eating that.".format(item_sought.get('name'))
                    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
                # ewitem.item_drop(food_item.id_item)

                recover_hunger = item_obj.item_props.get('recover_hunger')

            else:
                recover_hunger = 100

            item_obj.item_props = {
                'id_food': "convertedfood",
                'food_name': "",
                'food_desc': "",
                'recover_hunger': recover_hunger,
                'inebriation': 0,
                'str_eat': str_eat,
                'time_expir': time.time() + ewcfg.std_food_expir,
                'time_fridged': 0,
                'perishable': True,
            }
            if item_obj.item_type != ewcfg.it_food:
                mutation_data.data = '{}'.format(time_now)
            if is_brick == 0:
                response = ""
                responses = await user_data.eat(item_obj)
            user_data.persist()
    elif item_search == "":
        response = "Devour what?"
    else:
        response = "Are you sure you have that item?"

    resp_ctn.add_channel_response(cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
    for resp in responses: resp_ctn.add_channel_response(cmd.message.channel, resp)
    return await resp_ctn.post()


async def longdrop(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()
    poi = poi_static.id_to_poi.get(user_data.poi)

    destination = ewutils.flattenTokenListToString(cmd.tokens[1])
    dest_poi = poi_static.id_to_poi.get(destination)

    item_search = ewutils.flattenTokenListToString(cmd.tokens[2:])
    item_sought = bknd_item.find_item(item_search=item_search, id_user=cmd.message.author.id, id_server=user_data.id_server)

    if ewcfg.mutation_id_longarms not in mutations:
        response = "As if anything on you was long enough to do that."
    elif cmd.tokens_count == 1:
        response = "You'll need for information that that. Try !longdrop <location> <item>."
    elif not item_sought:
        response = "You don't have that item."
    elif dest_poi == None:
        response = "Never heard of it."
    elif poi_utils.inaccessible(user_data=user_data, poi=dest_poi) or dest_poi.is_street:
        response = "Your arm hits a wall before it can make the drop off. Shit, probably can't take it over there."
    elif user_data.poi not in dest_poi.neighbors.keys() and dest_poi.id_poi not in poi.mother_districts:
        response = "You can't take it that far. What if a bird or car runs into your hand?"
    else:
        item_obj = EwItem(item_sought.get('id_item'))
        if item_obj.soulbound == True and item_obj.item_props.get('context') != 'housekey':
            response = "You still can't drop a soulbound item. Having really long arms doesn't grant you that ability."
        elif item_obj.item_type == ewcfg.it_weapon and user_data.weapon >= 0 and item_obj.id_item == user_data.weapon:
            if user_data.weaponmarried:
                weapon = static_weapons.weapon_map.get(item_obj.item_props.get("weapon_type"))
                response = "As much as it would be satisfying to just chuck your {} down an alley and be done with it, here in civilization we deal with things *maturely.* You’ll have to speak to the guy that got you into this mess in the first place, or at least the guy that allowed you to make the inane decision in the first place. Luckily for you, they’re the same person, and he’s at the Dojo.".format(
                    weapon.str_weapon)
                return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            else:
                user_data.weapon = -1
                user_data.persist()

        itm_utils.item_drop(id_item=item_sought.get('id_item'), other_poi=dest_poi.id_poi)
        response = "You stretch your arms and drop your " + item_sought.get("name") + ' into {}.'.format(dest_poi.str_name)
        await ewrolemgr.updateRoles(client=cmd.client, member=cmd.message.author)
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def skullbash(cmd):
    user_data = EwUser(member=cmd.message.author)
    item_stash = bknd_item.inventory(id_user=cmd.message.author.id, id_server=user_data.id_server)
    item_sought = None
    for item_piece in item_stash:
        item = EwItem(id_item=item_piece.get('id_item'))
        if item_piece.get('item_type') == ewcfg.it_furniture and item.item_props.get('id_furniture') == "brick":
            item_sought = item_piece

    if item_sought:
        if user_data.life_state == ewcfg.life_state_corpse:
            response = "Your head is too incorporeal to do that."
        else:
            ewutils.active_restrictions[user_data.id_user] = 2
            response = "You suck in your gut and mentally prepare to lose a few brain cells. 3...2...1...WHACK! Ugh. You're gonna need a minute."
            await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))
            await asyncio.sleep(600)
            ewutils.active_restrictions[user_data.id_user] = 0
            response = "The stars slowly begin to fade from your vision. Looks like you're lucid again."
    else:
        response = "You don't have a hard enough brick to bash your head in."

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def slap(cmd):
    if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

    time_now = int(time.time())
    user_data = EwUser(member=cmd.message.author)

    user_poi = poi_static.id_to_poi.get(user_data.poi)

    target_data = -1

    mutations = user_data.get_mutations()
    resp_cont = EwResponseContainer(id_server=cmd.guild.id)

    if cmd.tokens_count < 3:
        response = "You'll need to specify who and where you're slapping. Try !slap <target> <location>."
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    dest_poi = cmd.tokens[2].lower()
    dest_poi_obj = poi_static.id_to_poi.get(dest_poi)

    response = ""

    if cmd.mentions_count == 0:
        response = "Who are you slapping?"
    elif cmd.mentions_count > 1:
        response = "Nobody's that good at slapping. Do it to one person at a time."
    else:
        target_data = EwUser(member=cmd.mentions[0])

    if response != "":
        return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

    if target_data.poi != user_data.poi:
        response = "Not right now. You can't slap what you can't see."
    elif user_data.id_user == target_data.id_user:
        response = "Stop hitting yourself."
    elif ewutils.active_restrictions.get(target_data.id_user) != None and ewutils.active_restrictions.get(target_data.id_user) > 0:
        response = "They're in the middle of something, be patient."
    elif target_data.life_state == ewcfg.life_state_corpse:
        response = "You give {} a good whack. They're a ghost though, so your hand passes straight through.".format(cmd.mentions[0].display_name)
    elif ewcfg.mutation_id_ditchslap not in mutations:
        response = "You wind up your good arm and tacoom {} hard in the {}. The air gets knocked out of them but they stay firmly in place.".format(cmd.mentions[0].display_name, random.choice(['face', 'face', 'face', 'ass']))
    else:
        mutation_data = EwMutation(id_mutation=ewcfg.mutation_id_ditchslap, id_user=cmd.message.author.id, id_server=cmd.message.guild.id)

        if len(mutation_data.data) > 0:
            time_lastuse = int(mutation_data.data)
        else:
            time_lastuse = 0

        if dest_poi_obj.id_poi not in user_poi.neighbors.keys():
            response = "You can't hit them that far."
        elif move_utils.inaccessible(user_data=target_data, poi=dest_poi_obj):
            response = "That place is locked up good. You can't get a good launch angle to send them there."
        # elif time_lastuse + 180 * 60 > time_now:
        # response = "Your arm is spent from the last time you obliterated someone. Try again in {} minutes.".format(math.ceil((time_lastuse + 180*60 - time_now)/60))
        elif user_data.faction != target_data.faction:
            response = "You try to slap {}, but they realize what you're doing and jump back. Welp, back to the drawing board.".format(cmd.mentions[0].display_name)
        elif user_poi.id_poi in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown] or user_poi.is_apartment:
            response = "They're currently in their room. You'd have to carry {} out of it to slap them, which would be gay.".format(cmd.mentions[0].display_name)
        elif ewcfg.status_slapped_id in target_data.getStatusEffects():
            response = "Don't turn this into domestic abuse now. Can't you see they're still reeling from the last time?"
        elif (ewutils.clenched.get(target_data.id_user) == None or ewutils.clenched.get(target_data.id_user) == 0) and (user_poi.is_subzone or user_poi.is_district):
            response = "You wind up your slappin' hand and take a swing, but {} is all relaxed and you can't get a good angle. They end up flying into the wall. Better not touch people who aren't prepared to get hit...".format(cmd.mentions[0].display_name)
        else:
            response = "You wind up your slap. This one's gonna hurt. Steady as she goes...WHAM! {} is sent flying helplessly into {}!".format(cmd.mentions[0].display_name, dest_poi_obj.str_name)
            target_data.applyStatus(id_status=ewcfg.status_slapped_id)
            dm_response = "WHAP! {} smacked you into {}!".format(cmd.message.author.display_name, dest_poi_obj.str_name)
            target_response = "**CRAAAAAAAAAAAASH!** You arrive in {}!".format(dest_poi_obj.str_name)
            ewutils.moves_active[cmd.message.author.id] = 0
            target_data.poi = dest_poi_obj.id_poi
            user_data.time_lastenter = int(time.time())

            mutation_data.data = str(time_now)
            mutation_data.persist()

            if target_data.poi == ewcfg.poi_id_thesewers:
                await target_data.die(cause=ewcfg.cause_suicide)
                target_response += " But you hit your head really hard! Your precious little dome explodes into bits and pieces and you die!"
                target_died = True

            user_data.persist()

            if not target_died:
                await ewrolemgr.updateRoles(client=ewutils.get_client(), member=cmd.mentions[0], new_poi=target_data.poi)
                target_data.persist()

                await user_data.move_inhabitants(id_poi=dest_poi_obj.id_poi)

                await prank_utils.activate_trap_items(dest_poi_obj.id_poi, user_data.id_server, target_data.id_user)

            await fe_utils.send_message(cmd.client, cmd.mentions[0], fe_utils.formatMessage(cmd.mentions[0], dm_response))
            await fe_utils.send_message(cmd.client, fe_utils.get_channel(server=cmd.mentions[0].guild, channel_name=dest_poi_obj.channel), fe_utils.formatMessage(cmd.mentions[0], target_response))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def tracker(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()

    if ewcfg.mutation_id_oneeyeopen not in mutations:
        response = "Your third eye is tucked snugly into your forehead. Actually, who are you fooling? You don't have a third eye. What, are you, dimwitted?"
    else:
        mutation = EwMutation(id_server=cmd.message.guild.id, id_user=cmd.message.author.id, id_mutation=ewcfg.mutation_id_oneeyeopen)
        if mutation.data == "":
            response = "Your third eye isn't tracking anyone right now."
        else:
            target = EwPlayer(id_server=cmd.message.guild.id, id_user=mutation.data)
            response = "You're tracking {} right now. LOL, they're lookin pretty dumb over there.".format(target.display_name)

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


"""
Admin-only commands
"""

# Force a mutation to be grafted, ignoring incompatibilities and mutation level.
async def forcegraft(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    # Grab player or, if none specified, the author.
    if cmd.mentions_count == 1:
        user = cmd.mentions[0]
    else:
        user = cmd.message.author

    user_data = EwUser(member=user)

    # Get desired mutation
    target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])
    target = ewutils.get_mutation_alias(target_name)

    mutations = user_data.get_mutations()

    if target == 0:
        response = "There is not a \"{}\" mutation.".format(target_name)
    elif target in mutations:
        response = "You already have that mutation."
    else:
        # Add the mutation
        user_data.add_mutation(id_mutation=target, is_artificial=1)
        response = "You have forcibly grafted {}.".format(target)
    # Send message
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def forcechemo(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return await cmd_utils.fake_failed_command(cmd)

    # Grab player or, if none specified, the author.
    if cmd.mentions_count == 1:
        user = cmd.mentions[0]
    else:
        user = cmd.message.author

    user_data = EwUser(member=user)

    # Get desired mutation
    target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])
    target = ewutils.get_mutation_alias(target_name)

    mutations = user_data.get_mutations()

    if target == 0:
        response = "There is not a \"{}\" mutation.".format(target_name)
    elif target not in mutations:
        response = "You do not have that mutation."
    else:
        # Remove the mutation
        try:
            bknd_core.execute_sql_query(
                "DELETE FROM mutations WHERE {id_server} = %s AND {id_user} = %s AND {mutation} = %s".format(
                    id_server=ewcfg.col_id_server,
                    id_user=ewcfg.col_id_user,
                    mutation=ewcfg.col_id_mutation
                ), (
                    user_data.id_server,
                    user_data.id_user,
                    target,
                ))
        except:
            ewutils.logMsg("Failed to clear mutations for user {}.".format(user_data.id_user))
        response = "You have forcibly chemo'd {}.".format(target)
    # Send message
    await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def display_current_rotation(cmd):
    today = datetime.date.today()
    month = int(today.month)
    year = int(today.year)

    if cmd.tokens[0] == ewcfg.cmd_prefix + 'nextrotation' and cmd.message.author.guild_permissions.administrator:
        month = (month % 12) + 1
        year = year if month != 12 else year + 1
    elif cmd.tokens[0] == ewcfg.cmd_prefix + 'nextrotation':
        return

    current_rotation_data = bknd_core.execute_sql_query(
        "select {id_mutation}, {context_num} from mut_rotations where {month} = %s and {year} = %s and {id_server} = %s".format(
            id_mutation=ewcfg.col_id_mutation,
            context_num=ewcfg.col_id_context_num,
            month=ewcfg.col_id_month,
            year=ewcfg.col_id_year,
            id_server=ewcfg.col_id_server
        ), (month, year, cmd.guild.id))

    response = 'ACTIVE MUTATIONS\n'
    stat_resp = '\nADDITIONAL MODIFIERS\n'
    for piece in current_rotation_data:
        if piece[0] in mut_utils.stat_ranges.keys():
            if piece[1] == 1:
                continue
            stat_resp += mut_utils.stat_ranges.get(piece[0])[2].format(piece[1])
        else:
            mutation_obj = static_mutations.mutations_map.get(piece[0])
            response += mutation_obj.str_name + ', '

    if stat_resp != '\nADDITIONAL MODIFIERS\n':
        response += stat_resp

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def add_rotation_mut(cmd):
    target_name = cmd.tokens[1]
    target = ewutils.get_mutation_alias(target_name)
    today = datetime.date.today()
    month = int(today.month)
    year = int(today.year)
    if not cmd.message.author.guild_permissions.administrator:
        return
    if target == 0:
        response = "Not a mutation, genius. Can you believe this dev and/or mod runs the place?"
    else:
            if 'future' in cmd.tokens:
                month = (month % 12) + 1
                year = year if month != 12 else year + 1
            else:
                mut_utils.active_mutations.get(cmd.guild.id).append(target)

            response = "Added."

            bknd_core.execute_sql_query(
                "replace into mut_rotations({id_server}, {id_month}, {id_year}, {mutation}, {context_num}) values(%s, %s, %s, %s, %s)".format(
                    id_server=ewcfg.col_id_server,
                    id_month=ewcfg.col_id_month,
                    id_year=ewcfg.col_id_year,
                    mutation=ewcfg.col_id_mutation,
                    context_num=ewcfg.col_id_context_num
                ), (cmd.guild.id,
                    month,
                    year,
                    target,
                    1))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def drop_rotation_mut(cmd):
    target_name = cmd.tokens[1]
    target = ewutils.get_mutation_alias(target_name)
    today = datetime.date.today()
    month = int(today.month)
    year = int(today.year)
    # print("{} {} {}".format(cmd.guild.id, year, target))
    if not cmd.message.author.guild_permissions.administrator:
        return
    if target == 0:
        response = "Not a mutation, genius. Can you believe this dev and/or mod runs the place?"
    else:
        if 'future' in cmd.tokens:
            month = (month % 12) + 1
            year = year if month != 12 else year + 1
        else:
            mut_utils.active_mutations[cmd.guild.id].remove(target)
        response = "Removed."
        bknd_core.execute_sql_query(
            "delete from mut_rotations where {id_server} = %s and {id_month} = %s  and {id_year} = %s and {mutation} = %s".format(
                id_server=ewcfg.col_id_server,
                id_month=ewcfg.col_id_month,
                id_year=ewcfg.col_id_year,
                mutation=ewcfg.col_id_mutation
            ), (cmd.guild.id,
                month,
                year,
                target))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def change_rotation_stat(cmd):
    target_name = cmd.tokens[1]
    today = datetime.date.today()
    month = int(today.month)
    year = int(today.year)
    if not cmd.message.author.guild_permissions.administrator:
        return
    if cmd.tokens_count != 3:
        response = "You failed to fuck with everything. Try !changerotation <stat> <value>"
    else:
        if 'future' in cmd.tokens:
            month = (month % 12) + 1
            year = year if month != 12 else year + 1
        targetnum = round(float(cmd.tokens[2]), 2)
        response = "Successfully fucked with everything by setting {} to {}. You may need to restart to apply changes.".format(target_name, targetnum)
        bknd_core.execute_sql_query(
            "update mut_rotations set {context_num} = %s where {id_server} = %s and {id_month} = %s  and {id_year} = %s and {mutation} = %s".format(
                id_server=ewcfg.col_id_server,
                id_month=ewcfg.col_id_month,
                id_year=ewcfg.col_id_year,
                mutation=ewcfg.col_id_mutation,
                context_num=ewcfg.col_id_context_num
            ), (targetnum,
                cmd.guild.id,
                month,
                year,
                target_name))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def lock_mutation(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    target_name = cmd.tokens[1]
    target = ewutils.get_mutation_alias(target_name)

    if target == 0:
        response = "Not a mutation, genius. Can you believe this dev and/or mod runs the place?"
    else:
        response = "Locked in."

        bknd_core.execute_sql_query(
            "replace into mut_rotations({id_server}, {id_month}, {id_year}, {mutation}, {context_num}) values(%s, %s, %s, %s, %s)".format(
                id_server=ewcfg.col_id_server,
                id_month=ewcfg.col_id_month,
                id_year=ewcfg.col_id_year,
                mutation=ewcfg.col_id_mutation,
                context_num=ewcfg.col_id_context_num
            ), (cmd.guild.id,
                0,
                0,
                target,
                1))
    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))


async def unlock_mutation(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    target_name = cmd.tokens[1]
    target = ewutils.get_mutation_alias(target_name)

    if target == 0:
        response = "Not a mutation, genius. Can you believe this dev and/or mod runs the place?"
    else:
        response = "Released the lock for this mutation."

        bknd_core.execute_sql_query(
            "delete from mut_rotations where {id_server} = %s and {id_month} = %s  and {id_year} = %s and {mutation} = %s".format(
                id_server=ewcfg.col_id_server,
                id_month=ewcfg.col_id_month,
                id_year=ewcfg.col_id_year,
                mutation=ewcfg.col_id_mutation
            ), (cmd.guild.id,
                0,
                0,
                target))

    return await fe_utils.send_message(cmd.client, cmd.message.channel, fe_utils.formatMessage(cmd.message.author, response))

async def brace(cmd):
    user_data = EwUser(member=cmd.message.author)
    mutations = user_data.get_mutations()

    time_now = int(time.time())

    if ewcfg.mutation_id_nervesofsteel not in mutations:
        response = "Bet you'd flinch if you tried, bitch. Get stronger nerves before you attempt that kind of shit."
    else:

        mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_nervesofsteel)
        if len(mutation_data.data) > 0:
            time_lastuse = int(mutation_data.data)
        else:
            time_lastuse = 0

        if time_lastuse + 120 > time_now:
            response = "You can't do that again yet. Try again in about {} second(s)".format((time_lastuse+120)-time_now)
            #return await fe_utils.send_response(response, cmd)
        else:
            ewutils.moves_active[user_data.id_user] = 0
            ewutils.active_restrictions[user_data.id_user] = 2
            user_data.applyStatus(ewcfg.status_braced_id)
            await fe_utils.send_response("HIT THE DECK!", cmd)
            await asyncio.sleep(25)

            for x in range(5):
                await fe_utils.send_response("**{}!**".format(5-x), cmd)
                await asyncio.sleep(1)

            user_data.clear_status(id_status=ewcfg.status_braced_id)
            response = "**0!**"
            ewutils.active_restrictions[user_data.id_user] = 0

            mutation_data = EwMutation(id_user=user_data.id_user, id_server=user_data.id_server, id_mutation=ewcfg.mutation_id_nervesofsteel)
            mutation_data.data = str(time_now)
            mutation_data.persist()


    return await fe_utils.send_response(response, cmd)
