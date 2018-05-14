import MySQLdb
import datetime
import time

import ewcfg

""" Write the string to stdout with a timestamp. """
def logMsg(string):
	print("[{}] {}".format(datetime.datetime.now(), string))

	return string

""" read a file named fname and return its contents as a string """
def getValueFromFileContents(fname):
	token = ""

	try:
		f_token = open(fname, "r")
		f_token_lines = f_token.readlines()

		for line in f_token_lines:
			line = line.rstrip()
			if len(line) > 0:
				token = line
	except IOError:
		token = ""
		print("Could not read {} file.".format(fname))
	finally:
		f_token.close()

	return token

""" get the Discord API token from the config file on disk """
def getToken():
	return getValueFromFileContents("token")

""" get the Twitch client ID from the config file on disk """
def getTwitchClientId():
	return getValueFromFileContents("twitch_client_id")

""" print a list of strings with nice comma-and grammar """
def formatNiceList(names=[], conjunction="and"):
	l = len(names)

	if l == 0:
		return ''

	if l == 1:
		return names[0]
	
	return ', '.join(names[0:-1]) + '{comma} {conj} '.format(comma=(',' if l > 2 else ''), conj=conjunction) + names[-1]

""" turn a list of Users into a list of their respective names """
def userListToNameString(list_user):
	names = []

	for user in list_user:
		names.append(user.display_name)

	return formatNiceList(names)

""" turn a list of Roles into a map of name=>Role """
def getRoleMap(roles):
	roles_map = {}

	for role in roles:
		roles_map[role.name.replace(" ", "").lower()] = role

	return roles_map

""" connect to the database """
def databaseConnect():
	return MySQLdb.connect(host="localhost", user="rfck-bot", passwd="rfck", db="rfck")

""" get the slime count for the specified member (player). sets to 0 if they aren't in the database """
def getSlimesForPlayer(conn, cursor, member):
	user_slimes = 0

	cursor.execute("SELECT slimes FROM users WHERE id_user = %s AND id_server = %s", (member.id, member.server.id))
	result = cursor.fetchone();

	if result == None:
		cursor.execute("REPLACE INTO users(id_user, id_server) VALUES(%s, %s)", (member.id, member.server.id))
	else:
		user_slimes = result[0]

	return user_slimes

""" dump help document """
def getHelpText():
	text = ""

	try:
		f_help = open("help", "r")
		lines = f_help.readlines()

		for line in lines:
			text = text + line

	except IOError:
		text = ""
		print("Could not read help file.")
	finally:
		f_help.close()

	return text

""" format responses with the username: """
def formatMessage(user_target, message):
	return "*{}*: {}".format(user_target.display_name, message)

""" Returns the latest value, so that short PvP timer actions don't shorten remaining PvP time. """
def calculatePvpTimer(current_time_expirpvp, desired_time_expirpvp):
	if desired_time_expirpvp > current_time_expirpvp:
		return desired_time_expirpvp

	return current_time_expirpvp

""" Save a timestamped snapshot of the current market for historical purposes. """
def persistMarketHistory(market_data=None, conn=None, cursor=None):
	if market_data != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn = databaseConnect()
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			# Save data
			cursor.execute("INSERT INTO stats({}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, (SELECT sum({}) FROM users WHERE {} = %s), (SELECT sum({}) FROM users WHERE {} = %s), (SELECT count(*) FROM users WHERE {} = %s), (SELECT count(*) FROM users WHERE {} = %s AND {} > %s))".format(
				# Insert columns
				ewcfg.col_id_server,
				ewcfg.col_slimes_casino,
				ewcfg.col_rate_market,
				ewcfg.col_rate_exchange,
				ewcfg.col_total_slime,
				ewcfg.col_total_slimecredit,
				ewcfg.col_total_players,
				ewcfg.col_total_players_pvp,

				# Inner queries
				ewcfg.col_slimes,
				ewcfg.col_id_server,
				ewcfg.col_slimecredit,
				ewcfg.col_id_server,
				ewcfg.col_id_server,
				ewcfg.col_id_server,
				ewcfg.col_time_expirpvp
			), (
				market_data.id_server,
				market_data.slimes_casino,
				market_data.rate_market,
				market_data.rate_exchange,
				market_data.id_server,
				market_data.id_server,
				market_data.id_server,
				market_data.id_server,
				int(time.time())
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()


""" Parse a list of tokens and return an integer value. If allow_all, return -1 if the word 'all' is present. """
def getIntToken(tokens=[], allow_all=False):
	value = None

	for token in tokens[1:]:
		try:
			value = int(token)
			if value < 0:
				value = None
			break
		except:
			if allow_all and ("{}".format(token)).lower() == 'all':
				value = -1
			else:
				value = None

	return value

""" Get the map of weapon skills for the specified player. """
def weaponskills_get(id_server=None, id_user=None, member=None, conn=None, cursor=None):
	weaponskills = {}

	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn = databaseConnect()
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			cursor.execute("SELECT {weapon}, {weaponskill} FROM weaponskills WHERE {id_server} = %s AND {id_user} = %s".format(
				weapon=ewcfg.col_weapon,
				weaponskill=ewcfg.col_weaponskill,
				id_server=ewcfg.col_id_server,
				id_user=ewcfg.col_id_user
			), (
				id_server,
				id_user
			))

			data = cursor.fetchall()
			if data != None:
				for row in data:
					weaponskills[row[0]] = row[1]
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()

	return weaponskills

""" Set an individual weapon skill value for a player. """
def weaponskills_set(id_server=None, id_user=None, member=None, weapon=None, weaponskill=0, conn=None, cursor=None):
	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None and weapon != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn = databaseConnect()
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			cursor.execute("REPLACE INTO weaponskills({id_server}, {id_user}, {weapon}, {weaponskill}) VALUES(%s, %s, %s, %s)".format(
				id_server=ewcfg.col_id_server,
				id_user=ewcfg.col_id_user,
				weapon=ewcfg.col_weapon,
				weaponskill=ewcfg.col_weaponskill
			), (
				id_server,
				id_user,
				weapon,
				weaponskill
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()

""" Clear all weapon skills for a player (probably called on !revive). """
def weaponskills_clear(id_server=None, id_user=None, member=None, conn=None, cursor=None):
	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn = databaseConnect()
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			# Clear any records that might exist.
			cursor.execute("DELETE FROM weaponskills WHERE {id_server} = %s AND {id_user} = %s".format(
				id_server=ewcfg.col_id_server,
				id_user=ewcfg.col_id_user
			), (
				id_server,
				id_user
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()
