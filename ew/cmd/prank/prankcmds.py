import random

from ew.static import cfg as ewcfg
from ew.utils.combat import EwUser
import ew.utils.frontend as ewutils
from ew.utils import stats as ewstats
import ew.backend.item as bknd_item
import asyncio
import ew.utils.rolemgr as ewrolemgr

async def gambit(cmd):
    if cmd.mentions_count == 0:
        gambit = ewstats.get_stat(id_server=cmd.guild.id, id_user=cmd.message.author.id, metric=ewcfg.stat_gambit)
        response = "You currently have {:,} gambit.".format(gambit)

    else:
        member = cmd.mentions[0]
        gambit = ewstats.get_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_gambit)
        response = "{} currently has {:,} gambit.".format(member.display_name, gambit)

    # Send the response to the player.
    await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


async def credence(cmd):
    if cmd.mentions_count == 0:
        credence = ewstats.get_stat(id_server=cmd.guild.id, id_user=cmd.message.author.id, metric=ewcfg.stat_credence)
        credence_used = ewstats.get_stat(id_server=cmd.guild.id, id_user=cmd.message.author.id, metric=ewcfg.stat_credence_used)
            
        if credence > 0:
            response = "You have {:,} credence and {:,} credence used. Don't fuck this up.".format(credence, credence_used)
        else:
            response = "You don't have any credence. You'll need to build some up in the city before you can get to pranking again."

    else:
        member = cmd.mentions[0]
        credence = ewstats.get_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_credence)
        credence_used = ewstats.get_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_credence_used)

        if credence > 0:
            response = "They have {:,} credence and {:,} credence used. Time for a little anarchy.".format(credence, credence_used)
        else:
            response = "They don't have any credence."

    # Send the response to the player.
    await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


async def reset_prank_stats(cmd):
    if not cmd.message.author.server_permissions.administrator:
        return

    if cmd.mentions_count == 0:
        member = cmd.message.author
    else:
        member = cmd.mentions[0]


    ewstats.set_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_gambit, value=0)
    ewstats.set_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_credence, value=100)
    ewstats.set_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_credence_used, value=0)

    response = "Prank stats reset for {}.".format(member.display_name)
    await ewutils.send_message(cmd.client, cmd.message.channel, response)


async def set_gambit(cmd):
    if not cmd.message.author.server_permissions.administrator:
        return

    if cmd.mentions_count == 1:
        member = cmd.mentions[0]
    else:
        member = cmd.message.author

    if not len(cmd.tokens) > 1:
        return

    gambit_set = int(cmd.tokens[1])

    ewstats.set_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_gambit, value=gambit_set)
    ewstats.set_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_credence, value=100)
    ewstats.set_stat(id_server=cmd.guild.id, id_user=member.id, metric=ewcfg.stat_credence_used, value=0)

    response = "Gambit for {} set to {:,}.".format(member.display_name, gambit_set)

    await ewutils.send_message(cmd.client, cmd.message.channel, response)


async def point_and_laugh(cmd):
    if cmd.mentions_count == 1:
        member = cmd.mentions[0]

        response_choices = [
            "WHAT an *Asshole!*",
            "They have quite possibly NEVER had SEX!",
            "Dumbass!",
            "What a fucking freak!",
            "Holy shit, can you get any lower than this dude?",
            "Friccin Moron!",
            "Guess we're not all born winners..."
        ]

        choice_response = random.choice(response_choices)

        response = "You point and laugh at {}! {} LOL!!!".format(member.display_name, choice_response)
    else:
        response = "You point and laugh at... who, exactly?"

    return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))










