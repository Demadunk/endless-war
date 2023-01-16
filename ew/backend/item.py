import time
import traceback, sys

from . import core as bknd_core
from . import worldevent as bknd_event
from ..static import cfg as ewcfg
from ..static import cosmetics
from ..static import hue as hue_static
from ..static import items as static_items
from ..static import weapons as static_weapons
from ..utils import core as ewutils
from ew.backend.dungeons import EwGamestate
try:
    from ..utils import rutils as ewrelicutils
except:
    from ..utils import rutils_dummy as ewrelicutils

"""
	EwItem is the instance of an item (described by EwItemDef, linked by
	item_type) which is possessed by a player and stored in the database.
"""


class EwItem:
    id_item = -1
    id_server = -1
    id_owner = ""
    item_type = ""
    time_expir = -1

    stack_max = -1
    stack_size = 0
    soulbound = False

    template = "-2"

    item_props = None

    name = ""

    def __init__(
            self,
            id_item = None
    ):
        if (id_item != None):
            self.id_item = id_item

            self.item_props = {}
            # the item props don't reset themselves automatically which is why the items_prop table had tons of extraneous rows (like food items having medal_names)
            # self.item_props.clear()

            cache_result = bknd_core.get_cache_result(obj = self)
            if cache_result is not False:
                self.__dict__ = cache_result
            else:
                try:
                    conn_info = bknd_core.databaseConnect()
                    conn = conn_info.get('conn')
                    cursor = conn.cursor()

                    # Retrieve object
                    cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {} FROM items WHERE id_item = %s".format(
                        ewcfg.col_id_server,
                        ewcfg.col_id_user,
                        ewcfg.col_item_type,
                        ewcfg.col_time_expir,
                        ewcfg.col_stack_max,
                        ewcfg.col_stack_size,
                        ewcfg.col_soulbound,
                        ewcfg.col_template
                    ), (
                        self.id_item,
                    ))
                    result = cursor.fetchone()

                    if result != None:
                        # Record found: apply the data to this object.
                        self.id_server = result[0]
                        self.id_owner = result[1]
                        self.item_type = result[2]
                        self.time_expir = result[3]
                        self.stack_max = result[4]
                        self.stack_size = result[5]
                        self.soulbound = (result[6] != 0)
                        self.template = result[7]

                        # Retrieve additional properties
                        cursor.execute("SELECT {}, {} FROM items_prop WHERE id_item = %s".format(
                            ewcfg.col_name,
                            ewcfg.col_value
                        ), (
                            self.id_item,
                        ))

                        for row in cursor:
                            # this try catch is only necessary as long as extraneous props exist in the table
                            try:
                                self.item_props[row[0]] = row[1]
                            except:
                                ewutils.logMsg("extraneous item_prop row detected.")

                    else:
                        ewutils.logMsg("Item {} not found in cache or db".format(id_item))
                        # Item not found.
                        self.id_item = -1

                    self.fix_template()

                    if self.template == "-2":
                        self.persist()

                    #self.update_format()

                    self.update_name()
                    bknd_core.cache_data(obj = self)

                finally:
                    # Clean up the database handles.
                    cursor.close()
                    bknd_core.databaseClose(conn_info)

    """ Save item data object to the database. """

    def persist(self):

        self.update_name()
        self.fix_template()

        # Fix the expiration time before caching
        self.time_expir = self.time_expir if self.time_expir is not None else self.item_props['time_expir'] if 'time_expir' in self.item_props.keys() else 0

        bknd_core.cache_data(obj=self)

        try:
            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Save the object.
            cursor.execute("REPLACE INTO items({}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
                ewcfg.col_id_item,
                ewcfg.col_id_server,
                ewcfg.col_id_user,
                ewcfg.col_item_type,
                ewcfg.col_time_expir,
                ewcfg.col_stack_max,
                ewcfg.col_stack_size,
                ewcfg.col_soulbound,
                ewcfg.col_template
            ), (
                self.id_item,
                self.id_server,
                self.id_owner,
                self.item_type,
                self.time_expir,
                self.stack_max,
                self.stack_size,
                (1 if self.soulbound else 0),
                self.template
            ))

            # Remove all existing property rows.
            cursor.execute("DELETE FROM items_prop WHERE {} = %s".format(
                ewcfg.col_id_item
            ), (
                self.id_item,
            ))

            # Write out all current property rows.
            for name in self.item_props:
                cursor.execute("INSERT INTO items_prop({}, {}, {}) VALUES(%s, %s, %s)".format(
                    ewcfg.col_id_item,
                    ewcfg.col_name,
                    ewcfg.col_value
                ), (
                    self.id_item,
                    name,
                    self.item_props[name]
                ))

            conn.commit()
        finally:
            # Clean up the database handles.
            cursor.close()
            bknd_core.databaseClose(conn_info)

    def update_name(self):
        name_assigned = False
        if self.id_item > 0:
            name_prop_list = ["item_name", "food_name", "cosmetic_name", "weapon_name", "furniture_name", "title", "qitem_name" ,"medal_name", "relic_name"]
            if self.item_props is not None:
                for name_prop in name_prop_list:
                    if name_prop in self.item_props.keys():
                        self.name = self.item_props.get(name_prop)
                        name_assigned = True
                if ((not name_assigned) or self.name == "") and "weapon_type" in self.item_props.keys():
                    self.name = self.item_props.get("weapon_type")
                    name_assigned = True
            if not name_assigned:
                item_def = static_items.item_def_map.get(self.item_type)
                if item_def is not None:
                    self.name = item_def.str_name
                    # This should be followed by variable substitution where neccessary but
                    # item props arent properly defined with the item defs, and this code should
                    # only be run if the item has not had props generated and given yet.
                    # this function should be immediately rerun upon generation of item props
                    # anyways so this name should never be displayed
                else:
                    self.name = ""

    def fix_template(self):
        bad_templates = ["-2", "bad general item id", "bad food id", "bad weapon id", "bad cosmetic id", "bad furniture id"]

        if self.template in bad_templates:
            if self.item_type == ewcfg.it_item:
                if "id_name" in self.item_props.keys():
                    self.template = self.item_props.get("id_name", "bad general item id")
                elif "id_item" in self.item_props.keys():
                    self.template = self.item_props.get("id_item", "bad general item id")
                else:
                    self.template = "bad general item id"
            elif self.item_type == ewcfg.it_food:
                self.template = self.item_props.get("id_food", "bad food id")
            elif self.item_type == ewcfg.it_weapon:
                self.template = self.item_props.get("weapon_type", "bad weapon id")
            elif self.item_type == ewcfg.it_cosmetic:
                self.template = self.item_props.get("id_cosmetic", "bad cosmetic id")
            elif self.item_type == ewcfg.it_furniture:
                self.template = self.item_props.get("id_furniture", "bad furniture id")
            elif self.item_type == ewcfg.it_book:
                self.template = "player book"
            elif self.item_type == ewcfg.it_medal:
                self.template = "MEDAL ITEM????"  # p sure these are fake news
            elif self.item_type == ewcfg.it_questitem:
                self.template = "QUEST ITEM????"

            if self.template not in bad_templates:
                self.persist()


"""
	Finds the amount of Slime Poudrins inside your inventory.
"""


def find_poudrin(id_user = None, id_server = None):
    items = inventory(
        id_user=id_user,
        id_server=id_server,
        item_type_filter=ewcfg.it_item
    )

    poudrins = []

    for poudrin in items:
        name = poudrin.get('name')
        if name != "Slime Poudrin":
            pass
        else:
            poudrins.append(poudrin)

    poudrins_amount = len(poudrins)

    return poudrins_amount


"""
    Delete the specified item by ID. Also deletes all items_prop values.
"""


def item_delete(
        id_item = None
):
    bknd_core.remove_entry(obj_type="EwItem", id_entry=id_item)

    try:
        conn_info = bknd_core.databaseConnect()
        conn = conn_info.get('conn')
        cursor = conn.cursor()

        # Create the item in the database.
        cursor.execute("DELETE FROM items WHERE {} = %s".format(
            ewcfg.col_id_item
        ), (
            id_item,
        ))

        conn.commit()
    finally:
        # Clean up the database handles.
        cursor.close()
        bknd_core.databaseClose(conn_info)

    remove_from_trades(id_item)


"""
    Create a new item and give it to a player.

    Returns the unique database ID of the newly created item.
"""


def item_create(
        item_type = None,
        id_user = None,
        id_server = None,
        stack_max = -1,
        stack_size = 0,
        item_props = None
):

    item_def = static_items.item_def_map.get(item_type)
    badRelic = 0


    if item_def == None:
        ewutils.logMsg('Tried to create invalid item_type: {}'.format(item_type))
        return




    if item_type == ewcfg.it_item:
        if "id_name" in item_props.keys():
            template_id = item_props.get("id_name", "bad general item id")
        elif "id_item" in item_props.keys():
            template_id = item_props.get("id_item", "bad general item id")
        else:
            template_id = "bad general item id"
    elif item_type == ewcfg.it_food:
        template_id = item_props.get("id_food", "bad food id")
    elif item_type == ewcfg.it_weapon:
        template_id = item_props.get("weapon_type", "bad weapon id")
    elif item_type == ewcfg.it_cosmetic:
        template_id = item_props.get("id_cosmetic", "bad cosmetic id")
    elif item_type == ewcfg.it_furniture:
        template_id = item_props.get("id_furniture", "bad furniture id")
    elif item_type == ewcfg.it_relic:
        template_id = item_props.get("id_relic", "bad relic id")
    elif item_type == ewcfg.it_book:
        template_id = "player book"
    elif item_type == ewcfg.it_medal:
        template_id = "MEDAL ITEM????" #p sure these are fake news

    elif item_type == ewcfg.it_questitem:
        template_id = "QUEST ITEM????"
    else:
        template_id = "-1"

    if (item_type == ewcfg.it_relic or item_props.get('acquisition') == 'relic') and ewrelicutils.canCreateRelic(template_id, id_server, 0 if ewutils.DEBUG_OPTIONS.get('duperelics') else 1) != 1:
        badRelic = 1

    if badRelic == 0:
        try:
            # Get database handles if they weren't passed.
            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            # Create the item in the database.

            cursor.execute("INSERT INTO items({}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s)".format(
                ewcfg.col_item_type,
                ewcfg.col_id_user,
                ewcfg.col_id_server,
                ewcfg.col_soulbound,
                ewcfg.col_stack_max,
                ewcfg.col_stack_size,
                ewcfg.col_template
            ), (
                item_type,
                id_user,
                id_server,
                (1 if item_def.soulbound else 0),
                stack_max,
                stack_size,
                template_id,
            ))

            item_id = cursor.lastrowid
            conn.commit()

            if item_id > 0:
                # If additional properties are specified in the item definition or in this create call, create and persist them.
                if item_props != None or item_def.item_props != None:
                    item_inst = EwItem(id_item = item_id)

                    if item_inst.item_type == ewcfg.it_relic:
                        gamestate = EwGamestate(id_state=template_id, id_server=id_server)
                        gamestate.number = item_id
                        gamestate.persist()
                    if item_def.item_props != None:
                        item_inst.item_props.update(item_def.item_props)

                    if item_props != None:
                        item_inst.item_props.update(item_props)
                    item_inst.persist()

                conn.commit()
        finally:
            # Clean up the database handles.
            cursor.close()
            bknd_core.databaseClose(conn_info)
        return item_id
    return None


    EwItem(id_item=item_id) # Ensure it is loaded into the cache
    return item_id


"""
	Drop all of a player's non-soulbound items into their district
"""


def item_dropall(user_data):
    try:
        bknd_core.execute_sql_query(
            "UPDATE items SET id_user = %s WHERE id_user = %s AND id_server = %s AND soulbound = 0", (
                user_data.poi,
                str(user_data.id_user),
                user_data.id_server
            ))

        # Get the item cache if it exists
        item_cache = bknd_core.get_cache(obj_type = "EwItem")
        if item_cache:
            # Get all non soulbound items belonging to the user in their current server
            criteria_for_drop = {"id_owner": user_data.id_user, "id_server": user_data.id_server, "soulbound": False}
            for item_data in item_cache.find_entries(criteria=criteria_for_drop):
                # Give the items to the floor
                item_data.update({"id_owner": user_data.poi})
                item_cache.set_entry(item_data)

    except Exception as e:
        ewutils.logMsg('Failed to drop items for user with id {}: {}'.format(user_data.id_user, e))





"""
    Dedorn all of a player's cosmetics
"""


def item_dedorn_cosmetics(
        id_server = None,
        id_user = None
):
    try:

        bknd_core.execute_sql_query(
            "UPDATE items_prop SET value = 'false' WHERE (name = 'adorned') AND {id_item} IN (\
                SELECT {id_item} FROM items WHERE {id_user} = %s AND {id_server} = %s\
            )".format(
                id_item=ewcfg.col_id_item,
                id_user=ewcfg.col_id_user,
                id_server=ewcfg.col_id_server
            ), (
                str(id_user),
                id_server
            ))

        # Get the item cache if it exists
        item_cache = bknd_core.get_cache(obj_type = "EwItem")
        if item_cache:
            # Find all adorned items belonging to the given user in that server
            for item_data in item_cache.find_entries(criteria={
                "id_owner": id_user,
                "id_server": id_server,
                "item_props": {"adorned": "true"}
            }):
                # change the tag to dedorned and save the data
                item_data.get("item_props").update({"adorned": False})
                item_cache.set_entry(item_data)

    except:
        ewutils.logMsg('Failed to dedorn cosmetics for user with id {}'.format(id_user))


"""
    Destroy all of a player's non-soulbound items.
"""


def item_destroyall(id_server = None, id_user = None, member = None):
    if member != None:
        id_server = member.guild.id
        id_user = member.id

    if id_server != None and id_user != None:
        try:
            # Get database handles if they weren't passed.
            conn_info = bknd_core.databaseConnect()
            conn = conn_info.get('conn')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM items WHERE {id_server} = %s AND {id_user} = %s AND {soulbound} = 0".format(
                id_user=ewcfg.col_id_user,
                id_server=ewcfg.col_id_server,
                soulbound=ewcfg.col_soulbound,
            ), (
                id_server,
                id_user
            ))

            conn.commit()

            # Get the item cache if it's being used
            item_cache = bknd_core.get_cache(obj_type = "EwItem")
            if item_cache:
                # Find all non soulbound items belonging to the given user in that server
                destruction_criteria = {"id_owner": id_user, "id_server": id_server, "soulbound": False}
                for item_data in item_cache.find_entries(criteria=destruction_criteria):
                    # attempt to delete the item from cache
                    item_cache.delete_entry(item_data)

        finally:
            # Clean up the database handles.
            cursor.close()
            bknd_core.databaseClose(conn_info)


"""
    Transfers adorned cosmetics and equipped weapons (no sidearms) from the source to the target.
"""


def item_loot(
        source_data = None,
        target_data = None,
):
    if source_data == None or target_data == None:
        return

    # Use the cache if possible
    item_cache = bknd_core.get_cache(obj_type = "EwItem")
    if item_cache is not False:
        # Find all cosmetics that can be moved and are adorned
        criteria = {
            "id_owner": source_data.id_user,
            "id_server": source_data.id_server,
            "soulbound": False,
            "item_type": ewcfg.it_cosmetic,
            "item_props": {"adorned": "true"}
        }
        movable_cosmetics = item_cache.find_entries(criteria=criteria)

        # Iterate through all found cosmetics
        for item_data in movable_cosmetics:
            # Dedorn the cosmetic
            item = EwItem(id_item=item_data.get("id_item"))
            item.item_props.update({"adorned": 'false'})
            item.persist()
            # Transfer ownership, abiding by capacity limits this time
            give_item(id_user=target_data.id_user, id_server=target_data.id_server)

        # if the source has a weapon equipped
        if source_data.weapon >= 0:
            weapons_held = inventory(
                id_user=target_data.id_user,
                id_server=target_data.id_server,
                item_type_filter=ewcfg.it_weapon
            )

            # give the target the weapon if they have inventory space for it
            if len(weapons_held) <= target_data.get_weapon_capacity():
                give_item(id_user=target_data.id_user, id_server=target_data.id_server, id_item=source_data.weapon)

    # Use the database if there's no cache
    else:

        try:
            # Transfer adorned cosmetics
            data = bknd_core.execute_sql_query(
                "SELECT id_item FROM items " +
                "WHERE id_user = %s AND id_server = %s AND soulbound = 0 AND item_type = %s AND id_item IN (" +
                "SELECT id_item FROM items_prop " +
                "WHERE name = 'adorned' AND value = 'true' " +
                ")"
                , (
                    source_data.id_user,
                    source_data.id_server,
                    ewcfg.it_cosmetic
                ))

            for row in data:
                item_data = EwItem(id_item=row[0])
                item_data.item_props["adorned"] = 'false'
                item_data.id_owner = target_data.id_user
                item_data.persist()

            ewutils.logMsg('Transferred {} cosmetic items.'.format(len(data)))

            if source_data.weapon >= 0:
                weapons_held = inventory(
                    id_user=target_data.id_user,
                    id_server=target_data.id_server,
                    item_type_filter=ewcfg.it_weapon
                )

                if len(weapons_held) <= target_data.get_weapon_capacity():
                    give_item(id_user=target_data.id_user, id_server=target_data.id_server, id_item=source_data.weapon)

        except:
            ewutils.logMsg("Failed to loot items from user {}".format(source_data.id_user))


"""
    Check how many items are in a given district or player's inventory
"""


def get_inventory_size(owner = None, id_server = None):
    if owner != None and id_server != None:
        # Get data from cache if possible
        item_cache = bknd_core.get_cache(obj_type = "EwItem")
        if item_cache is not False:
            target_items = item_cache.find_entries(criteria = {"id_owner": owner, "id_server": id_server})
            return len(target_items)

        else:
            try:
                items_in_poi = bknd_core.execute_sql_query("SELECT {id_item} FROM items WHERE {id_owner} = %s AND {id_server} = %s".format(
                    id_item=ewcfg.col_id_item,
                    id_owner=ewcfg.col_id_user,
                    id_server=ewcfg.col_id_server
                ), (
                    owner,
                    id_server
                ))

                return len(items_in_poi)

            except:
                return 0
    else:
        return 0


"""
    Get a list of items for the specified player.

    Specify an item_type_filter to get only those items. Be careful: This is
    inserted into SQL without validation/sanitation.
"""


def inventory(
        id_user = None,
        id_server = None,
        item_type_filter = None,
        item_sorting_method = None,
        item_prop_method = None,
):
    items = []

    # Grab the cache if it exists
    item_cache = bknd_core.get_cache(obj_type = "EwItem")
    if (item_cache is not False) and (id_server is not None):
        # Setup criteria
        criteria = {}
        if id_user is not None: criteria.update({"id_owner": id_user})
        if id_server is not None: criteria.update({"id_server": id_server})
        if item_type_filter is not None: criteria.update({"item_type": item_type_filter})
        if item_prop_method is not None: criteria.update({"item_props": item_prop_method})

        found_items = item_cache.find_entries(criteria=criteria)

        # Give a quantity to each item
        for item_data in found_items:
            items.append(item_data)

            # Calculate quantity and set it for the object, cant wait for this to cause a major bug
            quantity = 1
            if item_data.get('stack_max') > 0:
                quantity = item_data.get('stack_size')

            item_data.update({'quantity': quantity})

        # Sort the list by type if demanded, otherwise by id
        if item_sorting_method == "type":
            items.sort(key = lambda i: i.get("item_type"))
        else:
            items.sort(key=lambda i: i.get("id_item"))

        return items

    try:

        time_before = time.time()
        conn_info = bknd_core.databaseConnect()
        conn = conn_info.get('conn')
        cursor = conn.cursor()

        sql = "SELECT {}, {}, {}, {}, {} FROM items WHERE {} = %s"
        if id_user != None:
            sql += " AND {} = '{}'".format(ewcfg.col_id_user, str(id_user))
        if item_type_filter != None:
            sql += " AND {} = '{}'".format(ewcfg.col_item_type, item_type_filter)
        if item_sorting_method != None:
            if item_sorting_method == 'type':
                sql += " ORDER BY {}".format(ewcfg.col_item_type)
            if item_sorting_method == 'id':
                sql += " ORDER BY {}".format(ewcfg.col_id_item)

        if id_server != None:
            cursor.execute(sql.format(
                ewcfg.col_id_item,
                ewcfg.col_item_type,
                ewcfg.col_soulbound,
                ewcfg.col_stack_max,
                ewcfg.col_stack_size,

                ewcfg.col_id_server
            ), [
                id_server
            ])
            # DEBUG: for profiling
            # time_after = time.time()
            # ewutils.logMsg("Time for items fetch: {}".format(time_after - time_before))

            # time_before = time.time()
            for row in cursor:
                id_item = row[0]
                item_type = row[1]
                soulbound = (row[2] == 1)
                stack_max = row[3]
                stack_size = row[4]

                if item_type == 'slimepoudrin':
                    item_data = EwItem(id_item=id_item)
                    item_type = ewcfg.it_item
                    item_data.item_type = item_type
                    for item in static_items.item_list:
                        if item.context == "poudrin":
                            item_props = {
                                'id_item': item.id_item,
                                'context': item.context,
                                'item_name': item.str_name,
                                'item_desc': item.str_desc
                            }
                    item_def = static_items.item_def_map.get(item_type)
                    item_data.item_props.update(item_def.item_props)
                    item_data.item_props.update(item_props)
                    item_data.persist()

                    ewutils.logMsg('Updated poudrin to new format: {}'.format(id_item))

                if item_type == ewcfg.it_cosmetic:
                    item_data = EwItem(id_item=id_item)
                    item_type = ewcfg.it_cosmetic
                    item_data.item_type = item_type

                    if 'fashion_style' not in item_data.item_props.keys():
                        if item_data.item_props.get('id_cosmetic') == 'soul':
                            item_data.item_props = {
                                'id_cosmetic': item_data.item_props['id_cosmetic'],
                                'cosmetic_name': item_data.item_props['cosmetic_name'],
                                'cosmetic_desc': item_data.item_props['cosmetic_desc'],
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
                                'user_id': item_data.item_props['user_id']
                            }
                        elif item_data.item_props.get('id_cosmetic') == 'scalp':
                            item_data.item_props = {
                                'id_cosmetic': item_data.item_props['id_cosmetic'],
                                'cosmetic_name': item_data.item_props['cosmetic_name'],
                                'cosmetic_desc': item_data.item_props['cosmetic_desc'],
                                'str_onadorn': ewcfg.str_generic_onadorn,
                                'str_unadorn': ewcfg.str_generic_unadorn,
                                'str_onbreak': ewcfg.str_generic_onbreak,
                                'rarity': ewcfg.rarity_plebeian,
                                'attack': 1,
                                'defense': 0,
                                'speed': 0,
                                'ability': None,
                                'durability': ewcfg.generic_scalp_durability,
                                'size': 1,
                                'fashion_style': ewcfg.style_cool,
                                'freshness': 0,
                                'adorned': 'false',
                            }
                        elif item_data.item_props.get('rarity') == ewcfg.rarity_princeps:

                            # TODO: Make princeps have custom stats, etc. etc.
                            current_name = item_data.item_props.get('cosmetic_name')
                            current_desc = item_data.item_props.get('cosmetic_desc')

                            print("Updated Princep '{}' for user with ID {}".format(current_name, id_user))

                            item_data.item_props = {
                                'id_cosmetic': 'princep',
                                'cosmetic_name': current_name,
                                'cosmetic_desc': current_desc,
                                'str_onadorn': ewcfg.str_generic_onadorn,
                                'str_unadorn': ewcfg.str_generic_unadorn,
                                'str_onbreak': ewcfg.str_generic_onbreak,
                                'rarity': ewcfg.rarity_princeps,
                                'attack': 3,
                                'defense': 3,
                                'speed': 3,
                                'ability': None,
                                'durability': ewcfg.base_durability * 100,
                                'size': 1,
                                'fashion_style': ewcfg.style_cool,
                                'freshness': 100,
                                'adorned': 'false',
                            }

                            pass
                        elif item_data.item_props.get('context') == 'costume':

                            item_data.item_props = {
                                'id_cosmetic': 'dhcostume',
                                'cosmetic_name': item_data.item_props['cosmetic_name'],
                                'cosmetic_desc': item_data.item_props['cosmetic_desc'],
                                'str_onadorn': ewcfg.str_generic_onadorn,
                                'str_unadorn': ewcfg.str_generic_unadorn,
                                'str_onbreak': ewcfg.str_generic_onbreak,
                                'rarity': ewcfg.rarity_plebeian,
                                'attack': 1,
                                'defense': 1,
                                'speed': 1,
                                'ability': None,
                                'durability': ewcfg.base_durability * 100,
                                'size': 1,
                                'fashion_style': ewcfg.style_cute,
                                'freshness': 0,
                                'adorned': 'false',
                            }
                        elif item_data.item_props.get('id_cosmetic') == 'cigarettebutt':
                            item_data.item_props = {
                                'id_cosmetic': 'cigarettebutt',
                                'cosmetic_name': item_data.item_props['cosmetic_name'],
                                'cosmetic_desc': item_data.item_props['cosmetic_desc'],
                                'str_onadorn': ewcfg.str_generic_onadorn,
                                'str_unadorn': ewcfg.str_generic_unadorn,
                                'str_onbreak': ewcfg.str_generic_onbreak,
                                'rarity': ewcfg.rarity_plebeian,
                                'attack': 2,
                                'defense': 0,
                                'speed': 0,
                                'ability': None,
                                'durability': ewcfg.base_durability / 2,
                                'size': 1,
                                'fashion_style': ewcfg.style_cool,
                                'freshness': 5,
                                'adorned': 'false',
                            }

                        else:
                            # print('ITEM PROPS: {}'.format(item_data.item_props))

                            item = cosmetics.cosmetic_map.get(item_data.item_props.get('id_cosmetic'))

                            if item == None:
                                if item_data.item_props.get('id_cosmetic') == None:
                                    print('Item {} lacks an id_cosmetic attribute. Formatting now...'.format(id_item))
                                    placeholder_id = 'oldcosmetic'
                                else:
                                    print('Item {} has an invalid id_cosmetic of {}. Formatting now...'.format(item_data.item_props, item_data.item_props.get('id_cosmetic')))
                                    placeholder_id = item_data.item_props.get('id_cosmetic')

                                item_data.item_props = {
                                    'id_cosmetic': placeholder_id,
                                    'cosmetic_name': item_data.item_props.get('cosmetic_name'),
                                    'cosmetic_desc': item_data.item_props.get('cosmetic_desc'),
                                    'str_onadorn': ewcfg.str_generic_onadorn,
                                    'str_unadorn': ewcfg.str_generic_unadorn,
                                    'str_onbreak': ewcfg.str_generic_onbreak,
                                    'rarity': ewcfg.rarity_plebeian,
                                    'attack': 1,
                                    'defense': 1,
                                    'speed': 1,
                                    'ability': None,
                                    'durability': ewcfg.base_durability,
                                    'size': 1,
                                    'fashion_style': ewcfg.style_cool,
                                    'freshness': 0,
                                    'adorned': 'false',
                                }

                            else:

                                item_data.item_props = {
                                    'id_cosmetic': item.id_cosmetic,
                                    'cosmetic_name': item.str_name,
                                    'cosmetic_desc': item.str_desc,
                                    'str_onadorn': item.str_onadorn if item.str_onadorn else ewcfg.str_generic_onadorn,
                                    'str_unadorn': item.str_unadorn if item.str_unadorn else ewcfg.str_generic_unadorn,
                                    'str_onbreak': item.str_onbreak if item.str_onbreak else ewcfg.str_generic_onbreak,
                                    'rarity': item.rarity if item.rarity else ewcfg.rarity_plebeian,
                                    'attack': 0,
                                    'defense': 0,
                                    'speed': 0,
                                    'ability': item.ability if item.ability else None,
                                    'durability': item.durability if item.durability else ewcfg.base_durability,
                                    'size': item.size if item.size else 1,
                                    'fashion_style': item.style if item.style else ewcfg.style_cool,
                                    'freshness': item.freshness if item.freshness else 0,
                                    'adorned': 'false',
                                }

                        item_data.persist()
                        ewutils.logMsg('Updated cosmetic to new format: {}'.format(id_item))

                item_def = static_items.item_def_map.get(item_type)

                if (item_def != None):
                    items.append({
                        'id_item': id_item,
                        'item_type': item_type,
                        'soulbound': soulbound,
                        'stack_max': stack_max,
                        'stack_size': stack_size,

                        'item_def': item_def
                    })

            # DEBUG: for profiling
            # time_after = time.time()
            # ewutils.logMsg("Time for item preparation: {}".format(time_after - time_before))
            # time_before = time.time()
            if len(items) > 0:
                item_ids = tuple(map(lambda i: i.get('id_item'), items))

                item_map = {}

                for item in items:
                    item['item_props'] = {}
                    item_map[item.get('id_item')] = item

                cursor.execute("SELECT id_item, name, value FROM items_prop WHERE id_item IN %s", (item_ids,))

                for row in cursor:
                    id_item = row[0]
                    name = row[1]
                    value = row[2]

                    item = item_map.get(id_item)
                    item.get('item_props')[name] = value

            # DEBUG: for profiling
            # time_after = time.time()

            # ewutils.logMsg("Time for item props fetch: {}".format(time_after - time_before))
            # time_before = time.time()

            for item in items:
                item_def = item.get('item_def')
                id_item = item.get('id_item')
                name = item_def.str_name
                # print("761 -- {}".format(name))

                quantity = 1
                if item.get('stack_max') > 0:
                    quantity = item.get('stack_size')

                item['quantity'] = quantity

                # Name requires variable substitution. Look up the item properties.
                if name.find('{') >= 0:
                    item_inst = item

                    if item_inst != None and item_inst.get('id_item') >= 0:
                        name = name.format_map(item_inst.get('item_props'))

                        if name.find('{') >= 0:
                            try:
                                name = name.format_map(item_inst.get('item_props'))
                            except:
                                pass
                        # print("Exception caught in ewitem -- Item might have brackets inside name.")
                        # If a key error comes from here, it's likely that an item somehow got a { symbol placed inside its name
                        # Normally curly brackets are used for renaming an item based on what comes from item_def, such as {item_name}
                        # Therefore, in most circumstances we can ignore when a key error comes from here, since that item has already been given a name.

                # if a weapon has no name show its type instead
                if name == "" and item_inst.get('item_type') == ewcfg.it_weapon:
                    name = item_inst.get('item_props').get("weapon_type")

                item['name'] = name
            time_after = time.time()

        # DEBUG: for profiling
        # ewutils.logMsg("Time for name assignment: {}".format(time_after - time_before))
    finally:
        # Clean up the database handles.
        cursor.close()
        bknd_core.databaseClose(conn_info)

    return items



    #Assign an existing item to a player



def give_item(
        member = None,
        id_item = None,
        id_user = None,
        id_server = None
):
    if id_user is None and id_server is None and member is not None:
        id_server = member.guild.id
        id_user = str(member.id)

    if id_server is not None and id_user is not None and id_item is not None:
        item = EwItem(id_item=id_item)
        item.id_owner = id_user

        # Ensure general limit implementation
        if ewutils.is_player_inventory(id_user, id_server):
            # But only for players
            other_items = inventory(
                id_user=id_user,
                id_server=id_server,
                item_type_filter=item.item_type
            )

            if len(other_items) >= ewcfg.generic_inv_limit:
                del other_items
                return False

        bknd_core.execute_sql_query(
            "UPDATE items SET id_user = %s WHERE id_server = %s AND {id_item} = %s".format(
                id_item=ewcfg.col_id_item
            ), (
                id_user,
                id_server,
                id_item
            )
        )

        bknd_core.cache_data(obj = item)

        remove_from_trades(id_item)

        # Reset the weapon's damage modifying stats
        if item.item_type == ewcfg.it_weapon:
            item.id_owner = id_user
            item.item_props["kills"] = 0
            item.item_props["consecutive_hits"] = 0
            item.item_props["time_lastattack"] = 0
            item.persist()
    return True


def give_item_multi(id_list = None, destination = None):
    if id_list is not None and destination is not None:
        for id_item in id_list:
            remove_from_trades(id_item)

        try:

            drop_list = ','.join(map(str, id_list))

            bknd_core.execute_sql_query(
                "UPDATE items SET {id_user} = %s WHERE id_item IN({drop_list})".format(
                    id_user=ewcfg.col_id_user,
                    drop_list=drop_list
                ),
                (
                    [destination]
                ))

        except Exception as e:
            ewutils.logMsg('Failed to mass move items with Exception: {}. \nDrop List:{} \nDestination:{}'.format(e, ','.join(map(str, id_list)), destination))
            traceback.print_exc(file=sys.stdout)

        item_cache = bknd_core.get_cache(obj_type="EwItem")
        for ids in id_list:
            cache_item = item_cache.get_entry(unique_vals={"id_item": ids})
            cache_item.update({'id_owner': destination})
            item_cache.set_entry(data=cache_item)

"""
    Return false if a player's inventory is at or over capacity for a specific item type
    >return_strings will return a response instead of a yes/no. good for quick general inventory checks
    >items_added is for when more than one item will be added to the inventory. they would all need to be the same item type for this check to work
    >pronoun: you or they. what's it gonna be
"""


def check_inv_capacity(user_data = None, item_type = None, return_strings = False, pronoun = 'You', items_added = 1):
    true_bool = True
    false_bool = False

    if return_strings:
        true_bool = ""
        false_bool = "You can't carry any more items."

    if items_added <= 0: #if items are being removed or the count remains the same
        return true_bool

    if user_data is not None and item_type is not None:
        if item_type == ewcfg.it_food:
            if return_strings:
                false_bool = "{} can't carry any more food.".format(pronoun)
            food_items = inventory(
                id_user=user_data.id_user,
                id_server=user_data.id_server,
                item_type_filter=ewcfg.it_food
            )
            if len(food_items) + (items_added - 1) >= user_data.get_food_capacity():
                return false_bool
            else:
                return true_bool
        elif item_type == ewcfg.it_weapon:
            if return_strings:
                false_bool = "{} can't carry any more weapons.".format(pronoun)
            weapons_held = inventory(
                id_user=user_data.id_user,
                id_server=user_data.id_server,
                item_type_filter=ewcfg.it_weapon
            )

            if len(weapons_held) + (items_added - 1) >= user_data.get_weapon_capacity():
                return false_bool
            else:
                return true_bool
        elif item_type == ewcfg.it_relic:
            if return_strings:
                false_bool = "{} can't carry any more relics.".format(pronoun)
            relics_held = inventory(
                id_user=user_data.id_user,
                id_server=user_data.id_server,
                item_type_filter=ewcfg.it_relic
            )

            if len(relics_held) + (items_added - 1) >= ewcfg.relic_item_limit:
                return false_bool
            else:
                return true_bool

        else:
            if return_strings:
                false_bool = "{} can't carry any more items.".format(pronoun)
            other_items = inventory(
                id_user=user_data.id_user,
                id_server=user_data.id_server,
                item_type_filter=item_type
            )

            if len(other_items) + (items_added - 1) >= ewcfg.generic_inv_limit:
                return false_bool
            else:
                return true_bool

    else:
        return false_bool


"""
	Find a single item in the player's inventory (returns either a (non-EwItem) item or None)
"""


def find_item(item_search = None, id_user = None, id_server = None, item_type_filter = None, admin = 0):
    item_sought = None

    # search for an ID instead of a name
    try:
        item_search_int = int(item_search)
    except:
        item_search_int = None
    if item_search:
        items = inventory(id_user=id_user, id_server=id_server, item_type_filter=item_type_filter)
        item_sought = None

        item_search_list = list(map(lambda it: {
            "id_item": it.get("id_item"),
            "name": it.get("name"),
            "original": it
        }, items))

        # find the first (i.e. the oldest) item that matches the search
        for item in item_search_list:
            item_name = ewutils.flattenTokenListToString(item.get('name'))
            if item.get('id_item') == item_search_int or item_name == item_search:
                item_sought = item.get("original")
                break
            if item_sought == None and item_search in item_name:
                item_sought = item.get("original")

        # Trust me just this once, this was necessary. use createall to make a huge item store and snag or scavenge
        # Open task manager at look at memory usage after ratelimiting the bot. It's insane
        del items

    return item_sought


# search and remove the given item from an ongoing trade
def remove_from_trades(id_item):
    for trader in ewutils.trading_offers:
        for item in ewutils.trading_offers.get(trader):
            if id_item == item.get("id_item"):
                ewutils.trading_offers.get(trader).remove(item)

                ewutils.active_trades.get(trader)["state"] = ewcfg.trade_state_ongoing
                ewutils.active_trades.get(ewutils.active_trades.get(trader).get("trader"))["state"] = ewcfg.trade_state_ongoing
                return


def equip(user_data, weapon_item = None):
    weapon = static_weapons.weapon_map.get(weapon_item.item_props.get("weapon_type"))

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "Ghosts can't equip weapons."
    elif user_data.life_state == ewcfg.life_state_juvenile and ewcfg.weapon_class_juvie not in weapon.classes and not ewcfg.slimernalia_active:
        response = "Juvies can't equip weapons."
    elif user_data.weaponmarried == True:
        current_weapon = EwItem(id_item=user_data.weapon)
        if weapon_item.item_props.get("married") == str(user_data.id_user):
            response = "You equip your " + (weapon_item.item_props.get("weapon_type") if len(weapon_item.item_props.get("weapon_name")) == 0 else weapon_item.item_props.get("weapon_name"))
            user_data.weapon = weapon_item.id_item

            if ewcfg.weapon_class_captcha in weapon.classes:
                captcha = ewutils.generate_captcha(length=weapon.captcha_length, user_data=user_data)
                weapon_item.item_props["captcha"] = captcha
                response += "\nSecurity code: **{}**".format(ewutils.text_to_regional_indicator(captcha))
        else:
            partner_name = current_weapon.item_props.get("weapon_name")
            if partner_name in [None, ""]:
                partner_name = "partner"
            response = "You reach to pick up a new weapon, but your old {} remains motionless with jealousy. You dug your grave, now decompose in it.".format(partner_name)
    else:

        response = "You equip your " + (weapon_item.item_props.get("weapon_type") if len(weapon_item.item_props.get("weapon_name")) == 0 else weapon_item.item_props.get("weapon_name")) + "."
        user_data.weapon = weapon_item.id_item

        if user_data.sidearm == user_data.weapon:
            user_data.sidearm = -1

        if ewcfg.weapon_class_captcha in weapon.classes:
            captcha = ewutils.generate_captcha(length=weapon.captcha_length, user_data=user_data)
            weapon_item.item_props["captcha"] = captcha
            response += "\nSecurity code: **{}**".format(ewutils.text_to_regional_indicator(captcha))

    return response


def equip_sidearm(user_data, sidearm_item = None):
    sidearm = static_weapons.weapon_map.get(sidearm_item.item_props.get("weapon_type"))

    if user_data.life_state == ewcfg.life_state_corpse:
        response = "Ghosts can't equip weapons."
    elif user_data.life_state == ewcfg.life_state_juvenile and ewcfg.weapon_class_juvie not in sidearm.classes and not ewcfg.slimernalia_active:
        response = "Juvies can't equip weapons."
    elif user_data.weaponmarried == True and int(sidearm_item.item_props.get("married")) == user_data.id_user:
        current_weapon = EwItem(id_item=user_data.weapon)
        partner_name = current_weapon.item_props.get("weapon_name")
        if partner_name in [None, ""]:
            partner_name = "partner"
        response = "Your {} is motionless in your hand, frothing with jealousy. You can't sidearm it like one of your side ho pickaxes.".format(partner_name)
    else:

        response = "You sidearm your " + (sidearm_item.item_props.get("weapon_type") if len(sidearm_item.item_props.get("weapon_name")) == 0 else sidearm_item.item_props.get("weapon_name")) + "."
        user_data.sidearm = sidearm_item.id_item

        if user_data.weapon == user_data.sidearm:
            user_data.weapon = -1

    return response


def get_fashion_stats(user_data):
    cosmetics = inventory(
        id_user=user_data.id_user,
        id_server=user_data.id_server,
        item_type_filter=ewcfg.it_cosmetic
    )

    result = [0] * 3

    cosmetic_items = []
    for cosmetic in cosmetics:
        cosmetic_items.append(EwItem(id_item=cosmetic.get('id_item')))

    for cos in cosmetic_items:
        if cos.item_props['adorned'] == 'true':

            cosmetic_count = sum(1 for cosmetic in cosmetic_items if cosmetic.item_props['cosmetic_name'] == cos.item_props['cosmetic_name']
                                 and cosmetic.item_props['adorned'] == 'true')

            if cos.item_props.get('attack') == None:
                print('Failed to get attack stat for cosmetic with props: {}'.format(cos.item_props))

            result[0] += int(int(cos.item_props['attack']) / cosmetic_count)
            result[1] += int(int(cos.item_props['defense']) / cosmetic_count)
            result[2] += int(int(cos.item_props['speed']) / cosmetic_count)

    return result


def get_freshness(user_data, adorned_id_list = None):
    cosmetic_items = []
    # Allow a list of adorned ids to be passed in lieu of searching for them
    if adorned_id_list is None:
        cosmetics = inventory(
            id_user=user_data.id_user,
            id_server=user_data.id_server,
            item_type_filter=ewcfg.it_cosmetic
        )
        for cosmetic in cosmetics:
            cosmetic_items.append(EwItem(id_item=cosmetic.get('id_item')))
    else:
        # build cosmetic_items from passed in ids
        for it_id in adorned_id_list:
            cosmetic_items.append(EwItem(id_item=it_id))


    adorned_cosmetics = sum(1 for cosmetic in cosmetic_items if cosmetic.item_props['adorned'] == 'true')

    mutations = user_data.get_mutations()
    bonus_freshness = 500 if ewcfg.mutation_id_unnaturalcharisma in mutations else 0

    if len(cosmetic_items) == 0 or adorned_cosmetics < 2:
        return bonus_freshness

    base_freshness = 0
    hue_count = {}
    style_count = {}

    # get base freshness, hue and style counts
    for cos in cosmetic_items:
        if cos.item_props['adorned'] == 'true':

            cosmetic_count = sum(1 for cosmetic in cosmetic_items if cosmetic.item_props['cosmetic_name'] == cos.item_props['cosmetic_name']
                                 and cosmetic.item_props['adorned'] == 'true')

            base_freshness += int(cos.item_props['freshness']) / cosmetic_count

            hue = hue_static.hue_map.get(cos.item_props.get('hue'))
            if hue is not None:
                if hue_count.get(hue):
                    hue_count[hue] += 1
                else:
                    hue_count[hue] = 1

            style = cos.item_props['fashion_style']
            if style_count.get(style):
                style_count[style] += 1
            else:
                style_count[style] = 1

    # calc hue modifier
    hue_mod = 1
    if len(hue_count) > 0:

        complimentary_hue_count = 0
        dominant_hue = max(hue_count, key=lambda key: hue_count[key])

        for hue in hue_count:
            if hue.id_hue == dominant_hue.id_hue or hue.id_hue in dominant_hue.effectiveness or hue.is_neutral:
                complimentary_hue_count += hue_count[hue]

        if hue_count[dominant_hue] / adorned_cosmetics >= 0.6 and complimentary_hue_count == adorned_cosmetics:
            hue_mod = 5

    # calc style modifier
    style_mod = 1
    dominant_style = max(style_count, key=lambda key: style_count[key])

    if style_count[dominant_style] / adorned_cosmetics >= 0.6:
        style_mod = style_count[dominant_style] / adorned_cosmetics * 10

    return int(base_freshness * hue_mod * style_mod) + bonus_freshness


def get_weaponskill(user_data):
    # Get the skill for the user's current weapon.
    if user_data.weapon != None and user_data.weapon >= 0:
        skills = ewutils.weaponskills_get(
            id_server=user_data.id_server,
            id_user=user_data.id_user
        )

        weaponskill = 0
        weapon_item = EwItem(id_item=user_data.weapon)
        if weapon_item.item_props.get("weapon_type") in skills:
            weaponskill = skills[weapon_item.item_props.get("weapon_type")]

    else:
        weaponskill = 0

    return weaponskill


""" Loads every item in the database into the cache. Returns true if successful, otherwise false. """

def load_items_cache():
    #try:
    # Grab the ID of every extant item
    results = bknd_core.execute_sql_query("SELECT {id_item} FROM items".format(id_item=ewcfg.col_id_item))

    # Initialize an EwItem for each returned ID
    tracker = 0
    for row in results:
        tracker += 1
        EwItem(id_item=row[0])
        if tracker % 1000 == 0:
            ewutils.logMsg("Loaded {} EwItems into cache.".format(tracker))

    # Tell the client it didn't error out halfway
    return True

    #except:
        #ewutils.logMsg("Failed to load all items from database into cache.")
        #return False


bknd_core.cache_type_to_load_fn.update({"EwItem": load_items_cache})
