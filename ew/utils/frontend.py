import asyncio
import sys
import traceback
import random

import discord

from . import core as ewutils
from . import rolemgr as ewrolemgr
from ..backend import core as bknd_core
from ..backend.hunting import EwEnemyBase as EwEnemy
from ..backend.item import EwItem
from ..backend.player import EwPlayer
from ..backend.user import EwUserBase as EwUser
from ..static import cfg as ewcfg
from ..static import hunting as hunt_static
from ..static import poi as poi_static
from ..static import weapons as static_weapons
from ew.backend.dungeons import EwGamestate
from ew.utils import stats as ewstats

channel_map = {}
"""
    channel_map = {
        server_id : {
            channel_str: channel_obj
            }
        }
"""


class Message:
    # Send the message to this exact channel by name.
    channel = None

    # Send the message to the channel associated with this point of interest.
    id_poi = None

    # Should this message echo to adjacent points of interest?
    reverb = None
    message = ""

    def __init__(
            self,
            channel = None,
            reverb = False,
            message = "",
            id_poi = None
    ):
        self.channel = channel
        self.reverb = reverb
        self.message = message
        self.id_poi = id_poi


"""
	Class for storing, passing, editing and posting channel responses and topics
"""


class EwResponseContainer:
    client = None
    id_server = -1
    channel_responses = {}
    channel_topics = {}
    members_to_update = []

    def __init__(self, client = None, id_server = None):
        self.client = client if client is not None else ewutils.get_client()
        self.id_server = id_server
        self.channel_responses = {}
        self.channel_topics = {}
        self.members_to_update = []

    def add_channel_response(self, channel, response):
        # Try to keep channels as objects where possible. between thread, regular, and dm channels, names are spooky to rely on
        if isinstance(channel, str):
            seek = get_channel(server=self.client.get_guild(int(self.id_server)), channel_name=channel)
            channel = seek if seek is not None else channel

        # Report bad inputs
        if not hasattr(channel, "send"):
            ewutils.logMsg("Error: add_channel_response could not parse channel from {}".format(channel))

        # Attempt to split at newlines if it exceeds the max length
        responses = []
        if len(response) > ewcfg.discord_message_length_limit and len(response.split("\n")) > 2:
            temp_str = response.split("\n", 1)[0]
            for shortstr in response.split("\n")[1:]:
                shortstr = "\n" + shortstr
                if len(temp_str) + len(shortstr) < ewcfg.discord_message_length_limit:
                    temp_str += shortstr
                else:
                    responses.append(temp_str)
                    temp_str = shortstr
            responses.append(temp_str)

        # Add response to existing entry for its channel, or create a new entry
        if channel in self.channel_responses:
            if len(responses) > 1:  # Use listed responses only when splitting successfully created at least 2
                self.channel_responses[channel] += responses
            else:
                self.channel_responses[channel].append(response)
        else:
            if len(responses) > 1:
                self.channel_responses[channel] = responses
            else:
                self.channel_responses[channel] = [response]

    def add_channel_topic(self, channel, topic):
        if isinstance(channel, str):  # For consistency (Even though this is commented out of post???)
            seek = get_channel(server=self.client.get_guild(int(self.id_server)), channel_name=channel)
            channel = seek if seek is not None else channel

        self.channel_topics[channel] = topic

    def add_member_to_update(self, member):
        for update_member in self.members_to_update:
            if update_member.id == member.id:
                return

        self.members_to_update.append(member)

    def add_response_container(self, resp_cont):
        for ch in resp_cont.channel_responses:
            responses = resp_cont.channel_responses[ch]
            for r in responses:
                self.add_channel_response(ch, r)

        for ch in resp_cont.channel_topics:
            self.add_channel_topic(ch, resp_cont.channel_topics[ch])

        for member in resp_cont.members_to_update:
            self.add_member_to_update(member)

    def format_channel_response(self, channel, member):
        if channel in self.channel_responses:
            for i in range(len(self.channel_responses[channel])):
                self.channel_responses[channel][i] = formatMessage(member, self.channel_responses[channel][i])

    async def post(self, channel = None, delete_after = None):
        self.client = ewutils.get_client()
        messages = []

        if self.client is None:
            ewutils.logMsg("Couldn't find client")
            return messages

        server = self.client.get_guild(int(self.id_server))
        if server is None:
            ewutils.logMsg("Couldn't find server with id {}".format(self.id_server))
            return messages

        for member in self.members_to_update:
            await ewrolemgr.updateRoles(client=self.client, member=member)

        for ch in self.channel_responses:
            if channel is None:
                # add_channel_response should be catching any string entries
                current_channel = ch
            else:
                current_channel = channel
            try:
                response = ""
                while len(self.channel_responses[ch]) > 0:
                    if len(self.channel_responses[ch][0]) > ewcfg.discord_message_length_limit:
                        response += "\n" + self.channel_responses[ch].pop(0)
                        length = len(response)
                        split_list = [(response[i:i + 2000]) for i in range(0, length, 2000)]
                        for blurb in split_list:
                            message = await send_message(client = self.client, channel=current_channel, text = blurb, delete_after=delete_after)
                            if message:
                                messages.append(message)
                        response = ""
                    elif len(response) == 0 or len("{}\n{}".format(response, self.channel_responses[ch][0])) < ewcfg.discord_message_length_limit:
                        response += "\n" + self.channel_responses[ch].pop(0)
                    else:
                        message = await send_message(client = self.client, channel=current_channel, text =response, delete_after=delete_after)
                        if message:
                            messages.append(message)
                        response = ""
                message = await send_message(client = self.client, channel=current_channel, text = response, delete_after=delete_after)
                messages.append(message)
            except Exception as e:
                ewutils.logMsg('Resp cont failed to send message to channel {}: {}\n{}'.format(ch, self.channel_responses[ch], e))

        return messages


def readMessage(fname):
    msg = Message()

    try:
        f = open(fname, "r")
        f_lines = f.readlines()

        count = 0
        for line in f_lines:
            line = line.rstrip()
            count += 1
            if len(line) == 0:
                break

            args = line.split('=')
            if len(args) == 2:
                field = args[0].strip().lower()
                value = args[1].strip()

                if field == "channel":
                    msg.channel = value.lower()
                elif field == "poi":
                    msg.poi = value.lower()
                elif field == "reverb":
                    msg.reverb = True if (value.lower() == "true") else False
            else:
                count -= 1
                break

        for line in f_lines[count:]:
            msg.message += (line.rstrip() + "\n")
    except:
        ewutils.logMsg('failed to parse message.')
        traceback.print_exc(file=sys.stdout)
    finally:
        f.close()

    return msg





def formatMessage(user_target, message):
    """ Format responses with the target's display name, e.g. Dev: You have 69 slime.
        - user_target needs to be either an EwEnemy or a discord Member/EwPlayer
    """

    if hasattr(user_target, "id_enemy"):
        if user_target.life_state == ewcfg.enemy_lifestate_alive:
            # Send messages for normal enemies, and allow mentioning with @
            if user_target.identifier != '':
                return "*{} [{}]* {}".format(user_target.display_name, user_target.identifier, message)
            else:
                return "*{}:* {}".format(user_target.display_name, message)
        # If the display name belongs to an unactivated raid boss, hide its name while it's counting down.
        elif user_target.display_name in ewcfg.raid_boss_names and user_target.life_state == ewcfg.enemy_lifestate_unactivated:
            return "{}".format(message)

    # If user_target isn't an enemy, catch the exception.
    else:
        if hasattr(user_target, "id_user") and hasattr(user_target, "id_server"):
            user_obj = EwUser(id_server=user_target.id_server, id_user=user_target.id_user)
        else:
            user_obj = EwUser(member=user_target)
        mutations = user_obj.get_mutations()
        if ewcfg.mutation_id_amnesia in mutations:
            display_name = '?????'
        else:
            display_name = user_target.display_name

        return "*{}:* {}".format(display_name, message).replace("{", "\{").replace("@", "{at}")


"""
	Send a message to multiple chat channels at once. "channels" can be either a list of discord channel objects or strings
"""


async def post_in_channels(id_server, message, channels = None):
    client = ewutils.get_client()
    server = client.get_guild(id=id_server)

    if channels is None and server is not None:
        channels = server.channels

    for channel in channels:
        if type(channel) is str:  # if the channels are passed as strings instead of discord channel objects
            channel = get_channel(server, channel)
        if channel is not None and channel.type == discord.ChannelType.text:
            await channel.send(content=message)
    return


def get_channel(server: discord.Guild, channel_name: str):
    """ Find a chat channel by name in a server. """
    server_channel_map = channel_map.get(server.id)
    found_ch = server_channel_map.get(channel_name)

    if not found_ch:
        # Look up the channel in discord and assign it to the map
        for chan in server.channels:
            if chan.name == channel_name:
                channel_map[server.id][channel_name] = chan
                found_ch = chan

        if not found_ch and not ewutils.DEBUG:
            ewutils.logMsg(f'Error: In get_channel(), could not find channel using channel_name "{channel_name}"')
            return None

    return found_ch


def map_channels(server):
    """ Map every channel str to the proper channel object """
    ch_found = 0
    total_ch = len(poi_static.poi_list)

    server_channel_map = {}

    # Map POI Channels
    for poi in poi_static.poi_list:
        ch_search = poi.channel
        for chan in server.channels:
            if chan.name == ch_search:
                server_channel_map[ch_search] = chan
                ch_found += 1

    channel_map[server.id] = server_channel_map

    ewutils.logMsg(f"{server.name}: Found {ch_found} POI channels. {total_ch - ch_found} POI channels missing.")


def find_kingpin(id_server, kingpin_role):
    data = bknd_core.execute_sql_query("SELECT id_user FROM users WHERE id_server = %s AND {life_state} = %s AND {faction} = %s".format(
        life_state=ewcfg.col_life_state,
        faction=ewcfg.col_faction
    ), (
        id_server,
        ewcfg.life_state_kingpin,
        ewcfg.faction_rowdys if kingpin_role == ewcfg.role_rowdyfucker else ewcfg.faction_killers
    ))

    kingpin = None

    if len(data) > 0:
        id_kingpin = data[0][0]
        kingpin = EwUser(id_server=id_server, id_user=id_kingpin)

    return kingpin


"""
	Posts a message both in CK and RR.
"""


async def post_in_hideouts(id_server, message):
    await post_in_channels(
        id_server=id_server,
        message=message,
        channels=[ewcfg.channel_copkilltown, ewcfg.channel_rowdyroughhouse]
    )

# FIXME remove client from this and a bunch of other front end commands, it's completely useless
async def send_message(client, channel, text=None, embed=None, delete_after=None, filter_everyone=True):
    """
        Proxy to discord.py channel.send with exception handling
        - channel is a discord Channel
    """
    # Handle oversized messages recursively - yes, this is modified from resp_cont
    if text and len(text) > ewcfg.discord_message_length_limit:
        length = len(text)
        split_list = [(text[i:i + 2000]) for i in range(0, length, 2000)]
        if len(split_list) >= 3:
            ewutils.logMsg(f"Tried to send oversize message with {len(split_list)} parts - John Discord (rate limit) doesn't like this.")
        for blurb in split_list:
            try:
                await send_message(client=client, channel=channel, text=blurb, delete_after=delete_after, embed=embed)
            except Exception as e:
                ewutils.logMsg(f"Failed to send message to channel {channel}, reason was: {e}")
            embed = None
        return

    # catch any future @everyone exploits
    if filter_everyone:
        mention_allows = discord.AllowedMentions(everyone=False, users=True, roles=False)
    else: # allow @everyone (and everything)
        mention_allows = discord.AllowedMentions(everyone=True, users=True, roles=True)

    try:
        # Whitespace messages will always fail to send, don't clutter the log
        if text and not text.isspace():
            return await channel.send(content=text, delete_after=delete_after, allowed_mentions=mention_allows, embed=embed)
        if embed is not None:
            return await channel.send(embed=embed)
    except discord.errors.Forbidden:
        ewutils.logMsg('Could not message user: {}\n{}'.format(channel, text))
        raise
    except Exception as e:
        ewutils.logMsg('Send message failed to send message to channel: {}\n{}: {}'.format(channel, text, e))


async def send_response(response_text, cmd = None, delete_after = None, name = None, channel = None, format_name = True, format_ats = True, allow_everyone = False, embed = None):
    """ Simpler to use wrapper for send_message that formats message by default """

    if cmd is None and channel is None:
        raise Exception("No channel to send message to")

    if channel is None:
        channel = cmd.message.channel

    if name is None and cmd:
        name = cmd.author_id.display_name
        user_data = EwUser(member=cmd.message.author)
        user_mutations = user_data.get_mutations()
        if ewcfg.mutation_id_amnesia in user_mutations:
            name = '?????'

    if format_name and name:
        response_text = "*{}:* {}".format(name, response_text)

    if ewutils.DEBUG:  # to see when the bot uses send_response vs send_message in --debug mode
        response_text = "--{}".format(response_text)

    if format_ats:
        response_text = response_text.replace("@", "{at}")

    try:
        # The None is for send_message's vestigial client bit. I gotta put it in like this or otherwise the millions
        # of implementations that rely on client as a positional will break
        # and i do not wish to change every instance of send_message today

        return await send_message(None, channel=channel, text=response_text, delete_after=delete_after, filter_everyone=not allow_everyone, embed=embed)
    except discord.errors.Forbidden:
        ewutils.logMsg('Could not respond to user: {}\n{}'.format(channel, response_text))
        raise
    except Exception as e:
        ewutils.logMsg('Send response failed to send message to channel: {}\n{}:\n{}'.format(channel, response_text, e))


"""
	Proxy to discord.py message.edit() with exception handling.
"""


async def edit_message(client, message, text):
    try:
        return await message.edit(content=str(text))
    except Exception as e:
        ewutils.logMsg('Failed to edit message. Updated text would have been:\n{}\n{}'.format(text, e))


async def delete_last_message(client, last_messages, tick_length):
    if len(last_messages) == 0:
        return
    await asyncio.sleep(tick_length)
    try:
        msg = last_messages[-1]
        await msg.delete()
        pass
    except:
        ewutils.logMsg("failed to delete last message")


def create_death_report(cause=None, user_data=None, deathmessage = ""):
    client = ewutils.get_client()
    server = client.get_guild(user_data.id_server)

    # User display name is used repeatedly later, grab now
    user_member = server.get_member(user_data.id_user)
    user_player = EwPlayer(id_user=user_data.id_user)
    user_nick = user_player.display_name

    deathreport = "You arrive among the dead. {}".format(ewcfg.emote_slimeskull)
    deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    report_requires_killer = [ewcfg.cause_killing, ewcfg.cause_busted, ewcfg.cause_burning, ewcfg.cause_killing_enemy]
    if cause in report_requires_killer:  # Only deal with enemy data if necessary
        killer_isUser = cause in [ewcfg.cause_killing, ewcfg.cause_busted, ewcfg.cause_burning]
        killer_isEnemy = cause in [ewcfg.cause_killing_enemy]
        if killer_isUser:  # Generate responses for dying to another player
            # Grab user data
            killer_data = EwUser(id_user=user_data.id_killer, id_server=user_data.id_server)
            player_data = EwPlayer(id_user=user_data.id_killer)

            # Get the weapon that killed you
            weapon = static_weapons.weapon_map.get(user_data.trauma, None)

            killer_nick = player_data.display_name

            if (cause == ewcfg.cause_killing) and weapon:  # Response for dying to another player
                deathreport = "You were {} by {}. {}".format(weapon.str_killdescriptor, killer_nick, ewcfg.emote_slimeskull)
                deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

            if cause == ewcfg.cause_busted:  # Response for being busted
                deathreport = "Your ghost has been busted by {}. {}".format(killer_nick, ewcfg.emote_bustin)
                deathreport = "{} ".format(ewcfg.emote_bustin) + formatMessage(user_player, deathreport)

            if cause == ewcfg.cause_burning:  # Response for burning to death
                deathreport = "You were {} by {}. {}".format(static_weapons.weapon_map.get(ewcfg.weapon_id_molotov).str_killdescriptor, killer_nick, ewcfg.emote_slimeskull)
                deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

        if killer_isEnemy:  # Generate responses for being killed by enemy
            # Grab enemy data
            killer_data = EwEnemy(id_enemy=user_data.id_killer, id_server=user_data.id_server)

            if killer_data.attacktype != ewcfg.enemy_attacktype_unarmed:
                used_attacktype = hunt_static.attack_type_map.get(killer_data.attacktype)
            else:
                used_attacktype = ewcfg.enemy_attacktype_unarmed
            if cause == ewcfg.cause_killing_enemy:  # Response for dying to enemy attack
                # Get attack kill description
                kill_descriptor = "beaten to death"
                if used_attacktype != ewcfg.enemy_attacktype_unarmed:
                    kill_descriptor = used_attacktype.str_killdescriptor

                # Format report
                deathreport = "You were {} by {}. {}".format(kill_descriptor, killer_data.display_name, ewcfg.emote_slimeskull)
                deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    if cause == ewcfg.cause_donation:  # Response for overdonation
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, "You have died in a medical mishap. {}".format(ewcfg.emote_slimeskull))

    if cause == ewcfg.cause_suicide:  # Response for !suicide
        deathreport = "You arrive among the dead by your own volition. {}".format(ewcfg.emote_slimeskull)
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    if cause == ewcfg.cause_drowning:  # Response for disembarking into the slime sea
        deathreport = "You have drowned in the slime sea. {}".format(ewcfg.emote_slimeskull)
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    if cause == ewcfg.cause_falling:  # Response for disembarking blimp over the city
        deathreport = "You have fallen to your death. {}".format(ewcfg.emote_slimeskull)
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    if cause == ewcfg.cause_bleeding:  # Response for bleed death
        deathreport = "{skull} *{uname}*: You have succumbed to your wounds. {skull}".format(skull=ewcfg.emote_slimeskull, uname=user_nick)

    if cause == ewcfg.cause_weather:  # Response for death by bicarbonate rain
        deathreport = "{skull} *{uname}*: You have been cleansed by the bicarbonate rain. {skull}".format(skull=ewcfg.emote_slimeskull, uname=user_nick)

    if cause == ewcfg.cause_cliff:  # Response for falling or being pushed off cliff
        deathreport = "You fell off a cliff. {}".format(ewcfg.emote_slimeskull)
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    if cause == ewcfg.cause_backfire:  # Response for death by self backfire
        weapon_item = EwItem(id_item=user_data.weapon)
        weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))
        deathreport = "{} killed themselves with their own {}. Dumbass.".format(user_nick, weapon.str_name)

    if cause == ewcfg.cause_praying:  # Response for praying
        deathreport = formatMessage(user_member, "{} owww yer frickin bones man {}".format(ewcfg.emote_slimeskull, ewcfg.emote_slimeskull))

    if cause == ewcfg.cause_poison:  # Response for praying
        deathreport = formatMessage(user_member, "{} couldn't stop guzzling poison. {}".format(user_nick, ewcfg.emote_slimeskull))
    
    if cause == ewcfg.cause_crushing: # Response for crushing a negapoudrin/negaslimeoid core
        deathreport = "You bit into **NEGASLIME**, dink. Fucking idiot. {}".format(ewcfg.emote_slimeskull)
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    if cause == ewcfg.cause_gay: # Response for being gay in July
        deathreport = "https://cdn.discordapp.com/attachments/431240644464214017/982634916854497321/unknown.png"
        deathreport = formatMessage(user_player, deathreport)

    if (cause == ewcfg.cause_debris):  # Response for being hit by poudrin hail
        deathreport = "Your head was smushed in by falling debris. {}".format(ewcfg.emote_slimeskull)
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    if deathmessage != "":
        deathreport = "{} {}".format(deathmessage, ewcfg.emote_slimeskull)
        deathreport = "{} ".format(ewcfg.emote_slimeskull) + formatMessage(user_player, deathreport)

    return (deathreport)


async def update_slimernalia_kingpin(client, server):
    
    # Depose current slimernalia kingpin
    kingpin_state = EwGamestate(id_server=server.id, id_state='slimernaliakingpin')
    if not kingpin_state.value:
        old_kingpin_id = -1
    else:
        old_kingpin_id = int(kingpin_state.value)

    if old_kingpin_id != None and old_kingpin_id > 0:
        kingpin_state.value = '-1'
        kingpin_state.persist()
        try:
            ewutils.logMsg(f"Attempted to dethrone {old_kingpin_id} from slimernalia kingpin...")
            old_kingpin_member = server.get_member(old_kingpin_id)
            await ewrolemgr.updateRoles(client=client, member=old_kingpin_member)
        except:
            ewutils.logMsg("Error removing kingpin of slimernalia role from {} in server {}.".format(old_kingpin_id, server.id))

    # Update the new kingpin of slimernalia

    new_kingpin_id = ewutils.get_most_festive(server)
    # Quit out if there wasn't anybody suitable for crowning
    if new_kingpin_id == 1 or new_kingpin_id is None:
        return ewutils.logMsg("Skipped crowning new kingpin: No suitable candidates.")

    kingpin_state.value = str(new_kingpin_id)
    # Needs to be something or otherwise it breaks
    kingpin_state.bit = 0
    kingpin_state.persist()

    # Reset the new kingpin's festivity upon getting the award
    old_festivity = ewstats.get_stat(id_server=server.id, id_user=new_kingpin_id, metric=ewcfg.stat_festivity)
    ewstats.set_stat(id_server=server.id, id_user=new_kingpin_id, metric=ewcfg.stat_festivity, value=0)

    new_kingpin_member = None
    try:
        new_kingpin_member = await get_member(server, new_kingpin_id)
        await ewrolemgr.updateRoles(client=client, member=new_kingpin_member)
    except Exception as e:
        ewutils.logMsg("Error adding kingpin of slimernalia role to user {} in server {}: {}".format(new_kingpin_id, server.id, e))

    if new_kingpin_member:
        # Format and release a message from Phoebus about how who just won and how much slime they got
        announce_content = ewcfg.slimernalia_kingpin_announcement.format(player=("@" + str(new_kingpin_member.id)), festivity=old_festivity) 

        announce = discord.Embed()
        announce.set_thumbnail(url="https://i.imgur.com/aVfaB9I.png")
        announce.description = "**Phoebus**{}".format(ewcfg.emote_verified)
        announce.color = discord.Color.green()
        announce.add_field(name='\u200b', value=announce_content)

        channel = get_channel(server=server, channel_name="auditorium")

        await send_message(client, channel, embed=announce)


async def announce_event_stage_increase(client: discord.Client, server: discord.Guild, send_all=True):
    channel_obj = get_channel(server=server, channel_name="auditorium")
    announce_obj = EwResponseContainer(client=client, id_server=server.id)
    if send_all:
        for stage in ewcfg.event_stage_announcements[:ewcfg.event_stage - 1]:
            announce_obj.add_channel_response(channel_obj, stage)
    else:
        if ewcfg.event_stage >= 0:
            announce_obj.add_channel_response(channel_obj, ewcfg.event_stage_announcements[ewcfg.event_stage - 1])

    return await announce_obj.post()


def check_user_has_role(server, member, checked_role_name):
    checked_role = discord.utils.get(server.roles, name=checked_role_name)
    if checked_role not in member.roles:
        return False
    else:
        return True


def return_server_role(server, role_name):
    return discord.utils.get(server.roles, name=role_name)


async def collect_topics(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    client = ewutils.get_client()
    server = client.get_guild(cmd.guild.id)
    topic_count = 0

    for channel in server.channels:

        if channel.type != discord.ChannelType.text:
            continue
        elif channel.topic == None or channel.topic == '':
            continue
        elif channel.topic == '(Closed indefinitely) Currently controlled by no one.':
            continue

        found_poi = False
        for poi in poi_static.poi_list:
            if channel.name == poi.channel:
                found_poi = True
                break

        if found_poi:
            topic_count += 1
            print('\n{}\n=================\n{}'.format(channel.name, channel.topic))

    print('POI topics found: {}'.format(topic_count))


async def sync_topics(cmd):
    if not cmd.message.author.guild_permissions.administrator:
        return

    for poi in poi_static.poi_list:

        poi_has_blank_topic = False
        if poi.topic == None or poi.topic == '':
            poi_has_blank_topic = True

        channel = get_channel(cmd.guild, poi.channel)

        if channel == None:
            ewutils.logMsg('Failed to get channel for {}'.format(poi.id_poi))
            continue

        if channel.topic == poi.topic:
            continue

        if (poi_has_blank_topic and channel.topic == None) or (poi_has_blank_topic and channel.topic == ''):
            continue

        if poi_has_blank_topic:
            new_topic = ''
            debug_info = 'be a blank topic.'
        else:
            new_topic = poi.topic
            debug_info = poi.topic

        try:
            await asyncio.sleep(2)
            channel = await channel.edit(topic=new_topic)
            ewutils.logMsg('Changed channel topic for {} to {}'.format(channel, debug_info))
        except:
            ewutils.logMsg('Failed to set channel topic for {} to {}'.format(channel, debug_info))

    ewutils.logMsg('Finished syncing topics.')


"""
    A get_member replacement for discord.py's implementation, how it should have been done anyway
    Takes a guild and user id, returns a Discord Member if found, otherwise None
    Checks discord.py user cache for the member, and then queries discord if not found
"""
async def get_member(guild, member_id):
    # Check for member in discord.py cache
    member = guild.get_member(member_id)

    # Sometimes discord.py fails cache members for no apparent reason, lets fix that
    if member is None:
        # query that insists on returning a list cause rapptz is lazy and so am I
        mem_list = await guild.query_members(user_ids=[member_id], presences=True)

        # retrieve the member from the list if it's there
        member = mem_list[0] if len(mem_list) == 1 else None

    return member


async def talk_bubble(response = "", name = "", image = None, channel = None, color = "", npc_obj = None, delete_after = None):
    bubble = discord.Embed()
    client = ewutils.get_client()
    if name != "" and channel is not None:
        if npc_obj == None:
            bubble.description = name
            if image == "":
                bubble.set_thumbnail(url=ewcfg.default_thumbnail)
            else:
                bubble.set_thumbnail(url=image)
        elif npc_obj != None:
            bubble.description = npc_obj.str_name
            bubble.set_thumbnail(url=npc_obj.image_profile)

        if color != "":
            bubble.color = discord.Colour(int(color, 16))

        else:
            bubble.color = discord.Colour(int("33cc4a", 16))
        bubble.add_field(name='\u200b', value=response)
        await send_message(client, channel, embed=bubble, delete_after=delete_after)


async def prompt(cmd = None, target = None, question = "", wait_time = 30, accept_command = 'accept', decline_command = 'refuse', checktarget = False):

    if cmd is not None:
        if accept_command[0] == ewcfg.cmd_prefix:
            final_accept = accept_command
        else:
            final_accept = ewcfg.cmd_prefix + accept_command

        if decline_command[0] == ewcfg.cmd_prefix:
            final_decline = decline_command
        else:
            final_decline = ewcfg.cmd_prefix + decline_command

        await send_message(cmd.client, cmd.message.channel, text=question)

        try:
            message = await cmd.client.wait_for('message', timeout=30, check=lambda message: message.author == (target if checktarget else cmd.message.author) and message.content.lower() in [final_accept, final_decline])

            if message is not None:
                if message.content.lower() == final_accept:
                    accepted = True
                if message.content.lower() == final_decline:
                    accepted = False

        except Exception as e:
            ewutils.logMsg("Frontend util prompt threw Exception: {}".format(e))
            accepted = False
    else:
        accepted = False

    return accepted