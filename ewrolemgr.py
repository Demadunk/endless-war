import asyncio
import time
import discord

import ewcfg
import ewutils
import ewitem

from ew import EwUser

class EwRole:
	id_server = ""
	id_role = ""
	name = ""

	def __init__(self, id_server = None, name = None, id_role = None):
		if id_server is not None and name is not None:
			self.id_server = id_server
			self.name = name


			data = ewutils.execute_sql_query("SELECT {id_role} FROM roles WHERE id_server = %s AND {name} = %s".format(
				id_role = ewcfg.col_id_role,
				name = ewcfg.col_role_name
			), (
				id_server,
				name
			))

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.id_role = data[0][0]
			else:  # create new entry
				ewutils.execute_sql_query("REPLACE INTO roles ({id_server}, {name}) VALUES (%s, %s)".format(
					id_server = ewcfg.col_id_server,
					name = ewcfg.col_role_name
				), (
					id_server,
					name
				))
		elif id_server is not None and id_role is not None:
			self.id_server = id_server
			self.id_role = id_role


			data = ewutils.execute_sql_query("SELECT {name} FROM roles WHERE id_server = %s AND {id_role} = %s".format(
				id_role = ewcfg.col_id_role,
				name = ewcfg.col_role_name
			), (
				id_server,
				id_role
			))

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.name = data[0][0]

	def persist(self):
		ewutils.execute_sql_query("REPLACE INTO roles (id_server, {id_role}, {name}) VALUES(%s, %s, %s)".format(
			id_role = ewcfg.col_id_role,
			name = ewcfg.col_role_name
		), (
			self.id_server,
			self.id_role,
			self.name
		))
			

"""
	Find relevant roles and save them to the database.
"""
def setupRoles(client = None, id_server = ""):
	
	roles_map = ewutils.getRoleMap(client.get_server(id_server).roles)
	# for poi in ewcfg.poi_list:
	# 	if poi.role in roles_map:
	# 		try:
	# 			role_data = EwRole(id_server = id_server, name = poi.role)
	# 			role_data.id_role = roles_map[poi.role].id
	# 			role_data.persist()
	# 		except:
	# 			ewutils.logMsg('Failed to set up role {}'.format(poi.role))

	for faction_role in ewcfg.faction_roles:
		if faction_role in roles_map:
			try:
				role_data = EwRole(id_server = id_server, name = faction_role)
				role_data.id_role = roles_map[faction_role].id
				role_data.persist()
			except:
				ewutils.logMsg('Failed to set up role {}'.format(faction_role))

	for misc_role in ewcfg.misc_roles:
		if misc_role in roles_map:
			try:
				role_data = EwRole(id_server = id_server, name = misc_role)
				role_data.id_role = roles_map[misc_role].id
				role_data.persist()
			except:
				ewutils.logMsg('Failed to set up role {}'.format(misc_role))

"""
	Hide the names of poi roles behind a uniform alias
"""
async def hideRoleNames(client = None, id_server = ""):
	
	server = client.get_server(id_server)
	roles_map = ewutils.getRoleMap(server.roles)
	for poi in ewcfg.poi_list:
		try:
			if poi.role in roles_map:
				role = roles_map[poi.role]
				await client.edit_role(server = server, role = role, name = ewcfg.generic_role_name)
		except:
			ewutils.logMsg('Failed to hide role name for {}'.format(poi.role))

"""
	Restore poi roles to their original names
"""
async def restoreRoleNames(cmd):

	member = cmd.message.author
	
	if not member.server_permissions.administrator:
		return
	
	client = cmd.client
	server = member.server
	for poi in ewcfg.poi_list:
		try:
			role_data = EwRole(id_server = server.id, name = poi.role)
			for role in server.roles:
				if role.id == role_data.id_role:
					await client.edit_role(server = server, role = role, name = role_data.name)
		except:
			ewutils.logMsg('Failed to restore role name for {}'.format(poi.role))

"""
	Fix the Discord roles assigned to this member.
"""
async def updateRoles(
	client = None,
	member = None,
	server_default = None
):
	time_now = int(time.time())

	if server_default != None:
		user_data = EwUser(id_user=member.id, id_server = server_default)
	else:
		user_data = EwUser(member=member)

	id_server = user_data.id_server
	
	if member == None:
		return ewutils.logMsg("error: member was not supplied for updateRoles")

	#roles_map = ewutils.getRoleMap(member.server.roles)
	roles_map_user = ewutils.getRoleIdMap(member.roles)

	if user_data.life_state != ewcfg.life_state_kingpin and ewcfg.role_kingpin in roles_map_user:
		# Fix the life_state of kingpins, if somehow it wasn't set.
		user_data.life_state = ewcfg.life_state_kingpin
		user_data.persist()

	elif user_data.life_state != ewcfg.life_state_grandfoe and ewcfg.role_grandfoe in roles_map_user:
		# Fix the life_state of a grand foe.
		user_data.life_state = ewcfg.life_state_grandfoe
		user_data.persist()

	faction_roles_remove = [
		ewcfg.role_juvenile,
		ewcfg.role_juvenile_active,
		ewcfg.role_juvenile_pvp,
		ewcfg.role_rowdyfuckers,
		ewcfg.role_rowdyfuckers_pvp,
		ewcfg.role_rowdyfuckers_active,
		ewcfg.role_copkillers,
		ewcfg.role_copkillers_pvp,
		ewcfg.role_copkillers_active,
		ewcfg.role_corpse,
		ewcfg.role_corpse_pvp,
		ewcfg.role_corpse_active,
		ewcfg.role_kingpin,
		ewcfg.role_grandfoe,
		ewcfg.role_slimecorp,
		ewcfg.role_tutorial,
		ewcfg.role_shambler,
	]

	# Manage faction roles.
	faction_role = ewutils.get_faction(user_data = user_data)

	faction_roles_remove.remove(faction_role)

	pvp_role = None
	active_role = None
	if faction_role in ewcfg.role_to_pvp_role:

		if user_data.time_expirpvp >= time_now:
			pvp_role = ewcfg.role_to_pvp_role.get(faction_role)
			faction_roles_remove.remove(pvp_role)

		# if ewutils.is_otp(user_data):
		# 	active_role = ewcfg.role_to_active_role.get(faction_role)
		# 	faction_roles_remove.remove(active_role)

	tutorial_role = None
	if user_data.poi in ewcfg.tutorial_pois:
		tutorial_role = ewcfg.role_tutorial
		faction_roles_remove.remove(tutorial_role)

	# Manage location roles.
	# user_poi = ewcfg.id_to_poi.get(user_data.poi)
	# print(user_poi.id_poi)
	# if user_poi != None:
	# 	poi_role = user_poi.role
	# 	poi_permissions = user_poi.permissions
	# else:
	# 	poi_role = None
	# 	poi_permissions = None
		
		
	poi_permissions_remove = []
	# for poi in ewcfg.poi_list:
	# 	if poi.permissions != None and poi.permissions != poi_permissions:
	# 		poi_permissions_remove.append(poi.id_poi)

	# poi_roles_remove = []
	# for poi in ewcfg.poi_list:
	# 	if poi.role != None and poi.role != poi_role:
	# 		poi_roles_remove.append(poi.role)

	misc_roles_remove = [
		ewcfg.role_gellphone,
		ewcfg.role_slimernalia
	]

	# Remove user's gellphone role if they don't have a phone
	role_gellphone = None
	gellphones = ewitem.find_item_all(item_search = ewcfg.item_id_gellphone, id_user = user_data.id_user, id_server = user_data.id_server, item_type_filter = ewcfg.it_item)
	gellphone_active = False

	for phone in gellphones:
		phone_data = ewitem.EwItem(id_item = phone.get('id_item'))
		if phone_data.item_props.get('active') == 'true':
			gellphone_active = True
			break
		
	if gellphone_active == True:
		role_gellphone = ewcfg.role_gellphone
		misc_roles_remove.remove(ewcfg.role_gellphone)

	role_slimernalia = None
	#if user_data.slimernalia_kingpin == True:
	#	role_slimernalia = ewcfg.role_slimernalia
	#	misc_roles_remove.remove(ewcfg.role_slimernalia)


	role_ids = []
	for role_id in roles_map_user:

		try:
			role_data = EwRole(id_server = id_server, id_role = role_id)
			roleName = role_data.name
			if roleName != None and roleName not in faction_roles_remove and roleName not in misc_roles_remove: #  and roleName not in poi_roles_remove
				role_ids.append(role_data.id_role)
		except:
			ewutils.logMsg('error: couldn\'t find role with id {}'.format(role_id))

	
	try:
		role_data = EwRole(id_server = id_server, name = faction_role)
		if not role_data.id_role in role_ids:
			role_ids.append(role_data.id_role)
			#ewutils.logMsg('found role {} with id {}'.format(role_data.name, role_data.id_role))
	except:
		ewutils.logMsg('error: couldn\'t find role {}'.format(faction_role))

	try:
		role_data = EwRole(id_server = id_server, name = pvp_role)
		if not role_data.id_role in role_ids:
			role_ids.append(role_data.id_role)
			#ewutils.logMsg('found role {} with id {}'.format(role_data.name, role_data.id_role))
	except:
		ewutils.logMsg('error: couldn\'t find role {}'.format(pvp_role))

	try:
		role_data = EwRole(id_server = id_server, name = active_role)
		if not role_data.id_role in role_ids:
			role_ids.append(role_data.id_role)
			#ewutils.logMsg('found role {} with id {}'.format(role_data.name, role_data.id_role))
	except:
		ewutils.logMsg('error: couldn\'t find role {}'.format(active_role))

	try:
		role_data = EwRole(id_server = id_server, name = tutorial_role)
		if not role_data.id_role in role_ids:
			role_ids.append(role_data.id_role)
			#ewutils.logMsg('found role {} with id {}'.format(role_data.name, role_data.id_role))
	except:
		ewutils.logMsg('error: couldn\'t find role {}'.format(tutorial_role))

	# try:
	# 	role_data = EwRole(id_server = id_server, name = poi_role)
	# 	if not role_data.id_role in role_ids:
	# 		role_ids.append(role_data.id_role)
	# 		#ewutils.logMsg('found role {} with id {}'.format(role_data.name, role_data.id_role))
	# except:
	# 	ewutils.logMsg('error: couldn\'t find role {}'.format(poi_role))

	try:
		role_data = EwRole(id_server = id_server, name = role_gellphone)
		if not role_data.id_role in role_ids:
			role_ids.append(role_data.id_role)
			#ewutils.logMsg('found role {} with id {}'.format(role_data.name, role_data.id_role))
	except:
		ewutils.logMsg('error: couldn\'t find role {}'.format(role_gellphone))

	try:
		role_data = EwRole(id_server = id_server, name = role_slimernalia)
		if not role_data.id_role in role_ids:
			role_ids.append(role_data.id_role)
			#ewutils.logMsg('found role {} with id {}'.format(role_data.name, role_data.id_role))
	except:
		ewutils.logMsg('error: couldn\'t find role {}'.format(role_slimernalia))

	#if faction_role not in role_names:
	#	role_names.append(faction_role)
	#if poi_role != None and poi_role not in role_names:
	#	role_names.append(poi_role)

	#replacement_roles = []
	#for name in role_names:
	#	role = roles_map.get(name)

	#	if role != None:
	#		replacement_roles.append(role)
	#	else:
	#		ewutils.logMsg("error: role missing \"{}\"".format(name))

	#ewutils.logMsg('looking for {} roles to replace'.format(len(role_ids)))
	replacement_roles = []

	for role in member.server.roles:
		if role.id in role_ids:
			#ewutils.logMsg('found role {} with id {}'.format(role.name, role.id))
			replacement_roles.append(role)

	#ewutils.logMsg('found {} roles to replace'.format(len(replacement_roles)))
	
	try:
		await client.replace_roles(member, *replacement_roles)
	except:
		ewutils.logMsg('error: failed to replace roles for {}'.format(member.display_name))

	
	await refresh_user_perms(client = client, id_server = id_server, used_member = member)

	#try:
	#	await client.replace_roles(member, *replacement_roles)
	#except:
	#	ewutils.logMsg('error: failed to replace roles for {}'.format(member.display_name))

async def refresh_user_perms(client, id_server, used_member = None, startup = False):
	#try:
	server = client.get_server(id_server)
	
	member_list = []
	#subzone_member_list = []
	
	for poi in ewcfg.poi_list:
		
		channel = ewutils.get_channel(server, poi.channel)
		if channel == None:
			# Second try
			channel = ewutils.get_channel(server, poi.channel)
			if channel == None:
				continue
				
		#print('{} overwrites: {}'.format(poi.id_poi, channel.overwrites))
		for tuple in channel.overwrites:
			#print('tuplevar: {}'.format(tuple[0]) + '\n\n')
			if tuple[0] not in server.roles:
				member = tuple[0]
				member_list.append(tuple[0])
				
				
				user_data = EwUser(member=member)
				
				if user_data.poi != poi.id_poi:
					
					
					
					# Incorrect overwrite found for user

					for i in range(ewcfg.permissions_tries):
						await client.delete_channel_permissions(channel, member)
						
					print('deleted overwrite in {} for {}'.format(channel, member))
				
				#elif user_data.poi == poi.id_poi:
					correct_poi = ewcfg.id_to_poi.get(user_data.poi)
					correct_channel = ewutils.get_channel(server, correct_poi.channel)
					
					permissions_dict = correct_poi.permissions
					overwrite = discord.PermissionOverwrite()
					overwrite.read_messages = True if ewcfg.permission_read_messages in permissions_dict[user_data.poi] else False
					overwrite.send_messages = True if ewcfg.permission_send_messages in permissions_dict[user_data.poi] else False
					
					#print(permissions_dict[user_data.poi])

					for i in range(ewcfg.permissions_tries):
						await client.edit_channel_permissions(correct_channel, member, overwrite)

					#print('corrected overwrite in {} for {}'.format(correct_channel, member))
					print('updated permissions for {} in {}'.format(member, user_data.poi))
					
				else:
					pass
					# print(member)
					# print(poi.str_name)
					
	if used_member != None:
		
		if used_member not in member_list:
			# Member has no overwrites -- fix this:
			user_data = EwUser(member=used_member)
			correct_poi = ewcfg.id_to_poi.get(user_data.poi)
			correct_channel = ewutils.get_channel(server, correct_poi.channel)
			
			
			permissions_dict = correct_poi.permissions
			overwrite = discord.PermissionOverwrite()
			overwrite.read_messages = True if ewcfg.permission_read_messages in permissions_dict[user_data.poi] else False
			overwrite.send_messages = True if ewcfg.permission_send_messages in permissions_dict[user_data.poi] else False

			for i in range(ewcfg.permissions_tries):
				await client.edit_channel_permissions(correct_channel, used_member, overwrite)

			# print('corrected overwrite in {} for {}'.format(correct_channel, member))
			print('updated permissions for {} in {}'.format(used_member, user_data.poi))

	if startup:
		# On startup, give out permissions where necessary. This should only need to be done once, when the update goes live.
		
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor();

		cursor.execute(
			"SELECT id_user, poi FROM users WHERE id_server = %s".format(
				slimes=ewcfg.col_slimes,
				life_state=ewcfg.col_life_state,
				life_state_kingpin=ewcfg.life_state_kingpin
			), (
				id_server,
			))
		
		

		users = cursor.fetchall()

		for user in users:

			member = server.get_member(user[0])
			
			#print(member)
			#print(member_list)
			
			user_poi = ewcfg.id_to_poi.get(user[1])

			if member == None:
				# Second try.
				member = server.get_member(user[0])
				if member == None:
					continue
				
			if member not in member_list:
				
				# Member has no overwrite -- fix this:
				user_data = EwUser(member=member)
				correct_poi = ewcfg.id_to_poi.get(user_data.poi)

				if correct_poi != None:
					permissions_dict = user_poi.permissions
				else:
					continue
				
				correct_channel = ewutils.get_channel(server, correct_poi.channel)

				#print(user_data.poi)
				
				overwrite = discord.PermissionOverwrite()
				overwrite.read_messages = True if ewcfg.permission_read_messages in permissions_dict[user_data.poi] else False
				overwrite.send_messages = True if ewcfg.permission_send_messages in permissions_dict[user_data.poi] else False

				for i in range(ewcfg.permissions_tries):
					await client.edit_channel_permissions(correct_channel, member, overwrite)

				# print('corrected overwrite in {} for {}'.format(correct_channel, member))
				print('added permissions for {} in {}'.format(member, user_data.poi))

	#except:
		#ewutils.logMsg('caught exception while refreshing permissions')

# Change all permissions for POI channels
async def change_perms(cmd):
	member = cmd.message.author
	client = ewutils.get_client()

	if not member.server_permissions.administrator:
		return

	user_data = EwUser(member=member)

	allow_or_deny = None
	if cmd.tokens_count > 1:
		allow_or_deny = cmd.tokens[1].lower()

		if allow_or_deny == 'allow':
			allow_or_deny = True
			response = "DEBUG: ALLOWED READ AND SEND ACCESS TO ALL POI CHANNELS/CATEGORIES."
			await ewutils.send_message(client, cmd.message.channel, ewutils.formatMessage(member, response))
		elif allow_or_deny == 'deny':
			allow_or_deny = False
			response = "DEBUG: DENIED READ AND SEND ACCESS TO ALL POI CHANNELS/CATEGORIES."
			await ewutils.send_message(client, cmd.message.channel, ewutils.formatMessage(member, response))
		elif allow_or_deny == 'nuetral':
			allow_or_deny = 'None'
			response = "DEBUG: SET READ AND SEND ACCESS FOR ALL POI CHANNELS/CATEGORIES TO NEUTRAL."
			await ewutils.send_message(client, cmd.message.channel, ewutils.formatMessage(member, response))
		else:
			response = "ERROR: INVALID ANSWER."
			return await ewutils.send_message(client, cmd.message.channel, ewutils.formatMessage(member, response))

	server = client.get_server(id=user_data.id_server)

	for poi in ewcfg.poi_list:
		channel = ewutils.get_channel(server, poi.channel)
		
		if channel == None:
			print(poi.id_poi)
			continue
		
		role = discord.utils.get(server.roles, name='@everyone')

		overwrite = discord.PermissionOverwrite()
		
		if allow_or_deny == True:
			overwrite.read_messages = True
			overwrite.send_messages = True
		elif allow_or_deny == False:
			overwrite.read_messages = False
			overwrite.send_messages = False
		elif allow_or_deny == 'None':
			overwrite.read_messages = None
			overwrite.send_messages = None
			
		overwrite.read_message_history = None
		
		if allow_or_deny == True or allow_or_deny == False or allow_or_deny == 'None':
			
			for i in range(ewcfg.permissions_tries):
				await client.edit_channel_permissions(channel, role, overwrite)

			print('set read/send perms in {} to {}'.format(channel, allow_or_deny))
			
	print('got through all channels in changeperms')

# Remove all user overwrites in the server's POI channels
async def remove_user_overwrites(cmd):
	
	if not cmd.message.author.server_permissions.administrator:
		return
	
	server = cmd.message.server
	client = ewutils.get_client()
	
	for poi in ewcfg.poi_list:
		
		searched_channel = poi.channel
		
		channel = ewutils.get_channel(server, searched_channel)
		
		if channel == None:
			# Second try
			channel = ewutils.get_channel(server, searched_channel)
			if channel == None:
				continue
				
		# print('{} overwrites: {}'.format(poi.id_poi, channel.overwrites))
		for tuple in channel.overwrites:
			# print('tuplevar: {}'.format(tuple[0]) + '\n\n')
			if tuple[0] not in server.roles:
				member = tuple[0]
				
				print('removed overwrite in {} for {}'.format(channel, member))

				for i in range(ewcfg.permissions_tries):
					await client.delete_channel_permissions(channel, member)
		

	response = "DEBUG: ALL USER OVERWRITES DELETED."
	return await ewutils.send_message(client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))