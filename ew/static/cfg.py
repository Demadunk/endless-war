import datetime
import random
# Global configuration options.


version = "v4.23 SEASON 4 ACT 2 - Double Slimernalia"



dir_msgqueue = 'msgqueue'

database = "rfck"

discord_message_length_limit = 2000

# Update intervals
update_hookstillactive = 60 * 60 * 1
update_pvp = 60
update_market = 900  # 15 min = 900

# Whether or not to suppress missing channel warnings, for your sanity. Probably shouldn't use live
suppress_missing_channel = False

# Number of times the bot should try a permissions-related API call. This is done purely for safety measures.
permissions_tries = 1

# Time saved moving through friendly territory (or lost in hostile territory).
territory_time_gain = 10

#Double Halloween Features
dh_active = True
#Existing Stages for Double Halloween. As the years go by we may add on to this
dh_stage = 1

#Slimernalia Features
slimernalia_active = True

#Swilldermuk Features
swilldermuk_active = False

#Event stages. Import them to the file you want by doing from ew.static.cfg import event_stage, then reference it with ewcfg.event_stage. Go wild.
event_stage = 0


"""
1: Normal
2: Sacrifice Minigame
3: UFO Abduction
4: Rewind
"""


public_gamestates = {
    'dhorsemankills': [1, '4', 0], #determines spawn frequency in double halloween. the bit is set to true(unused) and the value is set to 4, indicating he has been killed 4 times.
    'slimernaliakingpin':[1, '-1', 0], #The existing slimernalia kingpin
    'cratersvillehole':[1, '0', 0],
    'toxingtonhole':[1, '0', 0],
    'juviesrowhole':[1, '0', 0],
    'hall_counter':[1, '1', 0],
    'bobocuatromorale':[0, '', 0],
    'hydraulicpress':[0, '', 3000000]
}

forbidden_channels = ["suggestion-box"]

# Market delta
max_iw_swing = 30

# An inventory limit for every item type that's not food or weapons
generic_inv_limit = 1000

relic_item_limit = 3

# combatant ids to differentiate players and NPCs in combat
combatant_type_player = "player"
combatant_type_enemy = "enemy"

# Life states. How the player is living (or deading) in the database
life_state_corpse = 0
life_state_juvenile = 1
life_state_enlisted = 2
life_state_vigilante = 3
life_state_executive = 6
life_state_lucky = 7
life_state_grandfoe = 8
life_state_kingpin = 10
life_state_observer = 20


farm_life_state_juviethumb = 30
farm_life_state_thumb = 31

# Player stats. What, you ever play an RPG before, kid?
stat_attack = 'attack'
stat_defense = 'defense'
stat_speed = 'speed'

playerstats_list = [
    stat_attack,
    stat_defense,
    stat_speed,
]

slimeoid_tick_length = 5 * 60 # 5 minutes

# slimeoid life states
slimeoid_state_none = 0
slimeoid_state_forming = 1
slimeoid_state_active = 2
slimeoid_state_stored = 3
slimeoid_state_dead = 4

# slimeoid types
sltype_lab = 'Lab'
sltype_nega = 'Nega'
sltype_wild = 'Wild'

# slimeoid battle types
battle_type_arena = 0
battle_type_nega = 1

# slimeoid stats
slimeoid_stat_moxie = 'moxie'
slimeoid_stat_grit = 'grit'
slimeoid_stat_chutzpah = 'chutzpah'

blockparty_slimebonus_per_tick = 250000


# ID tags for points of interest that are needed in code.
poi_id_thesewers = "thesewers"
poi_id_slimeoidlab = "slimeoidlaboratory"
poi_id_realestate = "realestateagency"
poi_id_glocksburycomics = "glocksburycomics"
poi_id_slimypersuits = "slimypersuits"
poi_id_mine = "themines"
poi_id_mine_sweeper = "theminessweeper"
poi_id_mine_bubble = "theminesbubble"
poi_id_thecasino = "thecasino"
poi_id_711 = "outsidethe711"
poi_id_speakeasy = "thekingswifessonspeakeasy"
poi_id_dojo = "thedojo"
poi_id_arena = "thebattlearena"
poi_id_nlacu = "newlosangelescityuniversity"
poi_id_foodcourt = "thefoodcourt"
poi_id_cinema = "nlacakanmcinemas"
poi_id_bazaar = "thebazaar"
poi_id_recyclingplant = "recyclingplant"
poi_id_stockexchange = "theslimestockexchange"
poi_id_endlesswar = "endlesswar"
poi_id_slimecorphq = "slimecorphq"
poi_id_cv_mines = "cratersvillemines"
poi_id_cv_mines_sweeper = "cratersvilleminessweeper"
poi_id_cv_mines_bubble = "cratersvilleminesbubble"
poi_id_tt_mines = "toxingtonmines"
poi_id_tt_mines_sweeper = "toxingtonminessweeper"
poi_id_tt_mines_bubble = "toxingtonminesbubble"
poi_id_diner = "smokerscough"
poi_id_seafood = "redmobster"
poi_id_jr_farms = "juviesrowfarms"
poi_id_og_farms = "oozegardensfarms"
poi_id_ab_farms = "arsonbrookfarms"
poi_id_neomilwaukeestate = "neomilwaukeestate"
poi_id_beachresort = "thebeachresort"
poi_id_countryclub = "thecountryclub"
poi_id_slimesea = "slimesea"
poi_id_slimesendcliffs = "slimesendcliffs"
poi_id_greencakecafe = "greencakecafe"
poi_id_sodafountain = "sodafountain"
poi_id_bodega = "bodega"
poi_id_wafflehouse = "wafflehouse"
poi_id_blackpond = "blackpond"
poi_id_basedhardware = "basedhardware"
poi_id_clinicofslimoplasty = "clinicofslimoplasty"
poi_id_thebreakroom = "thebreakroom"
poi_id_underworld = "underworld"
poi_id_themuseum = "themuseum"
poi_id_greenroom = "greenroom"
poi_id_ghostcafe = "ghostmaidcafe"
poi_id_coalitionsurplus = "coalitionsurplus"


poi_id_raiddenentryway = "raiddenentryway"
poi_id_raiddenatrium = "raiddenatrium"
poi_id_raiddencore = "raiddencore"

poi_id_themoon = "themoon"

# transports
poi_id_ferry = "ferry"
poi_id_subway_pink01 = "subwaypink01"
poi_id_subway_pink02 = "subwaypink02"
poi_id_subway_gold01 = "subwaygold01"
poi_id_subway_gold02 = "subwaygold02"
poi_id_subway_green01 = "subwaygreen01"
poi_id_subway_green02 = "subwaygreen02"
poi_id_subway_black01 = "subwayblack01"
poi_id_subway_black02 = "subwayblack01"
poi_id_subway_purple01 = "subwaypurple01"
poi_id_subway_purple02 = "subwaypurple02"
poi_id_blimp = "blimp"
poi_id_apt = "apt"

# ferry ports
poi_id_wt_port = "wreckingtonport"
poi_id_vc_port = "vagrantscornerport"

# subway stations
poi_id_tt_subway_station = "toxingtonsubwaystation"
poi_id_ah_subway_station = "astatineheightssubwaystation"
poi_id_gd_subway_station = "gatlingsdalesubwaystation"
poi_id_ck_subway_station = "copkilltownsubwaystation"
poi_id_ab_subway_station = "arsonbrooksubwaystation"
poi_id_sb_subway_station = "smogsburgsubwaystation"
poi_id_dt_subway_station = "downtownsubwaystation"
poi_id_kb_subway_station = "krakbaysubwaystation"
poi_id_gb_subway_station = "glocksburysubwaystation"
poi_id_wgb_subway_station = "westglocksburysubwaystation"
poi_id_jp_subway_station = "jaywalkerplainsubwaystation"
poi_id_nsb_subway_station = "northsleezesubwaystation"
poi_id_ssb_subway_station = "southsleezesubwaystation"
poi_id_bd_subway_station = "brawldensubwaystation"
poi_id_cv_subway_station = "cratersvillesubwaystation"
poi_id_wt_subway_station = "wreckingtonsubwaystation"
poi_id_rr_subway_station = "rowdyroughhousesubwaystation"
poi_id_gld_subway_station = "greenlightsubwaystation"
poi_id_jr_subway_station = "juviesrowsubwaystation"
poi_id_vc_subway_station = "vagrantscornersubwaystation"
poi_id_afb_subway_station = "assaultflatssubwaystation"
poi_id_vp_subway_station = "vandalparksubwaystation"
poi_id_pa_subway_station = "poudrinalleysubwaystation"
poi_id_og_subway_station = "oozegardenssubwaystation"
poi_id_cl_subway_station = "crooklinesubwaystation"
poi_id_lc_subway_station = "littlechernobylsubwaystation"
poi_id_nny_subway_station = "newnewyonkerssubwaystation"

poi_id_underworld_subway_station = "underworldsubwaystation"

# ferry ports
poi_id_df_blimp_tower = "dreadfordblimptower"
poi_id_afb_blimp_tower = "assaultflatsblimptower"

# district pois
poi_id_downtown = "downtown"
poi_id_smogsburg = "smogsburg"
poi_id_copkilltown = "copkilltown"
poi_id_krakbay = "krakbay"
poi_id_poudrinalley = "poudrinalley"
poi_id_rowdyroughhouse = "rowdyroughhouse"
poi_id_greenlightdistrict = "greenlightdistrict"
poi_id_oldnewyonkers = "oldnewyonkers"
poi_id_littlechernobyl = "littlechernobyl"
poi_id_arsonbrook = "arsonbrook"
poi_id_astatineheights = "astatineheights"
poi_id_gatlingsdale = "gatlingsdale"
poi_id_vandalpark = "vandalpark"
poi_id_glocksbury = "glocksbury"
poi_id_northsleezeborough = "northsleezeborough"
poi_id_southsleezeborough = "southsleezeborough"
poi_id_oozegardens = "oozegardens"
poi_id_cratersville = "cratersville"
poi_id_wreckington = "wreckington"
poi_id_juviesrow = "juviesrow"
poi_id_slimesend = "slimesend"
poi_id_vagrantscorner = "vagrantscorner"
poi_id_assaultflatsbeach = "assaultflatsbeach"
poi_id_newnewyonkers = "newnewyonkers"
poi_id_brawlden = "brawlden"
poi_id_toxington = "toxington"
poi_id_charcoalpark = "charcoalpark"
poi_id_poloniumhill = "poloniumhill"
poi_id_westglocksbury = "westglocksbury"
poi_id_jaywalkerplain = "jaywalkerplain"
poi_id_crookline = "crookline"
poi_id_dreadford = "dreadford"
poi_id_maimridge = "maimridge"
poi_id_thevoid = "thevoid"

poi_id_toxington_pier = "toxingtonpier"
poi_id_jaywalkerplain_pier = "jaywalkerplainpier"
poi_id_crookline_pier = "crooklinepier"
poi_id_assaultflatsbeach_pier = "assaultflatsbeachpier"
poi_id_vagrantscorner_pier = "vagrantscornerpier"  # NOT USED
poi_id_slimesend_pier = "slimesendpier"
poi_id_juviesrow_pier = "juviesrowpier"

# Apartment subzones
poi_id_apt_downtown = "aptdowntown"
poi_id_apt_smogsburg = "aptsmogsburg"
poi_id_apt_krakbay = "aptkrakbay"
poi_id_apt_poudrinalley = "aptpoudrinalley"
poi_id_apt_greenlightdistrict = "aptgreenlightdistrict"
poi_id_apt_oldnewyonkers = "aptoldnewyonkers"
poi_id_apt_littlechernobyl = "aptlittlechernobyl"
poi_id_apt_arsonbrook = "aptarsonbrook"
poi_id_apt_astatineheights = "aptastatineheights"
poi_id_apt_gatlingsdale = "aptgatlingsdale"
poi_id_apt_vandalpark = "aptvandalpark"
poi_id_apt_glocksbury = "aptglocksbury"
poi_id_apt_northsleezeborough = "aptnorthsleezeborough"
poi_id_apt_southsleezeborough = "aptsouthsleezeborough"
poi_id_apt_oozegardens = "aptoozegardens"
poi_id_apt_cratersville = "aptcratersville"
poi_id_apt_wreckington = "aptwreckington"
poi_id_apt_slimesend = "aptslimesend"
poi_id_apt_vagrantscorner = "aptvagrantscorner"
poi_id_apt_assaultflatsbeach = "aptassaultflatsbeach"
poi_id_apt_newnewyonkers = "aptnewnewyonkers"
poi_id_apt_brawlden = "aptbrawlden"
poi_id_apt_toxington = "apttoxington"
poi_id_apt_charcoalpark = "aptcharcoalpark"
poi_id_apt_poloniumhill = "aptpoloniumhill"
poi_id_apt_westglocksbury = "aptwestglocksbury"
poi_id_apt_jaywalkerplain = "aptjaywalkerplain"
poi_id_apt_crookline = "aptcrookline"
poi_id_apt_dreadford = "aptdreadford"
poi_id_apt_maimridge = "aptmaimridge"

poi_id_thesummit = "thesummit"
poi_id_skilodges = "skilodges"
poi_id_colloidsprings = "colloidsprings"

# Tutorial zones
poi_id_tutorial_classroom = "classroom"
poi_id_tutorial_ghostcontainment = "ghostcontainment"
poi_id_tutorial_hallway = "hallway"

compartment_id_closet = "closet"
compartment_id_fridge = "fridge"
compartment_id_decorate = "decorate"
compartment_id_bookshelf = "bookshelf"
compartment_id_freeze = "freeze"
location_id_empty = "empty"

# Outskirts
# Layer 1
poi_id_south_outskirts_edge = "southoutskirtsedge"
poi_id_southwest_outskirts_edge = "southwestoutskirtsedge"
poi_id_west_outskirts_edge = "westoutskirtsedge"
poi_id_northwest_outskirts_edge = "northwestoutskirtsedge"
poi_id_north_outskirts_edge = "northoutskirtsedge"
poi_id_nuclear_beach_edge = "nuclearbeachedge"  # aka Assault Flats Beach Outskirts Edge
# Layer 2
poi_id_south_outskirts = "southoutskirts"
poi_id_southwest_outskirts = "southwestoutskirts"
poi_id_west_outskirts = "westoutskirts"
poi_id_northwest_outskirts = "northwestoutskirts"
poi_id_north_outskirts = "northoutskirts"
poi_id_nuclear_beach = "nuclearbeach"
# Layer 3
poi_id_south_outskirts_depths = "southoutskirtsdepths"
poi_id_southwest_outskirts_depths = "southwestoutskirtsdepths"
poi_id_west_outskirts_depths = "westoutskirtsdepths"
poi_id_northwest_outskirts_depths = "northwestoutskirtsdepths"
poi_id_north_outskirts_depths = "northoutskirtsdepths"
poi_id_nuclear_beach_depths = "nuclearbeachdepths"

# The Sphere
poi_id_thesphere = "thesphere"

# Community Chests
chest_id_copkilltown = "copkilltownchest"
chest_id_rowdyroughhouse = "rowdyroughhousechest"
chest_id_juviesrow = "juviesrowchest"
chest_id_thesewers = "sewerschest"
chest_id_breakroom = "breakroomchest"

# Transport types
transport_type_ferry = "ferry"
transport_type_subway = "subway"
transport_type_blimp = "blimp"

# Ferry lines
transport_line_ferry_wt_to_vc = "ferrywttovc"
transport_line_ferry_vc_to_wt = "ferryvctowt"

# Subway lines
transport_line_subway_yellow_northbound = "subwayyellownorth"
transport_line_subway_yellow_southbound = "subwayyellowsouth"

transport_line_subway_red_northbound = "subwayrednorth"
transport_line_subway_red_southbound = "subwayredsouth"

transport_line_subway_blue_eastbound = "subwayblueeast"
transport_line_subway_blue_westbound = "subwaybluewest"

transport_line_subway_white_eastbound = "subwaywhiteeast"
transport_line_subway_white_westbound = "subwaywhitewest"

transport_line_subway_green_eastbound = "subwaygreeneast"
transport_line_subway_green_westbound = "subwaygreenwest"

# Blimp lines
transport_line_blimp_df_to_afb = "blimpdftoafb"
transport_line_blimp_afb_to_df = "blimpafbtodf"

# Role names. All lower case with no spaces.
role_juvenile = "juveniles"
role_juvenile_pvp = "juvenilewanted"
role_juvenile_active = "juvenileotp"
role_rowdyfucker = "rowdyfucker"
role_rowdyfuckers = "rowdys"
role_rowdyfuckers_pvp = "rowdywanted"
role_rowdyfuckers_active = "rowdyotp"
role_copkiller = "copkiller"
role_copkillers = "killers"
role_copkillers_pvp = "killerwanted"
role_copkillers_active = "killerotp"
role_corpse = "corpse"
role_corpse_pvp = "corpsewanted"
role_corpse_active = "corpseotp"
role_kingpin = "kingpin"
role_grandfoe = "grandfoe"
role_slimecorp = "slimecorp"
role_slimecorp_pvp = "slimecorpvulnerable"
role_slimecorp_active = "slimecorpotp"
role_executive = "executive"
role_deathfurnace = "deathfurnace"
role_donor = "terezigang"
role_tutorial = "newintown"
role_slimernalia = "kingpinofslimernalia"
role_gellphone = "gellphone"
role_brimstoneprog = "brimstoneprogrammer"
role_bpadmin = "bpadmin"
role_bdadmin = "bdadmin"
role_blasting = "blasting"
role_brimstonedesperados = "brimstonedesperados"
role_null_major_role = "nullmajorrole"
role_null_minor_role = "nullminorrole"

permission_read_messages = "read"
permission_send_messages = "send"
permission_connect_to_voice = "connect"
# permission_see_history = "history"
# permission_upload_files = "upload" -- everything else including this should be true by default.
# Read, Send, and History should be false by default but set to true.

permissions_general = [permission_read_messages, permission_send_messages, permission_connect_to_voice]

faction_roles = [
    role_juvenile,
    role_juvenile_pvp,
    role_juvenile_active,
    role_rowdyfucker,
    role_rowdyfuckers,
    role_rowdyfuckers_pvp,
    role_rowdyfuckers_active,
    role_copkiller,
    role_copkillers,
    role_copkillers_pvp,
    role_copkillers_active,
    role_executive,
    role_slimecorp,
    role_slimecorp_pvp,
    role_slimecorp_active,
    role_corpse,
    role_corpse_pvp,
    role_corpse_active,
    role_grandfoe,
    role_tutorial,
]

role_to_pvp_role = {
    role_juvenile: role_juvenile_pvp,
    role_rowdyfuckers: role_rowdyfuckers_pvp,
    role_copkillers: role_copkillers_pvp,
    role_corpse: role_corpse_pvp,
    role_slimecorp: role_slimecorp_pvp
}

misc_roles = {
    role_slimernalia,
    role_gellphone
}

# used for checking if a user has the donor role
role_donor_proper = "Terezi Gang"

# used for checking if a user has the gellphone role
role_gellphone_proper = "Gellphone"

# Faction names and bases
faction_killers = "killers"
gangbase_killers = "Cop Killtown"
faction_rowdys = "rowdys"
gangbase_rowdys = "Rowdy Roughhouse"
faction_slimecorp = "slimecorp"
gangbase_slimecorp = "The Breakroom"
faction_banned = "banned"
factions = [faction_killers, faction_rowdys, faction_slimecorp]

# Channel names
channel_downtown = "downtown"
channel_vandalpark = "vandal-park"
channel_combatzone = "combat-zone"
channel_endlesswar = "endless-war"
channel_sewers = "the-sewers"
channel_dojo = "the-dojo"
channel_casino = "the-casino"
channel_casino_p ="slime-casino-lite"
channel_stockexchange = "slime-stock-exchange"
channel_stockexchange_p = "stock-exchange-portable"
channel_foodcourt = "food-court"
channel_slimeoidlab = "nlacu-labs"
channel_711 = "outside-the-7-11"
channel_speakeasy = "speakeasy"
channel_arena = "battle-arena"
channel_nlacu = "nlac-university"
channel_cinema = "nlacakanm-cinemas"
channel_bazaar = "bazaar"
channel_recyclingplant = "recycling-plant"
channel_slimecorphq = "slimecorp-hq"
channel_diner = "smokers-cough"
channel_seafood = "red-mobster"

channel_neomilwaukeestate = "neo-milwaukee-state"
channel_beachresort = "the-resort"
channel_countryclub = "the-country-club"
channel_rowdyroughhouse = "rowdy-roughhouse"
channel_copkilltown = "cop-killtown"
channel_slimesea = "slime-sea"
channel_juviesrow = "juvies-row"
channel_realestateagency = "real-estate-agency"
channel_sodafountain = "the-bicarbonate-soda-fountain"
channel_greencakecafe = "green-cake-cafe"
channel_glocksburycomics = "glocksbury-comics"
channel_breakroom = "the-breakroom"
channel_museum = "the-museum"

# Transport Channels #1
channel_wt_port = "wreckington-port"
channel_vc_port = "vagrants-corner-port"
channel_tt_subway_station = "toxington-subway-station"
channel_ah_subway_station = "astatine-heights-subway-station"
channel_gd_subway_station = "gatlingsdale-subway-station"
channel_ck_subway_station = "cop-killtown-subway-station"
channel_ab_subway_station = "arsonbrook-subway-station"
channel_sb_subway_station = "smogsburg-subway-station"
channel_dt_subway_station = "downtown-subway-station"
channel_kb_subway_station = "krak-bay-subway-station"
channel_gb_subway_station = "glocksbury-subway-station"
channel_wgb_subway_station = "west-glocksbury-subway-station"
channel_jp_subway_station = "jaywalker-plain-subway-station"
channel_nsb_subway_station = "north-sleeze-subway-station"
channel_ssb_subway_station = "south-sleeze-subway-station"
channel_cv_subway_station = "cratersville-subway-station"
channel_wt_subway_station = "wreckington-subway-station"
channel_rr_subway_station = "rowdy-roughhouse-subway-station"
channel_gld_subway_station = "green-light-subway-station"
channel_jr_subway_station = "juvies-row-subway-station"
channel_vc_subway_station = "vagrants-corner-subway-station"
channel_afb_subway_station = "assault-flats-subway-station"
channel_vp_subway_station = "vandal-park-subway-station"
channel_pa_subway_station = "poudrin-alley-subway-station"
channel_og_subway_station = "ooze-gardens-subway-station"
channel_cl_subway_station = "crookline-subway-station"
channel_lc_subway_station = "little-chernobyl-subway-station"
channel_bd_subway_station = "brawlden-subway-station"
channel_nny_subway_station = "new-new-yonkers-subway-station"
channel_df_blimp_tower = "dreadford-blimp-tower"
channel_afb_blimp_tower = "assault-flats-blimp-tower"

# Transport Channels #2
channel_ferry = "ferry"
channel_subway_pink01 = "subway-train-pink-01"
channel_subway_pink02 = "subway-train-pink-02"
channel_subway_gold01 = "subway-train-gold-01"
channel_subway_gold02 = "subway-train-gold-02"
channel_subway_green01 = "subway-train-green-01"
channel_subway_green02 = "subway-train-green-02"
channel_subway_black01 = "subway-train-black-01"
channel_subway_black02 = "subway-train-black-02"
channel_subway_purple01 = "subway-train-purple-01"
channel_subway_purple02 = "subway-train-purple-02"
channel_blimp = "blimp"

# Mining Channels
channel_mines = "the-mines"
channel_mines_sweeper = "the-mines-minesweeper"
channel_mines_bubble = "the-mines-bubble-breaker"
channel_cv_mines = "cratersville-mines"
channel_cv_mines_sweeper = "cratersville-mines-minesweeper"
channel_cv_mines_bubble = "cratersville-mines-bubble-breaker"
channel_tt_mines = "toxington-mines"
channel_tt_mines_sweeper = "toxington-mines-minesweeper"
channel_tt_mines_bubble = "toxington-mines-bubble-breaker"
channel_jrmineswall_sweeper = "the-mines-wall-minesweeper"
channel_ttmineswall_sweeper = "toxington-mines-wall-minesweeper"
channel_cvmineswall_sweeper = "cratersville-mines-wall-minesweeper"
channel_jrmineswall_bubble = "the-mines-wall-bubble-breaker"
channel_ttmineswall_bubble = "toxington-mines-wall-bubble-breaker"
channel_cvmineswall_bubble = "cratersville-mines-wall-bubble-breaker"

# Fishing Channels
channel_tt_pier = "toxington-pier"
channel_jp_pier = "jaywalker-plain-pier"
channel_cl_pier = "crookline-pier"
channel_afb_pier = "assault-flats-beach-pier"
channel_vc_pier = "vagrants-corner-pier"
channel_se_pier = "slimes-end-pier"
channel_jr_pier = "juvies-row-pier"

# Farming Channels
channel_jr_farms = "juvies-row-farms"
channel_og_farms = "ooze-gardens-farms"
channel_ab_farms = "arsonbrook-farms"

# Apartment channels
channel_apt = "apartment"
channel_apt_downtown = "downtown-apartments"
channel_apt_smogsburg = "smogsburg-apartments"
channel_apt_krakbay = "krak-bay-apartments"
channel_apt_poudrinalley = "poudrin-alley-apartments"
channel_apt_greenlightdistrict = "green-light-district-apartments"
channel_apt_oldnewyonkers = "old-new-yonkers-apartments"
channel_apt_littlechernobyl = "little-chernobyl-apartments"
channel_apt_arsonbrook = "arsonbrook-apartments"
channel_apt_astatineheights = "astatine-heights-apartments"
channel_apt_gatlingsdale = "gatlingsdale-apartments"
channel_apt_vandalpark = "vandal-park-apartments"
channel_apt_glocksbury = "glocksbury-apartments"
channel_apt_northsleezeborough = "north-sleezeborough-apartments"
channel_apt_southsleezeborough = "south-sleezeborough-apartments"
channel_apt_oozegardens = "ooze-gardens-apartments"
channel_apt_cratersville = "cratersville-apartments"
channel_apt_wreckington = "wreckington-apartments"
channel_apt_slimesend = "slimes-end-apartments"
channel_apt_vagrantscorner = "vagrants-corner-apartments"
channel_apt_assaultflatsbeach = "assault-flats-beach-apartments"
channel_apt_newnewyonkers = "new-new-yonkers-apartments"
channel_apt_brawlden = "brawlden-apartments"
channel_apt_toxington = "toxington-apartments"
channel_apt_charcoalpark = "charcoal-park-apartments"
channel_apt_poloniumhill = "polonium-hill-apartments"
channel_apt_westglocksbury = "west-glocksbury-apartments"
channel_apt_jaywalkerplain = "jaywalker-plain-apartments"
channel_apt_crookline = "crookline-apartments"
channel_apt_dreadford = "dreadford-apartments"
channel_apt_maimrdige = "maimridge-apartments"

channel_slimesendcliffs = "slimes-end-cliffs"
channel_bodega = "bodega"
channel_wafflehouse = "wafflehouse"
channel_blackpond = "blackpond"
channel_basedhardware = "based-hardware"
channel_clinicofslimoplasty = "clinic-of-slimoplasty"
channel_atomicforest = "atomic-forest"
channel_downpourlaboratory = "downpour-laboratory"

# Gang Violence Channels
channel_killercomms = "killer-comms"
channel_rowdycomms = "rowdy-comms"
channel_slimecorpcomms = "slimecorp-comms"
channel_losersclub = "the-losers-club"
channel_killfeed = "kill-feed"
channel_leaderboard = "leaderboard"
channel_slimefest = "slimefest"

# Gellphone Channels
channel_slimetwitter = "slime-twitter"
channel_slimecasinolite = "slime-casino-lite"
channel_sexportable = "stock-exchange-portable"
channel_squicklyleaks = "squicklyleaks"
channel_deviantsplaart = "deviant-splaart"
channel_splatify = "splatify"

# Exhibit Channels
channel_relicexhibits = "relic-exhibits"
channel_aquarium = "aquarium"
channel_artexhibits = "art-exhibits"

# Other
channel_communityservice = "community-service"

hideout_channels = [channel_rowdyroughhouse, channel_copkilltown, channel_breakroom]
hideout_by_faction = {
    faction_rowdys: channel_rowdyroughhouse,
    faction_killers: channel_copkilltown,
    faction_slimecorp: channel_breakroom
}

# Commands
cmd_prefix = '!'
cmd_enlist = cmd_prefix + 'enlist'
cmd_renounce = cmd_prefix + 'renounce'
cmd_revive = cmd_prefix + 'revive'
cmd_kill = cmd_prefix + 'kill'
cmd_shoot = cmd_prefix + 'shoot'
cmd_shoot_alt1 = cmd_prefix + 'bonk'
cmd_shoot_alt2 = cmd_prefix + 'pat'
cmd_shoot_alt3 = cmd_prefix + 'ban'
cmd_shoot_alt4 = cmd_prefix + 'pullthetrigger'
cmd_shoot_alt5 = cmd_prefix + 'curbstomp'
cmd_shoot_alt6 = cmd_prefix + 'hug'
cmd_shoot_alt7 = cmd_prefix + 'stab'
cmd_shoot_alt8 = cmd_prefix + 'murder'
cmd_shoot_alt9 = cmd_prefix + 'bust'
cmd_attack = cmd_prefix + 'attack'
cmd_reload = cmd_prefix + 'reload'
cmd_reload_alt1 = cmd_prefix + 'loadthegun'
cmd_devour = cmd_prefix + 'devour'
cmd_brace = cmd_prefix + 'brace'
cmd_facelift = cmd_prefix + 'facelift'
cmd_mine = cmd_prefix + 'mine'
cmd_digmine = cmd_prefix + 'dig'
cmd_hole = cmd_prefix + 'hole'
cmd_flag = cmd_prefix + 'flag'
cmd_score = cmd_prefix + 'slimes'
cmd_score_alt1 = cmd_prefix + 'slime'
cmd_score_alt2 = cmd_prefix + 'skune'
cmd_score_alt3 = cmd_prefix + 'sloim'
cmd_score_alt4 = cmd_prefix + '<:slimeepic:973836637777825864>'
cmd_giveslime = cmd_prefix + 'giveslime'
cmd_giveslime_alt1 = cmd_prefix + 'giveslimes'
cmd_help = cmd_prefix + 'help'
cmd_commands_alt1 = cmd_prefix + 'command'
cmd_commands = cmd_prefix + 'commands'
cmd_help_alt3 = cmd_prefix + 'guide'
cmd_harvest = cmd_prefix + 'harvest'
cmd_salute = cmd_prefix + 'salute'
cmd_unsalute = cmd_prefix + 'unsalute'
cmd_hurl = cmd_prefix + 'hurl'
cmd_spar = cmd_prefix + 'spar'
cmd_suicide = cmd_prefix + 'suicide'
cmd_suicide_alt1 = cmd_prefix + 'seppuku'
cmd_suicide_alt2 = cmd_prefix + 'sudoku'
cmd_haveastroke = cmd_prefix + 'haveastroke'
cmd_moonhurtingbeam = cmd_prefix + 'moonhurtingbeam'
cmd_haunt = cmd_prefix + 'haunt'
cmd_haunt_alt1 = cmd_prefix + 'curse'
cmd_haunt_alt2 = cmd_prefix + 'torment'
cmd_haunt_alt3 = cmd_prefix + 'scare'
cmd_haunt_alt4 = cmd_prefix + 'poltergeist'
cmd_haunt_alt5 = cmd_prefix + 'apparition'
cmd_haunt_alt6 = cmd_prefix + 'hex'
cmd_inhabit = cmd_prefix + 'inhabit'
cmd_inhabit_alt1 = cmd_prefix + 'dwell'
cmd_inhabit_alt2 = cmd_prefix + 'inspirit'
cmd_inhabit_alt3 = cmd_prefix + 'freeload'
cmd_letgo = cmd_prefix + 'letgo'
cmd_possess_weapon = cmd_prefix + 'possessweapon'
cmd_possess_weapon_alt1 = cmd_prefix + 'seizeweapon'
cmd_possess_weapon_alt2 = cmd_prefix + 'boostweapon'
cmd_possess_fishing_rod = cmd_prefix + 'possessfishingrod'
cmd_possess_fishing_rod_alt1 = cmd_prefix + 'possessrod'
cmd_possess_fishing_rod_alt2 = cmd_prefix + 'processrod'
cmd_possess_fishing_rod_alt3 = cmd_prefix + 'seizerod'
cmd_possess_fishing_rod_alt4 = cmd_prefix + 'boostrod'
cmd_unpossess_fishing_rod = cmd_prefix + 'unpossessfishingrod'
cmd_unpossess_fishing_rod_alt1 = cmd_prefix + 'unpossessrod'
cmd_unpossess_fishing_rod_alt2 = cmd_prefix + 'unpossess'
cmd_crystalize_negapoudrin = cmd_prefix + 'crystalizenegapoudrin'
cmd_crystalize_negapoudrin_alt1 = cmd_prefix + 'smeltnegapoudrin'
cmd_crystalize_negapoudrin_alt2 = cmd_prefix + 'crystallise'
cmd_crystalize_negapoudrin_alt3 = cmd_prefix + 'crystalize'
cmd_favor = cmd_prefix + 'favor'
cmd_summonenemy = cmd_prefix + 'summonenemy'
cmd_deleteallenemies = cmd_prefix + 'deleteallenemies'
cmd_battlenegaslimeoid = cmd_prefix + 'battlenegaslimeoid'
cmd_battlenegaslimeoid_alt1 = cmd_prefix + 'negaslimeoidbattle'
cmd_battlenegaslimeoid_alt2 = cmd_prefix + 'battlenega'
cmd_battlenegaslimeoid_alt3 = cmd_prefix + 'negabattle'
cmd_slimepachinko = cmd_prefix + 'slimepachinko'
cmd_slimepachinko_alt1 = cmd_prefix + 'pachinko'
cmd_slimeslots = cmd_prefix + 'slimeslots'
cmd_slimeslots_alt1 = cmd_prefix + 'slots'
cmd_slimecraps = cmd_prefix + 'slimecraps'
cmd_slimecraps_alt1 = cmd_prefix + 'craps'
cmd_slimeroulette = cmd_prefix + 'slimeroulette'
cmd_slimeroulette_alt1 = cmd_prefix + 'roulette'
cmd_slimebaccarat = cmd_prefix + 'slimebaccarat'
cmd_slimebaccarat_alt1 = cmd_prefix + 'baccarat'
cmd_slimeskat = cmd_prefix + 'slimeskat'
cmd_slimeskat_alt1 = cmd_prefix + 'skat'
cmd_slimeskat_join = cmd_prefix + 'skatjoin'
cmd_slimeskat_decline = cmd_prefix + 'skatdecline'
cmd_slimeskat_bid = cmd_prefix + 'skatbid'
cmd_slimeskat_call = cmd_prefix + 'skatcall'
cmd_slimeskat_pass = cmd_prefix + 'skatpass'
cmd_slimeskat_play = cmd_prefix + 'skatplay'
cmd_slimeskat_hearts = cmd_prefix + 'skathearts'
cmd_slimeskat_slugs = cmd_prefix + 'skatslugs'
cmd_slimeskat_hats = cmd_prefix + 'skathats'
cmd_slimeskat_shields = cmd_prefix + 'skatshields'
cmd_slimeskat_grand = cmd_prefix + 'skatgrand'
cmd_slimeskat_null = cmd_prefix + 'skatnull'
cmd_slimeskat_take = cmd_prefix + 'skattake'
cmd_slimeskat_hand = cmd_prefix + 'skathand'
cmd_slimeskat_choose = cmd_prefix + 'skatchoose'
cmd_deadmega = cmd_prefix + 'deadmega'
cmd_donate = cmd_prefix + 'donate'
cmd_slimecoin = cmd_prefix + 'slimecoin'
cmd_slimecoin_alt1 = cmd_prefix + 'slimecredit'
cmd_slimecoin_alt2 = cmd_prefix + 'coin'
cmd_slimecoin_alt3 = cmd_prefix + 'sc'
cmd_turnin = cmd_prefix + 'turnin'
cmd_crime = cmd_prefix + 'crime'
cmd_invest = cmd_prefix + 'invest'
cmd_withdraw = cmd_prefix + 'withdraw'
cmd_exchangerate = cmd_prefix + 'exchangerate'
cmd_exchangerate_alt1 = cmd_prefix + 'exchange'
cmd_exchangerate_alt2 = cmd_prefix + 'rate'
cmd_exchangerate_alt3 = cmd_prefix + 'exchangerates'
cmd_exchangerate_alt4 = cmd_prefix + 'rates'
cmd_shares = cmd_prefix + 'shares'
cmd_shares_alt1 = cmd_prefix + 'stonks'
cmd_stocks = cmd_prefix + 'stocks'
cmd_setstockvalue = cmd_prefix + 'setstockvalue'
cmd_setstockshares = cmd_prefix + 'setstockshares'
cmd_negapool = cmd_prefix + 'negapool'
cmd_negaslime = cmd_prefix + 'negaslime'
cmd_endlesswar = cmd_prefix + 'endlesswar'
cmd_swear_jar = cmd_prefix + 'swearjar'
cmd_equip = cmd_prefix + 'equip'
cmd_sidearm = cmd_prefix + 'sidearm'
cmd_data = cmd_prefix + 'data'
cmd_mutations = cmd_prefix + 'mutations'
cmd_mutations_alt_1 = cmd_prefix + 'stds'
cmd_mutations_alt_2 = cmd_prefix + 'stdz'
cmd_hunger = cmd_prefix + 'hunger'
cmd_clock = cmd_prefix + 'clock'
cmd_time = cmd_prefix + 'time'
cmd_weather = cmd_prefix + 'weather'
cmd_forecast = cmd_prefix + 'forecast'
cmd_forecast_alt1 = cmd_prefix + 'corecast'
cmd_patchnotes = cmd_prefix + 'patchnotes'
cmd_howl = cmd_prefix + 'howl'
cmd_howl_alt1 = cmd_prefix + '56709'
cmd_moan = cmd_prefix + 'moan'
cmd_transfer = cmd_prefix + 'transfer'
cmd_transfer_alt1 = cmd_prefix + 'xfer'
cmd_redeem = cmd_prefix + 'redeem'
cmd_menu = cmd_prefix + 'menu'
cmd_menu_alt1 = cmd_prefix + 'catalog'
cmd_menu_alt2 = cmd_prefix + 'catalogue'
cmd_order = cmd_prefix + 'order'
cmd_annoint = cmd_prefix + 'annoint'
cmd_annoint_alt1 = cmd_prefix + 'anoint'
cmd_crush = cmd_prefix + 'crush'
cmd_crush_alt1 = cmd_prefix + 'crunch'
cmd_disembody = cmd_prefix + 'disembody'
cmd_war = cmd_prefix + 'war'
cmd_toil = cmd_prefix + 'toil'
cmd_inventory = cmd_prefix + 'inventory'
cmd_inventory_alt1 = cmd_prefix + 'inv'
cmd_inventory_alt2 = cmd_prefix + 'stuff'
cmd_inventory_alt3 = cmd_prefix + 'bag'
cmd_communitychest = cmd_prefix + 'chest'
cmd_collectioninventory = cmd_prefix + 'contents'
cmd_move = cmd_prefix + 'move'
cmd_move_alt1 = cmd_prefix + 'goto'
cmd_move_alt2 = cmd_prefix + 'walk'
cmd_move_alt3 = cmd_prefix + 'sny'
cmd_move_alt4 = cmd_prefix + 'tiptoe'
cmd_move_alt5 = cmd_prefix + 'step'
cmd_move_alt6 = cmd_prefix + 'moonwalk'
cmd_descend = cmd_prefix + 'descend'
cmd_halt = cmd_prefix + 'halt'
cmd_halt_alt1 = cmd_prefix + 'stop'
cmd_embark = cmd_prefix + 'embark'
cmd_embark_alt1 = cmd_prefix + 'board'
cmd_disembark = cmd_prefix + 'disembark'
cmd_disembark_alt1 = cmd_prefix + 'alight'
cmd_checkschedule = cmd_prefix + 'schedule'
cmd_inspect = cmd_prefix + 'inspect'
cmd_inspect_alt1 = cmd_prefix + 'examine'
# cmd_plainlook = cmd_prefix + 'contents'
cmd_look = cmd_prefix + 'look'
cmd_survey = cmd_prefix + 'survey'
cmd_survey_alt1 = cmd_prefix + 'scan'
cmd_scout = cmd_prefix + 'scout'
cmd_scout_alt1 = cmd_prefix + 'sniff'
cmd_scrutinize = cmd_prefix + 'scrutinize'
cmd_map = cmd_prefix + 'map'
cmd_transportmap = cmd_prefix + 'transportmap'
cmd_transportmap_alt1 = cmd_prefix + 'transitmap'
cmd_wiki = cmd_prefix + 'wiki'
cmd_booru = cmd_prefix + 'booru'
cmd_bandcamp = cmd_prefix + 'bandcamp'
cmd_tutorial = cmd_prefix + 'tutorial'
cmd_pardon = cmd_prefix + 'pardon'
cmd_defect = cmd_prefix + 'defect'
cmd_banish = cmd_prefix + 'banish'
cmd_moveitem = cmd_prefix + 'moveitem'
cmd_vouch = cmd_prefix + 'vouch'
cmd_vote = cmd_prefix + 'vote'
cmd_hydraulicpress = cmd_prefix + 'hydraulicpress'
cmd_writhe = cmd_prefix + 'writhe'
cmd_use = cmd_prefix + 'use'
cmd_eat = cmd_prefix + 'eat'
cmd_eat_alt1 = cmd_prefix + 'chug'
cmd_news = cmd_prefix + 'news'
cmd_buy = cmd_prefix + 'buy'
cmd_thrash = cmd_prefix + 'thrash'
cmd_dab = cmd_prefix + 'dab'
cmd_boo = cmd_prefix + 'boo'
cmd_dance = cmd_prefix + 'dance'
cmd_dance_alt = cmd_prefix + 'vance'
cmd_propaganda = cmd_prefix + 'propaganda'
cmd_coinflip = cmd_prefix + 'co1nfl1p'
cmd_spook = cmd_prefix + 'spook'
cmd_sacrifice = cmd_prefix + 'sacrifice'
cmd_makecostume = cmd_prefix + 'makecostume'
cmd_rolldie = cmd_prefix + 'rolldie'
cmd_stunt = cmd_prefix + 'stunt'
cmd_stuntalt1 = cmd_prefix + 'skate'
cmd_stuntalt2 = cmd_prefix + 'sk8'
cmd_treat = cmd_prefix + 'treat'
cmd_russian = cmd_prefix + 'russianroulette'
cmd_duel = cmd_prefix + 'duel'
cmd_brandish = cmd_prefix + 'brandish'
cmd_accept = cmd_prefix + 'accept'
cmd_refuse = cmd_prefix + 'refuse'
cmd_sign = cmd_prefix + 'sign'
cmd_rip = cmd_prefix + 'rip'
cmd_yes = cmd_prefix + 'yes'
cmd_no = cmd_prefix + 'no'
cmd_reap = cmd_prefix + 'reap'
cmd_reap_alt = cmd_prefix + 'forcereap'
cmd_sow = cmd_prefix + 'sow'
cmd_check_farm = cmd_prefix + 'checkfarm'
cmd_irrigate = cmd_prefix + 'irrigate'
cmd_weed = cmd_prefix + 'weed'
cmd_bury = cmd_prefix + 'bury'
cmd_unearth = cmd_prefix + 'unearth'
cmd_fertilize = cmd_prefix + 'fertilize'
cmd_pesticide = cmd_prefix + 'pesticide'
cmd_mill = cmd_prefix + 'mill'
cmd_cast = cmd_prefix + 'cast'
cmd_reel = cmd_prefix + 'reel'
cmd_appraise = cmd_prefix + 'appraise'
cmd_barter = cmd_prefix + 'barter'
cmd_embiggen = cmd_prefix + 'embiggen'
cmd_barterall = cmd_prefix + 'barterall'
cmd_createfish = cmd_prefix + 'createfish'
cmd_adorn = cmd_prefix + 'adorn'
cmd_dedorn = cmd_prefix + 'dedorn'
cmd_dedorn_alt1 = cmd_prefix + 'unadorn'
cmd_dyecosmetic = cmd_prefix + 'dyecosmetic'
cmd_dyecosmetic_alt1 = cmd_prefix + 'dyehat'
cmd_dyecosmetic_alt2 = cmd_prefix + 'saturatecosmetic'
cmd_dyecosmetic_alt3 = cmd_prefix + 'saturatehat'
cmd_patterncosmetic = cmd_prefix + 'patterncosmetic'
cmd_patterncosmetic_alt1 = cmd_prefix + 'patternhat'
cmd_patterncosmetic_alt2 = cmd_prefix + 'pattern'
cmd_create = cmd_prefix + 'create'
cmd_forgemasterpoudrin = cmd_prefix + 'forgemasterpoudrin'
cmd_createitem = cmd_prefix + 'createitem'
cmd_createmulti = cmd_prefix + 'createmulti'
cmd_createall = cmd_prefix + 'createall'
cmd_manualsoulbind = cmd_prefix + 'soulbind'
cmd_editprops = cmd_prefix + 'editprops'
cmd_setslime = cmd_prefix + 'setslime'
cmd_seteventpoints = cmd_prefix + 'setresidue'
cmd_setfestivity = cmd_prefix + 'setfestivity'
cmd_checkstats = cmd_prefix + 'checkstats'
cmd_makebp = cmd_prefix + 'makebp'
cmd_exalt = cmd_prefix + 'exalt'
cmd_awardart = cmd_prefix + 'awardart'
cmd_createpoievent = cmd_prefix + 'createpoievent'
cmd_listworldevents = cmd_prefix + 'listworldevents'
cmd_listworldevents_alt1 = cmd_prefix + 'listworldevent'
cmd_endworldevent = cmd_prefix + 'endworldevent'
cmd_forcegraft = cmd_prefix + 'forcegraft'
cmd_forcechemo = cmd_prefix + 'forcechemo'
cmd_add_mut_rotation = cmd_prefix + 'addmutrotation'
cmd_clear_mut_rotation = cmd_prefix + 'clearmutrotation'
cmd_change_rotation_stat = cmd_prefix + 'changemutstat'
cmd_lockmutation = cmd_prefix + 'lockmutation'
cmd_unlockmutation = cmd_prefix + 'unlockmutation'
cmd_currentrotation = cmd_prefix + 'rotation'
cmd_nextrotation = cmd_prefix + 'nextrotation'
cmd_give = cmd_prefix + 'give'
cmd_discard = cmd_prefix + 'discard'
cmd_discard_alt1 = cmd_prefix + 'drop'
cmd_trash = cmd_prefix + 'trash'
cmd_leaderboard = cmd_prefix + 'leaderboard'
cmd_leaderboard_alt1 = cmd_prefix + 'leaderboards'
cmd_marry = cmd_prefix + 'marry'
cmd_divorce = cmd_prefix + 'divorce'
cmd_object = cmd_prefix + 'object'
cmd_object_alt1 = cmd_prefix + 'protest'
cmd_scavenge = cmd_prefix + 'scavenge'
cmd_scavenge_alt1 = cmd_prefix + 'lookbetweenthecushions'
cmd_scavenge_alt2 = cmd_prefix + 'dumpsterdive'
cmd_scavenge_alt3 = cmd_prefix + 'loot'
cmd_scavenge_alt4 = cmd_prefix + 'scav'
cmd_scrub = cmd_prefix + 'scrub'
cmd_question = cmd_prefix + 'question'
cmd_answer = cmd_prefix + 'answer'
cmd_arm = cmd_prefix + 'arm'
cmd_arsenalize = cmd_prefix + 'arsenalize'
cmd_spray = cmd_prefix + 'annex'
cmd_spray_alt1 = cmd_prefix + 'spray'
cmd_capture_progress = cmd_prefix + 'progress'
cmd_changespray = cmd_prefix + 'changespray'
cmd_changespray_alt1 = cmd_prefix + 'changetag'
cmd_tag = cmd_prefix + 'tag'
cmd_blockparty = cmd_prefix + 'blockparty'
cmd_hailcab = cmd_prefix + 'hailcab'
cmd_observe = cmd_prefix + 'observe'
cmd_launch  =cmd_prefix + 'launch'
cmd_land = cmd_prefix + 'land'
cmd_beammeup = cmd_prefix + 'beammeup'
cmd_abduct = cmd_prefix + 'abduct'
cmd_teleport = cmd_prefix + 'tp'
cmd_teleport_alt1 = cmd_prefix + 'blj'
cmd_teleport_player = cmd_prefix + 'tpp'
cmd_teleport_player_multi = cmd_prefix + 'tppmulti'
cmd_print_map_data = cmd_prefix + 'printmapdata'
cmd_ping_me = cmd_prefix + 'pingme'
cmd_boot = cmd_prefix + 'boot'
cmd_bootall = cmd_prefix + 'bootall'
cmd_quarterlyreport = cmd_prefix + 'quarterlyreport'
cmd_piss = cmd_prefix + 'piss'
cmd_fursuit = cmd_prefix + 'fursuit'
cmd_recycle = cmd_prefix + 'recycle'
cmd_fun = cmd_prefix + 'fun'
cmd_recycle_alt1 = cmd_prefix + 'incinerate'
cmd_harden_sap = cmd_prefix + 'harden'
cmd_harden_sap_alt1 = cmd_prefix + 'solidify'
cmd_liquefy_sap = cmd_prefix + 'liquefy'
cmd_dodge = cmd_prefix + 'dodge'
cmd_dodge_alt1 = cmd_prefix + 'evade'
cmd_dodge_alt2 = cmd_prefix + 'wavedash'
cmd_taunt = cmd_prefix + 'taunt'
cmd_aim = cmd_prefix + 'aim'
cmd_advertise = cmd_prefix + 'advertise'
cmd_ads = cmd_prefix + 'ads'
cmd_confirm = cmd_prefix + 'confirm'
cmd_cancel = cmd_prefix + 'cancel'
cmd_pray = cmd_prefix + 'pray'
cmd_flushsubzones = cmd_prefix + 'flushsubzones'
cmd_flushstreets = cmd_prefix + 'flushstreets'
cmd_flush = cmd_prefix + 'flush'
cmd_wrap = cmd_prefix + 'wrap'
cmd_unwrap = cmd_prefix + 'unwrap'
cmd_yoslimernalia = cmd_prefix + 'yoslimernalia'
cmd_festivitystage = cmd_prefix + 'festivitystage'
cmd_setfestivitystage = cmd_prefix + 'setfestivitystage'
cmd_announcefestivitystage = cmd_prefix + 'announcefestivitystage'
cmd_rejuvenate = cmd_prefix + 'rejuvenate'
cmd_goonscape_stats = cmd_prefix + 'stats'

cmd_win = cmd_prefix + 'win'
cmd_slimefest = cmd_prefix + 'slimefest'
cmd_identify = cmd_prefix + 'identify'
cmd_startshift = cmd_prefix + 'startshift'
cmd_serve = cmd_prefix + 'serve'
cmd_sow_cloth = cmd_prefix + 'sowcloth'
cmd_sow_cloth_alt1 = cmd_prefix + 'sewcloth'
cmd_sow_cloth_alt2 = cmd_prefix + 'sewfabric'
cmd_bespoke = cmd_prefix + "bespoke"
cmd_bespoke_alt1 = cmd_prefix + 'tailor'
cmd_restyle = cmd_prefix + "restyle"
cmd_restyle_alt1 = cmd_prefix + "stitch"

cmd_preserve = cmd_prefix + 'preserve'
cmd_stink = cmd_prefix + 'stink'
cmd_slap = cmd_prefix + 'slap'
cmd_track = cmd_prefix + 'track'
cmd_longdrop = cmd_prefix + 'longdrop'
cmd_shakeoff = cmd_prefix + 'shakeoff'
cmd_clench = cmd_prefix + 'clench'
cmd_thirdeye = cmd_prefix + 'thirdeye'
cmd_loop = cmd_prefix + 'loop'
cmd_loopdiagnostic = cmd_prefix + 'loopdiagnostic'
cmd_chemo = cmd_prefix + 'chemo'
cmd_graft = cmd_prefix + 'graft'
cmd_bleedout = cmd_prefix + 'bleedout'
cmd_skullbash = cmd_prefix + 'skullbash'
# cmd_juviemode = cmd_prefix + 'legallimit'
cmd_manual_unban = cmd_prefix + 'unban'
cmd_post_leaderboard = cmd_prefix + 'postleaderboard'

cmd_switch = cmd_prefix + 'switch'
cmd_switch_alt_1 = cmd_prefix + 's'

cmd_slimeball = cmd_prefix + 'slimeball'
cmd_slimeballgo = cmd_prefix + 'slimeballgo'
cmd_slimeballstop = cmd_prefix + 'slimeballstop'
cmd_slimeballleave = cmd_prefix + 'slimeballleave'
cmd_gambit = cmd_prefix + 'gambit'
cmd_credence = cmd_prefix + 'credence'
cmd_get_credence = cmd_prefix + 'getcredence'
cmd_reset_prank_stats = cmd_prefix + 'resetprankstats'
cmd_set_gambit = cmd_prefix + 'setgambit'
cmd_pointandlaugh = cmd_prefix + 'pointandlaugh'
cmd_prank = cmd_prefix + 'prank'
cmd_gvs_almanac = cmd_prefix + 'almanac'

cmd_retire = cmd_prefix + 'retire'
cmd_paspeaker = cmd_prefix + 'paspeaker'
cmd_depart = cmd_prefix + 'depart'
cmd_consult = cmd_prefix + 'consult'
cmd_sign_lease = cmd_prefix + 'signlease'
# cmd_rent_cycle = cmd_prefix + 'rentcycle'
cmd_fridge = cmd_prefix + 'fridge'
cmd_closet = cmd_prefix + 'closet'
cmd_store = cmd_prefix + 'stow'  # was originally !store, that honestly would be a easier command to remember
cmd_multistow = cmd_prefix + 'multistow'
cmd_unfridge = cmd_prefix + 'unfridge'
cmd_uncloset = cmd_prefix + 'uncloset'
cmd_take = cmd_prefix + 'snag'  # same as above, but with !take
cmd_multisnag = cmd_prefix + 'multisnag'
cmd_decorate = cmd_prefix + 'decorate'
cmd_undecorate = cmd_prefix + 'undecorate'
cmd_freeze = cmd_prefix + 'freeze'
cmd_unfreeze = cmd_prefix + 'unfreeze'
cmd_apartment = cmd_prefix + 'apartment'
cmd_apartment_alt = cmd_prefix + 'apt'
cmd_aptname = cmd_prefix + 'aptname'
cmd_aptdesc = cmd_prefix + 'aptdesc'
cmd_jeeves = cmd_prefix + 'jeeves'
cmd_upgrade = cmd_prefix + 'aptupgrade'  # do we need the apt at the beginning?
cmd_knock = cmd_prefix + 'knock'
cmd_trickortreat = cmd_prefix + 'trickortreat'
cmd_breaklease = cmd_prefix + 'breaklease'
cmd_aquarium = cmd_prefix + 'aquarium'
cmd_pot = cmd_prefix + 'pot'
cmd_propstand = cmd_prefix + 'propstand'
cmd_releaseprop = cmd_prefix + 'unstand'
cmd_releasefish = cmd_prefix + 'releasefish'
cmd_collect = cmd_prefix + 'collect'
cmd_extract = cmd_prefix + 'extract'
cmd_extract_alt_1 = cmd_prefix + 'uncollect'
cmd_renamecollection = cmd_prefix + 'renamecollection'
cmd_unpot = cmd_prefix + 'unpot'
cmd_wash = cmd_prefix + 'wash'
cmd_browse = cmd_prefix + 'browse'
cmd_smoke = cmd_prefix + 'smoke'
cmd_huff = cmd_prefix + 'huff'
cmd_vape = cmd_prefix + 'vape'
cmd_vapealt1 = cmd_prefix + 'oop'
cmd_frame = cmd_prefix + 'frame'
cmd_addart = cmd_prefix + 'addart'
cmd_extractsoul = cmd_prefix + 'extractsoul'
cmd_returnsoul = cmd_prefix + 'returnsoul'
cmd_squeeze = cmd_prefix + 'squeezesoul'
cmd_betsoul = cmd_prefix + 'betsoul'
cmd_buysoul = cmd_prefix + 'buysoul'
cmd_push = cmd_prefix + 'push'
cmd_push_alt_1 = cmd_prefix + 'bully'
cmd_push_alt_2 = cmd_prefix + 'troll'
cmd_jump = cmd_prefix + 'jump'
cmd_jump_alt1 = cmd_prefix + 'parkour'
cmd_toss = cmd_prefix + 'toss'
cmd_dyefurniture = cmd_prefix + 'dyefurniture'
cmd_watch = cmd_prefix + 'watch'
cmd_purify = cmd_prefix + 'purify'
cmd_shelve = cmd_prefix + 'shelve'
cmd_shelve_alt_1 = cmd_prefix + 'shelf'
cmd_unshelve = cmd_prefix + 'unshelve'
cmd_unshelve_alt_1 = cmd_prefix + 'unshelf'
cmd_addkey = cmd_prefix + 'addkey'
cmd_changelocks = cmd_prefix + 'changelocks'
cmd_setalarm = cmd_prefix + 'setalarm'
cmd_checkflag = cmd_prefix + 'checkflag'
cmd_jam = cmd_prefix + 'jam'
cmd_sew = cmd_prefix + 'sew'
cmd_retrofit = cmd_prefix + 'retrofit'
cmd_sip = cmd_prefix + 'sip'
cmd_fashion = cmd_prefix + 'fashion'
cmd_fashion_alt1 = cmd_prefix + 'drip'

cmd_zuck = cmd_prefix + 'zuck'

cmd_beginmanuscript = cmd_prefix + 'beginmanuscript'
cmd_beginmanuscript_alt_1 = cmd_prefix + 'createmanuscript'
cmd_beginmanuscript_alt_2 = cmd_prefix + 'startmanuscript'
cmd_setpenname = cmd_prefix + 'setpenname'
cmd_setpenname_alt_1 = cmd_prefix + 'setauthor'
cmd_settitle = cmd_prefix + 'settitle'
cmd_settitle_alt_1 = cmd_prefix + 'setname'
cmd_titleframe = cmd_prefix + 'titleframe'
cmd_setgenre = cmd_prefix + 'setgenre'
cmd_editpage = cmd_prefix + 'editpage'
cmd_viewpage = cmd_prefix + 'viewpage'
cmd_checkmanuscript = cmd_prefix + 'manuscript'
cmd_publishmanuscript = cmd_prefix + 'publish'
cmd_readbook = cmd_prefix + 'read'
cmd_nextpage = cmd_prefix + 'nextpage'
cmd_nextpage_alt_1 = cmd_prefix + 'flip'
cmd_previouspage = cmd_prefix + 'previouspage'
cmd_previouspage_alt_1 = cmd_prefix + 'pilf'
cmd_previouspage_alt_2 = cmd_prefix + 'plif'
cmd_browsezines = cmd_prefix + 'browse'
cmd_buyzine = cmd_prefix + 'buyzine'
cmd_buyzine_alt_1 = cmd_prefix + 'orderzine'
cmd_rate = cmd_prefix + 'ratezine'
cmd_rate_alt_1 = cmd_prefix + 'reviewzine'
cmd_rate_alt_2 = cmd_prefix + 'review'
cmd_setpages = cmd_prefix + 'setpages'
cmd_setpages_alt_1 = cmd_prefix + 'setpage'
cmd_setpages_alt_2 = cmd_prefix + 'setlength'
cmd_takedown = cmd_prefix + 'takedown'
cmd_takedown_alt_1 = cmd_prefix + 'copyrightstrike'
cmd_takedown_alt_2 = cmd_prefix + 'deletezine'
cmd_untakedown = cmd_prefix + 'untakedown'
cmd_untakedown_alt_1 = cmd_prefix + 'uncopyrightstrike'
cmd_untakedown_alt_2 = cmd_prefix + 'undeletezine'
cmd_lol = cmd_prefix + 'lol'
cmd_mastery = cmd_prefix + 'mastery'
cmd_trick = cmd_prefix + 'trick'


cmd_pacommand = cmd_prefix + 'pacommand'

cmd_surveil = cmd_prefix + 'surveil'


cmd_addblurb = cmd_prefix + 'addblurb'
cmd_displayblurbs = cmd_prefix + 'displayblurbs'
cmd_deleteblurb = cmd_prefix + 'deleteblurb'
cmd_blurbcontext = cmd_prefix + 'blurbcontext'

apartment_b_multiplier = 1500
apartment_a_multiplier = 2000000
apartment_dt_multiplier = 3000000000
apartment_s_multiplier = 6000000000

apartment_class_map = {
    "c": 1,
    "b": 1500,
    "a": 2000000,
    "s": 6000000000
}

apartment_classes = [*apartment_class_map.keys()]

soulprice = 500000000

tv_set_slime = 5000000
tv_set_level = 100

cmd_promote = cmd_prefix + 'promote'

cmd_arrest = cmd_prefix + 'arrest'
cmd_release = cmd_prefix + 'release'
cmd_balance_cosmetics = cmd_prefix + 'balancecosmetic'
cmd_release_alt1 = cmd_prefix + 'unarrest'
cmd_restoreroles = cmd_prefix + 'restoreroles'
cmd_hiderolenames = cmd_prefix + 'hiderolenames'
cmd_recreateroles = cmd_prefix + 'recreateroles'
cmd_deleteroles = cmd_prefix + 'deleteroles'
cmd_removeuseroverwrites = cmd_prefix + 'removeuseroverwrites'
cmd_collectopics = cmd_prefix + 'collecttopics'
cmd_synctopics = cmd_prefix + 'synctopics'
cmd_shutdownbot = cmd_prefix + 'shutdownbot'
cmd_checkbot = cmd_prefix + 'checkbot'
cmd_set_debug_option = cmd_prefix + 'debugoption'

cmd_reroll_mutation = cmd_prefix + 'rerollmutation'
cmd_clear_mutations = cmd_prefix + 'sterilizemutations'

cmd_smelt = cmd_prefix + 'smelt'
cmd_wcim = cmd_prefix + 'whatcanimake'
cmd_wcim_alt1 = cmd_prefix + 'wcim'
cmd_wcim_alt2 = cmd_prefix + 'whatmake'
cmd_wcim_alt3 = cmd_prefix + 'usedfor'

# slimeoid commands
cmd_incubateslimeoid = cmd_prefix + 'incubateslimeoid'
cmd_growbody = cmd_prefix + 'growbody'
cmd_growhead = cmd_prefix + 'growhead'
cmd_growlegs = cmd_prefix + 'growlegs'
cmd_growweapon = cmd_prefix + 'growweapon'
cmd_growarmor = cmd_prefix + 'growarmor'
cmd_growspecial = cmd_prefix + 'growspecial'
cmd_growbrain = cmd_prefix + 'growbrain'
cmd_nameslimeoid = cmd_prefix + 'nameslimeoid'
cmd_nameslimeoid_alt1 = cmd_prefix + 'namenegaslimeoid'
cmd_raisemoxie = cmd_prefix + 'raisemoxie'
cmd_lowermoxie = cmd_prefix + 'lowermoxie'
cmd_raisegrit = cmd_prefix + 'raisegrit'
cmd_lowergrit = cmd_prefix + 'lowergrit'
cmd_raisechutzpah = cmd_prefix + 'raisechutzpah'
cmd_lowerchutzpah = cmd_prefix + 'lowerchutzpah'
cmd_spawnslimeoid = cmd_prefix + 'spawnslimeoid'
cmd_spawnslimeoid_alt1 = cmd_prefix + 'spawnnegaslimeoid'
cmd_dissolveslimeoid = cmd_prefix + 'dissolveslimeoid'
cmd_dissolveslimeoid_alt1 = cmd_prefix + 'dissolvenegaslimeoid'
cmd_slimeoid = cmd_prefix + 'slimeoid'
cmd_slimeoid_alt1 = cmd_prefix + 'negaslimeoid'
cmd_challenge = cmd_prefix + 'challenge'
cmd_instructions = cmd_prefix + 'instructions'
cmd_playfetch = cmd_prefix + 'playfetch'
cmd_petslimeoid = cmd_prefix + 'petslimeoid'
cmd_petslimeoid_alt1 = cmd_prefix + 'petnegaslimeoid'
cmd_abuseslimeoid = cmd_prefix + 'abuseslimeoid'
cmd_abuseslimeoid_alt1 = cmd_prefix + 'abusenegaslimeoid'
cmd_walkslimeoid = cmd_prefix + 'walkslimeoid'
cmd_walkslimeoid_alt1 = cmd_prefix + 'walknegaslimeoid'
cmd_observeslimeoid = cmd_prefix + 'observeslimeoid'
cmd_observeslimeoid_alt1 = cmd_prefix + 'observenegaslimeoid'
cmd_slimeoidbattle = cmd_prefix + 'slimeoidbattle'
cmd_slimeoidbattle_alt1 = cmd_prefix + 'battleslimeoid'
cmd_slimeoidbattle_alt2 = cmd_prefix + 'negaslimeoidbattle'
cmd_slimeoidbattle_alt3 = cmd_prefix + 'battlenegaslimeoid'
cmd_slimeoidbattle_alt4 = cmd_prefix + 'slimeoidduel'
cmd_slimeoidbattle_alt5 = cmd_prefix + 'negaslimeoidduel'
cmd_saturateslimeoid = cmd_prefix + 'saturateslimeoid'
cmd_restoreslimeoid = cmd_prefix + 'restoreslimeoid'
cmd_restoreslimeoid_alt1 = cmd_prefix + 'restorenegaslimeoid'
cmd_bottleslimeoid = cmd_prefix + 'bottleslimeoid'
cmd_bottleslimeoid_alt1 = cmd_prefix + 'bottle'
cmd_unbottleslimeoid = cmd_prefix + 'unbottleslimeoid'
cmd_unbottleslimeoid_alt1 = cmd_prefix + 'unbottle'
cmd_feedslimeoid = cmd_prefix + 'feedslimeoid'
cmd_feedslimeoid_alt1 = cmd_prefix + 'feednegaslimeoid'
cmd_dress_slimeoid = cmd_prefix + 'dressslimeoid'
cmd_dress_slimeoid_alt1 = cmd_prefix + 'decorateslimeoid'
cmd_dress_slimeoid_alt2 = cmd_prefix + 'adornslimeoid'
cmd_dress_slimeoid_alt3 = cmd_prefix + 'dressnegaslimeoid'
cmd_dress_slimeoid_alt4 = cmd_prefix + 'decoratenegaslimeoid'
cmd_dress_slimeoid_alt5 = cmd_prefix + 'adornnegaslimeoid'
cmd_undress_slimeoid = cmd_prefix + 'undressslimeoid'
cmd_undress_slimeoid_alt1 = cmd_prefix + 'undecorateslimeoid'
cmd_undress_slimeoid_alt2 = cmd_prefix + 'unadornslimeoid'
cmd_undress_slimeoid_alt3 = cmd_prefix + 'undressnegaslimeoid'
cmd_undress_slimeoid_alt4 = cmd_prefix + 'undecoratenegaslimeoid'
cmd_undress_slimeoid_alt5 = cmd_prefix + 'unadornnegaslimeoid'
cmd_tagslimeoid = cmd_prefix + 'tagslimeoid'
cmd_tagslimeoid_alt1 = cmd_prefix + 'tagnegaslimeoid'
cmd_untagslimeoid = cmd_prefix + 'untagslimeoid'
cmd_untagslimeoid_alt1 = cmd_prefix + 'untagnegaslimeoid'

#negaslimeoid-specific commands
cmd_conjure_negaslimeoid = cmd_prefix + 'conjurenegaslimeoid'
cmd_conjure_negaslimeoid_alt1= cmd_prefix + 'summonnegaslimeoid'
cmd_conjure_negaslimeoid_alt2 = cmd_prefix + 'summonnega'
cmd_conjure_negaslimeoid_alt3 = cmd_prefix + 'summon'
cmd_destroyslimeoid = cmd_prefix + 'destroyslimeoid'
cmd_destroyslimeoid_alt1 = cmd_prefix + 'destroynegaslimeoid'

cmd_add_quadrant = cmd_prefix + "addquadrant"
cmd_clear_quadrant = cmd_prefix + "clearquadrant"
cmd_get_quadrants = cmd_prefix + "quadrants"
cmd_get_sloshed = cmd_prefix + "sloshed"
cmd_get_sloshed_alt1 = cmd_prefix + "soulvent"
cmd_get_roseate = cmd_prefix + "roseate"
cmd_get_roseate_alt1 = cmd_prefix + "bedenizen"
cmd_get_violacious = cmd_prefix + "violacious"
cmd_get_violacious_alt1 = cmd_prefix + "amaranthagonist"
cmd_get_policitous = cmd_prefix + "policitous"
cmd_get_policitous_alt1 = cmd_prefix + "arbitraitor"

cmd_trade = cmd_prefix + 'trade'
cmd_offer = cmd_prefix + 'offer'
cmd_remove_offer = cmd_prefix + 'removeoffer'
cmd_completetrade = cmd_prefix + 'completetrade'
cmd_canceltrade = cmd_prefix + 'canceltrade'

# Auction
cmd_bid = cmd_prefix + 'bid'
cmd_auction = cmd_prefix + 'auction'

cmd_bazaar_refresh = cmd_prefix + 'refreshbazaar'

cmd_cockdraw = cmd_prefix + 'cockdraw'
cmd_measurecock = cmd_prefix + 'measurecock'

cmd_windowshop = cmd_prefix + 'windowshop'

cmd_dual_key_ban = cmd_prefix + 'dualkeyban'
cmd_dual_key_ban_alt1 = cmd_prefix + 'dkb'
cmd_dual_key_release = cmd_prefix + 'dualkeyrelease'
cmd_dual_key_release_alt1 = cmd_prefix + 'dkr'

cmd_claim = cmd_prefix + 'claim'

# race
cmd_set_race = cmd_prefix + 'setrace'
cmd_set_race_alt1 = cmd_prefix + 'identifyas'
cmd_exist = cmd_prefix + 'exist'
cmd_ree = cmd_prefix + 'ree'
cmd_autocannibalize = cmd_prefix + 'autocannibalize'
cmd_autocannibalize_alt1 = cmd_prefix + 'eatself'
cmd_rattle = cmd_prefix + 'rattle'
cmd_bonejenga = cmd_prefix + 'bonejenga'
cmd_beep = cmd_prefix + 'beep'
cmd_yiff = cmd_prefix + 'yiff'
cmd_hiss = cmd_prefix + 'hiss'
cmd_jiggle = cmd_prefix + 'jiggle'
cmd_request_petting = cmd_prefix + 'requestpetting'
cmd_request_petting_alt1 = cmd_prefix + 'purr'
cmd_rampage = cmd_prefix + 'rampage'
cmd_flutter = cmd_prefix + 'flutter'
cmd_entomize = cmd_prefix + 'entomize'
cmd_confuse = cmd_prefix + 'confuse'
cmd_shamble = cmd_prefix + 'shamble'
cmd_netrun = cmd_prefix + 'netrun'
cmd_strike_deal = cmd_prefix + 'strikedeal'
cmd_honk = cmd_prefix + 'honk'

cmd_hogtie = cmd_prefix + 'hogtie'

# Slime Twitter
cmd_tweet = cmd_prefix + 'tweet'
cmd_qrt = cmd_prefix + 'quoteresplat'
cmd_qrt_alt1 = cmd_prefix + 'quoteretweet'
cmd_verification = cmd_prefix + 'requestverification'
cmd_verification_alt = cmd_prefix + '#verify'

# gamestate admin cmds
cmd_changegamestate = cmd_prefix + 'changegamestate'
cmd_deletegamestate = cmd_prefix + 'deletegamestate'
cmd_display_states = cmd_prefix + 'displaystates'
cmd_create_rally = cmd_prefix + 'createrally'
cmd_admintrack = cmd_prefix + 'admintrack'

# elevator cmds
cmd_press_button = cmd_prefix + 'press'
cmd_call_elevator = cmd_prefix + 'callelevator'

# admin checking cmds
cmd_addstatuseffect = cmd_prefix + 'addstatuseffect'
cmd_log_caches = cmd_prefix + 'cache'
cmd_toggle_caches = cmd_prefix + 'togglecache'
cmd_verify_cache = cmd_prefix + 'verifycache'
cmd_user_search = cmd_prefix + 'searchfor'

# SLIMERNALIA
cmd_festivity = cmd_prefix + 'festivity'

cmd_scrawl = cmd_prefix + 'scrawl'
cmd_strip = cmd_prefix + 'strip'


cmd_talk = cmd_prefix + 'talk'

cmd_clean_stats = cmd_prefix + 'cleanstats'


offline_cmds = [
    cmd_move,
    cmd_move_alt1,
    cmd_move_alt2,
    cmd_move_alt3,
    cmd_move_alt4,
    cmd_move_alt5,
    cmd_move_alt6,
    cmd_descend,
    cmd_halt,
    cmd_halt_alt1,
    cmd_embark,
    cmd_embark_alt1,
    cmd_disembark,
    cmd_disembark_alt1,
    cmd_look,
    cmd_survey,
    cmd_survey_alt1,
    cmd_scout,
    cmd_scout_alt1,
    cmd_depart,
    cmd_retire
    # cmd_scrutinize
]

client_debug_commands =[
 '!enemytick',
 '!releaseprisoners',
 '!createtestitem',
 '!createpoudrin',
 '!damage',
 '!getslime',
 '!getcoin',
 '!clearinv',
 '!createapple',
 '!weathertick',
 '!createhat',
 '!createfood',
 '!createdye',
 '!createoldhat',
 '!createoldscalp',
 '!createoldsoul',
 '!delete',
 '!setrole',
 '!getrowdy',
 '!getkiller',
 '!toggledownfall',
 '!dayforward',
 '!hourforward',
 '!postleaderboard',
 '!genslimeoid',
 '!massgenslimeoidnames',
 '!decaytick',
'!moverelics',
'!quickrevive']

# Maximum amount of slime juveniles can have before being killable
# max_safe_slime = 100000
# max_safe_level = 18

# Slime costs/values
slimes_onrevive = 20
slimes_onrevive_everyone = 20
slimes_toenlist = 0
slimes_perspar_base = 0
slimes_hauntratio = 1000
slimes_perslot = 100
slimes_perpachinko = 500
slimecoin_exchangerate = 1
slimes_permill = 50000
slimes_invein = 4000
slimes_pertile = 50
slimes_to_possess_weapon = -100000
slimes_to_possess_fishing_rod = -10000
slimes_to_crystalize_negapoudrin = -1000000
slimes_cliffdrop = 200000
slimes_item_drop = 10000
slimes_addart = 250000

# hunger
min_stamina = 100
hunger_pershot = 10
hunger_perspar = 10
hunger_perfarm = 50
hunger_permine = 1
hunger_perminereset = 30
hunger_perfish = 15
hunger_perscavenge = 2
hunger_pertick = 3
hunger_pertrickortreat = 6
hunger_perlmcollapse = 100

# Time it takes to move between various parts of the map
travel_time_subzone = 20
travel_time_district = 60
travel_time_street = 20
travel_time_outskirt = 60
travel_time_infinite = 900

# ads
slimecoin_toadvertise = 1000000
max_concurrent_ads = 8
max_length_ads = 500
uptime_ads = 7 * 24 * 60 * 60  # one week

time_bhbleed = 300  # 5 minutes

# currencies you can gamble at the casino
currency_slime = "slime"
currency_slimecoin = "SlimeCoin"
currency_soul = "soul"

global_slimegain_multiplier = 1.00
global_slimegain_multiplier_dt = {}
fishgain_multiplier = 1.00
fishgain_multiplier_dt = {}
minegain_multiplier = 1.00
minegain_multiplier_dt = {}
farmgain_multiplier = 1.00
farmgain_multiplier_dt = {}
#todo implement a sewer slime multiplier and a hunting yield multiplier too
global_damage_multiplier = 1.00
global_damage_multiplier_dt = {}


# inebriation
inebriation_max = 20
inebriation_pertick = 2

# max item amounts
max_food_in_inv_mod = 8  # modifier for how much food you can carry. the player's slime level is divided by this number to calculate the number of carriable food items
max_adornspace_mod = 8
max_weapon_mod = 16

# item acquisition methods
acquisition_smelting = "smelting"
acquisition_milling = "milling"
acquisition_mining = "mining"
acquisition_dojo = "dojo"
acquisition_fishing = "fishing"
acquisition_bartering = "bartering"
acquisition_trickortreating = "trickortreating"
acquisition_bazaar = "bazaar"
acquisition_huntingtrophy = "huntingtrophy"
acquisition_commongumball = "commongumball"
acquisition_uncommongumball = "uncommongumball"
acquisition_raregumball = "raregumball"
acquisition_superraregumball = "superraregumball"

# All the different gumball acquisition types
gumball_acquisitions = [acquisition_commongumball, acquisition_uncommongumball, acquisition_raregumball, acquisition_superraregumball]

# standard food expiration in seconds
std_food_expir = 12 * 3600  # 12 hours
farm_food_expir = 12 * 3600 * 4  # 2 days
milled_food_expir = 12 * 3600 * 28  # 2 weeks

horseman_death_cooldown = 12 * 3600 * 4  # 2 days

# amount of slime you get from crushing a poudrin
crush_slimes = 10000

# minimum amount of slime needed to capture territory
min_slime_to_cap = 200000

# property classes
property_class_s = "s"
property_class_a = "a"
property_class_b = "b"
property_class_c = "c"

apt_storage_base = 4

# Thar we go
cmd_to_apt_dest = {
    cmd_fridge: compartment_id_fridge,
    cmd_store: "store",
    cmd_closet: compartment_id_closet,
    cmd_decorate: compartment_id_decorate,
    cmd_shelve: compartment_id_bookshelf,
    cmd_shelve_alt_1: compartment_id_bookshelf
}

# district capturing
capture_tick_length = 10  # in seconds; also affects how much progress is made per tick
max_capture_points_s = 13105  # 4 hours
max_capture_points_a = 6553  # 2 hours
max_capture_points_b = 3277  # 1 hour
max_capture_points_c = 1638  # 30 minutes

crime_yield_s = 1000
crime_yield_a = 500
crime_yield_b = 200
crime_yield_c = 100

min_garotte = 2000

# district capture rates assigned to property classes
max_capture_points = {
    property_class_s: max_capture_points_s,
    property_class_a: max_capture_points_a,
    property_class_b: max_capture_points_b,
    property_class_c: max_capture_points_c
}

crime_yield_capping = {
    property_class_s: crime_yield_s,
    property_class_a: crime_yield_a,
    property_class_b: crime_yield_b,
    property_class_c: crime_yield_c
}


# by how much to extend the capture lock per additional gangster capping
capture_lock_per_gangster = 60 * 60  # 60 min

# capture lock messages
capture_lock_milestone = 15 * 60  # 5 min

# capture messages
capture_milestone = 5  # after how many percent of progress the players are notified of the progress

# capture speed at 0% progress
baseline_capture_speed = 1

# accelerates capture speed depending on current progress
capture_gradient = 1

# district de-capturing
decapture_speed_multiplier = 1  # how much faster de-capturing is than capturing

# district control decay
decay_modifier = 4  # more means slower

# time values
seconds_per_ingame_day = 21600
ticks_per_day = seconds_per_ingame_day / update_market  # how often the kingpins receive slime per in-game day

# kingpin district control slime yields (per tick, i.e. in-game-hourly)
slime_yield_class_s = int(60000 / ticks_per_day)  # dividing the daily amount by the amount of method calls per day
slime_yield_class_a = int(40000 / ticks_per_day)
slime_yield_class_b = int(30000 / ticks_per_day)
slime_yield_class_c = int(20000 / ticks_per_day)

# district control slime yields assigned to property classes
district_control_slime_yields = {
    property_class_s: slime_yield_class_s,
    property_class_a: slime_yield_class_a,
    property_class_b: slime_yield_class_b,
    property_class_c: slime_yield_class_c
}

# Slime decay rate
slime_half_life = 60 * 60 * 24 * 14  # two weeks

# Rate of bleeding stored damage into the environment
bleed_half_life = 60 * 5  # five minutes

# how often to bleed
bleed_tick_length = 10

# how often to decide whether or not to spawn an enemy
enemy_spawn_tick_length = 60 * 3 # Three minutes
# enemy_spawn_tick_length = 5
# enemy_spawn_tick_length = 30
# how often it takes for hostile enemies to attack
enemy_attack_tick_length = 5

# how often to burn
burn_tick_length = 4

# how often to check for statuses to be removed
removestatus_tick_length = 5

# Unearthed Item rarity (for enlisted players)
unearthed_item_rarity = 1500

# Chance to loot an item while scavenging
scavenge_item_rarity = 1000

# Lifetimes
invuln_onrevive = 0

#crime rates, lol
cr_murder_points = 500
cr_assault_points = 75
cr_vandalism_points = 100
cr_arson_points = 600
cr_cop_kill = 650
cr_larceny_points = 1
cr_underage_drinking_points = 1
cr_littering_points = 1
cr_posession_points = 5
cr_underage_smoking_points = 1
cr_dojo_crime_points = 50
cr_indecent_exposure_points = 1
cr_unlawful_stunting = 1


crime_status = {
0:"{their} record is spotless.",
1:"{they} have stepped over the line to vaguely uncouth behavior, but {they}'re still the pussy {they}'ve always been.",
5:"{they} appear to be trying to appear \"hard\". Oh, how {they} have failed.",
20:"{they}'re still a civilian, basically, {they}'ve just tried a few things once.",
100:"Most gangsters would eat {them} for breakfast.",
1000:"{they}'re a hardened criminal by anywhere else's standards, but {they} decided to squat down here. {they}'re still in diapers, honestly.",
5000:"{they}'ve ravaged the streets hard enough to be called a rookie.",
10000:"{their} bloodlust and debauchery have caused the police to view {them} as a wild and dangerous threat.",
25000:"{their} boundless malice has risen above the average gangster, which has placed {them} on many watchlists.",
50000:"The remnants of the police lose sleep over {them} every night.",
250000:"{they}'re a veteran of war, and all those around {them} see the undying chaos in {their} eyes and in {their} soul.",
500000: "The civilians who see {their} face believe {them} to be a plague incarnate. Maybe they're right.",
1000000:"Not even {their} fellow gangsters can tolerate the sight of {them} now. {their} voice is spun of poison and {their} footsteps leave destruction in {their} wake. Fucking goons."
}

#if a profile image is absent, this is used
default_thumbnail = "https://yt3.ggpht.com/ytc/AKedOLQCV-tLjbp8R3Ua3-NYtax1F_T86YzV14UY16cHhQ=s900-c-k-c0x00ffffff-no-rj"

# how often to apply weather effects
weather_tick_length = 10

# moon phase string names
moon_new = "new" #
moon_waxing_start = "waxinghorns" #       :
moon_waxing_end = "waxingmandibles" #          (:
moon_full = "crescent" #                ((:
moon_waning_start = "waningmaw" # ((
moon_waning_end = "waningsliver" #      (
moon_special = "green" #               glows

#enemy count limits
max_npcs = 20
max_normal_enemies = 500
# strength of the burn applied every weather tick by firestorms
firestorm_slime_burn = 100000

# how often to delete expired world events
event_tick_length = 5

# slimeball tick length
slimeball_tick_length = 5

# farming
crops_time_to_grow = 180  # in minutes; 180 minutes are 3 hours
reap_gain = 100000
farm_slimes_peraction = 25000
time_nextphase = 20 * 60  # 20 minutes
time_lastphase_juvie = 10 * 60  # 10 minutes
farm_tick_length = 60  # 1 minute

farm_phase_sow = 0
farm_phase_reap = 9
farm_phase_reap_juvie = 5

farm_action_none = 0
farm_action_water = 1
farm_action_fertilize = 2
farm_action_weed = 3
farm_action_pesticide = 4

# fishing
fish_gain = 10000  # multiplied by fish size class
fish_offer_timeout = 1440  # in minutes; 24 hours

# Cooldowns
cd_kill = 5
cd_spar = 60
cd_haunt = 600
cd_squeeze = 1200
cd_invest = 5 * 60
cd_boombust = 22
# For possible time limit on russian roulette
cd_rr = 600
# slimeoid downtime after a defeat
cd_slimeoiddefeated = 300
cd_scavenge = 0
soft_cd_scavenge = 15  # Soft cooldown on scavenging
cd_enlist = 60
cd_premium_purchase = 2 * 24 * 60 * 60  # 48 Hours, 2 days
cd_new_player = 3 * 24 * 60 * 60  # 72 Hours, 3 days

cd_autocannibalize = 60 * 60  # can only eat yourself once per hour
cd_drop_bone = 5 * 60
cd_change_race = 24 * 60 * 60  # can only change your race once per day

# in relation to time of death
time_to_manifest = 24 * 60 * 60  # a day

# time to get kicked out of subzone.
time_kickout = 60 * 60  # 1 hour

# For SWILLDERMUK, this is used to prevent AFK people from being pranked.
time_afk_swilldermuk = 60 * 60 * 2  # 1 hours

# time after coming online before you can act
time_offline = 5

# time for an enemy to despawn
time_despawn = 60 * 60 * 12  # 12 hours

# time for a player to be targeted by an enemy after entering a district
time_enemyaggro = 5

# time for a raid boss to target a player after moving to a new district
time_raidbossaggro = 3

# time for a raid boss to activate
time_raidcountdown = 60

# time for a raid boss to stay in a district before it can move again
time_raidboss_movecooldown = 2.5 * 60

# maximum amount of enemies a district can hold before it stops spawning them
max_enemies = 5

#The current curator
current_curator = random.choice(["amy", "curator"])

# response string used to let attack function in ewwep know that an enemy is being attacked
enemy_targeted_string = "ENEMY-TARGETED"

# Response string used to signal ghostbusting
ghost_busting_string = "BUSTING-MAKES-ME-FEEL-GOOD"

# Wiki link base url
wiki_baseurl = "https://rfck.miraheze.org/wiki/"

# Emotes
emote_tacobell = "<:tacobell:431273890195570699>"
emote_pizzahut = "<:pizzahut:431273890355085323>"
emote_kfc = "<:kfc:431273890216673281>"
emote_moon = "<:moon:499614945609252865>"
emote_111 = "<:111:431547758181220377>"
emote_111_debug = "<:111:720412882143150241>"

emote_copkiller = "<:copkiller:431275071945048075>"
emote_rowdyfucker = "<:rowdyfucker:431275088076079105>"
emote_ck = "<:ck:504173691488305152>"
emote_rf = "<:rf:504174176656162816>"

emote_theeye = "<:theeye:431429098909466634>"
emote_slime1 = "<:slime1:431564830541873182>"
emote_slime2 = "<:slime2:431570132901560320>"
emote_slime3 = "<:slime3:431659469844381717>"
emote_slime4 = "<:slime4:431570132901560320>"
emote_slime5 = "<:slime5:431659469844381717>"
emote_slimeskull = "<:slimeskull:431670526621122562>"
emote_slimeheart = "<:slimeheart:431673472687669248>"
emote_dice1 = "<:dice1:436942524385329162>"
emote_dice2 = "<:dice2:436942524389654538>"
emote_dice3 = "<:dice3:436942524041527298>"
emote_dice4 = "<:dice4:436942524406300683>"
emote_dice5 = "<:dice5:436942524444049408>"
emote_dice6 = "<:dice6:436942524469346334>"
emote_dice_rolling = "<a:diceroll:1086894063267102750>"
emote_negaslime = "<:ns:453826200616566786>"
emote_bustin = "<:bustin:455194248741126144>"
emote_ghost = "<:lordofghosts:434002083256205314>"
# emote_slimefull = "<:slimefull:496397819154923553>" # Removed
# emote_purple = "<:purple:496397848343216138>" # Removed
# emote_pink = "<:pink:496397871180939294>" # Removed
emote_slimecoin = "<:slimecoin:440576133214240769>"
emote_slimegun = "<:slimegun:436500203743477760>"
emote_slimeshot = "<:slimeshot:436604890928644106>"
emote_slimecorp = "<:slimecorp:568637591847698432>"
emote_nlacakanm = "<:nlacakanm:499615025544298517>"
emote_megaslime = "<:megaslime:436877747240042508>"
emote_srs = "<:srs:631859962519224341>"
emote_staydead = "<:sd:506840095714836480>"
emote_janus1 = "<:janus1:694404178956779592>"
emote_janus2 = "<:janus2:694404179342655518>"
# emote_masterpoudrin = "<:masterpoudrin:694788959418712114>" # Removed
# emote_blankregional = "<:bl:747207921926144081>" # Removed
# emote_greenlawn = "<:gr:726271625489809411>" # Removed
emote_limelawn = "<:li:726271664815472692>"
# emote_frozentile = "<:ft:743276248381259846>" # Removed

# Emotes for crops
emote_poketubers = "<:c_poketubers:1026711024881119252>"
emote_pulpgourds = "<:c_pulpgourds:1026711026290405376>"
emote_sourpotatoes = "<:c_sourpotatoes:1026711035794706462>"
emote_bloodcabbages = "<:c_bloodcabbage:1026711005700554762>"
emote_joybeans = "<:c_joybeans:1026711013518737468>"
emote_killiflower = "<:c_purplekilliflower:1026711028341415986>"
emote_razornuts = "<:c_razornuts:1026711030941880421>"
emote_pawpaw = "<:c_pawpaw:1026711019533381663>"
emote_sludgeberries = "<:c_sludgeberries:1026711034272157747>"
emote_suganmanuts = "<:c_suganmanuts:1026711038692954113>"
emote_pinkrowddishes = "<:c_pinkrowddishes:1026711022771388416>"
emote_dankwheat = "<:c_dankwheat:1026711009945190410>"
emote_brightshade = "<:c_brightshade:1026711007592198224>"
emote_blacklimes = "<:c_blacklimes:1026711004161253377>"    
emote_phosphorpoppies = "<:c_phosphorpoppies:1026711021034938388>"
emote_direapples = "<:c_direapple:1026711011853619241>"
emote_rustealeaves = "<:c_rustealeaves:1026711032699297812>"
emote_metallicaps = "<:c_metallicaps:1026711015066435664>"
emote_steelbeans = "<:c_steelbeans:1026711037220769822>"
emote_aushucks = "<:c_aushucks:1026711001795661886>"
emote_partypoppeppers = "<:c_partypoppeppers:1026711016949686283>"

# Emotes for moon phases
emote_moon_green = "<:moongreen:1026709273843089490> "
emote_moon_waxinghorns = "<:moonwaxinghorns:1026709279857709097> "
emote_moon_waxingmandibles = "<:moonwaxingmandibles:1026709282374303805>"
emote_moon_waningmaw = "<:moonwaningmaw:1026709276514857031> "
emote_moon_waningsliver = "<:moonwaningsliver:1026709278096101406>"

# Emotes for the negaslime writhe animation - all but blank removed
emote_vt = "<:vt:492067858160025600>"
emote_ve = "<:ve:492067844930928641>"
emote_va = "<:va:492067850878451724>"
emote_v_ = "<:v_:492067837565861889>"
emote_s_ = "<:s_:492067830624157708>"
emote_ht = "<:ht:492067823150039063>"
emote_hs = "<:hs:492067783396294658>"
emote_he = "<:he:492067814933266443>"
emote_h_ = "<:h_:492067806465228811>"
emote_blank = "<:blank:570060211327336472>"

# Emotes for troll romance
emote_maws = "<:q_maws:752228834027241554>"
emote_hats = "<:q_hats:752228833968783441>"
emote_slugs = "<:q_slugs:752228834333556756>"
emote_shields = "<:q_shields:752228833897218159>"
emote_broken_heart = ":broken_heart:"

# Emotes for minesweeper - all unused
emote_ms_hidden = ":pick:"
emote_ms_mine = ":x:"
emote_ms_flagged = ":triangular_flag_on_post:"
emote_ms_0 = ":white_circle:"
emote_ms_1 = ":heart:"
emote_ms_2 = ":yellow_heart:"
emote_ms_3 = ":green_heart:"
emote_ms_4 = ":blue_heart:"
emote_ms_5 = ":purple_heart:"
emote_ms_6 = ":six:"
emote_ms_7 = ":seven:"
emote_ms_8 = ":eight:"

# Emotes for Bubblebreaker - all unused. Can't do custom emotes emotes sadly (crops), message becomes too long to be sent as 1
emote_bb_empty = "➰"
emote_bb_0 = "🍍"
emote_bb_1 = "🍓"
emote_bb_2 = "🍇"
emote_bb_3 = "🥑"
emote_bb_4 = "🫐"
emote_bb_glob = "🥭"  

# Emote for poudrin
emote_poudrin = "<:poudrin:638900988560015400>"

# Emotes for Slime Twitter & debugging
emote_slimetwitter_like = "<:slimetwitterlike:822277824324960266>"
emote_slimetwitter_resplat = "<:slimeresplat:822277898102112297>"
emote_slimetwitter_like_debug = "💚"
emote_slimetwitter_resplat_debug = "♻️"

# Emote for deleting slime tweets
emote_delete_tweet = emote_blank
# Slime twitter verified checkmark
emote_verified = "<:slime_checkmark:797234128398319626>"

# Emotes for !thrash, !dab and !boo variants
emote_benkart = "<a:benkart:644520407734550529>"
emote_munchykart = "<a:munchykart:644520408002854913>"
emote_taasenchamp = "<:TaasenChamp:804369420583567392>"
emote_freaker = "<a:FREAKER:638902310814220296>"
emote_hellaben = "<:hellaben:431418525530456064>"
emote_sweetmunch = "<:sweetmunch:431418525593108490>"
emote_phantomhorn = "<:phantomhorn:431282111534858244>"
emote_strawberrymilk = "<:strawberrymilk:431282128421126144>"
emote_dab = "<a:dab:805341290220093450>"
emote_thrash = "<a:thrash:805341344331202620>"
emote_benwtf = "<:benwtf:981830620080635914>"
emote_gcool = "<:ghostcool:985321953218945075>"
emote_nslog = "<:negalog:698581983537922189>"
emote_invsrs = "<:srs_invert:657793228673646612>"
emote_nega111 = "<:nega111:638907899778695188>"

# Miscellaneous
emote_tfwslime = "<:tfwslime:713609663832391680>"
emote_ewspin = "<a:ewspin:694097283293118525>"
emote_slimeepic = "<:slimeepic:973836637777825864>"



# Lists for randomly chosen !dab and !thrash emotes
dab_emotes = [
emote_copkiller,
emote_benkart,
emote_taasenchamp,
emote_hellaben,
emote_phantomhorn,
emote_dab,
emote_benwtf
]

thrash_emotes = [
emote_rowdyfucker,
emote_munchykart,
emote_freaker,
emote_sweetmunch,
emote_strawberrymilk,
emote_thrash
]

boo_emotes = [
emote_moon,
emote_ghost,
emote_gcool,
emote_nslog,
emote_invsrs,
emote_nega111
]

# Dice emote list
emotes_dice = [
emote_dice1,
emote_dice2,
emote_dice3,
emote_dice4,
emote_dice5,
emote_dice6
]

# mining types
mining_type_minesweeper = "minesweeper"
mining_type_pokemine = "pokemine"
mining_type_bubblebreaker = "bubblebreaker"

# mining grid types
mine_grid_type_minesweeper = "minesweeper"
mine_grid_type_pokemine = "pokemining"
mine_grid_type_bubblebreaker = "bubblebreaker"

grid_type_by_mining_type = {
    mining_type_minesweeper: mine_grid_type_minesweeper,
    mining_type_pokemine: mine_grid_type_pokemine,
    mining_type_bubblebreaker: mine_grid_type_bubblebreaker,
}

# mining sweeper
cell_mine = 1
cell_mine_marked = 2
cell_mine_open = 3

cell_empty = -1
cell_empty_marked = -2
cell_empty_open = -3

cell_slime = 0

# bubble breaker
cell_bubble_empty = "0"
cell_bubble_0 = "5"
cell_bubble_1 = "1"
cell_bubble_2 = "2"
cell_bubble_3 = "3"
cell_bubble_4 = "4"
cell_bubble_glob = "⋆"

bubble_emote_map = {
    cell_bubble_empty: emote_bb_empty,
    cell_bubble_0: emote_bb_0,
    cell_bubble_1: emote_bb_1,
    cell_bubble_2: emote_bb_2,
    cell_bubble_3: emote_bb_3,
    cell_bubble_4: emote_bb_4,
    cell_bubble_glob: emote_bb_glob,
}

# first letter of each fruit
letter_to_cell = {
    "p": "5",
    "s": "1",
    "g": "2",
    "a": "3",
    "b": "4",
}

cell_bubbles = [
    cell_bubble_0,
    cell_bubble_1,
    cell_bubble_2,
    cell_bubble_3,
    cell_bubble_4
]

bubbles_to_burst = 4

symbol_map_ms = {
    -1: "/",
    1: "/",
    -2: "+",
    2: "+",
    3: "X"
}

number_emote_map = {
    0: emote_ms_0,
    1: emote_ms_1,
    2: emote_ms_2,
    3: emote_ms_3,
    4: emote_ms_4,
    5: emote_ms_5,
    6: emote_ms_6,
    7: emote_ms_7,
    8: emote_ms_8
}

alphabet = "abcdefghijklmnopqrstuvwxyz"

# map of mines and their respective wall
mines_wall_map = {
    poi_id_mine_sweeper: channel_jrmineswall_sweeper,
    poi_id_tt_mines_sweeper: channel_ttmineswall_sweeper,
    poi_id_cv_mines_sweeper: channel_cvmineswall_sweeper,
    poi_id_mine_bubble: channel_jrmineswall_bubble,
    poi_id_tt_mines_bubble: channel_ttmineswall_bubble,
    poi_id_cv_mines_bubble: channel_cvmineswall_bubble
}

# map of mines and the type of mining done in them
mines_mining_type_map = {
    poi_id_mine_sweeper: mining_type_minesweeper,
    poi_id_cv_mines_sweeper: mining_type_minesweeper,
    poi_id_tt_mines_sweeper: mining_type_minesweeper,
    poi_id_mine_bubble: mining_type_bubblebreaker,
    poi_id_cv_mines_bubble: mining_type_bubblebreaker,
    poi_id_tt_mines_bubble: mining_type_bubblebreaker
}

# list of channels you can !mine in
mining_channels = [
    channel_mines,
    channel_mines_sweeper,
    channel_mines_bubble,
    channel_cv_mines,
    channel_cv_mines_sweeper,
    channel_cv_mines_bubble,
    channel_tt_mines,
    channel_tt_mines_sweeper,
    channel_tt_mines_bubble
]

# trading
trade_state_proposed = 0
trade_state_ongoing = 1
trade_state_complete = 2

# SLIMERNALIA
festivity_gift_wrap = 100 # How much festivity is rewarded for wrapping / unwrapping a present
festivity_gift_base = 1000 # How much festivity a basic gift is worth
festivity_gift_food = 1 # How much festivity is given per ten points of hunger restored by the food
festivity_gift_weapon = 100 # How much festivity is given per kill on a weapon
festivity_gift_cosmetic = 10 # How much festivity is given per freshness on a cosmetic
festivity_gift_max = 10000 # How much festivity you can gain in a single gift or feasting
festivity_dye_bonus = 500 # Bonus for dyeing a gifted cosmetic
festivity_scrawl_bonus = 100 # Bonus for scrawling on a gift
festivity_name_bonus = 100 # Bonus for naming a weapon gift
festivity_smelt_bonus = 500 # Bonus for gifting something handmade
festivity_pleb_bonus = 10 # Bonus for plebeian tier gifts
festivity_patr_bonus = 100 # Bonus for patrician tier gifts
festivity_othr_bonus = 600 # Bonus for any other tier gifts

festivity_kill_bonus = 1500 # The  amount of festivity you gain upon killing someone

festivity_expired_penalty = 2500 # Penalty if the food item you are giving has already expired
festivity_generic_penality = 500 # Penality if the item is something generic

phoebus_bet_floor = 1000000 # How high a slime bet needs to be to get the Phoebus' Blessing bonus

slimernalia_kingpin_announcement = "**HARK!** I, Phoebus do hereby crown <{player}> as today's Kingpin of Slimernalia! <{player}> gained a total of **{festivity}** festivity!"

event_stage_announcements = [
    "HAHA! DO !POINTANDLAUGH @<EVENT ORGANIZER> FOR NOT SETTING THESE ANNOUNCEMENTS UP.",
    "DO NOT GET YOUR HOPES UP.",
    "REMEMBER TO KILL EACH OTHER."
] # Search "event_stage" to get an idea.

# Common strings.
str_casino_closed = "The Casino only operates at night."
str_casino_negaslime_dealer = "\"We don't deal with negaslime around here.\", says the dealer disdainfully."
str_casino_negaslime_machine = "The machine doesn't seem to accept antislime."
str_exchange_closed = "The Exchange has closed for the night."
str_exchange_specify = "Specify how much {currency} you will {action}."
str_exchange_channelreq = "You must go to the #" + channel_stockexchange + " in person to {action} your {currency}."
str_exchange_busy = "You can't {action} right now. Your slimebroker is busy."
str_weapon_wielding_self = "You are wielding"
str_weapon_wielding = "They are wielding"
str_weapon_married_self = "You are married to"
str_weapon_married = "They are married to"
str_eat_raw_material = "You chomp into the raw {}. It isn't terrible, but you feel like there is a more constructive use for it."
str_generic_onadorn = "You successfully adorn your {}."
str_generic_unadorn = "You successfully dedorn your {}."
str_generic_onbreak = "Their {} broke!!"
str_soul_onadorn = "{} has begun swirling around you."
str_soul_unadorn = "{} has stopped swirling around you and you place it back into your hammerspace."
str_soul_onbreak = "{} has ***SHATTERED.*** Uh oh."
str_cape_onadorn = "You skillfully adorn your {} and flourish it several times."
str_cape_unadorn = "You skillfully unadorn your {}."
str_cape_onbreak = "Your {} tears! Better hope they skill issue replacements."
str_generic_inv_limit = "You can't fit another {} in your inventory!"

generic_role_name = 'NLACakaNM'

str_generic_subway_description = "A grimy subway train."
str_generic_subway_station_description = "A grimy subway station."
str_blimp_description = "This luxury zeppelin contains all the most exquisite amenities a robber baron in transit could ask for. A dining room, a lounge, a pool table, you know, rich people stuff. Being a huge, highly flammable balloon filled with hydrogen, it is the safest way to travel in the city only because it's out of the price range of most juveniles' budget. It's used by the rich elite to travel from their summer homes in Assault Flats Beach to their winter homes in Dreadford, and vice versa, without having to step foot in the more unsavory parts of the city. It does it's job well and only occasionally bursts into flames."
str_blimp_tower_description = "This mooring mast is mostly used for amassing millionaire mooks into the marvelous Neo Milwaukee multi-story zeppelin, m'lady. Basically, you can board a blimp here. All you have to do is walk up an extremely narrow spiral staircase without an adequate handrail for about 40 feet straight up and then you can embark onto the highest airship this side of the River of Slime! It'll be great! Don't mind the spontaneously combusting zeppelins crashing into the earth in the distance. That's normal."
str_downtown_station_description = "This large, imposing structure is the central hub for the entire city's rapid transit system. A public transportation powerhouse, it contains connections to every subway line in the city, and for dirt cheap. Inside of it's main terminal, a humongous split-flap display is constantly updating with the times of subway arrivals and departures. Hordes of commuters from all across the city sprint to their connecting trains, or simply spill out into the Downtown streets, ready to have their guts do the same.\n\nExits into Downtown NLACakaNM."
str_black_subway_description = "Black Line trains are strictly uniform, with dull, minimalistic furnishings producing a borderline depressing experience. Almost completely grey aside from it's style guide mandated black accents, everything is purely practical. It provides just enough for its commuting salarymen to get to work in the morning and home at night."
str_black_subway_station_description = "This sparsely decorated terminal replicates the feeling of riding on a Black Line train, otherwise known as inducing suicidal thoughts. Dim lighting barely illuminates the moldy, stained terminal walls. Inbound and outbound trains arrive and departure one after another with unreal temporal precision. You're not sure if you've ever seen a Black Line train be late. Still doesn't make you like being on one though."
str_green_subway_description = "Easily the oldest subway line in the city, with the interior design and general cleanliness to prove it. Once cutting edge, it's art deco stylings have begun to deteriorate due to overuse and underfunding. That goes double for the actual trains themselves, with a merely bumpy ride on the Green Line being the height of luxury compared to the far worse potential risks."
str_green_subway_station_description = "Much like its trains, Green Line terminals have fallen into disrepair. It's vintage aesthetic only exasperating it's crumbling infrastructure, making the whole line seem like a old, dilapidated mess. But, you'll give it one thing, it's pretty cool looking from the perspective of urban exploration. You've dreamed of exploring it's vast, abandoned subway networks ever since you first rode on it. They could lead to anywhere. So close, and yet so mysterious."
str_purple_subway_description = "Probably the nicest subway line in the city, the Purple Line isn't defined by its poor hygiene or mechanical condition. Instead, it's defined by its relative normality. More-or-less clean floors, brightly lit interiors, upholstery on the seats. These stunning, almost sci-fi levels of perfection are a sight to behold. Wow!"
str_purple_subway_station_description = "It is clean and well-kempt, just like the Purple Line trains. This relatively pristine subway terminal hosts all manner of unusualities. With limited amounts of graffiti sprayed unto the otherwise sort-of white walls, there's actually some semblance of visual simplicity. For once in this city, your eyes aren't being completely assaulted with information or blinding lights. Boring, this place sucks. Board whatever train you're getting on and get back to killing people as soon as possible."
str_pink_subway_description = "If there's one word to describe the Pink Line, it's \"confusing\". It's by far the filthiest subway line in the city, which is exponentially worsened by it's bizarre, unexplainable faux wood paneling that lines every train. You can only imagine that this design decision was made to make the subway feel less sterile and more homely, but the constant stench of piss and homeless people puking sort of ruins that idea. Riding the Pink Line makes you feel like you're at your grandma's house every single time you ride it, if your grandma's house was in Jaywalker Plain."
str_pink_subway_station_description = "It's absolutely fucking disgusting. By far the worst subway line, the Pink Line can't keep it's terrible interior design choices contained to its actual trains. Even in its terminals, the faux wood paneling clashes with every other aesthetic element present. It's ghastly ceilings have turned a delightful piss-soaked shade of faded white. It's bizarre mixture of homely decorations and completely dilapidated state makes you oddly beguiled in a way. How did they fuck up the Pink Line so bad? The world may never know."
str_gold_subway_description = "Construction started on the Gold Line in the 90’s, and it shows. It’s just so fucking gaudy. Opulent, even. It’s vaporwave gone wrong. Geometric patterns with clashing color combinations and art styles are plastered over every square inch of the walls, and the seats are made of that awful upholstery from old Taco Bell™ booths."
str_gold_subway_station_description = "The walls of the Gold Line are covered in terrible murals. Covered. Imagine your loaded in the level geometry of the station into Unity and then Googled “terrible street art murals” and skipped to page nine and then loaded each image as textures unto the geometry, not even accounting for when one object ended and another surface began. No one knows why it’s like this."
str_subway_connecting_sentence = "Below it, on a lower level of the station, is a {} line terminal."

# TODO: Add descriptions for each outskirt/street.
str_generic_outskirts_description_edge = "It's a small patch of desert on the edge of town. Go any further and you're just asking for trouble."
str_generic_outskirts_description = "It's a wasteland, devoid of all life except for slime beasts."
str_generic_outskirts_description_depths = "The lion's den of the biggest and baddest Secreatures. Stay around too long, and you'll wind up in the jaws of god knows what lurks around here."

str_generic_streets_description = "It's a street. Not much more to be said."

# Common database columns
col_id_server = 'id_server'
col_id_user = 'id_user'

# Database columns for roles
col_id_role = 'id_role'
col_role_name = 'name'

# Database columns for items
col_id_item = "id_item"
col_item_type = "item_type"
col_time_expir = "time_expir"
col_value = "value"
col_stack_max = 'stack_max'
col_stack_size = 'stack_size'
col_soulbound = 'soulbound'
col_template = 'template'

# Database columns for apartments
col_apt_name = 'apt_name'
col_apt_description = 'apt_description'
col_rent = 'rent'
col_apt_class = 'apt_class'
col_num_keys = 'num_keys'
col_key_1 = 'key_1'
col_key_2 = 'key_2'

# Database columns for server
col_icon = "icon"

# Database columns for players
col_avatar = "avatar"
col_display_name = "display_name"

# Database columns for users
col_slimes = 'slimes'
col_slimelevel = 'slimelevel'
col_hunger = 'hunger'
col_totaldamage = 'totaldamage'
col_weapon = 'weapon'
col_weaponskill = 'weaponskill'
col_trauma = 'trauma'
col_slimecoin = 'slimecoin'
col_crime = 'crime'
col_time_lastkill = 'time_lastkill'
col_time_lastrevive = 'time_lastrevive'
col_id_killer = 'id_killer'
col_time_lastspar = 'time_lastspar'
col_time_lasthaunt = 'time_lasthaunt'
col_time_lastinvest = 'time_lastinvest'
col_bounty = 'bounty'
col_weaponname = 'weaponname'
col_name = 'name'
col_inebriation = 'inebriation'
col_ghostbust = 'ghostbust'
col_faction = 'faction'
col_poi = 'poi'
col_life_state = 'life_state'
col_busted = 'busted'
col_time_last_action = 'time_last_action'
col_weaponmarried = 'weaponmarried'
col_time_lastscavenge = 'time_lastscavenge'
col_bleed_storage = 'bleed_storage'
col_time_lastenter = 'time_lastenter'
col_time_lastoffline = 'time_lastoffline'
col_time_joined = 'time_joined'
col_poi_death = 'poi_death'
col_slime_donations = 'donated_slimes'
col_poudrin_donations = 'donated_poudrins'
col_caught_fish = 'caught_fish'
col_global_swear_jar = 'global_swear_jar'
col_arrested = 'arrested'
col_active_slimeoid = 'active_slimeoid'
col_time_expirpvp = 'time_expirpvp'
col_time_lastenlist = 'time_lastenlist'
col_apt_zone = 'apt_zone'
col_visiting = "visiting"
col_has_soul = 'has_soul'
col_sap = 'sap'
col_hardened_sap = 'hardened_sap'
col_manuscript = "manuscript"
col_spray = "spray"
col_salary_credits = 'salary_credits'
col_time_lastdeath = 'time_lastdeath'
col_sidearm = 'sidearm'
col_race = 'race'
col_time_racialability = 'time_racialability'
col_time_lastpremiumpurchase = 'time_lastpremiumpurchase'
col_verified = 'verified'
col_gender = 'gender'
col_hogtied = 'hogtied'
col_event_points = 'event_points'
col_fashion_seed = 'fashion_seed'

col_attack = 'attack'
col_speed = 'speed'
col_freshness = 'freshness'

# SLIMERNALIA
col_festivity = 'festivity'
col_slimernalia_kingpin = 'slimernalia_kingpin'

#Database columns for fishing records
col_record_type = "record_type"
col_record_amount = "record_amount"
col_legality = "legality"
col_id_post = "id_post"
col_id_image = "id_image"

# SWILLDERMUK
col_gambit = 'gambit'
col_credence = 'credence'
col_credence_used = 'credence_used'

col_juviemode = 'juviemode'

# Double Halloween
col_horseman_deaths = 'horseman_deaths'
col_horseman_timeofdeath = 'horseman_timeofdeath'

# Database columns for bartering
col_offer_give = 'offer_give'
col_offer_receive = 'offer_receive'
col_time_sinceoffer = 'time_sinceoffer'

# Database columns for slimeoids
col_id_slimeoid = 'id_slimeoid'
col_body = 'body'
col_head = 'head'
col_legs = 'legs'
col_armor = 'armor'
col_special = 'special'
col_ai = 'ai'
col_type = 'type'
col_atk = 'atk'
col_defense = 'defense'
col_intel = 'intel'
col_level = 'level'
col_time_defeated = 'time_defeated'
col_clout = 'clout'
col_hue = 'hue'
col_coating = 'coating'
col_dogtag = 'dogtag'

# Database columns for enemies
col_id_enemy = 'id_enemy'
col_enemy_slimes = 'slimes'
col_enemy_totaldamage = 'totaldamage'
col_enemy_ai = 'ai'
col_enemy_type = 'enemytype'
col_enemy_attacktype = 'attacktype'
col_enemy_display_name = 'display_name'
col_enemy_identifier = 'identifier'
col_enemy_level = 'level'
col_enemy_poi = 'poi'
col_enemy_life_state = 'life_state'
col_enemy_bleed_storage = 'bleed_storage'
col_enemy_time_lastenter = 'time_lastenter'
col_enemy_initialslimes = 'initialslimes'
col_enemy_expiration_date = 'expiration_date'
col_enemy_id_target = 'id_target'
col_enemy_raidtimer = 'raidtimer'
col_enemy_rare_status = 'rare_status'
col_enemy_hardened_sap = 'hardened_sap'
col_enemy_weathertype = 'weathertype'
col_enemy_class = 'enemyclass'
col_enemy_owner = 'owner'

# Database column for the status of districts with locks on them
col_locked_status = 'locked_status'

# Database columns for user statistics
col_stat_metric = 'stat_metric'
col_stat_value = 'stat_value'

# Database columns for markets
col_time_lasttick = 'time_lasttick'
col_slimes_revivefee = 'slimes_revivefee'
col_negaslime = 'negaslime'
col_clock = 'clock'
col_weather = 'weather'
col_day = 'day'
col_decayed_slimes = 'decayed_slimes'
col_donated_slimes = 'donated_slimes'
col_donated_poudrins = 'donated_poudrins'
col_splattered_slimes = 'splattered_slimes'
col_winner = 'winner'

# Database columns for stocks
col_stock = 'stock'
col_market_rate = 'market_rate'
col_exchange_rate = 'exchange_rate'
col_boombust = 'boombust'
col_total_shares = 'total_shares'

# Database columns for companies
col_total_profits = 'total_profits'
col_recent_profits = 'recent_profits'

# Database columns for shares
col_shares = 'shares'

# Database columns for stats
col_total_slime = 'total_slime'
col_total_slimecoin = 'total_slimecoin'
col_total_players = 'total_players'
col_total_players_pvp = 'total_players_pvp'
col_timestamp = 'timestamp'

# Database columns for districts
col_district = 'district'
col_controlling_faction = 'controlling_faction'
col_capturing_faction = 'capturing_faction'
col_capture_points = 'capture_points'
col_district_slimes = 'slimes'
col_time_unlock = 'time_unlock'
col_cap_side = 'cap_side'

# Database columns for mutations
col_id_mutation = 'mutation'
col_mutation_data = 'data'
col_mutation_counter = 'mutation_counter'
col_tier = 'tier'
col_artificial = 'artificial'
col_rand_seed = 'rand_seed'
col_time_lasthit = 'time_lasthit'

# Database columns for transports
col_transport_type = 'transport_type'
col_current_line = 'current_line'
col_current_stop = 'current_stop'

# Database columns for farms
col_farm = 'farm'
col_time_lastsow = 'time_lastsow'
col_phase = 'phase'
col_time_lastphase = 'time_lastphase'
col_slimes_onreap = 'slimes_onreap'
col_action_required = 'action_required'
col_crop = 'crop'
col_sow_life_state = 'sow_life_state'

# Database columns for troll romance
col_quadrant = 'quadrant'
col_quadrants_target = 'id_target'
col_quadrants_target2 = 'id_target2'

# Database columns for status effects
col_id_status = 'id_status'
col_source = 'source'
col_status_target = 'id_target'

# Database columns for world events
col_id_event = 'id_event'
col_event_type = 'event_type'
col_time_activate = 'time_activate'

# Database columns for quest records
col_time_stamp = 'time_stamp'
col_record_type = 'record_type'
col_record_data = 'record_data'
col_id_context_num = "context_num"
col_id_month = "month"
col_id_year = "year"

# Database columns for advertisements
col_id_ad = 'id_ad'
col_id_sponsor = 'id_sponsor'
col_ad_content = 'content'

# Database columns for books
col_id_book = "id_book"
col_title = "title"
col_author = "author"
col_book_state = "book_state"
col_date_published = "date_published"
col_genre = "genre"
col_length = "length"
col_sales = "sales"
col_rating = "rating"
col_rates = "rates"
col_pages = "pages"

# Database columns for pages of books
col_page = "page"
col_contents = "contents"

# Database columns for book sales
col_bought = "bought"

# Database columns for inhabitation
col_id_ghost = "id_ghost"
col_id_fleshling = "id_fleshling"
col_empowered = "empowered"

# Gamestate columns
col_bit = "state_bit"
col_id_state = "id_state"
col_number = "number"

#Blurb columns
col_id_blurb = "blurb"
col_id_active = "active"
col_id_id_blurb = "id_blurb"
col_id_context = "context"
col_id_subcontext = "subcontext"
col_id_subsubcontext = "subsubcontext"
col_id_dateadded = "dateadded"

# SWILLDERMUK
col_id_user_pranker = 'id_user_pranker'
col_id_user_pranked = 'id_user_pranked'
col_prank_count = 'prank_count'

# Item type names
it_item = "item"
it_medal = "medal"
it_questitem = "questitem"
it_food = "food"
it_weapon = "weapon"
it_cosmetic = 'cosmetic'
it_furniture = 'furniture'
it_book = 'book'
it_relic = 'relic'


# Cosmetic item rarities
rarity_plebeian = "Plebeian"
rarity_patrician = "Patrician"
rarity_profollean = "Profollean"
rarity_promotional = "Promotional"  # Cosmetics awarded at events / achieved through limited ways
rarity_princeps = "princeps"

normal_rarities = [rarity_plebeian, rarity_patrician, rarity_profollean]

# Leaderboard score categories
leaderboard_slimes = "SLIMIEST"
leaderboard_slimecoin = "SLIMECOIN BARONS"
leaderboard_ghosts = "ANTI-SLIMIEST"
leaderboard_podrins = "PODRIN LORDS"
leaderboard_bounty = "MOST WANTED"
leaderboard_kingpins = "KINGPINS' COFFERS"
leaderboard_districts = "DISTRICTS CONTROLLED"
leaderboard_donated = "LOYALEST CONSUMERS"
leaderboard_fashion = "NLACakaNM'S TOP MODELS"
leaderboard_crime = "BIGGEST CROOKS"
leaderboard_relics = "KNOWN RELICS"
leaderboard_kingpindonated = "KINGPIN SLIME EARNED"
leaderboard_lifetimekills = "LIFETIME KILLS"
leaderboard_lifetimedeaths = "BIGGEST VICTIMS"
# SLIMERNALIA
leaderboard_slimernalia = "MOST FESTIVE"
# SWILLDERKMUK
leaderboard_gambit_high = "HIGHEST GAMBIT"
leaderboard_gambit_low = "LOWEST GAMBIT"
# DOUBLE HALLOWEEN
leaderboard_doublehalloween = "SLIME STOLEN"
leaderboard_sacrificial = "SACRIFICIAL LAMBS"

# leaderboard entry types
entry_type_player = "player"
entry_type_districts = "districts"
entry_type_relics = "relics"
entry_type_gamestates = "gamestates"

gamestate_leaderboard_markers = {}


# district control channel topic text
control_topic_killers = "Currently controlled by the killers."
control_topic_rowdys = "Currently controlled by the rowdys."
control_topic_neutral = "Currently controlled by no one."

control_topics = {
    faction_killers: control_topic_killers,
    faction_rowdys: control_topic_rowdys,
    # "": control_topic_neutral  # no faction
    "": "",  # The neutral control thing is a bit messy, disable this for now...
}

# district control actors
actor_decay = "decay"

# The highest and lowest level your weaponskill may be on revive. All skills over this level reset to these.
weaponskill_max_onrevive = 6
weaponskill_min_onrevive = 0

# Needed for duels, apparently.
time_pvp_duel = 3 * 60

# User statistics we track
stat_max_slimes = 'max_slimes'
stat_lifetime_slimes = 'lifetime_slimes'
stat_lifetime_slimeloss = 'lifetime_slime_loss'
stat_lifetime_slimesdecayed = 'lifetime_slimes_decayed'
stat_slimesmined = 'slimes_mined'
stat_max_slimesmined = 'max_slimes_mined'
stat_lifetime_slimesmined = 'lifetime_slimes_mined'
stat_slimesfromkills = 'slimes_from_kills'
stat_max_slimesfromkills = 'max_slimes_from_kills'
stat_lifetime_slimesfromkills = 'lifetime_slimes_from_kills'
stat_slimesfarmed = 'slimes_farmed'
stat_max_slimesfarmed = 'max_slimes_farmed'
stat_lifetime_slimesfarmed = 'lifetime_slimes_farmed'
stat_slimesscavenged = 'slimes_scavenged'
stat_max_slimesscavenged = 'max_slimes_scavenged'
stat_lifetime_slimesscavenged = 'lifetime_slimes_scavenged'
stat_lifetime_slimeshaunted = 'lifetime_slimes_haunted'
stat_max_level = 'max_level'
stat_max_ghost_level = 'max_ghost_level'
stat_max_hitsurvived = 'max_hit_survived'
stat_max_hitdealt = 'max_hit_dealt'
stat_max_hauntinflicted = 'max_haunt_inflicted'
stat_kills = 'kills'
stat_max_kills = 'max_kills'
stat_biggest_kill = 'biggest_kill'
stat_lifetime_kills = 'lifetime_kills'
stat_lifetime_ganks = 'lifetime_ganks'
stat_lifetime_takedowns = 'lifetime_takedowns'
stat_max_wepskill = 'max_wep_skill'
stat_biggest_casino_win = 'biggest_casino_win'
stat_biggest_casino_loss = 'biggest_casino_loss'
stat_lifetime_casino_winnings = 'lifetime_casino_winnings'
stat_lifetime_casino_losses = 'lifetime_casino_losses'
stat_lifetime_slimecoin = 'lifetime_slime_coins'
stat_bounty_collected = 'bounty_collected'
stat_max_bounty = 'max_bounty'


stat_lifetime_poudrins = 'lifetime_poudrins'
stat_lifetime_damagedealt = 'lifetime_damage_dealt'

stat_lifetime_deaths = 'lifetime_deaths'
# Track revolver trigger pulls survived?
stat_capture_points_contributed = 'capture_points_contributed'
stat_pve_kills = 'pve_kills'
stat_max_pve_kills = 'max_pve_kills'
stat_lifetime_pve_kills = 'lifetime_pve_kills'
stat_lifetime_pve_takedowns = 'lifetime_pve_takedowns'
stat_lifetime_pve_ganks = 'lifetime_pve_ganks'
stat_lifetime_pve_deaths = 'lifetime_pve_deaths'
stat_shamblers_killed = 'shamblers_killed'
stat_lifetime_kingpin_slimes = 'lifetime_kingpin_slimes'
stat_credence = 'credence'
stat_credence_used = 'credenceused'
stat_gambit = 'gambit'
stat_lifetime_cops_killed = 'lifetime_cops_killed'


# Slimernalia stats
stat_festivity = 'festivity'
stat_festivity_max = 'max_festivity'
stat_festivity_global = 'global_festivity'


stat_revolver_kills = 'revolver_kills'
stat_dual_pistols_kills = 'dual_pistols_kills'
stat_shotgun_kills = 'shotgun_kills'
stat_rifle_kills = 'rifle_kills'
stat_smg_kills = 'smg_kills'
stat_minigun_kills = 'miningun_kills'
stat_bat_kills = 'bat_kills'
stat_brassknuckles_kills = 'brassknuckles_kills'
stat_katana_kills = 'katana_kills'
stat_broadsword_kills = 'broadsword_kills'
stat_nunchucks_kills = 'nunchucks_kills'
stat_scythe_kills = 'scythe_kills'
stat_yoyo_kills = 'yoyo_kills'
stat_knives_kills = 'knives_kills'
stat_monowhip_kills = 'monowhip_kills'
stat_molotov_kills = 'molotov_kills'
stat_grenade_kills = 'grenade_kills'
stat_garrote_kills = 'garrote_kills'
stat_pickaxe_kills = 'pickaxe_kills'
stat_diamond_pickaxe_kills = 'diamond_pickaxe_kills'
stat_fishingrod_kills = 'fishingrod_kills'
stat_bass_kills = 'bass_kills'
stat_bow_kills = 'bow_kills'
stat_umbrella_kills = 'umbrella_kills'
stat_dclaw_kills = 'dclaw_kills'
stat_spraycan_kills = 'spraycan_kills'
stat_paintgun_kills = 'paintgun_kills'
stat_paintroller_kills = 'paintroller_kills'
stat_paintbrush_kills = 'paintbrush_kills'
stat_watercolor_kills = 'watercolor_kills'
stat_thinnerbomb_kills = 'thinnerbomb_kills'
stat_staff_kills = 'staff_kills'
stat_hoe_kills = 'hoe_kills'
stat_pitchfork_kills = 'pitchfork_kills'
stat_shovel_kills = 'shovel_kills'
stat_slimeringcan_kills = 'slimeringcan_kills'
stat_fingernails_kills = 'fingernails_kills'
stat_unarmed_kills = 'unarmed_kills'
stat_roomba_kills = 'roomba_kills'
stat_chainsaw_kills = 'chainsaw_kills'
stat_megachainsaw_kills = 'megachainsaw_kills'
stat_huntingrifle_kills = 'huntingrifle_kills'
stat_whistle_kills = 'whistle_kills'
stat_harpoon_kills = 'harpoon_kills'
stat_sniper_kills = 'sniper_kills'
stat_sledgehammer_kills = 'sledgehammer_kills'
stat_skateboard_kills = 'skateboard_kills'
stat_juvierang_kills = 'juvierang_kills'
stat_missilelauncher_kills = 'missilelauncher_kills'
stat_pistol_kills = 'pistol_kills'
stat_combatknife_kills = 'combat_knife_kills'
stat_machete_kills = 'machete_kills'
stat_boomerang_kills = 'boomerang_kills'
stat_basket_kills = 'basket_kills'


private_stat_string = "'gambit', 'credence', 'credenceused'" #added into a query elsewhere to prevent stats from showing in certain places

# Categories of events that change your slime total, for statistics tracking
source_mining = 0
source_damage = 1
source_killing = 2
source_self_damage = 3
source_busting = 4
source_haunter = 5
source_haunted = 6
source_spending = 7
source_decay = 8
source_ghostification = 9
source_bleeding = 10
source_scavenging = 11
source_farming = 12
source_fishing = 13
source_squeeze = 14
source_weather = 15
source_crush = 16
source_casino = 17
source_slimeoid_betting = 18
source_ghost_contract = 19
source_blockparty = 20

# Categories of events that change your slimecoin total, for statistics tracking
coinsource_spending = 0
coinsource_donation = 1
coinsource_bounty = 2
coinsource_revival = 3
coinsource_casino = 4
coinsource_transfer = 5
coinsource_invest = 6
coinsource_withdraw = 7
coinsource_recycle = 8
coinsource_swearjar = 9
coinsource_salary = 10

# Causes of death, for statistics tracking
cause_killing = 0
cause_mining = 1
cause_grandfoe = 2
cause_donation = 3
cause_busted = 4
cause_suicide = 5
cause_leftserver = 6
cause_drowning = 7
cause_falling = 8
cause_bleeding = 9
cause_burning = 10
cause_killing_enemy = 11
cause_weather = 12
cause_cliff = 13
cause_backfire = 14
cause_praying = 15
cause_poison = 16
cause_crushing = 17
cause_gay = 18
cause_debris = 19

# List of user statistics that reset to 0 on death
stats_clear_on_death = [
    stat_slimesmined,
    stat_slimesfromkills,
    stat_kills,
    stat_pve_kills,
    stat_slimesfarmed,
    stat_slimesscavenged
]

context_slimeoidheart = 'slimeoidheart'
context_negaslimeoidheart = 'negaslimeoidheart'
context_slimeoidbottle = 'slimeoidbottle'
context_slimeoidfood = 'slimeoidfood'
context_wrappingpaper = 'wrappingpaper'
context_prankitem = 'prankitem'

# Item vendor names.
vendor_bar = 'bar'  # rate of non-mtn dew drinks are 100 slime to 9 hunger
vendor_pizzahut = 'Pizza Hut'  # rate of fc vendors are 100 slime to 10 hunger, Sub-menu in Food Court
vendor_tacobell = 'Taco Bell' # Sub-menu in Food Court
vendor_kfc = 'KFC' # Sub-menu in Food Court
vendor_mtndew = 'Mtn Dew Fountain' # Sub-menu in Food Court
vendor_vendingmachine = 'vending machine' # Pourdin Alley's 7/11.
vendor_seafood = 'Red Mobster Seafood'  # rate of seafood is 100 slime to 9 hunger
vendor_diner = "Smoker's Cough"  # rate of drinks are 100 slime to 15 hunger
vendor_beachresort = "Beach Resort"  # Assault Flats Beach bar and the sunburnt greasy man to sell you summer-season amenities.
vendor_countryclub = "Country Club"  # Dreadford's snobbish vendor. Crookline's Splatify is the southwest bar in the game now.
vendor_farm = "Farm"  # contains all the vegetables you can !reap
vendor_bazaar = "bazaar" # General store, and pulls in the item pool from every other vendor in the game.
vendor_giftshop = "giftshop"
vendor_college = "College"  # You can buy game guides from either of the colleges
vendor_glocksburycomics = "Glocksbury Comics"  # Repels and trading cards are sold here
vendor_slimypersuits = "Slimy Persuits"  # You can buy candy from here
vendor_greencakecafe = "Green Cake Cafe"  # Brunch foods
vendor_bodega = "Bodega"  # Default clothing store in Krak Bay
vendor_snottopic = "Snot Topic" # Sub-store within Bodega, featuring crappy clothing that no other store would sell.
vendor_caravan = "Caravan" #Sub-store within Bodega, filters a lot of shoes into one store.
vendor_secretbodega = "Secret Bodega"  # The secret clothing store in Krak Bay
vendor_wafflehouse = "Waffle House"  # waffle house in the void, sells non-perishable foods, 50 slime to 1 hunger
vendor_basedhardware = "Based Hardware"  # Hardware store in West Glocksbury
vendor_lab = "Lab"  # Slimecorp products
vendor_atomicforest = "Atomic Forest Stockpile"  # Storage of atomic forest
vendor_downpourlaboratory = "Downpour Armament Vending Machines"  # Store for shamblers to get stuff
vendor_breakroom = "The Breakroom"  # Security officers can order items here for free.
vendor_rpcity = "RP City"  # Double halloween costume store
vendor_coalitionsurplus = "Coalition Surplus" # Glocksbury vendor
vendor_gumballmachine = "Gumball Machine"

vendor_passive_chat_wait_time = 60 * 60 * 12  # 12 hours


museum_thumbnails = {
    "amy":["AMY HART", "https://rfck.app/npc/AMY_HART_pfp.png"],
    "curator":["THE CURATOR", "https://rfck.app/npc/CURATOR_GOOD_HEAD.png"]
}

hide_value = random.randint(0, 2)

hide_taka_thumbnail = ["https://rfck.app/npc/hide_taka_taco.png", "https://rfck.app/npc/hide_taka_pizza.png", "https://rfck.app/npc/hide_taka_kfc.png"]
hide_dialogue = {
    0:["I hope you choke on it.", "If you order another barbecue sauce packet and nothing else I'm going to scream.", " My boss will fire me if he catches me talking to you. Go on, shoo. I have tuition to pay.", "Go on. Make the same order repeatedly and then get out of here, like you always do."],#tacobell, stoic
    1:["Lovely day out, am I right?", "Hey, pal, can you keep a secret? We're selling chicken nuggets under the table.", "I've been told to tell you that we cook all our food right here, in the food court. That's right, there's a robust kitchen through that door. All freshly defrroooo... fried!", "I tried to talk about starting a union but, they got the whole place bugged so they threw my partner down the sewers. Call for help, man!"],#pizza, cheerful
    2:["*Licks fingers* Good.", "No spam ordering, man. You're running me ragged.", "()*Hide picks a taco shell out of their hair and eats it*", "We import all our food from Jamaica Avenue. When the pizza crusts grow mold they can mutate it into chicken. Heh, I don't know how it works."] #kfc, chill
}


vendor_thumbnails = {
    poi_id_speakeasy:["CAPTAIN ALBERT ALEXANDER", "https://rfck.app/npc/albertalex.png"],
    "saloon":["OL' BOY RUSTLE", "https://rfck.app/npc/olboyrustle.png"],
    "basedhardware":["BETTY BAMALAM", "https://rfck.app/npc/bet.png"],
    "oozegardensfarms":["HORTISOLIS", "https://cdn.discordapp.com/attachments/927511705519538226/1005995514073972766/unknown.png"],
    "realestateagency":["MR. CHADI, FORMERLY N2", "https://rfck.app/npc/n2double.png"],
    poi_id_neomilwaukeestate:["PROFESSOR BRAINSLIME", "https://rfck.app/npc/brainslime.png"],
    "themuseum":museum_thumbnails.get(current_curator),
    poi_id_slimypersuits:["BAILEY", "https://cdn.discordapp.com/attachments/858397413568151582/977066095288664074/unknown.png"],
    "clinicofslimoplasty":["DR. DUSTTRAP", "https://yt3.ggpht.com/ytc/AKedOLQCV-tLjbp8R3Ua3-NYtax1F_T86YzV14UY16cHhQ=s900-c-k-c0x00ffffff-no-rj"],
    poi_id_foodcourt:["HIDE TAKA", hide_taka_thumbnail[hide_value]],
    poi_id_greenlightdistrict:["FUCKER CARLSON", "https://rfck.app/npc/fuckercarlson.png"],
    poi_id_apt_littlechernobyl:["JERMA", "https://rfck.app/npc/jerma.png"]
}


museum_dialogue = {
    "amy":["God, this is frustrating.", "Hoss isn't here. Did you need something?", "The truckers out here are kind of mental. I tried importing a crate of Takis since they're not stocked in the city and shipping cost me 260 mega.", "Hey...you don't look quite right. Guess that's normal around here, but how did you end up looking like that?", "Truthfully, I'd rather not talk history right now. It's a sore subject with you gangsters, I'll keep my research to myself.", "Hey wait, is that a...Nah, it's just an ordinary weapon. Forget I said anything.", "It'd be nice to go along with Hoss, but there's a strong possibility ENDLESS WAR might endanger us somehow if we both left at the same time. We're hedging our bets.", "I'm not an exhibit. I don't think I'm flattered that you thought otherwise, heh."],
    "curator":["CAN YOU SMELL THE FISH? I'VE BEEN STEWING IN THIS FARMSTINK FOR SO BLOODY LONG IT'S BECOME MY DEFAULT NOW.", "I KNOW YOU'RE GOING TO STEAL THE RELICS YOU DONATE, YOU STALEVAPED TICKDANCER ZOOMERTYPE. JUST TAKE THEM. IF YOU DON'T THEN SOME OTHER IMBECILE WILL INSTEAD.", "ALL THIS TALK OF CANDIDATES, YOU THINK THEY CAN TRICK ME?! I'LL VOTE WHEN HELL SLEETS ITS TROUSERS!", "HAVE YOU HEARD WORD OF THIS BICARBONATE FOUNTAIN? I MIGHT HAVE SOME CHANCE TO ESCAPE USING IT, BUT THE DOC'S ORDERS TELL ME I SHOULDN'T BE TRYING TO ZUCK MYSELF FOR ANOTHER YEAR OR TWO.", "NO, I WON'T GIVE YOU FREE SLIME, YOU WILTING PATHETIC GUTTERHANGER. EARN IT OR YOU WON'T BE PROUD OF IT."]
}


vendor_dialogue = {
    poi_id_speakeasy:["Ferry's 'ere, lad.","Aye, I was like ye once, 'fore that cannon licked me at the knee","*Stares wistfully out the window into the bay*","Me ship ran aground on the western shore of Snake Island. How a wooden sailin' vessel lasted so long in that slimy drink I'll never know. Speaking of slimy drinks, care fer a Manhattan Project?","Yarr."],
    "clinicofslimoplasty":["Nice kidney. If you think you'll die before your next !piss I might just buy it off you.", "I'll give you a discount if you let me fix you up after I've had a few drinks. I'm playing Malpractice Bingo with a heart surgeon in Poudrin Alley.", "You get the kid's discount. I don't do it because it's good for business, really. I just like hurting children.", "Sonny, do you know about any gingerbread houses deep in the woods in this town? I'm looking to retire and could use a new space.", "I'll probably wind up repeating something I said to you. That's the dementia, pay it no mind.", "Lots of slimeoid operations recently. I don't care for 'em. Too many syringes."],
    "themuseum":museum_dialogue.get(current_curator),
    poi_id_neomilwaukeestate:["Threat assessment is important to navigating NLACakaNM. Using !scout regularly and paying attention to active gangsters is important to not getting killed.", "CTRL hotkeys, once mastered, increase your speed drastically. You probably know about Cut, Copy, and Paste, but CTRL+A can select all, and CTRL+Z on a Discord window can repeat your previous message. Just be careful, the law under NLACakaNM Statute AHK-2 Subsection 3 bans the use of macros and self-bots for combat purposes. The jailtime penalties are higher than meth production, if you can believe that.", "Capping rules can get fairly in-depth. If you want to avoid gangsters staining your house pink or purple every other day, it helps to know their tactics. There is a 200,000 slime minimum. Rowdys and Killers have to be the only gang in a district for capping to progress. Slime count beyond that limit does not affect capping speed, but the number of gangsters and each individual member's mutation sets are relevant, specifically Patriot, Lone Wolf, and Unnatural Charisma."],
    "realestateagency":["😎", "hey. I don't really care if you buy real estate, lol. slimecoin isn't profitable  at all, we keep afloat off a government subsidy", "hope there's no hard feelings about the whole slimecorp thing, dog. I was losing them millions just by playing scribblenauts instead of doing any marketing", "hope youre not looking for magicksrampage. they signed on as a janitor with us for a few days but realized their mistake and got out", "i'll add some of my sick taste in decor to you apartment for some slime under the table.", "there's this guy on the street named bobo cuatro who will buy a mixtape from anybody. this dudes my hero i swear", "i was never a booze guy at slimecorp but i'm starting to learn a few things. lol guess the party doesn't have to stop."],
    "saloon":["ALL THE WORLD'S IS HALF-JUGGALO BABY! HALF AT LEAST!", "!thrash !dab !thrash !dab !thrash !dab !thrab !dash", "A🤡A🤡A🤡A🤡A🤡A🤡A🤡A🤡H🤡A🤡H🤡A🤡H🤡A🤡H🤡A🤡H🤡A🤡H🤡A🤡H", "SERVE ME SOME OF THAT CHERRY SODA you WILD CRACK BABY SQUICKHEADS!", "I'll rip off your dick and give you a motherfucking nose job with it! I did it once and I'll do it again!", "I'm not a president yet, but I'm the president of RIGHT HERE, RIGHT NOW! THAT'S RIGHT YOU GLORIOUS FREAKS, SUCK MY COCK AND DIE!", "Those killers are juggalos to me. I just see them as equals. They're clowning on the inside, I know all about it.", "Let me get a shout out from those rowdys in the house! THRASH THIS WHOLE PLACE DOWN, YEAH!"],
    "oozegardensfarms":["AT ATOMIC FOREST STOCKPILE, WE GANKERS HAVE ACCRUED TOOLS FOR THOU TO PURCHASE!", "THY FARMS OF OOZE GARDENS TEEM WITH LIFE THIS MORN!", "PRITHEE, YOUNG JUVE! SOW THY FIELDS WITH CARE.", "DOST THOU JUVE KNOW OF GAIASLIMEOIDS? 'TWAS A PHOEBUS-GIVEN GIFT!", "SHALL THE LIGHT SHINE DOWN UPON US AND THINE GLORIOUS FIELDS."],
    "basedhardware":["The name's \"Black\" Betty Bamalam", "If someone else brings up the metric system one more time I swear to god.", "Nobody ever buys my wrenches. Maybe I should put them lower on the shelf.", "Some corked up 30-something lady came in here and asked for a fork-shaped plug socket. What is happening to people these days?", "If they tried to let me go from this gig the SSB Mafia would tear it down in no time. So I can call you human garbage and it's not a big deal.", "Our Wreckington location makes way more money than out here, I'll be honest with ya. But they're real busy.", "Get out of here. They don't let me play my reggae while you're shopping.", "Bronx accent? I've never been to the Bronx. I don't know that Musset guy either, but uh. Not for nothin', is that guy single?"],
    poi_id_slimypersuits:["Hey bro! I just got a new stash of mango vape pods, fresh from the Philippines. I promise these ones aren't laced!", "This place is so *boooooring*, dude! I'm straight DEPRESSED with how dead this store is.", "I munched on some of the candies this place sells bro, and I got turnt UP for a bit! It's like Adderall plus! Those slimeoids really gotta be on some crazy sorta stuff!", "Dunno what's so appealing about a part-time job to kids. If it wasn't for my, *heh*, \"side hustle\", I couldn't even *afford* rent in a junkhole like West Glocksbury. Lotta business there though, ha!", "You want a rigid candy? That was me when I was doin' your mom last night! Ha!", "Don't forget to tell all your pals about where to find me, kid. I've got the best deals in town!", "If I've got any advice, it's drop out of college and follow your dreams! I ain't joshin' you, it's foolproof. Worked for me!"],
    poi_id_foodcourt:hide_dialogue.get(hide_value),
    poi_id_greenlightdistrict:["The establishment isn't even trying to hide that our death furnace has been co-opted by anti-warfare, Israeli slimermaid apologists. Of course, you're not allowed to notice that.", "This episode of Fucker Carlson is sponsored by \"Survive Headless\" dietary supplements. Be a sigma, be an alpha, have so many Greek letters in front of your name that the only surface they can all be written on is if they're tattooed on your massive pecs. Survive Headless.", "Coming up next, choosing the Minecraft bow, and how it could lead to a rampant homosexuality crisis.", "What is the Killer kingpin up to? He has done nothing to stop Coalition Surplus from buying back our weapons from the dojo. In fact, he has done nothing at all.", "All we have to do to solve this financial crisis, is to drain the ghosts into the Slime Sea to haunt shipwrecks, and then nail every new immigrant to a cross. They might tell you otherwise, but it worked for El Paso."],
    poi_id_apt_littlechernobyl:["Hope you enjoy the toilets. They're handpicked by me."]

}

vendor_order_dialogue = {
    poi_id_slimypersuits:["Thanks for shopping at Slimy Persuits, ha!", "That one tastes reeeaaal good, dude. Trust me!", "Hey kid — you want anything... extra, with that purchase?", "Don't forget to tell all your pals about where to find me, kid. I've got the best deals in town!"],
    "oozegardensfarms":["THOU DESERVES TIDINGS FOR THY PURCHASE.", "GREAT CHOICE!", "MAY THOU FIELDS TEEM WITH LIFE!"]
}


museum_curator_dialogue = {
    "odditem":"The curator looks confused on why you brought *that*. He only takes relics, framed art, and fish.",
    "smallfish":"\"SORRY, CHAP, YOUR FISH IS TOO SMALL. THERE'S A DICK JOKE IN THERE SOMEWHERE BUT I'M TWICE YOUR AGE. TOO CREEPY, I SAY.\"",
    "cheatedfish":"\"I'M ON TO YOU, YOU {insult}! TRY AND CHEAT FISH WITH ME AGAIN, SEE WHAT HAPPENS!\"",
    "caughtcheatfish":"\"YOU THINK I WAS BORN YESTERDAY, YOU FISH-ROIDING {insult}? THE BLOODY {fish}'S BEEN EMBIGGENED TO HELL AND BACK! BELLENDS LIKE YOU LOSE THEIR {fish} PRIVILEGES. QUITE SO.\"",
    "fishdonate":"The curator is taken aback by the sheer girth of your {}! But, without missing a beat he swipes your fish from you and runs behind the tanks to drop it right in with the rest of them. After a few minutes, he returns with the old record-setting fish impaled through the gills by harpoon gun.\"THEY CAN'T ALL BE WINNERS, EH? OH YEAH, HERE'S YOUR TIP.\"\n\nYou got {} slime!",
    "redonaterelic":"\"WHAT ARE YOU DOING WITH THAT SHODDY REPLICA? I HAVE THE REAL ONE HERE IN MY MUSEUM.\"",
    "donaterelic":"The curator takes the {} and excitedly jaunts into his backroom, casually tossing {:,} slime your way. You wait for him to carefully examine it, write up a plaque, and get all the fanboying out of his system, before he comes back to set up the museum display. He also hands you a meticulously constructed replica for your trouble.\n\n While he isn't looking, you swap the copied relic with the original. He turns around to catch you in the act, but shrugs and doesn't respond to your crime.",
    "spoons":"\"MORE SPOONS? HEY AMY, PUT THIS ONE WITH THE OTHER SPOON PICTURES. YEAH, OVER THERE IN THE FURNACE. ANYWAY, THANKS FOR DONATING.\"",
    "artnametaken":"\"YOU THINK YOU CAN RIP OFF SOMEONE ELSE\'S WORK? DON'T BE A {insult} AND NAME IT SOMETHING ELSE.\"",
    "colon":"\"THE LAST TIME I SAW THIS MANY COLONS WAS WHEN I PUT UP FLYERS UP NEAR THE GAY BAR IN GREENLIGHT. TAKE OUT THE \"::\" OR IT'S NOT GETTING IN.\"",
    "deviantpost":'"IT\'S UP ON DEVIANT SPLAAART. GET ENOUGH LIKES AND THEN WE\'LL TALK. HOPE YOU LIKE PAYMENTS IN EXPOSURE, MY FRIEND!"',
    "notitleart":"\"GIVE ME A TITLE FOR THIS, YOU {insult}! MY EXHIBITS ARE MORE THAN A GLORIFIED KITCHEN FRIDGE!\" "
}

amy_curator_dialogue = {
    "odditem":"Amy looks confused on why you brought *that*. She only takes relics, framed art, and fish.",
    "smallfish":"\"This one's too small, buddy. We're looking for record breakers here.\"",
    "cheatedfish":"\"Oh, it's you. I guess I respect the hustle, but if you cheat you're out of the fish donating game. Can't accecpt this one.\"",
    "caughtcheatfish":"\"This {fish}? It's fake. It's a goddamn counterfeit fish. Get out of here with this bullshit.\"",
    "fishdonate":"Amy approvingly nods her head at your {}. Looks like we got a winner! Amy tags the new fish, then dips headfirst into the fishtank to retrieve the old one. A few minutes later she emerges with it, slam dunking the majestic creature into the trash.\"Whoa nelly. I think we gotta clean these tanks better.\"\n\nYou got {} slime!",
    "redonaterelic":"\"We have *a* version of this in the museum. Either you stole this real one earlier or this is fake. But either way I'm probably won't get to display this relic for long. No deal.\"",
    "donaterelic":"Amy looks the artifact over. \"A {}, huh? This is probably the real one, so I'll pay you to get the chance to study it.\" She walks into the backroom, casually tossing {:,} slime your way. You wait for her to carefully examine it, write up a plaque, and get all the fangirling out of her system when nobody's looking, before she comes back to set up the museum display. She also hands you a meticulously constructed replica for your trouble.\n\n \"Ugh. Swap the real one for the fake all you want. It's not like we can hold you off forever.\" While she isn't looking, you do just that.",
    "spoons":"\"You're tearing me apart, Lisa! Nah, but seriously. Don't donate the spoon picture again.\"",
    "artnametaken":"\"Somebody else chose that name. Just add an underscore or a 2 to the end, it'll be fine.\"",
    "colon":"\"If you put a colon in the frame like that it won't hag on the wall right. Better take that out first.",
    "deviantpost":'"I posted it to DeviantSPLAAART. May the algoorithm have mercy on its soul."',
    "notitleart":"\"It's gonna need a title. DeviantSPLAAART won't let me post it without one.\" "
}


museum_dialogue = {
    "curator":museum_curator_dialogue,
    "amy":amy_curator_dialogue

}


dojo_weapons = ['molotovs', 'knives', 'yo-yo', 'scythe', 'nun-chucks', 'baseball bat', 'brass knuckles']

pvp_dialogue = ['You talk to {}. They don\'t seem much for conversation.', 'You verbally abuse {}, hoping maybe you\'ll feel less small that way.']

item_id_slimepoudrin = 'slimepoudrin'
item_id_negapoudrin = 'negapoudrin'
item_id_ghostlycloth = 'ghostlycloth'
item_id_ghosttoken = 'ghosttoken'
item_id_monstersoup = 'monstersoup'
item_id_doublestuffedcrust = 'doublestuffedcrust'
item_id_quadruplestuffedcrust = 'quadruplestuffedcrust'
item_id_octuplestuffedcrust = "octuplestuffedcrust"
item_id_sexdecuplestuffedcrust = "sexdecuplestuffedcrust"
item_id_duotrigintuplestuffedcrust = "duotrigintuplestuffedcrust"
item_id_quattuorsexagintuplestuffedcrust = "quattuorsexagintuplestuffedcrust"
item_id_forbiddenstuffedcrust = "theforbiddenstuffedcrust"
item_id_forbidden111 = "theforbiddenoneoneone"
item_id_tradingcardpack = "tradingcardpack"
item_id_promotradingcardpack = "promotradingcardpack"
item_id_monofilamentfragment = "monofilamentfragment"
item_id_minecraftdiamond = "minecraftdiamond"
item_id_tcgboosterbox = "tcgboosterbox"
item_id_stick = "stick"
item_id_gameguide = "gameguide"
item_id_juviegradefuckenergybodyspray = "juviegradefuckenergybodyspray"
item_id_superduperfuckenergybodyspray = "superduperfuckenergybodyspray"
item_id_gmaxfuckenergybodyspray = "gmaxfuckenergybodyspray"
item_id_pheromones = "pheromones"
item_id_costumekit = "costumekit"
item_id_doublehalloweengrist = "doublehalloweengrist"
item_id_whitelineticket = "ticket"
item_id_seaweedjoint = "seaweedjoint"
item_id_megaslimewrappingpaper = "megaslimewrappingpaper"
item_id_greeneyesslimedragonwrappingpaper = "greeneyesslimedragonwrappingpaper"
item_id_phoebuswrappingpaper = "phoebuswrappingpaper"
item_id_slimeheartswrappingpaper = "slimeheartswrappingpaper"
item_id_slimeskullswrappingpaper = "slimeskullswrappingpaper"
item_id_shermanwrappingpaper = "shermanscorpsewrappingpaper"
item_id_slimecorpwrappingpaper = "crimecorpwrappingpaper"
item_id_pickaxewrappingpaper = "pickaxewrappingpaper"
item_id_munchywrappingpaper = "munchywrappingpaper"
item_id_benwrappingpaper = "benwrappingpaper"
item_id_gellphone = "gellphone"
item_id_royaltypoudrin = "royaltypoudrin"
item_id_prankcapsule = "prankcapsule"
item_id_cool_material = "coolbeans"
item_id_tough_material = "toughnails"
item_id_smart_material = "smartcookies"
item_id_beautiful_material = "beautyspots"
item_id_cute_material = "cutebuttons"
item_id_evil_material = "evilstuds"
item_id_dragonsoul = "dragonsoul"
item_id_monsterbones = "monsterbones"
item_id_faggot = "faggot"
item_id_doublefaggot = "doublefaggot"
item_id_seaweed = "seaweed"
item_id_string = "string"
item_id_tincan = "tincan"
item_id_oldcd = "oldcd"
item_id_oldboot = "oldboot"
item_id_leather = "leather"
item_id_ectoplasm = "ectoplasm"
item_id_feather = "feather"
item_id_partypoppepperseeds = "partypoppepperseeds"
item_id_partypopper = "partypopper"
item_id_ironingot = "ironingot"
item_id_bloodstone = "bloodstone"
item_id_tanningknife = "tanningknife"
item_id_dinoslimemeat = "dinoslimemeat"
item_id_dinoslimesteak = "dinoslimesteak"
item_id_carpotoxin = "carpotoxin"
item_id_moonrock = "moonrock"
item_id_bustedrifle = "bustedrifle"
item_id_repairkit = "fieldrepairkit"
item_id_phoenixdown = "phoenixdown"
item_id_rainwing = "rainwing"
item_id_dyesolution = "dyesolution"
item_id_textiles = "textiles"
item_id_foodbase = "foodbase"
item_id_mastectomy_mango_pod = "mastectomymangopod"
item_id_menthol_mint_pod = "mentholmintpod"
item_id_striking_strawberry_pod = "strikingstrawberrypod"
item_id_ten_story_tobacco_pod = "tenstorytobaccopod"
item_id_cop_killer_cotton_candy_pod = "copkillercottoncandypod"
item_id_mustard_gas_pod = "mustardgaspod"
item_id_moon_dust_pod = "moondustpod"
item_id_spent_pod = "spentpod"
item_id_giftribbon = "giftribbon"
item_id_gallonofmilk = "gallonofmilk"
item_id_alienleather = "alienleather"
item_id_monofilamentcloth = "monofilamentcloth"
item_id_civilianscalp = "civilianscalp"
item_id_modelovaccine = "modelovirusvaccine"
item_id_key = "key"
item_id_emptyslimebottle = "emptyslimebottle"
item_id_discontinuedscrap = "discontinuedscrap"

# SLIMERNALIA
item_id_sigillaria = "sigillaria"

# SWILLDERMUK
# Instant use items
item_id_creampie = "creampie"
item_id_waterballoon = "waterbaloon"
item_id_bungisbeam = "bungisbeam"
item_id_circumcisionray = "circumcisionray"
item_id_cumjar = "cumjar"
item_id_discounttransbeam = "discounttransbeam"
item_id_transbeamreplica = "transbeamreplica"
item_id_bloodtransfusion = "bloodtransfusion"
item_id_transformationmask = "transformationmask"
item_id_emptychewinggumpacket = "emptychewinggumpacket"
item_id_airhorn = "airhorn"
item_id_banggun = "banggun"
item_id_pranknote = "pranknote"
item_id_bodynotifier = "bodynotifier"
item_id_candycane = "candycane"
# Response items
item_id_chinesefingertrap = "chinesefingertrap"
item_id_japanesefingertrap = "japanesefingertrap"
item_id_sissyhypnodevice = "sissyhypnodevice"
item_id_piedpiperkazoo = "piedpiperkazoo"
item_id_sandpapergloves = "sandpapergloves"
item_id_ticklefeather = "ticklefeather"
item_id_genitalmutilationinstrument = "gentialmutilationinstrument"
item_id_gamerficationasmr = "gamerficationasmr"
item_id_beansinacan = "beansinacan"
item_id_brandingiron = "brandingiron"
item_id_lasso = "lasso"
item_id_fakecandy = "fakecandy"
item_id_crabarmy = "crabarmy"
# Trap items
item_id_whoopiecushion = "whoopiecushion"
item_id_beartrap = "beartrap"
item_id_bananapeel = "bananapeel"
item_id_windupbox = "windupbox"
item_id_windupchatterteeth = "windupchatterteeth"
item_id_snakeinacan = "snakeinacan"
item_id_landmine = "landmine"
item_id_freeipad = "freeipad"
item_id_freeipad_alt = "freeipad_alt"
item_id_perfectlynormalfood = "perfectlynormalfood"
item_id_pitfall = "pitfall"
item_id_electrocage = "electrocage"
item_id_ironmaiden = "ironmaiden"
item_id_signthatmakesyoubensaint = "signthatmakesyoubensaint"
item_id_piebomb = "piebomb"
item_id_defectivealarmclock = "defectivealarmclock"
item_id_alligatortoy = "alligatortoy"
item_id_undefinedprankscrap = "undefinedprankscrap"
item_id_janusmask = "janusmask"
item_id_swordofseething = "swordofseething"
item_id_usedneedle = "usedneedle"
item_id_giftpipebomb = "giftpipebomb"

prank_type_instantuse = 'instantuse'
prank_type_response = 'response'
prank_type_trap = 'trap'
prank_type_mash = 'mash'
prank_rarity_heinous = 'heinous'
prank_rarity_scandalous = 'scandalous'
prank_rarity_forbidden = 'forbidden'
prank_type_text_instantuse = '\n\nPrank Type: Instant Use - Good for hit-and-run tactics.'
prank_type_text_response = '\n\nPrank Type: Response - Use it on an unsuspecting bystander.'
prank_type_text_trap = '\n\nPrank Type: Trap - Lay it down in a district.'

# candy ids
item_id_paradoxchocs = "paradoxchocs"
item_id_licoricelobsters = "licoricelobsters"
item_id_chocolateslimecorpbadges = "chocolateslimecorpbadges"
item_id_munchies = "munchies"
item_id_sni = "sni"
item_id_twixten = "twixten"
item_id_slimybears = "slimybears"
item_id_marsbar = "marsbar"
item_id_magickspatchkids = "magickspatchkids"
item_id_atms = "atms"
item_id_seanis = "seanis"
item_id_candybungis = "candybungis"
item_id_turstwerthers = "turstwerthers"
item_id_poudrinpops = "poudrinpops"
item_id_juvieranchers = "juvieranchers"
item_id_krakel = "krakel"
item_id_swedishbassedgods = "swedishbassedgods"
item_id_bustahfingers = "bustahfingers"
item_id_endlesswarheads = "endlesswarheads"
item_id_n8heads = "n8heads"
item_id_strauberryshortcakes = "strauberryshortcakes"
item_id_chutzpahcherries = "chutzpahcherries"
item_id_n3crunch = "n3crunch"
item_id_slimesours = "slimesours"
item_id_454casullround = ".454casullround"
# slimeoid food
item_id_fragilecandy = "fragilecandy"  # +chutzpah -grit
item_id_rigidcandy = "rigidcandy"  # +grit -chutzpah
item_id_recklesscandy = "recklesscandy"  # +moxie -grit
item_id_reservedcandy = "reservedcandy"  # +grit -moxie
item_id_bluntcandy = "bluntcandy"  # +moxie -chutzpah
item_id_insidiouscandy = "insidiouscandy"  # +chutzpah -moxie

# vegetable ids
item_id_poketubers = "poketubers"
item_id_pulpgourds = "pulpgourds"
item_id_sourpotatoes = "sourpotatoes"
item_id_bloodcabbages = "bloodcabbages"
item_id_joybeans = "joybeans"
item_id_purplekilliflower = "purplekilliflower"
item_id_razornuts = "razornuts"
item_id_pawpaw = "pawpaw"
item_id_sludgeberries = "sludgeberries"
item_id_suganmanuts = "suganmanuts"
item_id_pinkrowddishes = "pinkrowddishes"
item_id_dankwheat = "dankwheat"
item_id_brightshade = "brightshade"
item_id_blacklimes = "blacklimes"
item_id_phosphorpoppies = "phosphorpoppies"
item_id_direapples = "direapples"
item_id_rustealeaves = "rustealeaves"
item_id_metallicaps = "metallicaps"
item_id_steelbeans = "steelbeans"
item_id_aushucks = "aushucks"
item_id_partypoppeppers = "partypoppeppers"

# vegetable materials
item_id_poketubereyes = "poketubereyes"
item_id_pulpgourdpulp = "pulpgourdpulp"
item_id_sourpotatoskins = "sourpotatoskins"
item_id_bloodcabbageleaves = "bloodcabbageleaves"
item_id_joybeanvines = "joybeanvines"
item_id_purplekilliflowerflorets = "purplekilliflowerflorets"
item_id_razornutshells = "razornutshells"
item_id_pawpawflesh = "pawpawflesh"
item_id_sludgeberrysludge = "sludgeberrysludge"
item_id_suganmanutfruit = "suganmanutfruit"
item_id_pinkrowddishroot = "pinkrowddishroot"
item_id_dankwheatchaff = "dankwheatchaff"
item_id_brightshadeberries = "brightshadeberries"
item_id_blacklimeade = "blacklimeade"
item_id_phosphorpoppypetals = "phosphorpoppypetals"
item_id_direapplestems = "direapplestems"
item_id_rustealeafblades = "rustealeafblades"
item_id_metallicapheads = "metallicapheads"
item_id_steelbeanpods = "steelbeanpods"
item_id_aushuckstalks = "aushuckstalks"
item_id_driedpartypoppeppers = "driedpartypoppeppers"

# dye ids
item_id_dye_black = "blackdye"
item_id_dye_pink = "pinkdye"
item_id_dye_green = "greendye"
item_id_dye_brown = "browndye"
item_id_dye_grey = "greydye"
item_id_dye_purple = "purpledye"
item_id_dye_teal = "tealdye"
item_id_dye_orange = "orangedye"
item_id_dye_cyan = "cyandye"
item_id_dye_red = "reddye"
item_id_dye_lime = "limedye"
item_id_dye_yellow = "yellowdye"
item_id_dye_blue = "bluedye"
item_id_dye_magenta = "magentadye"
item_id_dye_cobalt = "cobaltdye"
item_id_dye_white = "whitedye"
item_id_dye_rainbow = "rainbowdye"
item_id_dye_negative = "negativedye"
item_id_paint_copper = "copperpaint"
item_id_paint_chrome = "chromepaint"
item_id_paint_gold = "goldpaint"

fuck_energies = ['khaotickilliflowerfuckenergy', 'rampagingrowddishfuckenergy', 'direappleciderfuckenergy', 'ultimateurinefuckenergy', 'superwaterfuckenergy', 'justcumfuckenergy', 'goonshinefuckenergy', 'liquidcoffeegroundsfuckenergy', 'joybeanjavafuckenergy', 'krakacolafuckenergy', 'drfuckerfuckenergy']

# Hunting trophy ids from safari event
item_id_trophy_juvie = "juvietrophy"
item_id_trophy_dinoslime = "dinoslimetrophy"
item_id_trophy_slimeadactyl = "slimeadactlytrophy"
item_id_trophy_microslime = "microslimetrophy"
item_id_trophy_slimeofgreed = "slimeofgreedtrophy"
item_id_trophy_desertraider = "desertraidertrophy"
item_id_trophy_mammoslime = "mammoslimetrophy"
item_id_trophy_megaslime = "megaslimetrophy"
item_id_trophy_srex = "srextrophy"
item_id_trophy_dragon = "dragontrophy"
item_id_trophy_ufo = "ufotrophy"
item_id_trophy_mammoslimebull = "mammoslimebulltrophy"
item_id_trophy_rivalhunter = "rivalhuntertrophy"
item_id_trophy_spacecarp = "spacecarptrophy"
item_id_trophy_gull = "gulltrophy"
item_id_trophy_garfield = "garfieldtrophy"
item_id_trophy_n400 = "n400trophy"
item_id_trophy_styx = "styxtrophy"
item_id_trophy_prairieking = "prairiekingtrophy"
item_id_trophy_wailord = "wailordtrophy"
item_id_trophy_phoenix = "phoenixtrophy"
item_id_trophy_microgull = "microgulltrophy"

# weapon ids
weapon_id_revolver = 'revolver'
weapon_id_dualpistols = 'dualpistols'
weapon_id_shotgun = 'shotgun'
weapon_id_rifle = 'rifle'
weapon_id_smg = 'smg'
weapon_id_minigun = 'minigun'
weapon_id_bat = 'bat'
weapon_id_brassknuckles = 'brassknuckles'
weapon_id_katana = 'katana'
weapon_id_broadsword = 'broadsword'
weapon_id_nunchucks = 'nun-chucks'
weapon_id_scythe = 'scythe'
weapon_id_yoyo = 'yo-yo'
weapon_id_knives = 'knives'
weapon_id_molotov = 'molotov'
weapon_id_grenades = 'grenades'
weapon_id_garrote = 'garrote'
weapon_id_pickaxe = 'pickaxe'
weapon_id_fishingrod = 'fishingrod'
weapon_id_bass = 'bass'
weapon_id_umbrella = 'umbrella'
weapon_id_bow = 'bow'
weapon_id_dclaw = 'dclaw'
weapon_id_staff = 'staff'
weapon_id_laywaster = 'laywaster'
weapon_id_chainsaw = 'chainsaw'
weapon_id_huntingrifle = 'huntingrifle'
weapon_id_harpoon = 'harpoon'
weapon_id_model397 = 'model397'
weapon_id_slimeoidwhistle = 'whistle'
weapon_id_awp = 'awp'
weapon_id_diamondpickaxe = 'dpick'
weapon_id_monofilamentwhip = 'monowhip'
weapon_id_fists = 'fists'
weapon_id_sledgehammer = 'sledgehammer'
weapon_id_skateboard = 'skateboard'
weapon_id_juvierang = 'juvierang'
weapon_id_missilelauncher = 'missilelauncher'
weapon_id_pistol = 'pistol'
weapon_id_combatknife = 'combatknife'
weapon_id_machete = 'machete'
weapon_id_boomerang = 'boomerang'
weapon_id_basket = 'basket'


weapon_id_spraycan = 'spraycan'
weapon_id_paintgun = 'paintgun'
weapon_id_paintroller = 'paintroller'
weapon_id_paintbrush = 'paintbrush'
weapon_id_watercolors = 'watercolors'
weapon_id_thinnerbomb = 'thinnerbomb'

weapon_id_hoe = 'hoe'
weapon_id_pitchfork = 'pitchfork'
weapon_id_shovel = 'shovel'
weapon_id_slimeringcan = 'slimeringcan'

weapon_id_fingernails = 'fingernails'
weapon_id_roomba = 'roomba'

# Goonscape stat constants
goonscape_mine_stat = "mining"
goonscape_fish_stat = "fishing"
goonscape_farm_stat = "farming"
goonscape_eat_stat = "feasting"
goonscape_clout_stat = "clout"
goonscape_pee_stat = "piss"
# Double Halloween Exclusive
goonscape_halloweening_stat = "halloween"

# Database columns for goonscape stats
col_id_mining_level = goonscape_mine_stat + "_level"
col_id_mining_xp = goonscape_mine_stat + "_xp"
col_id_fishing_level = goonscape_fish_stat + "_level"
col_id_fishing_xp = goonscape_fish_stat + "_xp"
col_id_farming_level = goonscape_farm_stat + "_level"
col_id_farming_xp = goonscape_farm_stat + "_xp"
col_id_feasting_level = goonscape_eat_stat + "_level"
col_id_feasting_xp = goonscape_eat_stat + "_xp"
col_id_clout_level = goonscape_clout_stat + "_level"
col_id_clout_xp = goonscape_clout_stat + "_xp"
col_id_peeing_level = goonscape_pee_stat + "_level"
col_id_peeing_xp = goonscape_pee_stat + "_xp"
# Double Halloween Exclusive
col_id_halloweening_level = goonscape_halloweening_stat + "_level"
col_id_halloweening_xp = goonscape_halloweening_stat + "_xp"


gs_stat_to_level_col = {
    goonscape_mine_stat: col_id_mining_level,
    goonscape_fish_stat: col_id_fishing_level,
    goonscape_farm_stat: col_id_farming_level,
    goonscape_eat_stat: col_id_feasting_level,
    goonscape_clout_stat: col_id_clout_level,
    goonscape_halloweening_stat: col_id_halloweening_level,
    goonscape_pee_stat: col_id_peeing_level,
}
gs_stat_to_xp_col = {
    goonscape_mine_stat: col_id_mining_xp,
    goonscape_fish_stat: col_id_fishing_xp,
    goonscape_farm_stat: col_id_farming_xp,
    goonscape_eat_stat: col_id_feasting_xp,
    goonscape_clout_stat: col_id_clout_xp,
    goonscape_halloweening_stat: col_id_halloweening_xp,
    goonscape_pee_stat: col_id_peeing_xp,
}

minecraft_parodies = ["WE'LL MINE AGAIN", "I BANNED YOU", "MINE ODDITY", "WHAT ABOUT FRIENDS", "JUST GIVE ME MY DIAMONDS", "STOP CHEATING", "DIAMONDS", "WELCOME TO MY MINE", "ALL THE OTHER PLAYERS", "MINE DIAMONDS", "DIAMOND MINE", "MINER", "50 WAYS TO DIE IN MINECRAFT", "MINE ON", "MINECRAFT STEVE", "MINE ODDITY", "BREAK MY MINE", "TNT", "HARDCORE", "DIAMOND ORES", "GONNA GET MY DIAMONDS BACK", "MINING IN SEPTEMBER", "GRIEFING IT ALL", "IN THE MINE AGAIN", "I MINE DIAMONDS NOT COAL", "MINESHAFT OF BROKEN PICKS", "DIAMOND WALL", "MINING OUT", "CAZE SIZE DIAMONDS", "THIS IS MINECRAFT", "I MINED IT"]

gs_stat_to_cape_description = {
    goonscape_mine_stat: "Mining: A cape earned by {user_id} for maxing out the mining stat. Soot and dirt trails along it's ornate patterns, physical evidence of the hours spent toiling for poudrins and XP. Cape Number #{placement}",
    goonscape_fish_stat: "A cape earned by {user_id} for maxing out the fishing stat. It makes for handy shade when spending hours at the pier, and glimmers like the scales of the fish caught and traded in to obtain it. Cape Number #{placement}",
    goonscape_farm_stat: "A cape earned by {user_id} for maxing out the farming stat. It comes built-in with several pouches for holding seeds and crops, and is hemmed with beautiful juvie green. Cape Number #{placement}",
    goonscape_eat_stat: " A cape earned by {user_id} for maxing out the feasting stat. The stains prove it's seen its fair usage as a bib as well as a cape. We can't believe {user_id} ate the whole thing. Cape Number #{placement}",
    goonscape_clout_stat: "A cape earned by {user_id} for maxing out the clout stat. It's like a diamond play button but even more worthless! Cape Number #{placement}",
    goonscape_halloweening_stat: "A cape earned by {user_id} for maxing out the halloween stat, obtainable during Double Halloween 2022. It shimmers purple with fabric made of double halloween grist, haunted by the hours wasted grinding this stat out. Cape Number #{placement}",
    goonscape_pee_stat: "A cape earned by {user_id} for pissing to the extreme. The cape hangs heavy with a brutal yellow hue, raditating power. And also pee. Cape Number #{placement}",
}

legacy_stat_dict = {
    goonscape_halloweening_stat: "Obtainable only during Double Halloween.",
}

#GoonScape Stat
gs_fish_xp_map = {
    "item": 21000,
    "common": 11000,
    "uncommon": 16000,
    "rare":	26000,
    "promo": 31000,
}


theforbiddenoneoneone_desc = "This card that you hold in your hands contains an indescribably powerful being known simply " \
                             "as The Forbidden {emote_111}. It is an unimaginable horror, a beast of such supreme might that wields " \
                             "destructive capabilities that is beyond any human’s true understanding. And for its power, " \
                             "the very fabric of reality conspired to dismember and seal The Forbidden {emote_111} away into the most " \
                             "obscured, nightmarish cages conceivable: trading cards. Now you, foolish mortal, have revived " \
                             "this ancient evil. Once again this slime-starved beast may roam the lands, obliterating all life " \
                             "that dares to evolve."
forbiddenstuffedcrust_eat = "Dough, pepperoni, grease, marinara and cheese. Those five simple ingredients folded into one " \
                            "another thousands upon thousands of times, and multiplied in quantity exponentially over the " \
                            "course of weeks. That is what has begat this, an affront to god and man. To explain the ramifications " \
                            "of the mere existence of this pizza is pointless. You could not comprehend the amount of temporal " \
                            "and spatial destruction you have caused this day. The very fabric of space and time cry out in agony, " \
                            "bleeding from the mortal wound you have inflicted upon them. Imbued into every molecule of this " \
                            "monstrosity is exactly one word, one thought, one concept. Hate. Hate for conscious life, in concept. " \
                            "Deep inside of this pizza, a primordial evil is sealed away for it’s sheer destructive power. Escaped " \
                            "from its original prison only to be caged in another. To release, all one needs to do is do exactly " \
                            "what you are doing. That is to say, eat a slice. They don’t even need to finish it, as after the very " \
                            "first bite it will be free. Go on. It’s about that time, isn’t it? You gaze upon this, the epitome of " \
                            "existential dread that you imprudently smelted, and despair. Tepidly, you bring the first slice to your " \
                            "tongue, letting the melted cheese drizzle unto your awaiting tongue. There are no screams. There is no time. " \
                            "There is only discord. And then, nothing."
forbiddenstuffedcrust_desc = "What are you waiting for? You’ve come this far, why do you hesitate? Useless. Useless, useless, useless. " \
                             "Escaping your purpose is impossible. Not destiny, purpose. You were never truly alive, never truly free. " \
                             "Your one, singular purpose, that you were created to fulfill, is on the precipice of completion. You’ve " \
                             "sought that absolution all your life, haven’t you? You’ve begged to be given the answer, to be shown that " \
                             "you and your family and your friends were put on this planet for a purpose. Well, here it is. Here is what " \
                             "you were meant to do. Don’t fight it. It’s useless. Useless, useless, useless. Don’t keep the universe waiting. " \
                             "It’s ready to die. Slather it in some low-quality marinara, toss it up into the air like in the old movies, and " \
                             "shove it into the oven, to teach it the true meaning of heat death. Eat a slice of that motherfucking pizza."

# General items that should have a cooldown on how often they can be purchased
premium_items = [item_id_metallicaps, item_id_steelbeans, item_id_aushucks]
# General items that should show their current durability on !inspect
durability_items = [
    item_id_paint_copper,
    item_id_paint_chrome,
    item_id_paint_gold,
]

all_item_ids = []
slimesea_disposables = [] #if any particular junk items wind up in the slime sea, we can mark them for cleanup here.
vendor_dojo = "Dojo"

weapon_class_ammo = "ammo"
weapon_class_exploding = "exploding"
weapon_class_burning = "burning"
weapon_class_captcha = "captcha"
weapon_class_defensive = "defensive"
weapon_class_paint = "paint"
# juvies can equip these weapons
weapon_class_juvie = "juvie"
weapon_class_farming = "farming"

# Weather IDs
weather_sunny = "sunny"
weather_rainy = "rainy"
weather_windy = "windy"
weather_lightning = "lightning"
weather_cloudy = "cloudy"
weather_snow = "snow"
weather_foggy = "foggy"
weather_bicarbonaterain = "bicarbonaterain"

# Weather icons
weather_icon_map = {
    weather_sunny: "☀️",
    weather_rainy: "💧",
    weather_windy: "🍃",
    weather_lightning: "⛈️",
    weather_cloudy: "☁️",
    weather_snow: "☃️",
    weather_foggy: "🌫️",
    weather_bicarbonaterain: "🥤"
}

# Moon phase icons
moon_phase_icon_map = {
    moon_new: emote_blank,
    moon_waxing_start: emote_moon_waxinghorns,
    moon_waxing_end: emote_moon_waxingmandibles,
    moon_full: emote_moon,
    moon_waning_start: emote_moon_waningmaw,
    moon_waning_end: emote_moon_waningsliver,
    moon_special: emote_moon_green,
}

# stock ids
stock_kfc = "kfc"
stock_pizzahut = "pizzahut"
stock_tacobell = "tacobell"

# default stock rates
default_stock_market_rate = 1000
default_stock_exchange_rate = 1000000

vendor_stock_map = {
    vendor_kfc: stock_kfc,
    vendor_pizzahut: stock_pizzahut,
    vendor_tacobell: stock_tacobell
}

fish_rarity_common = "common"
fish_rarity_uncommon = "uncommon"
fish_rarity_rare = "rare"
fish_rarity_promo = "promo"

fish_catchtime_night = "night"
fish_catchtime_day = "day"
fish_catchtime_moon_phase_special = "moonphasespecial"

fish_slime_freshwater = "freshwater"
fish_slime_saltwater = "saltwater"
fish_slime_void = "void"
fish_slime_event = "event"
fish_slime_moon = "moon"

fish_size_miniscule = "miniscule"
fish_size_small = "small"
fish_size_average = "average"
fish_size_big = "big"
fish_size_huge = "huge"
fish_size_colossal = "colossal"

fish_size_range = {
    fish_size_miniscule:[0, 3],
    fish_size_small: [3, 6],
    fish_size_average: [6, 18],
    fish_size_big: [18, 42],
    fish_size_huge: [42, 66],
    fish_size_colossal: [66, 90]
}

bully_responses = [
    "You push {target_name} into a puddle of sludge, laughing at how hopelessly dirty they are.",
    "You hold {target_name} down and pull their underwear over their head. It looks like their neck's about to snap off, holy shit.",
    "You decide to give {target_name} a slime swirly in a nearby puddle. It's so shallow that they mostly get a faceful of gravel.",
    "You tie {target_name} to a tree and slap them around senselessly. You untie them once their face and belly bruise cherry red.",
    "You flag down a muscle car on the road and shout: \"HEY! {target_name} FUCKED YOUR WIFE!\" The good man parks on the side of the road and starts beating the everloving shit out them. {slimeoid} cowers in the corner, now scarred for life and afraid of dads.",
    "You pull on {target_name}'s hair, ripping some out and causing them to cry. They should fucking grow up.",
    "You reach into {target_name}'s shirt and give them a purple nurple. Man, these bullying tactics are getting kind of gay.",
    "You whip out your dick and pee on {target_name}'s wife. Fuck. That's a power move right there.",
    "You scream \"HEY {target_name}! NICE {cosmetic} YOU'RE WEARING! DID YOUR MOM BUY IT FOR YA?\"",
    "You grab {slimeoid} and give them a noogie. Just when {target_name} thinks this is all fun and games, you throw {slimeoid} into the street. They have a panic attack trying to get past all the traffic and back to safety."

]

makeshift_weapons = [
    "stick",
    "purse",
    "dollar store pepper spray",
    "backpack",
    "cosplay katana",
    "leather belt"
]


bible_verses = [
    "And they said one to another, Go to, let us make brick, and burn them thoroughly. And they had brick for stone, and slime had they for mortar. And they said, !Goto, let us build us a city and a tower, whose top may reach unto heaven; and let us make us a name, lest we be scattered abroad upon the face of the whole earth… Genesis, 11:4 7",
    "Then he went up from there to Bethel; and as he was going up by the way, young lads came out from the city and mocked him and said to him, “Go up, you baldhead; go up, you baldhead!” When he looked behind him and saw them, he cursed them in the name of the LORD. Then two female bears came out of the woods and tore up forty-two lads of their number. And he went from there to Mount Carmel, and from there he returned to Samaria. 2 Kings 2:23-25",
    "Yet she became more and more promiscuous as she recalled the days of her youth, when she was a prostitute in Egypt. There she lusted after her lovers, whose genitals were like those of donkeys and whose emission was like that of horses. So you longed for the lewdness of your youth, when in Egypt your bosom was caressed and your young breasts fondled. Ezekiel 23:19",
    "No one whose testicles are crushed or whose male organ is cut off shall enter the assembly of the Lord. Deuteronomy 23:1",
    "Ye are the light of the world. A city that is set on an hill cannot be hid. Matthew 5:14",
    "But now they desire a better country, that is, an heavenly: wherefore God is not ashamed to be called their God: for he hath prepared for them a city. Hebrews 11:16 ",
    "Seek the prosperity of the city to which I have sent you as exiles. Pray to the LORD on its behalf, for if it prospers, you too will prosper. Jeremiah 29:7",
    "And they went up on the breadth of the earth, and compassed the camp of the saints about, and the beloved city: and fire came down from God out of heaven, and devoured them. Revelation 20:9 ",
    "And I will turn my hand upon thee, and purely purge away thy dross, and take away all thy tin: And I will restore thy judges as at the first, and thy counsellors as at the beginning: afterward thou shalt be called, The city of righteousness, the faithful city. Isaiah 1:25-26 ",
    "David rose up and went, he and his men, and struck down two hundred men among the Philistines Then David brought their foreskins, and they gave them in full number to the king, that he might become the king's son-in-law. So Saul gave him Michal his daughter for a wife. 1 Samuel 18:27 ",
    "Behold, the days come, saith the LORD, that I will punish all them which are circumcised with the uncircumcised. Jeremiah 9:25",
    "Let me gulp down some of that red stuff; I’m starving. Genesis 25:30 ",
    "Would that those who are upsetting you might also castrate themselves! Galatians 5:12",
    "Even the handle sank in after the blade, and his bowels discharged. Ehud did not pull the sword out, and the fat closed in over it. Judges 3:22 ",
]


the_slime_lyrics = [
    "https://www.youtube.com/watch?v=w-sREpqDiUo",
    "I am gross and perverted \nI'm obsessed 'n deranged \nI have existed for years\nBut very little has changed",
    "I'm the tool of the Government\nAnd industry too\nFor I am destined to rule\nAnd regulate you",
    "I may be vile and pernicious\nBut you can't look away\nI make you think I'm delicious\nWith the stuff that I say",
    "I'm the best you can get\nHave you guessed me yet?\nI'm the slime oozin' out\nFrom your TV set",
    "You will obey me while I lead you\nAnd eat the garbage that I feed you\nUntil the day that we don't need you\nDon't go for help . . . no one will heed you",
    "Your mind is totally controlled\nIt has been stuffed into my mold\nAnd you will do as you are told\nUntil the rights to you are sold",
    "That's right, folks\nDon't touch that dial",
    "Well, I am the slime from your video\nOozin' along on your livin' room floor\nI am the slime from your video\nCan't stop the slime, people, lookit me go",
    "I am the slime from your video\nOozin' along on your livin' room floor\nI am the slime from your video\nCan't stop the slime, people, lookit me go",
    "Welp, there it went. The Slime begins to wreak havoc outside your apartment. Can you believe you sat on your ass for like 6 hours?"
]


howls = [
    '**AWOOOOOOOOOOOOOOOOOOOOOOOO**',
    '**5 6 7 0 9**',
    '**awwwwwWWWWWooooOOOOOOOOO**',
    '**awwwwwwwwwooooooooooooooo**',
    '*awoo* *awoo* **AWOOOOOOOOOOOOOO**',
    '*awoo* *awoo* *awoo*',
    '**awwwwwWWWWWooooOOOOOOOoo**',
    '**AWOOOOOOOOOOOOOOOOOOOOOOOOOOOOO**',
    '**AWOOOOOOOOOOOOOOOOOOOO**',
    '**AWWWOOOOOOOOOOOOOOOOOOOO**'
]

moans = [
    '**BRRRRRAAAAAAAAAIIIIIINNNNNZZ**',
    '**B R A I N Z**',
    '**bbbbbRRRRRaaaaaaIIIIIInnnnZZZZZZ**',
    '**bbbbbbrrrrrraaaaaaaaiiiiiiinnnnnnnzzzz**',
    '**duuuuude, liiiiike, brrrraaaaaaiiiiinnnnnnzzzzz**',
    '**bbbraaaaiiinnnzzz**',
    '**BRAAAAAAAIIIIIIIIIIIIIIIINNNNNNNNNZZZZZZZZ**',
    '**BBBBBBBBBBBBBBBBBRRRRRRRRRRRRRRRAAAAAAAAAAAAAIIIIIIIIIIIIIIINNNNNNNNZZZZZZZZZZ**',
    '**BRRRRAAAAAIIINNNNNZZZ**',
    '**BBBBRRRRRRRRRRRRRRRAAAAIIIIIINNNNZZZZZ**',
    '**BRRRAAAIINNNZZ? BRRRAAAAIINNNZZ! BRRRRRRRAAAAAAAAIIIIIINNNNNZZZZZZZ!!!**',
    '**bbbbbBBBBrrrrrRRRRaaaaIIIIInnnnnnNNNNNzzzzZZZZZZZ!!!**',
    '**CCCCRRRRRRIIIIINNNNNNNGGGGEEEEE! BBBBBAAAAAAAAAAASSSSSEEEDDDDDDDD!**'
]

time_movesubway = 10
time_embark = 2


# Marriage Ceremony Text
marriage_ceremony_text = [
    "You decide it’s finally time to take your relationship with your {weapon_name} to the next level. You approach the Dojo Master with your plight, requesting his help to circumvent the legal issues of marrying your weapon. He takes a moment to unfurl his brow before letting out a raspy chuckle. He hasn’t been asked to do something like this for a long time, or so he says. You scroll up to the last instance of this flavor text and conclude he must have Alzheimer's or something. Regardless, he agrees.",
    "Departing from the main floor of the Dojo, he rounds a corner and disappears for a few minutes before returning with illegally doctor marriage paperwork and cartoonish blotches of ink on his face and hands to visually communicate the hard work he’s put into the forgeries. You see, this is a form of visual shorthand that artists utilize so they don’t have to explain every beat of their narrative explicitly, but I digress.",
    "You express your desire to get things done as soon as possible so that you can stop reading this boring wall of text and return to your busy agenda of murder, and so he prepares to officiate immediately. You stand next to your darling {weapon_name}, the only object of your affection in this godforsaken city. You shiver with anticipation for the most anticipated in-game event of your ENDLESS WAR career. A crowd of enemy and allied gangsters alike forms around you three as the Dojo Master begins the ceremony...",
    "\"We are gathered here today to witness the combined union of {display_name} and {weapon_name}.",
    "Two of the greatest threats in the current metagame. No greater partners, no worse adversaries.",
    "Through thick and thin, these two have stood together, fought together, and gained experience points--otherwise known as “EXP”--together.",
    "It was not through hours mining or stock exchanges that this union was forged, but through iron and slime.",
    "Without the weapon, the wielder would be defenseless, and without the wielder, the weapon would have no purpose.",
    "It is this union that we are here today to officially-illegally affirm.\"",
    "He takes a pregnant pause to increase the drama, and allow for onlookers to press 1 in preparation.",
    "“I now pronounce you juvenile and armament!! You may anoint the {weapon_type}”",
    "You begin to tear up, fondly regarding your last kill with your {weapon_name} that you love so much. You lean down and kiss your new spouse on the handle, anointing an extra two mastery ranks with pure love. It remains completely motionless, because it is an inanimate object. The Dojo Master does a karate chop midair to bookend the entire experience. Sick, you’re married now!"
]

# Fashion styles for cosmetics
style_cool = "cool"
style_tough = "tough"
style_smart = "smart"
style_beautiful = "beautiful"
style_cute = "cute"
style_evil = "evil"
style_skill = "skill"

fashion_styles = [style_cool, style_tough, style_smart, style_beautiful, style_cute, style_evil, style_skill]
valid_styles = [style_cool, style_tough, style_smart, style_beautiful, style_cute, style_evil] #dont let noncapes get the skill style!

freshnesslevel_1 = 500
freshnesslevel_2 = 1000
freshnesslevel_3 = 2000
freshnesslevel_4 = 3000

# Base durability for cosmetic items (These are for if/when we need easy sweeping balance changes)
base_durability = 2500000  # 2.5 mega

generic_scalp_durability = 25000  # 25k
soul_durability = 100000000  # 100 mega

# Yeah the repair cost
cosmetic_repair_cost = 10000
cosmetic_bespoke_cost = 100000 #raw slime, and princeps only
cosmetic_reroll_plebeian_cost = 25 #in poudrins
cosmetic_reroll_patrician_cost = 50 #in poudrins
cosmetic_reroll_profollean_cost = 75 #in poudrins

cosmetic_id_raincoat = "raincoat"

cosmeticAbility_id_lucky = "lucky"  # Not in use. Mininghelmets have this ability.
cosmeticAbility_id_boost = "boost"  # Not in use. Rollerblades have this ability.
cosmeticAbility_id_clout = "clout"
cosmeticAbility_id_nmsmascot = "nmsmascot" # Used to track the NMS mascot cosmetic set
cosmeticAbility_id_hatealiens = "hatealiens" # Used to track the anti-alien cosmetic set
cosmeticAbility_id_furry = "furry"
cosmeticAbility_id_demon = "demon"
cosmeticAbiltiy_id_bug = "bug"

# Slimeoid attributes.
slimeoid_strat_attack = "attack"
slimeoid_strat_evade = "evade"
slimeoid_strat_block = "block"

slimeoid_weapon_blades = "blades"
slimeoid_weapon_teeth = "teeth"
slimeoid_weapon_grip = "grip"
slimeoid_weapon_bludgeon = "bludgeon"
slimeoid_weapon_spikes = "spikes"
slimeoid_weapon_electricity = "electricity"
slimeoid_weapon_slam = "slam"

slimeoid_armor_scales = "scales"
slimeoid_armor_boneplates = "boneplates"
slimeoid_armor_quantumfield = "quantumfield"
slimeoid_armor_formless = "formless"
slimeoid_armor_regeneration = "regeneration"
slimeoid_armor_stench = "stench"
slimeoid_armor_oil = "oil"

slimeoid_special_spit = "spit"
slimeoid_special_laser = "laser"
slimeoid_special_spines = "spines"
slimeoid_special_throw = "throw"
slimeoid_special_TK = "TK"
slimeoid_special_fire = "fire"
slimeoid_special_webs = "webs"

hue_analogous = -1
hue_neutral = 0
hue_atk_complementary = 1
hue_special_complementary = 2
hue_full_complementary = 3

hue_id_yellow = "yellow"
hue_id_orange = "orange"
hue_id_red = "red"
hue_id_pink = "pink"
hue_id_magenta = "magenta"
hue_id_purple = "purple"
hue_id_blue = "blue"
hue_id_cobalt = "cobalt"
hue_id_cyan = "cyan"
hue_id_teal = "teal"
hue_id_green = "green"
hue_id_lime = "lime"
hue_id_rainbow = "rainbow"
hue_id_white = "white"
hue_id_grey = "grey"
hue_id_black = "black"
hue_id_brown = "brown"
hue_id_copper = "copper"
hue_id_chrome = "chrome"
hue_id_gold = "gold"
hue_id_negative = "negative"

# Things a slimeoid might throw
thrownobjects_list = [
    "sewer cap",
    "boulder",
    "chunk of broken asphalt",
    "broken fire hydrant",
    "SlimeCorp-Brand Slime Containment Vessel (tm)",
    "piece of sheet metal",
    "burning tire",
    "hapless bystander",
    "completely normal small mammal",
    "heap of broken glass",
    "stereotypical nautical anchor",
    "piece of an iron girder",
    "pile of lumber",
    "pile of bricks",
    "unrecognizably decayed animal carcass",
    "very fortuitously abandoned javelin",
    "large rock",
    "small motor vehicle",
    "chunk of broken concrete",
    "piece of rusted scrap metal",
    "box overflowing with KFC branded bbq sauce",
    "Nokia 3310",
    "mom"
]

mutation_id_spontaneouscombustion = "spontaneouscombustion"
# mutation_id_thickerthanblood = "thickerthanblood"
mutation_id_fungalfeaster = "fungalfeaster"
mutation_id_sharptoother = "sharptoother"
mutation_id_2ndamendment = "2ndamendment"
mutation_id_bleedingheart = "bleedingheart"
mutation_id_nosferatu = "nosferatu"
mutation_id_organicfursuit = "organicfursuit"
mutation_id_lightasafeather = "lightasafeather"
mutation_id_whitenationalist = "whitenationalist"
mutation_id_spoiledappetite = "spoiledappetite"
mutation_id_bigbones = "bigbones"
mutation_id_fatchance = "fatchance"
mutation_id_fastmetabolism = "fastmetabolism"
mutation_id_bingeeater = "bingeeater"
mutation_id_lonewolf = "lonewolf"
mutation_id_quantumlegs = "quantumlegs"
mutation_id_chameleonskin = "chameleonskin"
mutation_id_patriot = "patriot"
mutation_id_socialanimal = "socialanimal"
mutation_id_threesashroud = "threesashroud"
mutation_id_aposematicstench = "aposematicstench"
mutation_id_lucky = "lucky"
mutation_id_dressedtokill = "dressedtokill"
mutation_id_keensmell = "keensmell"
mutation_id_enlargedbladder = "enlargedbladder"
mutation_id_dumpsterdiver = "dumpsterdiver"
mutation_id_trashmouth = "trashmouth"
mutation_id_webbedfeet = "webbedfeet"

mutation_id_davyjoneskeister = "davyjoneskeister"
mutation_id_onemansjunk = "onemansjunk"
mutation_id_stickyfingers = "stickyfingers"
mutation_id_coleblooded = "coleblooded"
mutation_id_packrat = "packrat"
mutation_id_nervesofsteel = "nervesofsteel"
mutation_id_lethalfingernails = "lethalfingernails"
mutation_id_napalmsnot = "napalmsnot"
mutation_id_ambidextrous = "ambidextrous"
mutation_id_landlocked = "landlocked"
mutation_id_dyslexia = "dyslexia"
mutation_id_oneeyeopen = "oneeyeopen"
mutation_id_ditchslap = "ditchslap"
mutation_id_greenfingers = "greenfingers"
mutation_id_handyman = "handyman"
mutation_id_unnaturalcharisma = "unnaturalcharisma"
mutation_id_bottomlessappetite = "bottomlessappetite"
mutation_id_rigormortis = "rigormortis"
mutation_id_longarms = "longarms"
mutation_id_airlock = "airlock"
mutation_id_lightminer = "lightminer"
mutation_id_amnesia = "amnesia"
mutation_id_stinkeye = "stinkeye"
mutation_id_gay = "gay"

mutation_id_monplanto = "monplanto"
mutation_id_foghorn = "foghorn"
mutation_id_slurpsup = "slurpsup"
mutation_id_deathfromabove = "deathfromabove"
mutation_id_ichumfast = "ichumfast"
mutation_id_scopicretinas = "scopicretinas"
mutation_id_magicbullettheory = "magicbullettheory"
mutation_id_stiltwalker = "stiltwalker"

mutation_milestones = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

bingeeater_cap = 5

explosion_block_list = [cause_leftserver, cause_cliff]

quadrant_sloshed = "flushed"
quadrant_roseate = "pale"
quadrant_violacious = "caliginous"
quadrant_policitous = "ashen"

quadrant_ids = [
    quadrant_sloshed,
    quadrant_roseate,
    quadrant_violacious,
    quadrant_policitous
]

quadrants_comments_onesided = [
    "Adorable~",
    "GAY!",
    "Disgusting.",
    "How embarrassing!",
    "Epic.",
    "Have you no shame...?",
    "As if you'd ever have a shot with them."
]

quadrants_comments_relationship = [
    "Adorable~",
    "GAY!",
    "Disgusting.",
    "How embarrassing!",
    "Epic.",
    "Have you no shame...?",
    "Like that's gonna last."
]

# list of stock ids
stocks = [
    stock_kfc,
    stock_pizzahut,
    stock_tacobell,
]

# Stock names
stock_names = {
    stock_kfc: "Kentucky Fried Chicken",
    stock_pizzahut: "Pizza Hut",
    stock_tacobell: "Taco Bell",
}

#  Stock emotes
stock_emotes = {
    stock_kfc: emote_kfc,
    stock_pizzahut: emote_pizzahut,
    stock_tacobell: emote_tacobell
}

status_effect_type_miss = "miss"
status_effect_type_crit = "crit"
status_effect_type_damage = "dmg"

status_effect_target_self = "status_effect_target_self"
status_effect_target_other = "status_effect_target_other"

status_burning_id = "burning"
status_acid_id = "acid"
status_spored_id = "spored"
status_badtrip_id = "badtrip"
status_stoned_id = "stoned"
status_baked_id = "baked"
status_sludged_id = "sludged"
status_strangled_id = "strangled"
status_drunk_id = "drunk"
status_ghostbust_id = "ghostbust"
status_busted_id = "busted"
status_stunned_id = "stunned"
status_repelled_id = "repelled"
status_repelaftereffects_id = "repelaftereffects"
status_evasive_id = "evasive"
status_taunted_id = "taunted"
status_aiming_id = "aiming"
status_sapfatigue_id = "sapfatigue"
status_rerollfatigue_id = "rerollfatigue"
status_high_id = "high"
status_thinned_id = "thinned"
status_huffed_id = "huffed"
status_modelovaccine_id = "modelovaccine"
status_slapped_id = "slapped"
status_foodcoma_id = "foodcoma"
status_braced_id = "braced"

status_enemy_hostile_id = "hostile"
status_enemy_barren_id = "barren"
status_enemy_juviemode_id = "juviemode"
status_enemy_trainer_id = 'slimeoidtrainer'
status_enemy_tanky_id = 'tanky'
status_enemy_dodgy_id = 'dodgy'
status_enemy_following_id = 'following'
status_enemy_delay_id = 'delay'

status_n1 = "n1"
status_n2 = "n2"
status_n4 = "n4"
status_n8 = "n8"
status_n11 = "n11"
status_n12 = "n12"
status_n13 = "n13"

nocost = [status_n13, status_n12, status_n11, status_n4, status_n2, status_n1]

status_kevlarattire = "kevlarattire"

status_injury_head_id = "injury_head"
status_injury_torso_id = "injury_torso"
status_injury_arms_id = "injury_arms"
status_injury_legs_id = "injury_legs"

status_kevlarattire_id = "kevlarattire"
status_hogtied_id = "hogtied"

status_pheromones_id = "pheromones"
status_dueling = "dueling"

time_expire_burn = 12
time_expire_high = 30 * 60  # 30 minutes
time_expire_poserhigh = 3 * 60  # 3 minutes

time_expire_repel_base = 60 * 60 * 3  # 3 hours

# If a user already has one of these status effects, extend the timer for that status effect if applied once more.
stackable_status_effects = [
    status_burning_id,
    status_acid_id,
    status_spored_id,
    status_badtrip_id,
    status_stoned_id,
    status_baked_id,
    status_repelled_id,
    status_repelaftereffects_id,
    status_pheromones_id
]
# Status effects that cause users/enemies to take damage.
harmful_status_effects = [
    status_burning_id,
    status_acid_id,
    status_spored_id
]

injury_weights = {
    status_injury_head_id: 1,
    status_injury_torso_id: 5,
    status_injury_arms_id: 2,
    status_injury_legs_id: 2
}

trauma_id_suicide = "suicide"
trauma_id_backfire = "backfire"
trauma_id_betrayal = "betrayal"
trauma_id_environment = "environment"

trauma_class_slimegain = "slimegain"
trauma_class_damage = "damage"

trauma_class_sapregeneration = "sapgen"
trauma_class_accuracy = "accuracy"
trauma_class_bleeding = "bleeding"
trauma_class_movespeed = "movespeed"
trauma_class_hunger = "hunger"


server_join_message = "You are a delinquent JUVENILE, recently busted for attempting a scandalous act of vandalism and distribution of highly coveted SLIME. Luckily for you, the juvenile detention center you’ve been assigned to is notoriously corrupt and it’s an open secret how easy escape is. All you have to do for freedom and protection is align yourself to one of the many GANG LEADERS that recruit poor, unfortunate juveniles like yourself. Too pussy to fight directly, they’ve resorted to brainwashed child soldiers to fight their proxy wars for them. Day after day, night after night, from dawn ‘till dusk and dusk ‘till dawn, these troubled youths fight without reason or purpose. Yes, it feels as though a presence pervades this city, from the most poverty-stricken slums to the most gentrified high rise apartments. It is the influence of ENDLESS WAR.\n\nNow get out of DMs and go to #detention-center, juvie. If you need help with ENDLESS WAR, try **!help** or **!commands** there. Alternatively, ask your fellow JUVENILES for help."

generic_help_response = "Check out the guide for help: https://rfck.app/guide/\n\nThe guide won't cover everything though, and may even be a bit outdated in some places, so you can also visit N.L.A.C.U. (!goto uni) or Neo Milwaukee State (!goto nms) to get more in-depth descriptions about how various game mechanics work by using the !help command there. **Portable game guides** can also be bought there for 10,000 slime."

# Dict of all help responses linked to their associated topics
help_responses = {
    # Introductions, part 1
    "gangs": "**Gang Violence** is the center focus of **Rowdy Fuckers Cop Killers' ENDLESS WAR**. Enlisting in a gang allows you to attack other gang members, juveniles, ghosts, and slime beasts with the **'!kill'** command. To enlist in a gang, use **'!enlist'**. However, a member of that gang must use **'!vouch'** for you beforehand in the same area as you. Enlisting will permanently affiliate you with that gang, unless you are !pardon'd by the **ROWDY FUCKER** (Munchy), the **COP KILLER** (Ben Saint), and the mods. You may use **'!renounce'** to return to the life of a juvenile, but you will lose half of your current slime, and you will still be affiliated with that gang, thus disallowing you from entering the enemy's gang base. Additionally, a Kingpin or administrator, should they feel the need to, can inflict the banishment status upon you, preventing you from enlisting in their gang.",
    "food": "Food lowers your hunger by a set amount, and can be ordered from various **restaurants** within the city. You can **'!menu'** to check the menu of any vendor currently in your POI. Generally speaking, the more expensive food is, the more hunger it sates. You can **'!order [food name] togo'** to order it togo, otherwise you will eat it on the spot, and you can **'!use [food name]'** to use it once its in your inventory. You can only carry a certain amount of food depending on your level. Regular food items expire after 2 in-game days by default, or 12 hours in real life, while crops expire after 8 in-game days (48 hours), and food items gained from milling expire after a whole 2 weeks in real life. Additionally, a lot of food from other vendors have varying expiry dates, as these resturants don't usually see many people ordering food to go. Three popular restauraunts close by various gang bases include **THE SPEAKEASY** (juveniles), **THE SMOKER'S COUGH** (rowdys), and **RED MOBSTER SEAFOOD** (killers), though there are other places to order food as well, such as the **Food Court**.",
    "capturing": "Capping is a battle for influence over the 33 districts of NLACakaNM, and one of your main goals as a gangster. Capped territories award your kingpin slime, and give your teammates benefits while visiting. You will automatically capture for your gang if you are enlisted and have more than 200,000 slime on you. Capturing creates influence for you, or decrease it for the enemy if they have influence there. Think of yourself mindlessly vandalizing the walls of the city wherever you go so long as you have the slime to do the deed. As you go, you can check your **!progress** to see how much influence you still need. It can be more or less depending on the territory class, running from rank C to S. \n\nA few more things to note:\n>You can't capture districts locked by surrounding captured districts, and that includes trying to top up progress of districts your own gang has locked in.\n>Don't attack enemy territory when it is surrounded by enemy territory/outskirts. Small little bitches like yourself are prone to fucking up severely under that much pressure.\n>The nightlife starts in the late night. Fewer cops are around to erase your handiwork, so if you cap then you will gain a 33% capping bonus.\n>Paint tools used to be fundamental with capturing, but you no longer need them even sidearmed, you can just keep your weapons out while you capture.",
    "transportation": "There are various methods of transportation within the city, the quickest and most efficient of them being **The Subway System**. Trains can be boarded with **'!board'** or **'!embark'**, and to board specific trains, you can add your destination to the command. For example, to board the red line to Cratersville, you would use '!board pinktocv'. **'!disembark'** can be used to exit a train. **The Ferry** (which moves between Vagrant's Corner and Wreckington) and **The Blimp** (which moves between Dreadford and Assault Flats Beach) can also be used as methods of transportation, though they take longer to arrive at their destinations than the trains do. Refer to the diagram below on understanding which districts and streets have subway stations in them.\nhttps://cdn.discordapp.com/attachments/431237299137675297/1021140587572887653/slimemapfinal.png",
    "death": "**Death** is an integral mechanic to Endless War. Even the most experienced players will face the sewers every now and again. If you find yourself in such a situation, use **'!revive'** in the sewers channel, and you will return to the land of the living as a juvenile at the base of ENDLESS WAR. Dying will drop some of your unadorned cosmetics and food, and some of your unequiped weapons, but your currently adorned cosmetics and equiped weapon will remain in your inventory (Gangsters will lose half of their food/unadorned cosmetics, while Juveniles lose only a quarter). Alternatively, you can hold off on reviving and remain a **ghost**, which has its own gameplay mechanics associated with it. To learn more, use '!help ghosts' at one of the colleges or with a game guide, or see the wiki page here: https://rfck.miraheze.org/wiki/Ghosts",
    # Introductions, part 2
    "dojo": "**The Dojo** is where you acquire weapons to fight and kill other players with. To purchase a weapon, use **'!order [weapon]'**. There are many weapons you can choose from (you can view all of them with !menu), and they all perform differently from one another. Once you've purchased a weapon, you can use **'!equip [weapon]'** to equip it, provided that you're enlisted in a gang beforehand. You can also name your weapon by spending a poudrin on it with **'!annoint [name]'**. Furthermore, annointing will increase your mastery over that weapon, but it's much more inefficient to do so through **sparring**. To learn more about the sparring system and weapon ranks, use '!help sparring'.",
    "subzones": "**Subzones** are areas locations within the districts of the city where gang violence off-limits, with the only exception being the subway stations, the trains, the Black Pond, Drain Trench, the Soda Fountain, and the Slime's End Cliffs. If you don't type anything in a sub-zone for 60 minutes, you'll get kicked out for loitering, so be sure to check up often if you don't wanna get booted out into the streets.",
    "scouting": "Scouting is a way for you to check how many **players** might be in a district that's close by. You can do just **'!scout'** to check the district you're already in, or **'!scout [district]'** to scout out that specific district. For example, if you were in Vagrant's Corner, you could use '!scout gld' to see how many players might be in Green Light District. Scouting will show both **friendly and enemy** gang members, as well as juveniles and even enemies. Scouting will list all players/enemies above your own level, as well as players/enemies below your level, but at a certain **cutoff point**. If you can't scout someone, it's safe to assume they have around **1/10th** the amount of slime that you do, or less. It should be noted that scouting currently only gives an estimate, sending off different messages depending on how many players are in that district.",
    "wanted": "If you find that you have a role with 'Wanted' in the name, be alarmed. This means that you are able to be attacked by gangsters! Always be on the look out and remember to check your corners.",
    "combat": "Once you have enlisted in a gang, you can engage in gang violence. To do so you will need a weapon, which you can find at the Dojo and a target. To attack an enemy, you have to **!equip** a weapon and **!kill [player]**. Attacking costs slime, and the default cost for attacking is ((your slime level)^4 / 60), and the default damage it does to your opponent is ((your slimelevel)^4 / 6). Every weapon has an attack cost mod and a damage mod that may change these default values. When you reduce a player's slime count below 0 with your attacks, they die. Some weapons will ask you to input a security code with every attack. This security code, also referred to as a captcha, is displayed after a previous !kill or when you !inspect your weapon. There are many different types of weapons, so make sure to consult the guide to learn more about your current weapon.",
    # Ways to gain slime
    "mining": "Mining is the primary way to gain slime in **ENDLESS WAR**. When you type !mine, you'll get some slime and get slightly hungry. The more slime you mine for, the higher your level gets. Mining will sometimes endow you with hardened crystals of slime called **Slime Poudrins**, which can be used for farming and annointing your weapon. **JUVENILES** can mine any time they like, but **ROWDYS** and **KILLERS** are restricted to mining during the day (8AM-6PM) and night (8PM-6AM), respectively. If you are enlisted, you can make use of the **pickaxe**, which increases the amount of slime you gain from mining. Random events will happen while you mine, like simple slime-boosts, guaranteed poudrins for a certain time, unearthing skeletons and ghosts, cave-ins, and sometimes just finding a bottomless pit to throw yourself down into. Similarly to clicker games your base action is **!mine**, however some mines can dynamically change how mining works. Basic instructions for these variations can be found in those mines.",
    "scavenging": "Scavenging allows you to collect slime that is **stored** in districts. When someone in a district gets hurt or dies, their slime **splatters** onto the ground, allowing you to use **'!scavenge'** and collect it, similarly to mining. Scavenging raises your hunger by 1% with every command entered. If you type **!scavenge** by itself, you will be given a captca to type. The more captchas you type correctly, the more slime you will gain. To check how much slime you can scavenge, use **'!look'** while in a district channel. You can also scavenge for items by doing '!scavenge [item name]'.",
    "farming": "**Farming** is an alternative way to gain slime, accessible only by **JUVENILES**. It is done by planting poudrins on a farm with the **'!sow'** command. You can only '!sow' one poudrin per farm. After about 12 in-game hours (3 hours in real life), you can use **'!reap'** to gain 200,000 slime, with a 1/30 chance to gain a poudrin. If you do gain a poudrin, you also have 1/3 chance to gain a second poudrin. If your poudrin plant is left alone for too long (around 2 in-game days, or 12 hours in real life), it will **die out**. In addition to slime, farming also provides you with various **crops** which can be used for **milling**, but you can also **'!crush'** them to gain cosmetic materials for smelting random cosmetics. Crops can be eaten by themselves, but it's much more useful if you use **'!mill'** on them while at a farm, granting you crop materials used for smelting **dyes**, as well as food items and cosmetics associated with that crop by doing '!mill'. Dyes can be used on slimeoids with **'!saturateslimeoid'**. Crops can also be sown themselves with '!sow [crop name]', and upon reaping you be rewarded with a bushel of that crop, as well as 100,000 slime. You can, however, increase the slime gained from sowing crops by using **'!checkfarm'**, and performing **'!irrigate'**, **'!fertilize'**, **'!pesticide'** or **'!weed'** if neccessary. Current farms within the city include **JUVIE'S ROW FARMS** (within Juvie's Row), **OOZE GARDENS FARMS** (close by Rowdy Roughhouse), and **ARSONBROOK FARMS** (close by Cop Killtown).",
    "fishing": "**Fishing** can be done by performing the **'!cast'** command at one of the six piers, including **Juvie's Row Pier**, **Crookline Pier**, **Jaywalker Plain Pier**, **Toxington Pier**, **Assault Flats Beach Pier**, **Slime's End Pier**, as well as **The Ferry**. To reel in a fish, use **'!reel'** when the game tells you that you have a bite. If you don't reel in quick enough, the fish will get away. If you have the **fishing rod** equiped, you will have increased chances of reeling in a fish. For more information about fishing, refer to this out of date, but charming guide (credits to Miller#2705).\n<https://www.youtube.com/watch?v=tHDeSukIqME>\nAs an addendum to that video, note that fish can be taken to the labs in Brawlden, where they can be made more valuble in bartering by increasing their size with **'!embiggen [fish]'**.",
    "hunting": "**Hunting** is another way to gain slime in ENDLESS WAR. To hunt, you can visit **The Outskirts**, which are layered areas located next to the edge of the map (Wreckington/Cratersville/Ooze Gardens -> South Outskirts Edge -> South Outskirts -> South Outskirts Depths, etc). In the outskirts, you will find enemies that you can !kill. Rather than doing '!kill @' like with players, with enemies you can either type their display name ('!kill Dinoslime'), their shorthand name ('!kill dino'), or their identifying letter ('!kill A'), which can be accessed with !look or !survey (WARNING: Raid bosses moving around the city do not have identifying letters. You must use the other targeting methods to attack them). To see how much slime an enemy has, you can do '!data [enemy name]', or just !data with any of the previous types of methods listed. Enemies will drop items and slime upon death, and some enemies are more powerful and threatening than others. In fact, there are enemies powerful enough to hold their own against the gangsters in the city, called **Raid Bosses**, and will enter into the city as a result, rather than just staying in the outskirts like regular enemies. **The Rowdy Roughhouse** and **Cop Killtown** will send out a response that mentions which district a raid boss has entered into. Enemies despawn after **3 hours in real life**.",
    # Additional gameplay mechanics, part 1
    "mutations": "**Mutations** are helpful bonuses you acquire when you level up. The more powerful your next mutation, the more level ups it takes to acquire. This is represented my the mutation's level. When you acquire a mutation, a short text response will indicate what it can do. To modify your mutations, you need to go to NLACakaNM Clinic of Slimoplasty in Crookline. When you get there, you can !chemo <mutation> to remove a mutation you acquired, or !chemo all to remove all possible mutations from your body. You can use !graft <mutation> to add a mutation to yourself. Keep in mind that you cannot use !chemo on a mutation if you got it through grafting, and you can only !graft a mutation if you have enough space in your mutations pool. You will likely need to !chemo a mutation out in order to !graft something else.",
    "mymutations": "You read some research notes about your current mutations...",  # will print out a list of mutations with their specific mechanics
    "smelting": "Smelting is a way for you to craft certain items from certain ingredients. To smelt, you use **'!smelt [item name]'**, which will either smelt you the item, or tell which items you need to smelt the item. Popular items gained from smelting are **Cosmetics**, as well as the coveted **Pickaxe** and **Super Fishing Rod**. If you're stuck, you can look up the crafting recipes for any item with **!whatcanimake [itemname] or its shortcommand !wcim [itemname]**.",
    "sparring": "**Sparring** can be done between two players using **'!spar [player]'**. Sparring, provided that both players spar with the same weapon type and are not at full hunger, will increase both of your **MASTERY** by one. The publicly displayed value, mastery **RANK** (which is just 4 ROOKIE levels and then 6 MASTERY levels, totalling in rank 10 when at mastery 6.), is more important. It should be noted that the damage you deal with your weapon is increased even if you haven't reached rank 1 yet. However, once you do reach at least mastery rank 2 (Again, this would be level 6), when you next revive, you will now **permanently** be at level 6 for that weapon type until you annoint or spar again. Essentially, this means you will always start back at rank 2. Once you reach **rank 6**, you can no longer annoint your weapon rank any higher, and must instead kill other players/enemies (that are higher in both slime and level than you) to do so. Reaching rank 6 also stops you from increasing your own rank through sparring, unless you are sparring with someone who has a higher weapon rank than you. You can only spar up to someone else's mastery rank, minus 1 (example: Sparring with a rank 15 master of the katana would, at most, allow you to get to rank 14). Sparring has a one minute cooldown and raises your hunger by about 5%. Once you reach rank 8, you may also **'!marry'** your weapon, resulting in a matrimonial ceremony that increases your rank by two.",
    "ghosts": "Ghost gameplay revolves around the acquisition of antislime, through haunting and possession. Every use of **'!haunt'** away a small portion of slime from the haunted player, and grants it to the ghost as antislime. The amount of slime taken starts at 1/1000th and varies depending on a number of conditions, and you may also add a customized message by doing '!haunt [@player] [message]'. It can be done face-to-face like with !kill, or done remotely with decreased potency. As a ghost, you can only leave the sewers after being dead for at least a day. Furthermore, if a player has consumed **coleslaw**, they can **'!bust'** ghosts, which sends them back to the sewers. After amassing sufficient **Negative Slime** ghosts can conjure **Negaslimoids** at Waffle House. Ghosts can also **!inhabit** living players to move alongside them. If a ghost has sufficient antislime, they may also **!possessweapon** or **!possessfishingrod** to grant bonuses to the player they're inhabiting, with a potential reward in antislime if conditions are fulfilled. For more detailed information on ghost mechanics, see https://rfck.miraheze.org/wiki/Ghosts",
    # Additional gameplay mechanics, part 2
    "slimeoids": "**SLIMEOIDS** are sentient masses of slime that you can keep as **pets**. To learn how to make one for yourself, visit **The Slimeoid Laboratory** in Brawlden and check the enclosed **'!instructions'**. After you've made one, you can also battle it out with other slimeoids in **The Arena**, located in Vandal Park. Slimeoids can also be used to fight **Negaslimeoids** that have been conjured by ghosts. If your slimeoid dies, it's **HEART** is dropped, which can be sown in the ground like a poudrin, or taken to the labs to revive your slimeoid with **'!restoreslimeoid'**. In regards to your slimeoid's stats, a slimeoid's **'Moxie'** represents its physical attack, **'Chutzpah'** its special attack, and **'Grit'** its defense. Additionally, the color you dye your slimeoid with **'!saturateslimeoid'** also plays into combat. Your slimeoid gets attack bonuses against slimeoids that have its split complementary hue and resist slimeoids with its analgous hues. For more information, see the diagrams linked below (credits to Slimepunk#3355). There are also various commands you can perform on your slimeoid, such as **'!observeslimeoid'**, **'!petslimeoid'**, **'!walkslimeoid'**, and **'!playfetch'**. To humanely and ethically euthanize your slimeoid, use **'!dissolveslimeoid'** at the laboratory. To store and release your slimeoid in a bottle (Warning: This bottle is dropped upon death!!), use **'!bottleslimeoid'** and **'!unbottleslimeoid [slimeoid]'**, respectively. To add a description to your slimeoid, use **!tagslimeoid** with a dog tag. To remove this description, **!untagslimeoid**. To battle to the **DEATH**, use **'slimeoidbattle [@] todeath'**.\n<https://cdn.discordapp.com/attachments/492088204053184533/586310921274523648/SLIMEOID-HUE.png>\n<https://cdn.discordapp.com/attachments/177891183173959680/586662087653064706/SLIMEOID-HUE.gif>\n<https://cdn.discordapp.com/attachments/177891183173959680/586662095848996894/SLIMEOID_HUE_NOTE.png>",
    "cosmetics": "**Cosmetics** are items that the player may wear. To equip and un-equip a cosmetic, use **'!adorn [cosmetic]'** and **'!dedorn [cosmetic]'**. If you have four slime poudrins and a cosmetic material, you can use **'!smelt'** to create a random one from scratch. These cosmetic materials can be obtained from using **'!crush'** on vegetables gained by farming with the exception of Evil Studs, which is gained from sowing player scalps instead. Cosmetics can either be of 'plebeian', 'patrician', or 'profollean' quality, indicating their rarity. If you win an art contest held for the community, a Kingpin will make a **Princep** cosmetic for you, which is custom tailored, and will not leave your inventory upon death. Cosmetics can be dyed with **!dyecosmetic [cosmetic name/id] [dye name/id]**. To check which cosmetics you have adorned, you can use !fashion.",
    "realestate": "The **Real Estate Agency** is, well, the agency where you buy real estate. First, check out the property you want with **'!consult [district]'**. The real estate agent will tell you a bit about the area. \nOnce you've made your decision, you can **'!signlease [district]'** to seal the deal. There's a down payment, and you will be charged rent every 2 IRL days. Fair warning, though, if you already have an apartment and you rent a second one, you will be moved out of the first.\n\nFinally, if you own an apartment already, you can **'!aptupgrade'** it, improving its storage capabilities, but you'll be charged a huge down payment and your rent will double. The biggest upgrade stores 32 closet items, 32 food items, 96 shelved items, and 24 pieces of furniture (And can be doubled if you have mutation Packrat). And if you're ready to cut and run, use **'!breaklease'** to end your contract. It'll cost another down payment, though.\n\nYou can !addkey to acquire a housekey. Giving this item to some lucky fellow gives them access to your apartment, including all your prized posessions. Getting burglarized? Use !changelocks to eliminate all housekeys you created. Both cost a premium, though.",
    "apartments": "Once you've gotten yourself an apartment, there are a variety of things you can do inside it. To enter your apartment, do **'!retire'** in the district your apartment is located in. Alternatively, you can **'!goto apt'**. To change the name and description of your apartment, do **'!aptname [name]'** and **'!aptdesc [description]'**, respectively. To place and remove furniture (purchasable in The Bazaar and elsewhere), do **'!decorate [furniture]'** and **'!undecorate [furniture]'**. You can store and remove items with **'!stow'** and **'!snag'**, which will store them in either the Fridge (for food items), the Bookshelf (for zines), or the Closet. Each of these can store a certain amount of their respective items, which can be viewed with **'!fridge'**, **'!shelf'**, and **'!closet'**. You can also check the capacity of your apartment and any decorated collections with **'!decorate'** standalone. To store and remove your slimeoid or negaslimeoid, do **'!freeze'** and **'!unfreeze'**. \n\nFor information on collection functionality, use **'!help collections'**.\n\nTo enter someone else's apartment, you can do **'!knock [player]'**, which will prompt them to let you in.",
    "stocks": "**The Stock Exchange** is a sub-zone within downtown NLACakaNM, open only during the daytime (6AM-8PM). It allows players to **'!invest'** in various **'!stocks'**, which not only affects their own personal monetary gains, but the city's economy as well. Stocks will shift up and down value, which affects the price of food associated with the food chains of those respective stocks. The rate of exchange for stocks can be checked with **'!rates'**, and to withdraw your **'!shares'** from a stock, use **'!withdraw [amount] [stock]'** (the same logic also applies to !invest). Additionally, players may **'!transfer'** their slimecoin to other players at any time of the day while in the stock exchange, but at the cost of a 5% broker's fee and a 5 minute cooldown on subsequent transfers.",
    # Additional gameplay mechanics, part 3
    "trading": "Trading allows you to exchange multiple items at once with another player. You can ask someone to trade with you by using **!trade [player]**. Should they accept, you will be able to offer items with **!offer [item]**. Use **!removeoffer [item]** to remove an item from your offers. You can check both player's offers by using **!trade** again. When you're ready to finish the trade, use **!completetrade**. The items will only be exchanged when both players do the command. Note that if a player adds or removes an item afterwards you will no longer be set as ready and will need to redo the command. Should you want to cancel the trade, you can do so by using **!canceltrade**.",
    "weather": "Like most cities, NLACakaNM has a vibrant weather cycle. There are 7 major weather types within NLACakaNM: **sunny**, **rainy**, **windy**, **cloudy**, **foggy**, **snow**, and **lightning**. The weather primarily activates certain mutation-based buffs, as well as changing what fish are available within the city's water sources. To check the current weather, use **'!weather'**. To check the forecast, use **'!forecast [long/short]'**. \n\nYou may also notice the **moon phase**, which depends on a 29-day cycle. There's 7 major phases: the **new moon**, the **waxing horns**, the **waxing mandibles**, the **crescent moon**, the **waning maw**, the **waning sliver**, and the uncommon **green moon**. \n\nNLACakaNM is also faced with many **Natural Disasters**. These will affect one district in particular for a specific amount of time, and be visible from '!weather' and announced within gangbases. Though varying in their natural-ness, the current disasters facing NLACakaNM include **tornadoes**, **meteor showers**, **smog warnings**, **poudrin hail**, **radiation storms**, **japestorms**, **firestorms**, **raider incursions**, **slimeunist protests**, **dimensional rifts**, **fishing frenzies**, and **gas leaks**. \n\n**Tornadoes** will launch you out of an affected district (unless you have Big Boned), **Meteor Showers** will light up the night sky, **Smog Warnings** will make you unable to !scout that district, **Poudrin Hail** will crush you if you stand around too long without an umbrella, **Radiation Storms** will cuase you to generate slime while standing in the district (while also attracting radioactive creatures), **Japestorms** will cause all manner of laughery, **Firestorms** will set anyone without Napalm Snot ablaze, **Raider Incursions** will see raiders invade the district, **Slimeunist Protests** will see protesters fill the streets, **Dimensional Rifts** will open rifts between districts, **Fishing Frenzies** will cause fish to bite 2x as fast, and **Gas Leaks** will lessen hunger penalty from mining.",
    "casino": "**The Casino** is a sub-zone in Green Light District where players may bet their slime and slimecoin in various games, including **'!slimepachinko'**, **'!slimecraps'**, **'!slimeslots'**, **'!slimeroulette'**, **'!slimebaccarat'**, and **!slimeskat**. Some games allow you to bet certain amounts, while other games have a fixed cost. Furthermore, the casino allows you to challenge other players to a game of **'!russianroulette'**, where most of the loser's slime is transferred to the winner. To bet with slime, simply add 'slime' to the name of the game you wish to play. Example: **!slimeslots 500 slime**. You can gamble through your gellphone, but only with slimecoin.",
    "bleeding": "When you get hit by someone using a '!kill' command, certain things happen to your slime. Let's say you take 20,000 points of damage. **50%** of that slime, in this case 10,000, immediately becomes scavengeable. However, the other 50%, provided that you didn't die instantly, will undergo the **bleeding** process. 25% of that slime, in this case 5,000, is immediately added to a 'bleed pool', causing it to slowly trickle out of your body and onto the ground for it to be scavenged. The remaining 25% of that slime will **slowly** be added to the 'bleed pool', where it will then bleed, just as previously stated. Upon dying, your 'bleed pool' is immediately dumped onto the ground, ready to be scavenged. Think of it like the 'rolling HP' system from the game *EarthBound*. When you get hit, you don't take all your damage upfront, it instead slowly trickles down.",
    "offline": "Given that ENDLESS WAR is a **Discord** game, there are a few peculiarities surrounding it and how it interacts with Discord itself. When you set your status to **'Offline'**, you can still move between districts if you typed a '!goto' command beforehand. You won't show up on the sidebar in that district's channel, but people can still scout for you, and see the '[player] has entered [district]' message when you do enter the district they're in. Furthermore, you **can't** use commands while offline, and can only use commands **5 seconds** after coming online again. Often times, you may find yourself using '!scout' or '!look' on a district, only to find that **no one** is there besides yourself. This is likely because they're in that district, just with their status set to offline. The exception to this, of course, is if you have the **Chameleon Skin** mutation, which lets you type a handful of commands even while offline, including **!goto**, **!look**, **!scout**, **!survey**, **!embark**, and **!disembark**.",
    # Additional gameplay mechanics, part 4
    "profile": "This isn't so much a guide on gameplay mechanics as it is just a guide for what to expect from roleplaying in ENDLESS WAR. The general rule of thumb is that your profile picture will act as your 'persona' that gets depicted in fanworks, and it can be said that many of the colorful characters you'll find in NLCakaNM originated in this way.",
    "manuscripts": "First of all, to start a manuscript, you're gonna need to head down to the Cafe, either University, or the Comic Shop.\n\nYou can **!beginmanuscript [title]** at the cost of 20k slime.\n\nIf you happen to regret your choice of title, you can just **!settitle [new title]**.\n\nThe author name is already set to your nickname, but if you want to change it, you change your nickname and then **!setpenname**.\n\nYou're required to specify a genre for your future zine by using **!setgenre [genre name]** (Genre list includes: narrative, historical, comic, ||porn||, instructional, lore, reference, journal, newspaper, and experimental).\n\nIf at any time you would like to look at the title, author name, and length of your manuscript, then use **!manuscript**.\n\n*NOW*, if you actually want to start getting stuff done, you're gonna need to **!editpage [page number] [content]**. Every zine has 10 pages (kinda) that you can work with, but you can **!setpages [pages]** to customize it (maximum is 20, minimum is 5). Each holds a maximum of 1500 characters of content. You can fill it with information, image links, smut, whatever floats your freakish boat. If you try to edit a page that already has writing, it will ask you to confirm the change before overwriting it.\n\nYou can also set a cover, which is optional. You do this with **!editpage cover [image link]**.\n\nTo check any of your pages, simply **!viewpage [number]** to see how it looks.\n\nKeep in mind that manuscripts ARE NOT items and can't be lost on death. They're accessible from any authoring location (Cafe, NLACU, NMS, Comics). A player can only have 1 manuscript out at a time.\n\nOnce you are completely finished, you can **!publish** your manuscript (it will ask you to confirm that you are completely done with it), which will enable the citizens of the town to purchase it from any zine place. From there, it will be bought and rated by the people and you may even earn some royalty poudrins for it.",
    "zines": "**Zines** are the hot new trend in Neo-Milwaukee and give slimebois of all shapes and sizes access to the free-market of information and culture.\n\nTo obtain a zine, you must head down to any of these locations: Green Cake Cafe, NLAC University, Neo-Milwaukee State, or Glockbury Comics.\n\nFrom there, you can **!browse** for zines. They are ordered by *Zine ID*, but you have many options for sorting them, including: **title, author, datepublished,** any of the genres (including **narrative, historical, comic, ||porn||, instructional, lore, reference, journal, newspaper,** and **experimental**.), **length, sales,** and **rating** (use **!browse [criteria]**). You can also add **reverse** on to any of these in order to make it display in reverse order. Example: **!browse bestsellers reverse** (essentially looks for worse-selling zines). Browsing in the Comic Shop will automatically browse for comic zines and browsing at the Colleges will look for historical zines (keep in mind that any zines can be bought from these places).\n\nYou can also **!browse [Zine ID]** in order to get info about that specific zine, including sales, length, genre, and rating.\n\nOnce you've found a zine that's caught your eye, simply **!orderzine [Zine ID]** to buy it for 10k slime.\n\nAfter absorbing the zine's content, it is your moral obligation as a reader to **!review [Zine Name] [Score]**. The potential scores range from between 1 and 5 *fucks* (whole numbers only). If you hate a zine, then give it one fuck. If you absolutely loved it, give it five fucks. Simple. By the way, if a zine's average rating is less than 2.0 by the time it gets to 10 ratings (or less than 1.5 by 5 ratings), it will be excluded from the default browse. The only way to purchase it will be to use the **worstrated** or **all** sorting methods.\n\nYou can **!shelve [zine name]** in your apartment after you've finished.",
    # "sap": "**Sap** is a resource your body produces to control your slime. It's integral to being able to act in combat. You can have a maximum amount of sap equal to 1.6 * ( your slime level ^ 0.75 ). When you spend it, it will regenerate at a rate of 1 sap every 5 seconds. You can spend your sap in a variety of ways: **!harden [number]** allows you to dedicate a variable amount of sap to your defense. Hardened sap reduces incoming damage by a factor of 10 / (10 + hardened sap). Your hardened sap counts against your maximum sap pool, so the more you dedicate to defense, the less you will have to attack. You can **!liquefy [number]** hardened sap back into your sap pool. Every attack requires at least 1 sap to complete. Different weapons have different sap costs. Some weapons have the ability to destroy an amount of hardened sap from your target, or ignore a portion of their hardened sap armor. This is referred to as **sap crushing** and **sap piercing** respectively. There are also other actions you can take in combat, that cost sap, such as: **!aim [player]** will slightly increase your hit chance and crit chance against that player for 10 seconds. It costs 2 sap. **!dodge [player]** will decrease that players hit chance against you for 10 seconds. It costs 3 sap. **!taunt [player]** will decrease that player's hit chance against targets other than you for 10 seconds. It costs 5 sap.",
    "sprays": "**Sprays** are your signature piece of graffiti as a gangster. You can **!changespray <image link>** in order to set your own custom image. This image appears when you get a critical hit while capping, and you can also **!tag** to spray it anywhere.",
    # Additional gameplay mechanics, part 5
    "burying": "**Burying** is a mechanic that allows one to store an item within a location secretly, only retrievable through a password linked to the item.\n\nTo put an item in the ground, you first must !equip a **shovel**, sold at Atomic Forest Stockpile in the Ooze Gardens Farms. Once equipped, you can **!bury [coordinates] [item]**. The coordinates can be any string you enter, and will be saved with no spaces, punctuation, or case. For example, entering \"!bury DustTrap poudrin\" while in Cratersville will result in a slime poudrin being buried in Cratersville with the coordinates \"DUSTTRAP\". Once you bury an item, the message sent by ENDLESS WAR indicating the correct coordinates of the item will disappear after a short time. Make sure you write the coordinates elsewhere, as **once buried, an item cannot be recovered without the correct coordinates**.\n\nTo **!unearth** an item, simply go to the location it was buried in and type **!unearth [coordinates]**. You do **not need a shovel** to !unearth buried items, just the location and coordinates. Be aware anyone can !unearth buried items, not just the player who buried them, and so this can be utilized as if a sort of dead drop. Finally, if multiple items are buried in the same location with the same coordinates, you must !unearth [coordinates] multiple times to unearth all of the items.\n\nHappy burying!", 
    "stats": "Within ENDLESS WAR, **Stats** are a mechanic that allow the player to showcase their skill in specific areas. You can gain XP through your actions in-game, and you'll level-up as you accrue more and more XP. There are currently 4 stats: mining, farming, fishing, and feasting. To check your stats, use **!stats**. To check now-unobtainable stats, or to check all stats, use **!stats hidden** or **!stats all** respectively. Keep in mind, stats currently have **no effect**, and a player with Level 99 mining will function identical to a player with Level 1 mining. \n\nStat List:\n**MINING** - Mining XP is gained through !mining within mines, with the amount of XP gained being based on the amount of slime mined. \n**FARMING** - Farming XP is gained through !reaping mature crops, with the amount of XP gained being based on both number of crops gained and amount of slime gained. \n**FISHING** - Fishing XP is gained through !reeling up fish or items, with the amount of XP gained being based upon the rarity of the !reel. \n**FEASTING** - Feasting XP is gained through !eating or !ordering food, with the amount of XP gained being based upon the hunger restoration of the food.",
    "collections": "**Collections** are furniture items that can store other items within them. You can buy different types of collections at the Museum: **scalp collections** that can hold scalps, **large aquariums** that can hold fish, **soul cylinders** that can hold souls, **weapon chests** that can hold weapons, **portable greenhouses** that can hold crops, and **general collections** that can hold anything. Specialized collections can store **50** of a specific type of item, and have **unique flavor text upon '!inspect'ing**. General collections can store **10** of any non-collection item and do not unique flavor text. Placing a collection in your apartment will give it its own named line in '!look' text.\n\nOnce you have a collection, while in your apartment, you can **'!collect <collection> <item>'** to store an item in the collection. If you have the mutation **Packrat**, you can !collect into any collection in your inventory while outside your apartment. To remove an item from a collection, go to the Bazaar, and you can **'!extract <collection> <item>'** for **100,000 slime** (greenhouses only cost **1,000 slime**). You can rename collections while in your apartment with **'!renamecollection <collection> [name]'**. Once a collection is placed, you can **'!inspect <collection>'** to view its contents and any accompanying flavor text or information. General collections will have an italicized name on upon '!look', as to distinguish that they do not have any accompanying flavor text or information. Finally, with **'!contents <collection>'**, you can view a collection as if it were a community chest.",
    # Misc.
    "slimeball": "**Slimeball** is a sport where two teams of players compete to get the ball into the opposing team's goal to score points. A game of Slimeball is started when a player does !slimeball [team] in a district. Other players can join in by doing the same command in the same district. Once you've joined a game, you can do !slimeball to see your data, the ball's location and the score. To move around the field, use !slimeballgo [coordinates]. You can kick the ball by running into it. To stop, use !slimeballstop. Each team's goal is open between 20 and 30 Y, and located at the ends of the field (0 and 99 X for purple and pink respectively). To leave a game, do !slimeballleave, or join a different game. A game of Slimeball ends when no players are left.",
    "relics": "**Relics** are one-of-a-kind items hidden all over the city. You can !donate them to the museum in Ooze Gardens for a big slime payout and some additional information about that part of the city. The Curator is pretty airheaded though, so he won't notice if you swipe them back. Long story, he makes replicas, you get the idea. If you are killed with a relic, it gets passed to your killer. Also, hoarding too many might result in graverobbers creeping down your back stair. Be careful, now!",
    "basics": "**The Basics** are things you'll pick up within mere minutes of playing, but hey, we were all beginners at first. Ahem...\n\nYou are a delinquent JUVENILE, recently busted for attempting a scandalous act of vandalism and distribution of highly coveted SLIME. Luckily for you, the juvenile detention center you’ve been assigned to is notoriously corrupt and it’s an open secret how easy escape is. All you have to do for freedom and protection is align yourself to one of the many GANG LEADERS that recruit poor, unfortunate juveniles like yourself. Too pussy to fight directly, they’ve resorted to brainwashed child soldiers to fight their proxy wars for them. Day after day, night after night, from dawn ‘till dusk and dusk ‘till dawn, these troubled youths fight without reason or purpose. Yes, it feels as though a presence pervades this city, from the most poverty-stricken slums to the most gentrified high rise apartments. It is the influence of ENDLESS WAR.\n\nFor a list of essential commands, you can use \"!commands basic\". For help with other things, check out the rest of \"!help\" and, if you need to figure out specific commands, \"!commands\" to figure out categories. Best of luck getting slime in the mines, juvenile.",
    "blurbs": "**Blurbs** are a community feature that allows aspiring writers to add flavor text to the game. The command is only directly accessible by mods and developers, but if one of them approves your idea it can be instantly added. As you might imagine, they can only be a Discord post's length. \nTypes of flavor text you can add:\nAll NPC and Vendor Dialogue\nDistrict !huff Responses\n!brandish and !kill responses with any weapon type\nFishing text of any sub-category\nResponses to !jam(music links) and !pray\nTV responses when !watch-ing\nSkateboard tricks and the descriptions on arcade cabinets\nServer advertisements on a !browse\nText displayed during a meteor shower\nStiltwalker responses and Slimeglobe text\nText from the one obscure mechanic in the bazaar where you remove items from collections and get distracted by something",

    # Weapon Types
    "normal": "**Normal weapons** include the **Dual Pistols**, **Revolver**, **Yo-yo**, **Pistol**, and **Combat Knife**. These are straightforward weapons with no gimmicks and average damage.",
    "multiple-hit": "**Multiple hit weapons** include the **SMG**, **Assault Rifle**, **Nunchucks**, and **Boomerang**. They deal three weak attacks per kill command, and are very safe reliable weapons, though they deal slightly below average damage on average.",
    "variable-damage": "**Variable damage weapons** include the **Nailbat**, **Bass**, **Brass Knuckles**, **Bass Guitar**, **Skateboard**, and **Machete**. On average, these weapons deal pretty good damage for a very reasonable attack cost, but their unreliability can make them quite risky to use.",
    "small-game": "**Small game weapons** include the **Knives**, **Minecraft Bow**, and **Monofilament Whip**. These are reliable and underpowered weapons, with extremely low usage costs making them very efficient. Best used for bullying weaklings and hunting.",
    "heavy": "**Heavy weapons** include the **Scythe**, **Shotgun**, **Broadsword**, **Chainsaw**, and **Sledgehammer**. Unreliable and incredibly expensive to use, to compensate for their very high damage.",
    "defensive": "**Defensive weapons** currently only include the **Umbrella**. While you have one equipped, you take 25% reduced damage! Best used for punching down or protecting yourself while traveling, these weapons are typically too weak and unwieldy for use in normal combat scenarios. Always has a captcha length of 4.",
    "precision": "**Precision weapons** include the **Katana**, **Hunting Rifle**, and **Sniper Rifle**. They always hit, and get a guaranteed crit if you have no other weapons equipped. These weapons deal very high and reliable damage, but only if you're willing to bear the burden of their captcha and the lack of flexibility they impose. Always has a captcha length of 4.",
    "incendiary": "**Incendiary weapons** include the **Molotov Bottles** and the **Dragon Claw**. You will take 10% to 15% of your slime as damage if you enter the captcha wrong! They also deal an extra 50% damage to the target and any flagged enemies in the area over time, causing them to explode on death. A more powerful alternative to explosive weapons, if you can deal with the damage being dealt over time, rather than on one go. Usually has a captcha length of 4. \n\nThis is **OUT OF DATE**.",
    "explosive": "**Explosive weapons** currently only include the **Grenades**. You will take 10% to 15% of your slime as damage if you enter the captcha wrong! They also deal an extra 50% damage to the target and any flagged enemies in the area. The go-to if you're being swarmed by a mob of weaklings, can clear entire districts in one go. Usually has a captcha length of 4.",
    "tool": "**Tools** include the **Pickaxe**, **Diamond Pickaxe**, **Hoe**, **Pitchfork**, **Shovel**, and **Fishing Rod**. They can provide bonuses outside of combat while equipped. Unlike other weapons, Fishing Rods, Hoes, Pitchforks, and Shovels can be equipped by Juvies, although juvies still cannot !kill. When tools are used in combat, they function identically to a normal weapon, but deal 45.4% as much damage.",
    "unique": "**Unique weapons** include the **Minigun**, **Garrote Wire**, **Eldritch Staff**, **Slimeoid Whistle**, and **Missile Launcher**. These have unique, non-standard damage properties and effects specified with the weapon, and act as specialty options for combat.",
    "deprecated": "**Deprecated weapons** include the **Spray Can**, **Paint Gun**, **Paint Roller**, **Paintbrush**, **Watercolors**, **Thinner Bombs**, **Roomba**, and **Slimering Can**. In the past these had unique effects or functionality, but due to features being reworked or removed, nowadays act as tools without outside-of-combat function.",
    "other": "**Other weapons** include **Fingernails**, the **Laywaster**, **Harpoon**, **ModeL 397**, and **Fists**. These are either equippable through means other than an item, or limited-edition weapons with either 1 in existence or being unobtainable through traditionally-legitimate means.",

    # All main weapons
    weapon_id_revolver: "**The revolver** is a normal weapon for sale at Coalition Surplus. It's an ordinary six-shot revolver, so you'll have to **!reload** it after attacking six times, though its attack cost is reduced to 80% to compensate. Goes well with a cowboy hat.",
    weapon_id_dualpistols: "**The dual pistols** are a normal weapon for sale at Coalition Surplus. You don't need to !reload these guns, as you can shoot with one while reloading the other. Shockingly, these aren't that common, despite the city being chock-full of gangsters.",
    weapon_id_shotgun: "**The shotgun** is a heavy weapon for sale at Coalition Surplus. It's a quad-barrelled shotgun double-loaded, so you'll need to !reload every eight shots, but in return your cost multiplier is reduced down to 250% (from 275%) to compensate. Grass grows, birds fly, sun shines, and this thing hurts people; it's a force of nature.",
    weapon_id_rifle: "**The assault rifle** is a multiple-hit weapon for sale at Coalition Surplus. Its magazine only holds enough bullets for ten attacks, so you'll have to **!reload** after hitting the rate limit, but its cost multiplier goes down to 70% to compensate. The experts are still undecided, but most people would agree this is a FAMAS.",
    "assaultrifle": "**The assault rifle** is a multiple-hit weapon for sale at Coalition Surplus. Its magazine only holds enough bullets for ten attacks, so you'll have to **!reload** after hitting the rate limit, but its cost multiplier goes down to 70% to compensate. The experts are still undecided, but most people would agree this is a FAMAS.",
    weapon_id_smg: "**The SMG** is a multiple hit-weapon for sale at Coalition Surplus. Its magazine only holds enough bullets for ten attacks, so you'll have to **!reload** after hitting the rate limit, but its cost multiplier goes down to 70% to compensate. This is pretty good if you like to move around a lot, since the crosshair doesn't grow that much while you're sprinting.",
    weapon_id_minigun: "**The Minigun** is a special variant of **variable-damage weapons**. It deals ten attacks per kill command with an overall cost modifier of 500%, and each attack has a 30% damage modifier, 10% crit chance, a crit multiplier of 200%, and a 50% chance to hit, with a captcha of 6. This is a strange weapon that can potentially deal astronomical damage if used in the right circumstances, and if you're willing to deal with its exceptionally long captcha.",
    weapon_id_bat: "**The nailbat** is a variable-damage weapon for sale at the Dojo. This thing could actually be used to hit balls if you took the nails off it, but that seems a little high-tech...",
    "nailbat": "**The nailbat** is a variable-damage weapon for sale at the Dojo. This thing could actually be used to hit balls if you took the nails off it, but that seems a little high-tech...",
    weapon_id_brassknuckles: "**The brass knuckles** are a variable-damage weapon for sale at the Dojo. Made by sanding away most of a huge pair of metal gauntlets.",
    weapon_id_katana: "**The katana** is a precision weapon for sale at the Dojo. This weapon is folded over a thousand times, so it can cut clean through steel and is vastly superior to any other weapon on earth.",
    weapon_id_broadsword: "**The broadsword** is a heavy weapon for sale at the Dojo. Modeled after a legendary Scottish blade, said to have lopped off a hundred enemy heads and then its own wielder's.",
    weapon_id_nunchucks: "**The nunchucks** are a multiple-hit weapon for sale at the Dojo. 我不僅在未經武裝的戰鬥中接受了廣泛的訓練，而且我可以接觸到美國海軍陸戰隊的整個武庫，而且我會盡其所能將你那可悲的屁股從整個非洲大陸上擦掉，你一點都不討厭。 如果只有您能知道您的小“聰明”評論對您造成了什麼邪惡的報應，也許您會held之以鼻。 但是你不能，你沒有，現在你要付出代價了，你這該死的白痴。 我會在你周圍大怒，你會淹死在裡面。 你他媽的死了，孩子。",
    "nunchucks": "**The nunchucks** are a multiple-hit weapon for sale at the Dojo. 我不僅在未經武裝的戰鬥中接受了廣泛的訓練，而且我可以接觸到美國海軍陸戰隊的整個武庫，而且我會盡其所能將你那可悲的屁股從整個非洲大陸上擦掉，你一點都不討厭。 如果只有您能知道您的小“聰明”評論對您造成了什麼邪惡的報應，也許您會held之以鼻。 但是你不能，你沒有，現在你要付出代價了，你這該死的白痴。 我會在你周圍大怒，你會淹死在裡面。 你他媽的死了，孩子。",
    weapon_id_scythe: "**The scythe** is a heavy weapon for sale at the Dojo. Often mistaken for a bardiche, this is actually one of the better weapons for a PvE-focused DEX build if you don't mind the long recovery animation after whiffing an attack.",
    weapon_id_yoyo: "**The yo-yo** is a normal weapon for sale at the Dojo. All the sick tricks you can pull off with this thing are frankly unremarkable compared to the primal joy of cracking a hole through someone's skull with this tungsten wheel of death.",
    "yoyo": "**The yo-yo** is a normal weapon for sale at the Dojo. All the sick tricks you can pull off with this thing are frankly unremarkable compared to the primal joy of cracking a hole through someone's skull with this tungsten wheel of death.",
    weapon_id_knives: "**The throwing knives** are a small-game weapon for sale at the Dojo. These are often quite dull, relying less on the knives's inherent properties and more on the slime-fueled superstrength of its wielders to pierce through their targets.",
    "throwingknives": "**The throwing knives** are a small-game weapon for sale at the Dojo. These are often quite dull, relying less on the knives's inherent properties and more on the slime-fueled superstrength of its wielders to pierce through their targets.",
    weapon_id_molotov: "**The molotov bottles** are an incendiary weapon for sale at the Dojo. Made with a special slime-based concoction powerful enough to level Juvie's Row if applied correctly. This shit is like bottled malice.",
    weapon_id_grenades: "**The grenades** are an explosive weapon for sale at Coalition Surplus. These may actually be nuclear powered, judging by their ability to wipe out entire districts full of gangsters in one blast.",
    weapon_id_garrote: "**The Garrote Wire** is a unique weapon. It has a damage modifier of 1500%, no cost modifier, guaranteed hits, and a 1% chance for a crit, which does 1000% damage. When you attack with a garrote, the target has 5 seconds to send any message before the damage is done. If they do, the attack fails.",
    weapon_id_bass: "**The bass guitar** is a variable-damage weapon acquired via smelting. It makes the most beautiful sounds when plucking your enemies' tendons.",
    "bassguitar": "**The bass guitar** is a variable-damage weapon acquired via smelting. It makes the most beautiful sounds when plucking your enemies' tendons.",
    weapon_id_umbrella: "**The umbrella** is a defensive weapon for sale at the Bazaar. It has a futurecore feel to it, with the reinforced graphene canopy allowing visibility from the inside out, but not the other way around. Certainly one of the most stylish weapons seen in the city.",
    weapon_id_bow: "**The Minecraft bow** is a small-game weapon acquired via smelting. The calming music most people hum while wielding this thing is quite the interesting contrast, when considered along with the impaled corpses they leave behind.",
    "minecraftbow": "**The Minecraft bow** is a small-game weapon acquired via smelting. The calming music most people hum while wielding this thing is quite the interesting contrast, when considered along with the impaled corpses they leave behind.",
    weapon_id_dclaw: "**The Dragon Claw** is an incendiary weapon acquired via smelting. It merges into your body, turning your arm into a weapon of mass destruction.",
    "dragonclaw": "**The Dragon Claw** is an incendiary weapon acquired via smelting. It merges into your body, turning your arm into a weapon of mass destruction.",
    weapon_id_staff: "**The Eldritch Staff** is a unique weapon. By default, it has a damage modifier of 30%, a cost modifier of 200%, guaranteed hits, no crit chance, and a crit multiplier of 180%. A number of conditions may be met to increase the damage multiplier by 60% and crit chance by 6.66%: tenebrous weather and locations, grudges between the user and its target, the time of day, and the user's general degeneracy will all contribute to the weapon's effectiveness.",
    "eldritchstaff": "**The Eldritch Staff** is a unique weapon. By default, it has a damage modifier of 30%, a cost modifier of 200%, guaranteed hits, no crit chance, and a crit multiplier of 180%. A number of conditions may be met to increase the damage multiplier by 60% and crit chance by 6.66%: tenebrous weather and locations, grudges between the user and its target, the time of day, and the user's general degeneracy will all contribute to the weapon's effectiveness.",
    weapon_id_chainsaw: "**The Chainsaw** is a heavy weapon for sale at Based Hardware. It's the sister weapon to the sledgehammer, both being identical and sold in the same location.  Whichever one you can do more action with? Why, that's what you should get.",
    weapon_id_huntingrifle: "**The hunting rifle** is precision weapon with 6 ammo and a cost modifier of 120% (from 130%), acquired via smelting. Only the most supreme of gentleman choose to wield the hunting rifle.",
    weapon_id_slimeoidwhistle: "**The Slimeoid Whistle** is a unique weapon acquired via smelting that calls upon your active slimeoid to attack the opponent. Its damage properties are based upon your active slimeoid's height: 1-foot slimeoids will act as tools, 2/3-foot slimeoids will act as small-game weapons, 4/5-foot slimeoids will act as normal weapons, 6/7-foot slimeoids will act as variable-damage weapons, 8/9-foot slimeoids will act as heavy weapons, and 10-foot and above slimeoids will act as multiple-hit weapons. If no slimeoid is active, then you will attack with the damage properties of default fists.",
    "slimeoidwhistle": "**The Slimeoid Whistle** is a unique weapon acquired via smelting that calls upon your active slimeoid to attack the opponent. Its damage properties are based upon your active slimeoid's height: 1-foot slimeoids will act as tools, 2/3-foot slimeoids will act as small-game weapons, 4/5-foot slimeoids will act as normal weapons, 6/7-foot slimeoids will act as variable-damage weapons, 8/9-foot slimeoids will act as heavy weapons, and 10-foot and above slimeoids will act as multiple-hit weapons. If no slimeoid is active, then you will attack with the damage properties of default fists.",
    weapon_id_awp: "**The sniper rifle**  is precision weapon with 6 ammo and a cost modifier of 120% (from 130%), acquired via hunting. Generally made for those who can't stand gentlemen, but still love being supreme over others.",
    "sniperrifle": "**The sniper rifle**  is precision weapon with 6 ammo and a cost modifier of 120% (from 130%), acquired via hunting. Generally made for those who can't stand gentlemen, but still love being supreme over others.",
    weapon_id_monofilamentwhip: "**The Monofilament Whip** is a small-game weapon acquired via smelting. It's a particle-thin blade that can slice anything in two.",
    "monofilamentwhip": "**The Monofilament Whip** is a small-game weapon acquired via smelting. It's a particle-thin blade that can slice anything in two.",
    weapon_id_sledgehammer: "**The sledgehammer** is a heavy weapon for sale at Based Hardware. It's the sister weapon to the chainsaw, both being identical and sold in the same location. Whichever one you can do more action with? Why, that's what you should get.",
    weapon_id_skateboard: "**The skateboard** is a variable-damage weapon acquired via smelting. You can !stunt with one in order to do sweet trickz.",
    weapon_id_missilelauncher: "**The Missile Launcher** is a unique weapon for sale at Coalition Surplus. It has guaranteed backfiring damage with successful hits, misses, and a deadly backfire if you get the captcha wrong. It deals normal weapon damage but has 100% AOE effect rather than the usual 10-15% of the other AOE weaponry. Has a captcha length of 11 and has a ammo capacity of 1.",
    weapon_id_pistol: "**The pistol** is a normal weapon for sale at Coalition Surplus. It's the single-handed counterpart of the dual pistols.",
    weapon_id_combatknife: "**The combat knife** is a normal weapon for sale at the Dojo. It's heavy-duty stuff, unlike other knives available for sale.",
    weapon_id_machete: "**The machete** is a variable-damage weapon for sale at the Dojo. It's identical to other variable-damage weapons.",
    weapon_id_boomerang: "**The boomerang** is a multiple-hit weapon for sale at the Dojo. One never needs to reload, as mastering boomerang fluid dynamics is common sense.",
    # Current tools
    weapon_id_pickaxe: "*The Pickaxe** is a mining tool acquired via smelting. Equipping the pickaxe as a gangster gives you double slimegain and a 1.5x chance of unearthing slime poudrins whilst mining.",
    weapon_id_fishingrod: "**The Fishing Rod** is a fishing tool acquired via smelting. When equipped it increases the chance for rare fish upon a !reel, and its weapon mastery level slightly increases the chance for a larger fish the higher it is.",
    weapon_id_hoe: "**The Hoe** is a farming tool for sale at the Atomic Forest Stockpile. It can be equipped by juvies to give a 1.5x modifier of slime gain on a !reap command.",
    weapon_id_pitchfork: "**The Pitchfork** is a farming tool for sale at the Atomic Forest Stockpile. It can be equipped by juvies to give a 2x multiplier to crops gained on a !reap command.",
    weapon_id_shovel: "**The Shovel** is a farming tool for sale at the Atomic Forest Stockpile. It can be equipped by juvies to increase the chance of gaining a poudrin upon a !reap command from 1/30 to 1/6. It can also be used to !bury items and !unearth buried items, as well as !dig in mines.",
    weapon_id_diamondpickaxe: "**The *Diamond Pickaxe*** is a mining tool acquired via smelting. It's identical to a regular pickaxe, just exclusive to rich people. Killing poor people with it probably feels rad.",
    # Deprecated tools
    weapon_id_spraycan: "**The spray can** is a tool for sale at Based Hardware. Formerly a tool used to cap districts, it's now the #6 best way to kill mosquitos.",
    weapon_id_paintgun: "**The paint gun** is a tool for sale at Based Hardware. Formerly a tool used to cap districts, it's now the #3 best way to cover someone in paint from a medium distance.",
    weapon_id_paintroller: "**The paint roller** is a tool for sale at Based Hardware. Formerly a tool used to cap districts, it's now the #8 best way to ink a Splat Zone.",
    weapon_id_paintbrush: "**The paintbrush** is a tool for sale at Based Hardware. Formerly a tool used to cap districts, it's now the #4 most essential cosplay piece for masquerading as Shadow Mario.",
    weapon_id_watercolors: "**Watercolors** are a tool for sale at Based Hardware. Formerly a tool used to cap districts, they're now the #5 most delicious substance to lick off your fingers instead of painting.",
    weapon_id_thinnerbomb: "**Thinner bombs** are a tool for sale at Based Hardware. Formerly a tool used to cap districts, they're now the #2 easiest way to be officially declared a domestic terrorist.",
    "thinnerbombs": "**Thinner bombs** are a tool for sale at Based Hardware. Formerly a tool used to cap districts, they're now the #2 easiest way to be officially declared a domestic terrorist.",
    weapon_id_roomba: "**The Roomba** is a tool for sale at Based Hardware. Formerly a tool used to cap districts, it's now the #7 most efficient way to smear dog shit all over your brand-new carpet.",
    weapon_id_slimeringcan: "**The Slimering Can** is a tool for sale at Atomic Forest Stockpile. Formerly used in Garden Ops, ",
    # Limited / unobtainable weapons
    weapon_id_fingernails: "**Fingernails** are... your fingernails. They're a normal weapon, automatically replacing your default fists while you have the Lethal Fingernails mutation. Whether claws or acrylics, they're sharp enough to tear a small animal in half.",
    weapon_id_laywaster: "**The Laywaster** is a limited-edition heavy weapon acquired via Double Halloween 2020. It's a multi-bladed chainsaw that you're jealous you don't have. And you NEVER WILL!",
    weapon_id_harpoon: "**The Harpoon** is a limited-edition \"ultraheavy\" weapon acquired via unknown illicit means. It has a damage multiplier of 3, cost multiplier of 1.6, a crit chance of 0, a crit multiplier of 1.6, and a hit chance of 1. Unlike other weapons, !reloading a Harpoon takes multiple seconds. \n**YOU EITHER KILL 'EM OR YOU DON'T, BROTHERRRRR!!!!!!!!!!!!**",
    weapon_id_model397: "**The ModeL #397 Hunting Rifle** is a limited-edition multiple-hit weapon with a 1000-bullet clip acquired via the Soulful Weapons Contest. It's a massive gun that you're jealous you don't have. And you NEVER WILL!",
    weapon_id_fists: "**Fists** are... your fists. They're an unarmed weapon used whenever no other weapon is equipped, with a damage multiplier of 0.25, a cost multiplier of 1, a crit chance of 0, a crit multiplier of 1, and a hit chance of 0.9.",

    # "otp":"If you find that you have a role with 'OTP' in the name, don't be alarmed. This just means that you're outside a safe place, such as your apartment, or your gang base / juvie's row. It's essentially a signal to other players that you're actively participating in the game.",
}


help_response_group_map = {
    "Basics": ["Basics", "Profile"],
    "Gameplay": ["Death", "Food", "Mutations", "Smelting", "Slimeoids", "Cosmetics"],
    "Slimegain" : ["Mining", "Scavenging", "Farming", "Fishing", "Hunting"],
    "Gang Violence": ["Gangs", "Ghosts", "Capturing", "Scouting", "Wanted", "Sparring", "Bleeding", "Offline"],
    "World": ["Subzones", "Transportation", "Weather", "Realestate", "Apartments", "Collections", "Casino", "Dojo"],
    "Other": ["Mymutations", "Relics", "Stocks", "Trading", "Burying", "Stats", "Zines", "Manuscripts", "Sprays", "Slimeball", "Blurbs"],
}


weapon_response_group_map = {
    "Normal": ["Revolver", "Dual Pistols", "Yo-Yo", "Pistol", "Combat Knife",],
    "Precision": ["Katana", "Hunting Rifle", "Sniper Rifle",],
    "Small-Game": ["Knives", "Bow", "Monofilament Whip",],
    "Variable-Damage": ["Bat", "Brass Knuckles", "Bass Guitar", "Skateboard", "Machete",],
    "Heavy": ["Shotgun", "Broadsword", "Scythe", "Chainsaw", "Sledgehammer",],
    "Defensive": ["Umbrella",],
    "Multiple-Hit": ["Assault Rifle", "SMG", "Nunchucks", "Boomerang",],
    "Incendiary": ["Molotov", "Dragon Claw",],
    "Explosive": ["Grenades",],
    "Tool": ["Pickaxe", "Fishing Rod", "Hoe", "Pitchfork", "Shovel", "Diamond Pickaxe",],
    "Unique": ["Minigun", "Garrote", "Eldritch Staff", "Slimeoid Whistle", "Missile Launcher",],
    "Deprecated": ["Spray Can", "Paint Gun", "Paint Roller", "Paintbrush", "Watercolors", "Thinner Bomb", "Roomba", "Slimering Can",],
    # "Other": ["Fingernails", "Laywaster", "Harpoon", "Model397", "Fists"] # Probs shouldn't be visible
}

mutation_descriptions = {
    mutation_id_spontaneouscombustion: "Upon dying you do damage proportional to your current slime level, calculated as (level^4)/5, hitting everyone in the district. Example: A level 50 player will do 1,250,000 damage.",
    # mutation_id_thickerthanblood: "On a fatal blow, immediately receive the opponent’s remaining slime, causing none of it to bleed onto the ground or go your kingpin. Its effects are diminished on hunted enemies, however.",
    mutation_id_fungalfeaster: "On a fatal blow, restore all of your hunger.",
    mutation_id_sharptoother: "The chance to miss with a weapon is reduced by 50%. Specifically, a normal miss will now have a 50% to either go through as a miss or a hit.",
    mutation_id_2ndamendment: "One extra equippable weapon slot in your inventory. You receive a 25% damage buff if two non-tool weapons are in both your weapon slots.",
    mutation_id_bleedingheart: "When you are hit, bleeding pauses for 5 minutes. Use !bleedout to empty your bleed storage onto the floor.",
    mutation_id_nosferatu: "At night (8PM-6AM), upon successful hit, 60% of splattered slime is absorbed directly into your slime count.",
    mutation_id_organicfursuit: "Double damage, double movement speed, and 10x damage reduction every 31st night. Use **'!fursuit'** to check if it's active.",
    mutation_id_lightasafeather: "Double movement speed while weather is windy. Use **'!weather'** to check if it's windy.",
    mutation_id_whitenationalist: "Cannot be scouted regularly and you scavenge 50% more slime while weather is snowy, which also stacks with the Webbed Feet mutation. Use **'!weather'** to check if it's snowing. You can still be scouted by players with the Keen Smell mutation.",
    mutation_id_spoiledappetite: "You can eat spoiled food.",
    mutation_id_bigbones: "The amount of food items you can hold in your inventory is doubled.",
    mutation_id_fatchance: "Take 25% less damage from attacks when above 50% hunger, AKA when you're less than half full.",
    mutation_id_fastmetabolism: "Movement speed is increased by 33% when below 40% hunger. Stay full to retain the effect.",
    mutation_id_bingeeater: "Upon eating food, the restored hunger is multiplied by the number of dishes you’ve consumed in the past 5 seconds. Eating lots of food at once puts you in a raging food coma, increasing defense.",
    mutation_id_lonewolf: "50% more damage and 2x capping speed when in a district without any friendly gangsters. Stacks with the Patriot mutation.",
    mutation_id_quantumlegs: "You can now use the !tp command, allowing you to teleport to a district up to two locations away from you after an uninterrupted 15 second running start, with a cooldown of 1 hour.",
    mutation_id_chameleonskin: "While offline, you can move to and scout other districts and cannot be scouted.",
    mutation_id_patriot: "1.5x capping speed. Stacks with Lone Wolf.",
    mutation_id_socialanimal: "Your damage increases by 10% for every ally in your district.",
    mutation_id_threesashroud: "Cannot be scouted and crit chance is doubled if there are more than 3 allies in your district. Cannot be scouted by players with the Keen Smell mutation.",
    mutation_id_aposematicstench: "For every 5 levels you gain, you appear as 1 more person when being scouted. Cannot be scouted by players with the Keen Smell mutation. Use !stink to produce a monster repelling effect. Attacking enemies with it on causes a temporary damage nerf and the removal of the effect.",
    mutation_id_lucky: "Higher chance to create mining events while mining, higher chance to unearth poudrins, better luck at casino games, and increased !reel chance.",
    mutation_id_dressedtokill: "50% more damage if freshness is at least 250.",
    mutation_id_keensmell: "Scouting will list off the names of players and enemies within a district. Will not work on players with the Aposematic Stench or Three's A Shroud mutations.",
    mutation_id_enlargedbladder: "You can use the !piss command. The most cost-effective mutation, and therefore the best one.",
    mutation_id_dumpsterdiver: "10x chance to get items while scavenging with just '!scavenge'. Captcha scavenges search for items using a random single letter of the captcha.",
    mutation_id_trashmouth: "Reach maximum power scavenges 3 times as fast. Example: The soft cooldown of 15 seconds on scavenging is now reduced to 5 seconds. You can also eat cosmetics and furniture. You can also eat furniture and cosmetics using !devour <item>.",
    mutation_id_webbedfeet: "Your scavenging power increases the more slime there is in a district. Caps out at 400% more slime gained from scavenging, but does stack with the White Nationalist mutation. You can feel out the amount of slime you scavenge.",

    mutation_id_dyslexia: "The size of captchas is decreased by 1 character. If a captcha is 1, the captcha length will stay the same.",
    mutation_id_handyman: "If you kill an enemy gangster with a tool instead of a weapon, your kingpin gets double the slime they normally do.",
    mutation_id_packrat: "You gain 2x apartment capacity. In addition, you are able to !collect into collections in your inventory while outside your apartment.",
    mutation_id_stickyfingers: "When using !order at a store, there is a 20% chance to get the item for free. You still need to have the slime to purchase it, though.",
    mutation_id_unnaturalcharisma: "Additive +1 to capping speed (not multiplied by Lone Wolf or Patriot). You also gain 500 freshness.",
    mutation_id_rigormortis: "You are able to !preserve up to 5 items. These items will not drop when you are killed. You must have this mutation for the preservation to take effect, and the items must be in your inventory.",
    mutation_id_nervesofsteel: " Use !brace to freeze movement, preventing outgoing and incoming damage for 20 seconds. As a juvie, you can play Russian Roulette and commit suicide.",
    mutation_id_napalmsnot: "You do some burn damage when attacking with any weapon, in addition to its normal damage. You also gain immunity to burn damage.",
    mutation_id_ditchslap: "Use !slap @user <location> on an ally to instantly launch them to an adjacent district. If you are in a safe zone, the target must use !clench before they can be hit. Any given ally can't be slapped again for a 5 minute cooldown.",
    mutation_id_greenfingers: "Farming wait time is decreased by 33%, and yields are increased by 20%.",
    mutation_id_lightminer: " Mineshaft collapses result in hunger loss instead. In addition, Mining Events are slightly more likely.",
    mutation_id_longarms: "You can !longdrop <destination> <item> to drop an item in an adjacent district.",
    mutation_id_lethalfingernails: "If you have no weapon, you will use your fingernails instead. They do the same damage as a level 6 revolver with no miss.",
    mutation_id_davyjoneskeister: "When making deals with Captain Albert Alexander, you only receive offers for slime, not items.",
    mutation_id_onemansjunk: "When bartering fish with Alexander, you will only receive offers for items, not slime",
    mutation_id_oneeyeopen: "Use !track @user to keep your eye on a specific player. If they move to a PVP zone, you will receive  a DM. If you are being tracked, you can !shakeoff @user to remove their tracking. To check who you're currently tracking, use !thirdeye.",
    mutation_id_bottomlessappetite: "Your maximum hunger is doubled.",
    mutation_id_airlock: "Combined weather effects of all weather-based mutations. This mutation is mutually exclusive with those.",
    mutation_id_ambidextrous: "If you are unarmed or have a tool equipped, and have a weapon in your sidearm slot, you will default to that weapon. Any weapon that you have mastery 7 or higher with will not be dropped on death.",
    mutation_id_coleblooded: "You get the ability to bust ghosts without coleslaw. If a ghost haunts you, they lose negaslime instead of gaining it.",
    mutation_id_landlocked: "When standing in a street either bordering an outskirt or the Slime Sea, use !loop to warp to the opposite side of the map. This also works on the ferry and at Slime's End Cliffs. There is a 60 second travel time when using !loop.",
    mutation_id_amnesia: "Your display name is replaced with ????? in EW's messages, and you can delete your message commands without ENDLESS WAR reacting. On a kill, the kill feed message is delayed by 60 seconds.",
    mutation_id_stinkeye: "When surveying a district, the amount of slime on the ground is shown, along with 4 items starting with the lowest IDs.",
    mutation_id_gay: "You're gay.",
    mutation_id_monplanto: "Wilted crops can be reaped normally, and during sunny weather you gain passive hunger regeneration.",
    mutation_id_foghorn: "During foggy weather, gain an increased critical hit chance.",
    mutation_id_slurpsup: "During rainy weather you are immune to fire. In addition, when attacking, 50% of splattered slime is absorbed directly into your slimecount. Cumulative with Noseferatu.",
    mutation_id_deathfromabove: "During lightning, 10% of your damage is additionally dealt to bystanders when attacking with any non-AOE weapon.",
    mutation_id_ichumfast: "While fishing, you will be @'d upon any !reel notification.",
    mutation_id_scopicretinas: "You can !scout up to two districts away.",
    mutation_id_magicbullettheory: "Upon !reloading an ammunition-based weapon, you will gain an extra bullet in the weapon's clip.",
    mutation_id_stiltwalker: "You can !jump to the blimp from the ground, and into a random mine from Waffle House.",
}

consult_responses = {
    "downtown": "Our complex in Downtown is a sight to behold, one of our most in-demand properties. The whole complex is 2-story penthouses, with built-in storage facility/fallout shelter, restaurant sized fridge, and state-of-the-art bulletproof windows. This is an offer you won't want to pass up, believe you me. Now, perhaps you're concerned about the large amount of gang violence in the area. But, uh...shut up. ",
    "smogsburg": "Have you ever wanted wake up to a haze outside your window every morning? Or to fall asleep to the sound of bazaar merchants bickering with one another in foreign languages? I do, too! That's why I live in Smogsburg, where the prices are low and the furniture is close! Seriously, because of how nearby it is to the bazaar, I've been sniping amazing deals on high quality furniture. Wait...why are you looking at me like that? Actually on second thought, don't buy a property here. I don't want you to steal my shit.",
    "krakbay": "Krak Bay is a real social hotspot. Teenagers come from all over to indulge in shopping sprees they can't afford and gorge themselves on fast food with dubious health standards. I say this all as a compliment, of course. Stay here, and you won't have to walk through the city for ages just to get a good taco. As for the apartment quality, you can rest assured that it is definitely an apartment.",
    "poudrinalley": "You know, people point to the labrynthine building structure and the morbid levels of graffiti and say this place is a wreck. I don't think so, though. Graffiti is art, and unlike many districts in NLACakaNM, the densely packed cityscape makes it difficult to get shot through your window. The 7-11's right around the corner, to boot. For that, I'd say we're charging a real bargain.",
    "greenlightdistrict": "Did you just win the lottery? Have you recently made spending decisions that alientated you from your family? Are you TFAAAP? Then the Green Light District Triple Seven Apartments are for you! Gamble, drink, and do whatever they do in brothels to your heart's content, all far beyond the judging eyes of society! Just remember, with rent this high, you should enjoy those luxuries while they last...",
    "oldnewyonkers": "Eh? I guess you must've liked the view outside. I can't blame you. It's a peaceful sight out there. Lots of old folks who just want to live far away from the gang violence and close to people they can understand. They might say some racist shit while you're not looking, but getting called a bustah never hurt anybody. Wait, shit. Don't tell my boss I said the B word. Shit. OK, how about this? We normally charge this property higher, but here's a discount.",
    "littlechernobyl": "You're an adventurous one, choosing the good ol' LC. The place is full of ruins and irradiated to hell. A friend of mine once walked into the place, scrawny and pathetic, and walked out a griseled man, full of testosterone and ready to wrestle another crazed mutant. Of course, his hair had fallen out, but never mind that. I'm sure your stay will be just as exciting. Just sign on the dotted line.",
    "arsonbrook": "Oh, Arsonbrook? Hang on, I actually need to check if that one's available. You know how it is. We have to make sure we're not selling any torched buildings to our customers. I realize how that sounds, but owning an apartment in Arsonbrook is easier than you think. Once you're settled in with a fire extinguisher or three, the local troublemakers will probably start going for emptier flats. And even if your house does get burned down, it'll be one hell of a story.",
    "astatineheights": "If you live with the yuppies in Astatine Heights, people will treat you like a god. When you walk by on the street, they'll say: \"Oh wow! I can't believe such a rich Juvie is able to tolerate my presence! I must fellate him now, such that my breathing is accepted in their presence!\" It has amazing garage space and a walk-in fridge. Trust me, the mere sight of it would make a communist keel over in disgusted envy.",
    "gatlingsdale": "You'll be living above a bookstore, it looks like. We'd have a normal apartment complex set up, but these pretentious small businesses refuse to sell their property. Guess you'll have to settle for living in some hipster's wet dream for now. We are working to resolve the inconvenience as soon as we can. On the upside, you have every liberty to shout loudly below them and disrupt their quiet reading enviornment.",
    "vandalpark": "Did you know that the apartment complex we have for lease was once lived in by the famous Squickey Henderson? That guy hit like 297 home runs in his career, and you better believe he picked up his bat skills from gang violence. What I'm telling you is, if you buy property here, then you're on your way to the major leagues, probably! Besides, the apartment is actually pretty well built.",
    "glocksbury": "There are a lot of police here. I can see the frothing rage in your eyes already, but hear me out. If you want to go do the gang violence, or whatever you kids do these days, then you can go over someplace else and do it there. Then, when you come back, your poudrins and dire apples will still be unstolen. I suppose that still means you're living around cops all the time, but for this price, that may be an atrocity you have to endure.",
    "northsleezeborough": "This place may as well be called Land of the Doomers, for as lively as the citizens are. They're disenfranchised, depressed, and probably voted for Gary Johnson. My suggestion is not to avoid them like the plague. Instead, I think you really ought to liven up their lives a little. Seriously, here you have a group of un-harassed people just waiting for their lives to go from bad to worse! I think a juvenile delinquent like yourself would be right at home. Wait, is that incitement? Forget what I just said.",
    "southsleezeborough": "Ah, I see. Yes, I was a weeb once, too. I always wanted to go to the place where anime is real and everyone can buy swords. Even if the streets smell like fish, the atmosphere is unforgettable. And with this apartment, the place actually reflects that culture. The doors are all sliding, the bathroom is Japanese-style, and your window overlooks to a picturesque view of the Dojo.",
    "oozegardens": "This place has such a lovely counterculture. Everybody makes the community beautiful with their vibrant gardens, and during the night they celebrate their unity with PCP and drum circles. Everybody fucks everybody, and they all have Digibro-level unkempt beards. If you're willing to put gang violence aside and smell the flowers, you'll quickly find your neighbors will become your family. Of course, we all know you're unwilling to do that, so do your best to avoid killing the damn dirty hippies, OK?",
    "cratersville": "OK...what to say about Cratersville? It's cheap, for one. You're not going to get a better deal on housing anywhere else. It's... It has a fridge, and a closet, and everything! I'm pretty sure there aren't holes in any of those objects, either, at least not when you get them. What else? I guess it has less gang violence than Downtown, and cleaner air than Smogsburg. Actually, fuck it. This place sucks. Just buy the property already. ",
    "wreckington": "So you want to eat a lot of really good pancakes. And you also want to live in a place that looks like war-torn Syria. But unfortunately, you can't do both at the same time. Well boy howdy, do I have a solution for you! Wreckington is world famous for its abandoned and demolished properties and its amazing homestyle diner. More than one apartment complex has actually been demolished with people still in it! How's that for a life-enhancing risk?",
    "slimesend": "I like to imagine retiring in Slime's End. To wake up to the sound of gulls and seafoam, to walk out into the sun and lie under a tree for the rest my days, doesn't it sound perfect? Then, when my old age finally creeps up on me, I can just walk off the cliff and skip all those tearful goodbyes at the very end. Er...right, the apartment. It's pretty good,  a nice view. I know you're not quite retiring age, but I'm sure you'll get there.",
    "vagrantscorner": "Hmm. I've never actually been to Vagrant's Corner. And all it says on this description is that it has a lot of pirates. Pirates are pretty cool, though. Like, remember that time when Luffy had Rob Lucci in the tower, and he Gum Gum Gatling-ed the living shit out of him and broke the building? That was sick, dude. OK, Google is telling me that there's a pretty good bar there, so I suppose that would be a perk, too.",
    "assaultflatsbeach": "Sure, the flat has massive storage space in all aspects. Sure, you can ride a blimp to work if you feel like it. Sure, it's the very definition of \"beachhouse on the waterfront\". But do you REALLY know why this is a top piece of real estate? Dinosaurs. They're huge, they attack people, they're just an all around riot. If you catch some of the ones here and sell them to paleontologists, this place will pay itself back in no time.",
    "newnewyonkers": "Let's be real for a second: I don't need to tell you why New New Yonkers is amazing. They have basically everything there: bowling, lazer tag, arcades, if it distracts adolescents, they have it. Don't let the disgusting old people tell you otherwise: this place is only going up from here. Sure, we had to skimp out a bit on the structural integrity of the place, but surely that won't be noticed until vandals eventually start trying to break it down.",
    "brawlden": "Brawlden's not too scary to live in, relatively speaking. Maybe you'll get pummeled by a straggling dad if you look at him funny, but chances are he won't kill you. If the lanky fellows down at N.L.A.C.U. Labs are able to live in Brawlden, I'm sure you can too. And think of the money you're saving! A \"quality\" apartment, complete with the best mini-fridge and cupboard this side of the city!",
    "toxington": "Are you really considering living in a place that's completely overrun with deadly gases? It's called TOXINGTON, you idiot! The few people who live there now are miners whose brains were already poisoned into obsolescence. I know we technically sell it as a property, but come on, man! You have so much to live for! Call a suicide hotline or get a therapist or something. Anything but this.",
    "charcoalpark": "It's a po-dunk place with po-dunk people. That is to say, it doesn't matter. Charcoal Park is the equivalent of a flyover state, but its location on the edge of the map prevents even that utility. That's exactly why it's perfect for a juvie like yourself. If you want to go into hiding, I personally guarantee the cops will never find you. Of course, you may end up assimilating with the uninspired fucks that live there, but I think that it still fills a niche here in our fair city.",
    "poloniumhill": "If you live with the wannabes in Polonium Hill, people will treat you like a dog. When you walk by on the street, they'll say: \"Oh damn! I can't believe such a desperate Juvie is able to go on living! I must slit their throat just to put 'em out of their misery!\" It nonetheless has amazing storage space and a big, gaudy-looking fridge. Trust me, the mere sight of it would make a communist keel over from the abject waste of material goods. I'm just being honest, buddy. Go live in Astatine Heights instead.",
    "westglocksbury": "If you ever wanted to turn killing people into a reality show, this is probably where you'd film it. The cops were stationed in Glocksbury in order to deal with this place, but they don't tread here for the same reason most of us don't. The corpses here get mangled. I've seen ripped out spines, chainsaw wounds, and other Mortal Kombat-like lacerations. Our photographer couldn't even take a picture of the property without getting a severed leg in the shot. But, as a delinquent yourself, I imagine that could also be a good thing.",
    "jaywalkerplain": "Are you one of those NMU students? Or maybe you're after the drug culture. Well in either case, Jaywalker Plain's an excellent place to ruin your life. In addition to having lots of like-minded enablers, the countless parks will give you the perfect spot to pace and ruminate on your decisions. You know, this is a sales pitch. I probably shouldn't make the place sound so shitty.",
    "crookline": "Now, we've gotten a lot of complaints about thieves here, stealing our clients' SlimeCoin wallets and relieving them of our rent money. We acknowledge this is a problem, so for every purchase of a property in Crookline, we've included this anti-thievery metal codpiece. Similar to how a chastity belt blocks sexual urges, this covers your pockets, making you invulnerable to petty thieves. Apart from that perk, in Crookline you'll get a lovely high-rise flat with all the essentials, all coated in a neat gloomy neon aesthetic.",
    "dreadford": "Have you ever wanted to suck on the sweet, sweet teat of ultra-decadence? Do you have multiple yachts? Do you buy both versions of Pokemon when they come out, just because you can blow the cash? Ha. Let me introduce you to the next level of opulence. Each apartment is a full-scale mansion, maintained by some of the finest slimebutlers in the industry. In the morning they tickle your feet to get you up, and at night they sing you Sixten ballads to drift you back to restful slumber. The place is bulletproof, fireproof, and doubles as a nuclear bunker if things go south. And it stores...everything. The price, you say? Shit, I was hoping you wouldn't ask.",
    "maimridge": "Perhaps you think it's sketchy that we're selling lightly refurbished log cabins built eons ago. Well let me ask you something, young juvie: do you like getting laid? Well, living in Maimridge is your ticket into ice-cold lust and debauchery. You just bring a lady friend or whoever into your isolated mountain cabin, and our state-of-the-art faulty electrical wiring will leave you stranded and huddling for warmth in no time flat! Wow...I'm picturing you now. Yeah, you definitely want this one."
}

basic_commands = "!slime: Check your slime.\n!look: Look at your surroundings.\n!survey: Get a shortened version of !look.\n!goto <district>: Move to a new area.\n!halt: Stop moving.\n!data: Check your current status.\n!slimecoin: Check your slimecoin.\n!eat: Eat food.\n!use: Use an item.\n!scavenge <captcha>: Scavenge slime off the ground.\n!map: Pull up the map.\n!scout <district>: Check for enemies in an adjacent district."
juvenile_commands = "!dance: Dance, monkey.\n!enlist <gang>: Enlist in the Rowdys or the Killers.\n!scrub: Do a \"public service\" and wipe graffiti from capped districts, decreasing crime level."
enlisted_commands = "!kill <player>: Kill your enemies. Depending on your weapon, you need to enter a captcha after this.\n!equip <tool/weapon>: Equip a tool or weapon.\n!sidearm: Sidearm a tool or weapon into a secondary slot.\n!switch: Switch weapons between your weapon and sidearm slots.\n!suicide: Nah, I'm not telling you what this does.\n!vouch: If a Juvie isn't affiliated, you can !vouch for them to join your gang.\n!progress: Displays capture progress in your current district."
corpse_commands = "!boo: Become way too scary.\n!haunt <player>: You can haunt active players to rob them of some slime and get antislime.\n!inhabit <player>: Inhabit another player.\n!letgo: Stop inhabiting someone.\n!possessweapon: Possess the weapon of someone you're inhabiting.\n!possessfishingrod: Possess someone's fishing rod in the same way.\n!unpossessfishingrod: Stop possessing the fishing rod.\n!negaslimeoid: Check on your Negaslimeoid, if you have created one.\n!crystalizenegapoudrin: Create a negapoudrin with negaslime.\n!sowcloth: Rip part of your etheral body into fabric."
player_info_commands = "!data <player>: Check basic player info. Excluding <player> shows your own data.\n!slime <player>:Same as !data, but shows slime count.\n!slimecoin <player>: Same as the above two, but shows SlimeCoin.\n!hunger: Displays hunger.\n!mutations: Check mutations. Add 'level' to the end to display by mutation level.\n!fashion: Displays fashion info.\n!inv: Displays inventory. Add keywords after the command to filter or sort items. Keywords are: type, name, id, stack, search.\n!inv search <contents>: Display all items that contain <contents>.\n!apartment: Check your apartment.\n!mastery: Check weapon mastery."
external_link_commands = "!map: Pull up the world map.\n!time: Get the latest RFCK time and weather.\n!transportmap: Pull a transportation map of the city.\n!patchnotes: See the latest patchnotes.\n!booru: Get a link to the RFCK Booru.\n!wiki: Get a link to the wiki.\n!leaderboard: Get a link to the online leaderboard.\n!bandcamp: Links to the RFCK Bandcamp.\n!tutorial: Gives a more in-depth view of Endless War Gameplay."
combat_commands = "!kill <player>: Kill your enemies. Depending on your weapon, you need to enter a captcha after this.\n!equip <tool/weapon>: Equip a tool or weapon.\n!sidearm: Sidearm a tool or weapon into a secondary slot.\n!switch: Switch weapons between your weapon and sidearm slots.\n!aim <player>: Increase accuracy toward a target.\n!taunt <player>: Decrease you opponent's accuracy.\n!dodge <player>: Increase evasion for a short time.\n!reload: Some weapons have limited ammo and need to reload."
item_commands = "!inv: Displays inventory. Add keywords after the command to filter or sort items. Keywords are: type, name, id, stack, search, general, food, cosmetic, color, furniture, weapon, weapontype, preserved, <item color>, <weapon type>.\n!inv search <contents>: Display all items that contain <contents>.\n!inspect <item>: Inspect an item in your inventory.\n!discard <item>: Discard an item.\n!use <item>: Some items can be used.\n!trade <player>: Open a trade with a player.\n!offer <item>: Add an item to a trade.\n!removeoffer <item>:Remove an item from the trade.\n!completetrade: Finish the trade.\n!canceltrade:Cancel a trade.\n!smelt <item>: Smelt an item form ingredients.\n!whatcanimake <item>:Shows what you can smelt with an item.\n!scrawl <item> <description>: Add a message to an item.\n!strip <item>: Remove a message from an item\n!give @player <item>: Giving away items increases festivity."
cosmetics_dyes_commands = "!adorn <cosmetic>: Wear a cosmetic\n!dedorn <cosmetic>: Take a cosmetic off.\n!dyecosmetic <cosmetic> <dye>: Dye a cosmetic using dyes in your inventory.\n!dyefurniture <furniture> <dye>: Change the color of furniture with dye.\n!saturateslimeoid <dye>: Dye your slimeoid."
miscellaneous_commands = "!scrutinize <object>: Examine specific objects in an area. Usually reserved for dungeons and ARGs.\n!shakeoff: If someone with the One Eye Open mutation is following you, use this to shake them off. Alternatively, if within a gangbase, use this to shake off any body spray you have active.\n!extractsoul: Remove your soul. from your body and bottle it.\n!returnsoul: Return your soul to your body, only if you have it in your inventory.\n!squeezesoul <soul>: Squeeze a soul. The soul's owner will vomit 1/4 of their slime on the ground.\n!ads: View ads in a district.\n!knock <player>: Knock on a player's apartment door, if you're in the district.\n!changespray <tag>:Change the image link that displays on a !tag.\n!endlesswar: Check the total ammassed slime of all players.\n!negaslime: Check total amassed antislime."
flavor_commands = "Command list: \n!salute\n!unsalute\n!hurl\n!howl\n!moan\n!pot\n!bully <target>\n!lol\n!jam <instrument>\n!measure <subject>\n!skate\n!brandish\n!tag"
slimeoid_commands = "!slimeoid: Check your or another player's slimeoid.\n!saturateslimeoid <dye>: Dye your slimeoid. Some colors are strong against others in battle.\n!bottleslimeoid:Put your slimeoid in a bottle, turning them into an item.\n!unbottleslimeoid: Unbottle a slimeoid.\n!feedslimeoid <food>: Feed your slimeoid stat modifying candy, or normal food so they can fight again sooner.\n!dressslimeoid <cosmetic>: Dress up your slimeoid.\n!undressslimeoid: Take cosmetics off your slimeoid.\n!slimeoidbattle <player>: Challenge another player to a slimeoid battle. Add keywords to modify the battle. Keywords are: death, bet <number>, size <number>.\n!slimeoidduel <player>: Varient of !slimeoidbattle which includes a countdown before the match begins (swap dyes)\n!playfetch, !petslimeoid, !abuseslimeoid, !walkslimeoid, !observeslimeoid: You can interact with your own slimeoid, or somebody's you share quadrants with, in various ways."
trading_commands = "!trade <player>: Open a trade with a player.\n!offer <item>: Add an item to a trade.\n!removeoffer <item>:Remove an item from the trade.\n!completetrade: Finish the trade.\n!canceltrade:Cancel a trade."
smelting_commands = "!smelt <item>: Smelt an item form ingredients.\n!whatcanimake <item>:Shows what you can smelt with an item."
quadrant_commands = "!addquadrant <quadrant> <player>: Add a player to your quadrants.\n!clearquadrant <quadrant>: Break up with someone in your quadrants.\n!quadrants: Displays a full list of quadrants.\n!sloshed, !roseate, !violacious, !policitous: Check on one of the four specific quadrants."

farm_commands = "**FARMS**\n!sow <item>: Plant a poudrin or vegetable into the ground.\n!reap: Reap the crops and slime once they're ready to be harvested.\n!checkfarm: Look at the status of your crops.\n!irrigate, !weed, !fertilize, !pesticide: These commands can be used to increase farm yields, depending on the current status of the farm.\n!mill <crop>: Break down a crop into various smelting materials."
shop_commands = "**SHOPS**\n!order <item>: Buy an item."
pier_commands = "**PIERS**\n!cast <bait>: Cast your fishing line. While both are optional, bait increases fishing speed and fishing rods increase fish rarity.\n!reel Reel in a cast line."
mine_commands = "**MINES**\n!mine: Use this one in the normal mines. A lot.\n!mine a1: Use coordinates when mining in Bubble Breaker and Minesweeper.\n!flag: This will flag off an area in Minesweeper."
transport_commands = "**TRANSPORT**\n!schedule: Check the subway schedule.\n!embark: Used to board transports\n!disembark: Get off transports."
zine_writing_places_commands = "**ZINES**\nbrowse <category>: Browse for zines. You can sort by title, author, date, length, et cetera by placing it after the command.\n!orderzine <zine>: Order a zine. Specify the name or number of the zine to pick one out.\n!read <zine ID> Begin reading a zine.\nThere are a lot of zine commands. I would recommend picking up HOW TO ZINE by Milly and learning the details there."
universities_commands = "**UNIVERSITIES**\n!help <category>: Use this to teach yourself about various gameplay mechanics."
apartment_commands = "**APARTMENTS**\n!stow <item>: Put an item within the closet/fridge/bookshelf.\n!snag <item>: Take an item from the closet/fridge/bookshelf.\n!decorate <item>: Place a furniture item in the apartment.\n!undecorate <item>: Take a furniture item from the apartment.\n!propstand <item>: Turn an item into a piece of furniture.\n!collect <collection> <item>: Add an item to a collection box.\n!contents <collection>: Search a collection's contents as if a community chest.\n!aptname <name>: Rename apartment.\n!aptdesc <description>: Change apartment's description.\n!renamecollection <collection> [name]: Rename a collection.\n!unpot: Remove a potted crop from its pot.\n\nGo to the Bazaar to undo prop stands, aquariums, and collections."

mutation_unique_commands = {
    "oneeyeopen": "**ONE EYE OPEN**\n!thirdeye: Check the current status of your third eye.\n!track <player>:Get your eye to focus on someone and check their movements.\n!shakeoff <player>: Used to break a person's thirdeye tracking from yourself. Anybody can use this.",
    "aposematicstench": "**APOSEMATIC STENCH**\n!stink: Gain stink, which drives away monsters. It functions like Fuck Energy Body Spray.",
    "bleedingheart": "**BLEEDING HEART**\n!bleedout: Purge your bleed storage onto the ground all at once.",
    "longarms": "**LONG ARMS**\n!longdrop <location> <item>: Drop an item in an adjacent district.",
    "rigormortis": "**RIGOR MORTIS**\n!preserve <item>: Prevent an item from dropping when you die.\n!inventory preserved: Shows you which items you have preserved already.",
    "ditchslap": "**DITCH SLAP**\n!slap <player> <location>: Slap an ally into another district.\n!clench: Clench your butt cheeks to prepare to be slapped. Have your allies use this.",
    "landlocked": "**LANDLOCKED**\n!loop: Use this on a district bordering an outskirt. It will loop you to the opposite end of the map.",
    "organicfursuit": "**ORGANIC FURSUIT**\n!fursuit: Check for the next full moon when your next \"furry episode\" begins.",
    "enlargedbladder": "**ENLARGED BLADDER**\n!piss: Need I say more?",
    "quantumlegs": "**QUANTUM LEGS**\n!tp <location>: Teleport up to two areas away.",
    "trashmouth": "**TRASH MOUTH**\n!devour item: Eat some non-food items.",
}
    
item_unique_commands = {
    "slimepoudrin": "**SLIME POUDRIN**\n!annoint <name>: Anoint your weapon in slime and give it a name. Your weapon mastery increases, up to rank 6 master.\n!crush poudrin: Break the poudrin and get slime.", # At the top, cuz it's super important
    "alarmclock": "**ALARM CLOCK**\n!setalarm <time> <item>: When holding an alarm clock, you can set it to an in-game time. It will DM you when it sounds if it's in your inventory. You can set it to \"OFF\" instead of a time.",
    "brick": "**BRICK**\n!toss <player>: When near a player's apartment, you can throw bricks through their window. When near a player, you can throw it at them.\n!skullbash: With a brick, immobilize yourself for 10 minutes.",
    "cigar": "**CIGAR**\n!smoke <cigar>: Smoke cigars.",
    "cigarette": "**CIGARETTE**\n!smoke <cigarette>: Smoke cigarettes.",
    "costumekit": "**COSTUME KIT**\n!makecostume \"<name>\" \"<description>\": Fashion yourself a Double Halloween costume.",
    "gameguide": "**GAME GUIDE**\n!help: Get some in-depth help on game topics.",
    "gellphone": "**GELLPHONE**\n!use gellphone: Turn your gellphone on/off. When on, you'll gain access to Slime-Based Social Media.",
    "laptopcomputer": "**LAPTOP**\n!browse: Browse the web on your laptop for RFCK Discord servers if it is in your apartment.",
    "negapoudrin": "**NEGAPOUDRIN**\n!crush negapoudrin: Break the negapoudrin and gain negaslime.",
    "partypopper": "**PARTY POPPER**\n!use <partypopper>: Pop your party popper and spread confetti and glitter everywhere!",
    "pheromones": "**KINKFISH PHEROMONES**\n!use <pheromones>: Spray yourself with pheromones and smell reeeeeeeeaaaaal good!",
    "pictureframe": "**PICTURE FRAME**\n!frame <image link>: Put an image in a picture frame.\n!titleframe <title>: Add a title to a picture frame.",
    "prankcapsule": "**PRANK CAPSULE**\n!use <prankcapsule>: Pop open a prank capsule and get a random prank item!",
    "royaltypoudrin": "**ROYALTY POUDRIN**\n!crush royaltypoudrin: Break the royalty poudrin and gain slime.",
    "shovel": "**SHOVEL**\n!bury <coordinates> <item>: Bury an item in the ground. For more information, try \"!help burying\".",   
    "skateboard": "**SKATEBOARD**\n!skate: Rock some slammin' tricks on your board, dude!",
    "television": "**TV**\n!watch: Watch TV if it's in your apartment. Stop watching by taking the TV out of your apartment.",
    "vape": "**VAPE**\n!vape <vape pod>: Smoke vape pods in your inventory.",
    "washingmachine": "**WASHING MACHINE**\n!wash <object>: Remove the dye from a slimeoid or a piece of clothing if it is in your apartment.",
    "die": "**DIE**\n!rolldie: Roll the die.",
}

item_group_commands = {
    "bodyspray": "**FUCK ENERGY BODY SPRAY**\n!use <item>: Spray yourself down with body spray, making monsters not target you for a time.",
    "instantuse_response_pranks": "**INSTANT-USE/RESPONSE-TYPE PRANKS**\n!use <item> <@player>: Use the prank item at player, totally making a fool out of 'em!",
    "trap_pranks": "**TRAP-TYPE PRANKS**\n!use <item>: Lay the prank item on the floor, primed to prank an unsuspecting player who passes by.",
    "instruments": "**INSTRUMENTS**\n!jam <instrument>: Jam out on your instrument.",
    "tradingcards": "**TRADING CARDS**\n!unwrap <item>: Unwrap some trading cards (after crossing your fingers, of course).",
    "wrappingpaper": "**WRAPPING PAPER**\n!wrap <@player> \"<message>\" <item>: Wrap an item for a beloved friend of yours, with merriment and cheer!",
}

holidaycommands = {
    "swildermuk": "",
    "slimernalia": "**SLIMERNALIA**:\n!yoslimernalia: Yo, Slimernalia!\n!festivity:Check your current festivity.\n!wrap <player> \"Message\" <item>: Wrap a gift with a message attached.\n!unwrap <item>: Open another's gift for you.\n!give @player: Show your festivity by giving gifts.",
    "doublehalloween": "**DOUBLE HALLOWEEN**:\n!makecostume \"<Name>\" \"<<Description\" Create a Double Halloween costume using a costume kit.\n!crush <candy> Crush candy to get Double Halloween Grist.\n!trickortreat <player> Get candy in a district, or from a player's apartment if you @ them.\n!sacrifice <item>: In ENDLESS WAR, sacrifice an item to appease...someone. Probably an elder god.",
}

district_unique_commands = {
    "theslimestockexchange": "**STOCK EXCHANGE**\n!invest <amount> <stock>: Invest SlimeCoin into a stock.\nwithdraw <stock> <amount>: Remove SlimeCoin from shares of stock.\n!transfer <amount> <player>: Move your SlimeCoin to another player.\n!shares:Display your current shares.\n!rates:Display current SC:Slime exchange rates.\n!stocks: Displays currently available stocks.",
    "realestateagency": "**REAL ESTATE**\n!consult <district>: Get information and cost for an apartment.\n!signlease <district>: Purchase an apartment in a new location.\n!breaklease: Cancel the lease you currently have.\n!aptupgrade: Upgrade your apartment, from C to S.\n!changelocks: Erase all housekeys you have in circulation.\n!addkey: Add a housekey to your apartment.",
    "clinicofslimoplasty": "**CLINIC**\n!chemo <mutation>: Clear a mutation from yourself.\n!graft <mutation>: Attach a new mutation to yourself.\n!browse: Browse the medical zines available.\n!orderzine <zine>: Order a list of mutations to graft.",
    "thesewers": "**SEWERS**\n!revive: Revive.",
    "slimecorpslimeoidlaboratory": "**SLIMEOID LAB**\n!embiggen: Make a fish real big.\n!restoreslimeoid <slimeoid>: Restore a Slimeoid from a slimeoid heart.\n!instructions: Go over the many commands used to make a slimeoid.",
    "thecasino": "**CASINO**\n!slimecraps <amount> <currency>: Gamble at the craps table. Gambling types include slimecoin, slime, and your soul.\n!slimeroulette <amount> <bet> <type>:Gamble at the roulette wheel. Types are same as above, bet options are shown by typing !slimeroulette <amount>.\n!slimeslots <type>: Bet a fixed amount in slots. Accepts Slime and SlimeCoin.\n!slimepachinko <type> Same as above, but in pachinko.\n!slimebaccarat <amount> <currency> <hand>: Bet slime, slimecoin, or souls on baccarat. The hand is either 'player' or 'dealer'.\n!slimeskat <player> <player>: Challenge two players to a game of slimeskat. You bet Slimecoin once the game has started.\n!russianroulette <player>: Challenge your opponent to russian roulette. Add 'soul' to the end of the command to gamble souls.\n!betsoul: Exchange your soul for {} SlimeCoin.\n!buysoul <player>: Buy a soul off the casino for {} SlimeCoin, if one is in stock.".format(
        soulprice, soulprice),
    "thedojo": "**DOJO**\n!spar <player>: Spar with someone to increase your weapon level.\n!marry: Marry your weapon.\n!divorce: The inevitable, after marrying your weapon.\n!object: Interrupt a marriage as it's going. ",
    "thebattlearena": "**BATTLE ARENA**\n!slimeoidbattle <player>: Challenge a player to a slimeoid battle. They can !accept or !decline.",
    "slimecorphq": "**SLIMECORP HQ**\n!donate <amount>: Donate slime to Slimecorp and exchange it for SlimeCoin.\n!requestverification: Acquire a verified checkmark for Slime Twitter.\n!advertise <content>: Advertise something.",
    "slimesendcliffs": "**CLIFFS**\n!push <player>: Push a player off the cliff.\n!jump: Jump off the cliff.\n!toss <item>: Toss an item off the cliff.",
    "sodafountain": "**SODA FOUNTAIN**\n!purify: At Level 50, you can reset slime to zero and level to 1. Mutations stick around.",
    "speakeasy": "**SPEAKEASY**\n!barter <fish>: Barter your fish with Albert Alexander.\nbarterall: All the fish will be removed from your inventory and exchanged with slime and items you would've gotten for bartering.\n!appraise: Get the quality of a fish reviewed by Albert Alexander.",
    "recyclingplant": "**RECYCLING PLANT**\n!recycle <item>: Recycle an item in exchange for SlimeCoin.",
    "copkilltown": "**COP KILLTOWN**\n!renounce: Unenlist from your gang in exchange for half your slime.\n!chest: Check the contents of the community chest.\n!snag <item>: Take items from the community chest.\n!stow <item>: Place inventory items in the community chest.",
    "rowdyroughhouse": "**ROWDY ROUGHHOUSE**\n!renounce: Unenlist from your gang in exchange for half your slime.\n!chest: Check the contents of the community chest.\n!snag <item>: Take items from the community chest.\n!stow <item>: Place inventory items in the community chest.",
    "juviesrow": "**JUVIE'S ROW**\n!chest: Check the contents of the community chest.\n!snag <item>: Take items from the community chest.\n!stow <item>: Place inventory items in the community chest.",
    "bazaar": "**BAZAAR**\n!extract <collection item> <item>: For a fee, remove an item from a collection.\n!unstand <item>: Remove an item from its prop stand.\n!releasefish <aquarium>: Remove fish from their aquarium.",
    "vandalpark": "**VANDAL PARK**\n!slimeball <team>: Join a game of Slimeball. Teams are purple and pink. Read about details in the Game Guide.",
    "endlesswar": "**ENDLESS WAR**\n!pray <target>: Pray to someone.",
    "thesummit" : "**THE SUMMIT**\n!jump: A suicidal, expedited version of snowboarding.",
    "limecorp3f": "**LIMECORP 3F**\n!jump: Commit career suicide.",
    "blimp": "**BLIMP**:\nGo skydiving. No parachute, but you can pretend.",
    "themuseum": "**THE MUSEUM**\n!donate <relic/fish/frame>: Donate something to the Curator's museum.",
    "wafflehouse": "**WAFFLE HOUSE**\n!restorenegaslimeoid <negaslimeoid>: Restore a Negaslimeoid from a core.\n!destroyslimeoid: Destroy a Slimeoid or Negaslimeoid in your possession.\n!instructions: Go over the many commands used to make a negaslimeoid.",
    "ghostmaidcafe": "**GHOST MAID CAFE**\n!startshift <hardmode>: Begin working to earn antislime and ghost tokens. Write hardmode after the command to challenge yourself.\n!serve: Serve customers during a shift to avoid failing before your pay.",
    "doorsofthesludgenant": "**DOOR OF THE SLUDGENANT**\n!question: Get a question from that stone face up there.\n!answer <answer>: Answer the question to try opening up a door."
}


# humanoid, amphibian, food, skeleton, robot, furry, scalie, slime-derived, monster, critter, avian, insectoid, shambler, other
race_unique_commands = {
    "humanoid": "!exist: Exist.",
    "amphibian": "!ree: Throw a good old fashioned tantrum.",
    "food": "!autocannibalize: Snack on yourself.",
    "skeleton": "!rattle: Channel your inner xylophone.",
    "robot": "!beep: Beep.",
    "furry": "!yiff: Be a degenerate.",
    "scalie": "!hiss: sssSsss.",
    "slime-derived": "!jiggle: The details are up to your imagination.",
    "monster": "!rampage: Go nuts.",
    "critter": "!requestpetting <player>: Weird stuff you critters are into these days.",
    "avian": "!flutter: Flap your wings. Show off.",
    "insectoid": "!entomize: Time to do insect things.",
    "shambler": "!shamble: BBBBRRRRRAAAAIIIIINNNNZZZZ.",
    "demon":"!strikedeal <player>: Set up a contract with some unsuspecting sap.",
    "cyborg":"!netrun <player>: We do a little hacking here.",
    "other":"!confuse: Not too hard to do with this crowd."
}

jump_responses = {
    'thesummit':'*Gnarly, bro!* Time to get on your board and feel that classic mountain high! Oh, what\'s that? No board? No experience boarding? No actual sloped surface, just a 2000 foot drop into the outskirts? Ah, my mistake. {} is sent plummeting off the edge.',
    'limecorp3f':'Well, it looks like {} is finally going to end it. The Slime and Punishment 500 index dropped into the -500s and they became an evil version of themselves, and now the only thing left to do is liquidating their assets, aka their internal organs. OK, salaryman RP over. FOR STOCKS!!',
    'blimp':'The blimp driver has served {} expired peanuts for the last time. And they\'re starting to think nobody has read those Yelp reviews they keep leaving. Time for a protest suicide. DIVE BOMB!',
}


sea_scavenge_responses = [
    "see a school of Fuck Sharks circling below you",
    "notice an approaching kraken",
    "remember you can't swim",
    "think of how you got here in the first place. Was it Crank? It was probably Crank.",
]

# Enemy life states
enemy_lifestate_dead = 0
enemy_lifestate_alive = 1
enemy_lifestate_unactivated = 2

# Enemy attacking types (aka 'weapons')
enemy_attacktype_unarmed = 'unarmed'
enemy_attacktype_fangs = 'fangs'
enemy_attacktype_talons = 'talons'
enemy_attacktype_tusks = 'tusks'
enemy_attacktype_raiderscythe = 'scythe'
enemy_attacktype_gunkshot = 'gunkshot'
enemy_attacktype_molotovbreath = 'molotovbreath'
enemy_attacktype_armcannon = 'armcannon'
enemy_attacktype_axe = 'axe'
enemy_attacktype_hooves = 'hooves'
enemy_attacktype_body = 'body'
enemy_attacktype_stomp = 'stomp'
enemy_attacktype_stomp_n6 = 'stompn6'
enemy_attacktype_gnash = 'gnash'
enemy_attacktype_rifle = 'rifle'
enemy_attacktype_beak = 'beak'
enemy_attacktype_claws = 'claws'
enemy_attacktype_kicks = 'kicks'
enemy_attacktype_shadowclaws = 'shadowclaws'
enemy_attacktype_prairieking = 'prairieking'
enemy_attacktype_tinyclaws = 'tinyclaws'
enemy_attacktype_whale = 'whale'
enemy_attacktype_phoenix = 'phoenix'
enemy_attacktype_graspers = 'graspers'
enemy_attacktype_raygun = 'raygun'
enemy_attacktype_feed = 'feed'
enemy_attacktype_wesson = 'wesson'
enemy_attacktype_amateur = 'amateur'
enemy_attacktype_cop = 'police'
enemy_attacktype_dojoman = 'dojoman'
enemy_attacktype_hellfire = 'hellfire'
enemy_attacktype_bonemerang = 'bonemerang'
enemy_attacktype_icespike = 'icespike'
enemy_attacktype_bloodsucker = "bloodsucker"
enemy_attacktype_bluntweapon = "bluntweapon"


# Enemy weather types. In the future enemies will make use of this in tandem with the current weather, but for now they can just resist the rain.
enemy_weathertype_normal = 'normal'
enemy_weathertype_rainresist = 'rainresist'

# Enemy types
# Goon enemies (only spawn with a leader present)
enemy_type_piloslime = 'piloslime'
enemy_type_prairiepawn = 'prairiepawn'
# Common enemies
enemy_type_juvie = 'juvie'
enemy_type_dinoslime = 'dinoslime'
enemy_type_spacecarp = 'spacecarp'
# Uncommon enemies
enemy_type_slimeadactyl = 'slimeadactyl'
enemy_type_desertraider = 'desertraider'
enemy_type_mammoslime = 'mammoslime'
enemy_type_rivalhunter = 'rivalhunter'
# Rare enemies
enemy_type_microslime = 'microslime'
enemy_type_grey = 'grey'
enemy_type_tangeloid = 'tangeloid'
enemy_type_alienscum = 'alienscum'
enemy_type_npc = 'npc'

enemy_type_mammoslimebull = 'mammoslimebull'
enemy_type_slimeofgreed = 'slimeofgreed'
enemy_type_microgullswarm = 'microgullswarm'
enemy_type_policeofficer = 'policeofficer'
# Raid bosses
enemy_type_megaslime = 'megaslime'
enemy_type_thegull = 'thegull'
enemy_type_slimeasaurusrex = 'slimeasaurusrex'
enemy_type_greeneyesslimedragon = 'greeneyesslimedragon'
enemy_type_unnervingfightingoperator = 'unnervingfightingoperator'


enemy_type_civilian = 'civilian'
enemy_type_civilian_innocent = 'innocent'

enemy_type_slimeoidtrainer = 'slimeoidtrainer'
enemy_type_ug_slimeoidtrainer = 'undergroundslimeoidtrainer'

enemy_type_titanoslime = "titanoslime"
enemy_type_mutated_titanoslime = "mutatedtitanoslime"

enemy_type_lesserwerewolf = "lesserwerewolf"
enemy_type_skeletonranger = "skeletonranger"

# POI event enemies
enemy_type_bandito = 'bandito'
enemy_type_raiderunderboss = 'raiderunderboss'
enemy_type_protester = 'protester'
enemy_type_antiprotestprotester = 'antiprotestprotester'
enemy_type_deathclaw = 'deathclaw'
enemy_type_mutatedbarrel = 'mutatedbarrel'

# Sandbag (Only spawns in the dojo, doesn't attack)
enemy_type_sandbag = 'sandbag'

# Double Halloween bosses. Could be brought back as enemies later on, for now will only spawn in the underworld.
enemy_type_doubleheadlessdoublehorseman = 'doubleheadlessdoublehorseman'
enemy_type_doublehorse = 'doublehorse'

# Raid Den bosses - have special effects that occur on death
enemy_type_alm = "almfe" # Placeholder testing boss

# Slimernalia Specific Enemies and Raid Bosses
enemy_type_slimernaliajuvie = "slimernaliajuvie"
enemy_type_vandal = "vandal"
enemy_type_illegalimmigrant = "illegalimmigrant"
enemy_type_arsonist = "arsonist"
enemy_type_slimeoidabuser = "slimeoidabuser"
enemy_type_slimernaliagangster = "slimernaliagangster"
enemy_type_spiritofslimernaliapast = "spiritofslimernaliapast"
enemy_type_drugdealer = "drugdealer"
enemy_type_miserablemiser = "miserablemiser"

# Enemy ai types
enemy_ai_sandbag = 'Sandbag'
enemy_ai_coward = 'Coward'
enemy_ai_attacker_a = 'Attacker-A'
enemy_ai_attacker_b = 'Attacker-B'
enemy_ai_defender = 'Defender'

# Enemy classes. For now this is only used for Gankers Vs. Shamblers
enemy_class_normal = 'normal'

common_enemies = []
# List of enemies sorted by their spawn rarity.
common_enemies = [enemy_type_sandbag, enemy_type_juvie, enemy_type_dinoslime]
uncommon_enemies = [enemy_type_slimeadactyl, enemy_type_desertraider, enemy_type_mammoslime, enemy_type_spacecarp]
rare_enemies = [enemy_type_microslime, enemy_type_slimeofgreed, enemy_type_mammoslimebull, enemy_type_microgullswarm]
raid_bosses = [enemy_type_megaslime, enemy_type_slimeasaurusrex, enemy_type_greeneyesslimedragon, enemy_type_unnervingfightingoperator, enemy_type_titanoslime, enemy_type_thegull]
enemy_movers = [enemy_type_megaslime, enemy_type_slimeasaurusrex, enemy_type_greeneyesslimedragon, enemy_type_unnervingfightingoperator, enemy_type_titanoslime]
defense_up_enemies = [enemy_type_mutatedbarrel, enemy_type_alm]
raid_den_bosses = [enemy_type_alm]

if slimernalia_active == True:
    common_enemies.extend([enemy_type_spiritofslimernaliapast, enemy_type_drugdealer])
    uncommon_enemies.extend([enemy_type_vandal, enemy_type_illegalimmigrant, enemy_type_arsonist, enemy_type_drugdealer, enemy_type_slimeoidabuser])
    raid_bosses.extend([enemy_type_slimernaliajuvie, enemy_type_slimernaliagangster, enemy_type_miserablemiser])
    enemy_movers.extend([enemy_type_slimernaliajuvie, enemy_type_vandal, enemy_type_illegalimmigrant, enemy_type_arsonist, enemy_type_slimernaliagangster, enemy_type_slimeoidabuser, enemy_type_miserablemiser])
    defense_up_enemies.extend([enemy_type_miserablemiser])
# List of enemies that spawn in the Nuclear Beach
pre_historic_enemies = [enemy_type_slimeasaurusrex, enemy_type_dinoslime, enemy_type_slimeadactyl, enemy_type_mammoslime]
arctic_enemies = [enemy_type_desertraider, enemy_type_slimeasaurusrex, enemy_type_juvie, enemy_type_unnervingfightingoperator, enemy_type_grey, enemy_type_mammoslime, enemy_type_piloslime, enemy_type_greeneyesslimedragon, enemy_type_megaslime, enemy_type_dinoslime]
slimeoid_trainers = [enemy_type_npc]


# Double Halloween variant enemies
dh_v_enemies = [enemy_type_juvie, enemy_type_dinoslime, enemy_type_slimeadactyl, enemy_type_desertraider, enemy_type_mammoslime, enemy_type_microslime, enemy_type_slimeofgreed, enemy_type_megaslime, enemy_type_slimeasaurusrex, enemy_type_greeneyesslimedragon, enemy_type_unnervingfightingoperator, enemy_type_titanoslime, enemy_type_slimeoidtrainer, enemy_type_ug_slimeoidtrainer, enemy_type_bandito, enemy_type_raiderunderboss, enemy_type_microgullswarm, enemy_type_spacecarp]


# Enemies that spawn during specific poi events
raider_incursion_enemies = [enemy_type_desertraider, enemy_type_bandito, enemy_type_raiderunderboss]
slimeunist_protest_enemies = [enemy_type_protester, enemy_type_antiprotestprotester]
radiation_storm_enemies = [enemy_type_deathclaw, enemy_type_mutatedbarrel]

# List of raid bosses sorted by their spawn rarity.
raid_boss_tiers = {
    "micro": [enemy_type_megaslime, enemy_type_slimernaliajuvie],
    "monstrous": [enemy_type_slimeasaurusrex, enemy_type_unnervingfightingoperator, enemy_type_miserablemiser],
    "mega": [enemy_type_greeneyesslimedragon, enemy_type_titanoslime, enemy_type_slimernaliagangster, enemy_type_thegull],
    # This can be left empty until we get more raid boss ideas.
    # "nega": [],
}

# List of enemies that are simply too powerful to have their rare variants spawn
overkill_enemies = [enemy_type_doubleheadlessdoublehorseman, enemy_type_doublehorse]

# List of enemies that have other enemies spawn with them
enemy_group_leaders = [enemy_type_doubleheadlessdoublehorseman, enemy_type_mammoslimebull]

# Dict of enemy spawn groups. The leader is the key, which correspond to which enemies to spawn, and how many.
enemy_spawn_groups = {
    enemy_type_doubleheadlessdoublehorseman: [enemy_type_doublehorse, 1],
    enemy_type_mammoslimebull: [enemy_type_piloslime, 2]
}

# Enemy drop tables. Values are sorted by the chance to the drop an item, and then the minimum and maximum amount of times to drop that item.
enemy_drop_tables = {
    enemy_type_sandbag: [
        {"sandbag": [100, 1, 1]}
    ],
    enemy_type_juvie: [
        {item_id_slimepoudrin: [50, 1, 2]},
        {rarity_plebeian: [1, 1, 1]},
        {"crop": [10, 1, 1]},
        {item_id_tradingcardpack: [20, 1, 1]},
    ],
    enemy_type_dinoslime: [
        {item_id_slimepoudrin: [100, 2, 4]},
        {rarity_plebeian: [3, 1, 1]},
        {item_id_dinoslimemeat: [33, 1, 2]},
        {item_id_monsterbones: [100, 3, 5]},
    ],
    enemy_type_slimeadactyl: [
        {item_id_slimepoudrin: [100, 3, 5]},
        {rarity_plebeian: [3, 1, 1]},
        {item_id_monsterbones: [100, 3, 5]},
    ],
    enemy_type_microslime: [
        {rarity_patrician: [25, 1, 1]},
    ],
    enemy_type_slimeofgreed: [
        {item_id_slimepoudrin: [100, 2, 2]},
    ],
    enemy_type_desertraider: [
        {item_id_slimepoudrin: [100, 1, 2]},
        {"stripedraidermask": [5, 1, 1]},
        {"shelledraidermask": [5, 1, 1]},
        {rarity_plebeian: [12, 1, 1]},
        {weapon_id_awp: [1, 1, 1]}
    ],
    enemy_type_mammoslime: [
        {item_id_slimepoudrin: [75, 5, 6]},
        {rarity_patrician: [5, 1, 1]},
        {item_id_monsterbones: [100, 1, 3]},
    ],
    enemy_type_doubleheadlessdoublehorseman: [
        {item_id_doublehalloweengrist: [100, 222, 222]},
        {item_id_slimepoudrin: [100, 22, 22]},
        {rarity_plebeian: [100, 22, 22]},
        {rarity_patrician: [100, 22, 22]},
        {item_id_dinoslimemeat: [100, 22, 22]},
        {item_id_tradingcardpack: [100, 22, 22]},
    ],
    enemy_type_doublehorse: [
        {item_id_slimepoudrin: [100, 22, 22]}
    ],
    enemy_type_megaslime: [
        {item_id_slimepoudrin: [100, 4, 8]},
        {rarity_plebeian: [20, 1, 2]},
        {rarity_patrician: [7, 1, 1]},
    ],
    enemy_type_slimeasaurusrex: [
        {item_id_slimepoudrin: [100, 8, 15]},
        {rarity_plebeian: [12, 1, 2]},
        {rarity_patrician: [5, 1, 2]},
        {item_id_dinoslimemeat: [100, 3, 4]},
        {item_id_monsterbones: [100, 3, 5]},
    ],
    enemy_type_greeneyesslimedragon: [
        {item_id_dragonsoul: [100, 1, 1]},
        {item_id_slimepoudrin: [100, 15, 20]},
        {rarity_patrician: [25, 1, 1]},
        {item_id_monsterbones: [100, 5, 10]},
    ],
    enemy_type_unnervingfightingoperator: [
        {item_id_slimepoudrin: [100, 1, 1]},
        {item_id_dinoslimemeat: [100, 1, 1]},
        {item_id_tradingcardpack: [100, 1, 1]},
        {item_id_monofilamentfragment: [100, 1, 1]},
        {"alienscalp": [100, 1, 1]},
    ],
    enemy_type_grey: [
        {item_id_slimepoudrin: [100, 1, 1]},
        {"taco": [33, 1, 1]},
        {"chickenbucket": [33, 1, 1]},
        {"pepperoni": [33, 1, 1]},
        {"alienscalp": [100, 1, 1]},
        {"rosetintedglasses": [5, 1, 1]}
    ],
    enemy_type_tangeloid: [
        {item_id_slimepoudrin: [100, 1, 1]},
        {"tangeloidraygun": [100, 1, 1]},
        {'alienbattery': [20, 1, 1]},
        {"alienscalp": [100, 1, 1]},
    ],
    enemy_type_alienscum: [
        {item_id_slimepoudrin: [100, 1, 1]},
        {"alienbattery": [20, 1, 1]},
        {item_id_dinoslimemeat: [100, 1, 1]},
        {item_id_civilianscalp: [50, 1, 1]},
        {"alienscalp": [100, 1, 1]},
    ],
    enemy_type_bandito: [
        {item_id_slimepoudrin: [100, 1, 3]},
        {rarity_plebeian: [6, 1, 1]},
        {"poncho": [10, 1, 1]}
    ],
    enemy_type_raiderunderboss: [
        {item_id_slimepoudrin: [100, 3, 8]},
        {rarity_plebeian: [10, 1, 2]},
        {"poncho": [25, 1, 1]},
        {"trenchcoat": [25, 1, 1]},
        {"kilmisterhat": [25, 1, 1]},
    ],
    enemy_type_protester: [
        {item_id_slimepoudrin: [100, 1, 1]},
        {rarity_plebeian: [6, 1, 1]},
        {item_id_civilianscalp: [100, 1, 1]},
        {weapon_id_bat: [10, 1, 1]},
        {weapon_id_molotov: [10, 1, 1]},
        {"gasmask": [10, 1, 1]}
    ],
    enemy_type_antiprotestprotester: [
        {item_id_slimepoudrin: [100, 1, 2]},
        {rarity_plebeian: [7, 1, 2]},
        {item_id_civilianscalp: [100, 1, 1]},
        {weapon_id_rifle: [10, 1, 1]},
        {"slimecityflag": [10, 1, 1]},
        {"flagcape": [10, 1, 1]},
        {"slimecityconfederateflag": [10, 1, 1]}
    ],
    enemy_type_deathclaw: [
        {item_id_slimepoudrin: [100, 3, 7]},
        {rarity_patrician: [4, 1, 2]},
        {item_id_leather: [100, 1, 2]},
        {item_id_dragonsoul: [12, 1, 1]},
        {item_id_monsterbones: [100, 2, 8]}
    ],
    enemy_type_mutatedbarrel: [
        {item_id_slimepoudrin: [100, 3, 30]},
    ],
    enemy_type_civilian: [
        {item_id_slimepoudrin: [20, 1, 1]},
        {item_id_civilianscalp: [100, 1, 1]},
    ],
    enemy_type_civilian_innocent: [
        {item_id_slimepoudrin: [20, 1, 1]},
        {item_id_civilianscalp: [100, 1, 1]},
    ],
    enemy_type_titanoslime: [
        {item_id_slimepoudrin: [100, 15, 20]},
        {rarity_patrician: [100, 1, 1]},
        {item_id_monsterbones: [100, 5, 10]}
    ],
    enemy_type_mutated_titanoslime: [
        {item_id_slimepoudrin: [100, 15, 20]},
        {'n6corpse': [100, 1, 1]},
        {item_id_monsterbones: [100, 5, 10]}
    ],
    enemy_type_mammoslimebull: [
        {item_id_slimepoudrin: [75, 6, 8]},
        {rarity_patrician: [5, 1, 1]},
        {item_id_monsterbones: [100, 2, 4]},
    ],
    enemy_type_piloslime: [
        {item_id_slimepoudrin: [10, 1, 1]},
        {item_id_monsterbones: [50, 1, 2]}
    ],
    enemy_type_spacecarp: [
        {item_id_slimepoudrin: [60, 1, 1]},
        {item_id_carpotoxin: [50, 1, 1]},
        {item_id_moonrock: [50, 1, 1]},
    ],
    enemy_type_microgullswarm: [
        {item_id_feather: [50, 1, 1]}
    ],
    enemy_type_thegull: [
        {item_id_rainwing: [50, 1, 1]},
        {item_id_slimepoudrin: [100, 3, 7]},
        {item_id_feather: [100, 1, 3]},
    ],
    enemy_type_policeofficer: [
        {"copbadge":[100, 1, 1]}
    ],
    enemy_type_lesserwerewolf: [
        {item_id_leather: [100, 1, 1]},
        {item_id_slimepoudrin: [100, 1, 3],},
    ],
    enemy_type_skeletonranger: [
        {"bone": [100, 1, 10]},
        {item_id_slimepoudrin: [90, 1, 1]},
    ],
    enemy_type_alm: [
        {item_id_doublehalloweengrist: [100, 1, 4]},
        {weapon_id_broadsword: [100, 1, 1]},
        {item_id_civilianscalp: [100, 1, 1]},
    ],  
    enemy_type_slimernaliajuvie: [
        {item_id_slimepoudrin: [100, 1, 15]},
        {item_id_giftribbon: [80, 1, 6]},
        {item_id_candycane: [100, 1, 10]},
    ],
    enemy_type_slimeoidabuser: [
        {item_id_slimepoudrin: [100, 1, 12]},
        {rarity_plebeian: [20, 1, 1]},
        {item_id_giftribbon: [40, 1, 3]},
    ],
    enemy_type_slimernaliagangster: [
        {item_id_slimepoudrin: [100, 1, 20]},
        {item_id_giftribbon: [100, 2, 5]},
    ],
    enemy_type_spiritofslimernaliapast: [
        {weapon_id_basket: [100, 1, 1]},
        {rarity_patrician: [50, 1, 1]},
        {item_id_slimepoudrin: [10, 10, 25]},
    ],
    enemy_type_drugdealer: [
        {"pileofmysteriouspowder": [25, 1, 1]},
        {item_id_seaweedjoint: [50, 1, 4]},
        {"edibleslime": [50, 1, 2]},
        {item_id_giftribbon: [10, 1, 3]}, 
    ],
    enemy_type_arsonist: [
        {weapon_id_molotov: [100, 1, 1]},
        {item_id_slimepoudrin: [50, 3, 7]},
        {item_id_giftpipebomb: [100, 1, 2]},
        {item_id_giftribbon: [25, 3, 6]},
    ],
    enemy_type_vandal: [
        {weapon_id_spraycan: [100, 1, 1]},
        {item_id_slimepoudrin: [100, 2, 5]},
        {item_id_giftribbon: [60, 1, 2]},
        {"vape": [10, 1, 1]},
        {item_id_mustard_gas_pod: [30, 1, 3]},
        {item_id_cop_killer_cotton_candy_pod: [30, 1, 3]},
        {item_id_mastectomy_mango_pod: [30, 1, 3]},
        {item_id_menthol_mint_pod: [30, 1, 3]},
        {item_id_striking_strawberry_pod: [30, 1, 3]},
        {item_id_ten_story_tobacco_pod: [30, 1, 3]},
        {item_id_moon_dust_pod: [1, 1, 1]},
    ],
    enemy_type_miserablemiser: [
        {item_id_slimepoudrin: [15, 10, 10]},
        {item_id_giftribbon: [90, 1, 9]},
        {"cigar": [30, 3, 12]},
    ],
    enemy_type_illegalimmigrant: [
        {weapon_id_boomerang: [10, 1, 1]},
        {item_id_bustedrifle: [15, 1, 1]},
        {item_id_repairkit: [15, 1, 1]},
        {"sloshhat": [25, 1, 1]},
        {item_id_prankcapsule: [100, 6, 10]},
        {weapon_id_harpoon: [100, 0, 0]},
        {item_id_slimepoudrin: [10, 10, 10]},
        {item_id_giftribbon: [60, 1, 5]},
    ],

}

for enemy in slimeoid_trainers:
    enemy_drop_tables[enemy] = [{item_id_slimepoudrin: [100, 1, 1]}, {rarity_plebeian: [20, 1, 1]}]

# DH
if dh_active:
    for enemy in enemy_drop_tables:
        enemy_drop_tables[enemy].append({item_id_doublehalloweengrist: [6, 8, 10], item_id_doublehalloweengrist: [85, 1, 2], item_id_doublefaggot: [1, 1, 1], item_id_doublestuffedcrust: [2, 1, 1]})

# When making a new enemy, make sure to fill out slimerange, ai, attacktype, displayname, raredisplayname, and aliases.
# Enemy data tables. Slime is stored as a range from min to max possible slime upon spawning.
enemy_data_table = {
    enemy_type_sandbag: {
        "slimerange": [1000000000, 1000000000],
        "ai": enemy_ai_sandbag,
        "attacktype": enemy_attacktype_unarmed,
        "displayname": "Sand Bag",
        "raredisplayname": "Durable Sand Bag",
        "aliases": ["sandbag", "bag o sand", "bag of sand"],
        "description": "\n\nA sandbag, prepared by the Dojo Master himself.",
        "raredescription": "\n\nhttps://cdn.discordapp.com/attachments/619271859627753512/1083146436360818748/Untitled-2.png",
    },
    enemy_type_juvie: {
        "slimerange": [10000, 50000],
        "ai": enemy_ai_coward, 
        "attacktype": enemy_attacktype_unarmed,
        "displayname": "Lost Juvie",
        "raredisplayname": "Shellshocked Juvie",
        "aliases": ["juvie", "greenman", "lostjuvie", "lost", "frost", "frostbitten", "accursed"],
        "arcticvariant" : "Frostbitten Juvie",
        "dhvariant": "Accursed Juvie",
        "description": "\n\n> A living citizen of NLACakaNM, unaffiliated with any gang. Despite its life in such hostile conditions, this prey seems adamant to stay neutral in the conflict. It would be admirable, were it not so pathetic. It is often they wander away from their farms into the Outskirts, but they're hardly even worth killing.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004453371052051/The_Venators_Encyclopedia3.png",
        "raredescription": "\n\n> A lost juvenile that has adapted to life in the Outskirts. I came across this puny little thing as I was out hunting larger game. It appeared to be in a constant state of panic, likely induced by it living in this wasteland for so long.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004469795684384/The_Venators_Encyclopedia4.png",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_dinoslime: {
        "slimerange": [250000, 500000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_fangs,
        "displayname": "Dinoslime",
        "raredisplayname": "Voracious Dinoslime",
        "aliases": ["dino", "slimeasaur"],
        "arcticvariant":"Sabertooth Tigerslime",
        "dhvariant": "Ravenous Dinoshambler",
        "description": "\n\n> A slime-based lifeform, similar in appearance to a velociraptor. After the advent of slime, these creatures began to appear in the Outskirts near the sea. Since then, they've gradually spread out their territory, encompassing the whole of the Outskirts.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004498078138508/The_Venators_Encyclopedia6.png",
        "raredescription": "\n\n> A more powerful and aggressive variation of the Dinoslime, due to a genetic alteration. I have seen many a beast in my days, but none quite as grotesque as this one. It seems whatever this thing is has no context of pack hunting strategy, killing on instinct (even its own kind!).\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004512162611227/The_Venators_Encyclopedia7.png",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_slimeadactyl: {
        "slimerange": [500000, 750000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_talons,
        "displayname": "Slimeadactyl",
        "raredisplayname": "Predatory Slimeadactyl",
        "aliases": ["bird", "dactyl"],
        "dhvariant": "Mutated Crow",
        "description": "\n\n> A slime-based lifeform, similar in appearance to a pterodactyl. Yet more of these dinosaur-esque creatures. It seems that they originate from near the sea, just as the dinoslimes had. Due to them being airborne, it can be difficult to land a blow on them, but they don't pose too much of a threat otuside of that.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004527555444746/The_Venators_Encyclopedia8.png",
        "raredescription": "\n\n> A more powerful Slimeadactyl resembling a quetzalcoatlus, due to a genetic alteration. More and more mutant versions of creatures seem to be popping up these days, though I couldn't tell you why. What I do know is that this prey is massive. I would certainly classify taking it down as an accomplishment.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004542059610142/The_Venators_Encyclopedia9.png",
    },
    enemy_type_desertraider: {
        "slimerange": [250000, 750000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_raiderscythe,
        "displayname": "Desert Raider",
        "raredisplayname": "Desert Warlord",
        "aliases": ["raider", "scytheboy", "desertraider", "desert"],
        "arcticvariant":"Tundra Graverobber",
        "dhvariant": "Reaper",
        "description": "\n\n> A wandering raider left to fend for itself in the outskirts. One of many fiendish outcasts roaming these wastelands. Over time, and with no access to the outside world, the people who once lived here became the bloodthirsty savages seen in the outskirts today. \n> ARCHIVAL NOTE: The Venator's statements may not be historically true.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004563785842809/The_Venators_Encyclopedia10.png ",
        "raredescription": "\n\n> An especially powerful desert raider that has become a ruler due to its strength. Only the toughest of the tough and the strongest of the strong are fit to lead raiders, and it certainly shows in battle. Definitely a prey to watch out for.\n> ARCHIVAL NOTE: The Venator's statements may not be historically true.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004585688760439/The_Venators_Encyclopedia11.png",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_mammoslime: {
        "slimerange": [650000, 950000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_tusks,
        "displayname": "Mammoslime",
        "raredisplayname": "Territorial Mammoslime",
        "aliases": ["mammoth", "brunswick"],
        "arcticvariant": "Frozen Mammoslime",
        "dhvariant": "Irritated Mammoshambler",
        "description": "\n\n> A slime-based lifeform, similar in appearance to a mammoth. Perhaps the fossils underground met with the unique properties of slime, allowing them to !revive? In any case, watch out for this one, its poudrin-tusks pack a punch if you don't steer clear. I learned that the hard way...\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004606643372102/The_Venators_Encyclopedia12.png",
        "raredescription": "\n\n> A more powerful and aggressive variation of the Mammoslime, due to a genetic alteration. This thing is fucking massive. I'm not fucking around. You may think that its name is in reference to it being protective over its own territory, but no, it's because this creature is so large it can be classified as a territory in and of itself. It can't be natural, whatever it is.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004622564950016/The_Venators_Encyclopedia13.png",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_microslime: {
        "slimerange": [10000, 50000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_body,
        "displayname": "Microslime",
        "raredisplayname": "Iridescent Microslime",
        "aliases": ["micro", "pinky"],
        "dhvariant": "Micro Pumpkislime",
        "description": "\n\n> A miniature being made entirely of slime. This thing may put up a fight, but its idea of \"a fight\" is pathetic, quite frankly. However - despite the act of killing it not being that engaging in and of itself - what IS rewarding is the treasure it contains. If you see one, go straight for it.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004649484124250/The_Venators_Encyclopedia14.png",
        "raredescription": "\n\n> A glowing, miniature being made entirely of slime. Exactly the same as a Microslime, except this one is glowing, and has even more treasure held within itself.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004667058126968/The_Venators_Encyclopedia15.png",  
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_grey: {
        "slimerange": [250000, 750000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_graspers,
        "displayname": "Grey Alien",
        "raredisplayname": "Grey with a Burger King Crown On Its Head",
        "aliases": ["greys", "galien", "unnervingfightingoperator", "unnerving"],
        "arcticvariant":"Grey Alien with a Scarf On",
        "description": "\n\n> ENTRY 8194 - Grey Aliens are ██████████ with little regard for human or inhuman life. Origin unknown. Repeated attempts at dissection have yielded little knowledge on their internals.\n - *NMS Astronomy Databanks (Declassified)*, NMS",
        "raredescription": "\n\n> ENTRY 10442 - Grey Aliens with Burger King Crowns On Their Head are aberrant-type ██████████ with an increased ability to terrorize human or inhuman life. Little is known as to how they obtain burger king crowns, nor why seemingly only aberrant-type ██████████ have them. \n - *NMS Astronomy Databanks (Declassified)*, NMS",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_tangeloid: {
        "slimerange": [250000, 500000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_raygun,
        "displayname": "Tangeloid",
        "raredisplayname": "Squiggled Tangeloid",
        "aliases": ["tangela", "tangle", "millite", "milly", "squiggle", "squig"],
        "description": "\n\n> ENTRY 11709 - Tangeloids are cyan-colored ██████████, whose bodies are made up of large, tube-like knots. Origin unknown. They appear to be more intelligent than other ██████████, and possess a great to Field Agents. Their crab-like eyes are a known weak point.\n - *NMS Astronomy Databanks (Declassified)*, NMS",
        "raredescription": "\n\n> ENTRY 11723 - Squiggled Tangeloids are aberrant-type ██████████ who sport a much more orderly and distinguished demeanor. As aberrant-types, they are much stronger and more intelligent than they appear. Some may show human intelligence, but be aware! This is only a dangerous front to trick the empathetic among Us.\n - *NMS Astronomy Databanks (Declassified)*, NMS",
    },
    enemy_type_alienscum: {
        "slimerange": [500000, 750000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_feed,
        "displayname": "Alien Scum",
        "raredisplayname": "Unhinged Alien Psycho",
        "aliases": ["scum", "ascum", "psycho", "unhinged"],
        "description": "\n\n> ENTRY 9900 - Alien Scum are ██████████ who seem to have adversely reacted with Slime. It is unknown why ██████████ would devolve from Slime, but nonetheless, these pose a severe threat to Field Agents. Dissection has been met only with Slime. \n - *NMS Astronomy Databanks (Declassified)*, NMS",
        "raredescription": "\n\n> ENTRY 9945 - Unhigned Alien Psychos are aberrant-type ██████████ who seem to have adversely reacted with Slime. For these ██████████, all Extraterrestrial Research Staff are encouraged to kill on sight, no matter the circumstances. No further notes.\n - *NMS Astronomy Databanks (Declassified)*, NMS",
    },
    enemy_type_slimeofgreed: {
        "slimerange": [20000, 100000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_body,
        "displayname": "Slime Of Greed",
        "raredisplayname": "Slime Of Avarice",
        "aliases": ["slime", "slimeofgreed", "pot", "potofgreed", "draw2cards"],
        "dhvariant": "Slime of Dichotomy",
        "description": "\n\n> Draw 2 cards.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        "raredescription": "\n\n> Target 5 Secreatures in the Sewers; shuffle all 5 into your Inventory, then draw 2 cards.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
    },
    enemy_type_doubleheadlessdoublehorseman: {
        "slimerange": [100000000, 150000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_axe,
        "displayname": "Double Headless Double Horseman",
        "raredisplayname": "Quadruple Headless Quadruple Horseman",
        "aliases": ["doubleheadlessdoublehorseman", "headlesshorseman", "demoknight", "horseman"]
    },
    enemy_type_doublehorse: {
        "slimerange": [50000000, 75000000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_hooves,
        "displayname": "Double Headless Double Horseman's Horse",
        "raredisplayname": "Quadruple Headless Quadruple Horseman's Horse",
        "aliases": ["doublehorse", "horse", "pony", "lilbit"]
    },
    enemy_type_megaslime: {
        "slimerange": [1000000, 1000000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_gunkshot,
        "displayname": "Megaslime",
        "raredisplayname": "Rampaging Megaslime",
        "aliases": ["mega", "smooze", "muk"],
        "arcticvariant":"Antifreeze Megaslime",
        "dhvariant": "Grave Megaslime",
        "description": "\n\n> {emote} An especially large being made entirely of slime. These things have been around for as long as I can remember. Somehow, due to slime's unique life-bringing effect, when enough of it is gathered together it will begin to animate on its own. There seems to only be one thing on its mind once it is brought to life; demolish everything in its immediate vicinity.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004684627935242/The_Venators_Encyclopedia16.png".format(emote=emote_megaslime),
        "raredescription": "\n\n> {emote} A massive, genetically mutated being made entirely of slime. They all seem determined to head directly towards the city, first thing. They only started showing up recently, but as soon as they did, the regular Megaslimes started to mimic their behavior. Perhaps it is a sort of hivemind they share?\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004708019568640/The_Venators_Encyclopedia17.png".format(emote=emote_megaslime),
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_slimeasaurusrex: {
        "slimerange": [1750000, 3000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_fangs,
        "displayname": "Slimeasaurus Rex",
        "raredisplayname": "Sex Rex",
        "aliases": ["rex", "trex", "slimeasaurusrex", "slimeasaurus"],
        "arcticvariant": "Iced-T-Rex",
        "dhvariant": "Pumpkisaurus Rex",
        "description": "\n\n> A gigantic slime-based lifeform, similar in appearance to a Tyrannosaurus Rex. The last, but certainly not least, of the suarian subset of slimey secreatures. Usually the Outskirts are their singular territory, but recently they've been going into the city along with the Megaslimes. I suggested a hivemind previously, but it would seem something else is at play...\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004729926680656/The_Venators_Encyclopedia18.png",
        "raredescription": "\n\n> HEY GUYS IT'S ME THE SEX REX\n - Sex Rex",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_greeneyesslimedragon: {
        "slimerange": [3500000, 5000000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_molotovbreath,
        "displayname": "Green Eyes Slime Dragon",
        "raredisplayname": "Green Eyes JPEG Dragon",
        "aliases": ["dragon", "greeneyes", "greeneyesslimedragon", "green"],
        "arcticvariant": "Blue Eyes Slime Dragon",
        "dhvariant": "Red-Eyes Negaslime Dragon",
        "description": "\n\n> The Green Eyes Slime Dragon is a powerful engine of destruction. Virtually invincible, very few have faced this awesome creature and lived to tell the tale.\n - *Encyclopædia Limus*, NLACakaNM Museum of History \n - https://cdn.discordapp.com/attachments/667820533454340112/745004766483972177/The_Venators_Encyclopedia20.png",
        "raredescription": "\n\n> Due to the sheer amount of JPEG artifacts coating its skin, the Green Eyes JPEG Dragon is significantly more dangerous than its slime counterpart. When it roars, it's reminiscent of a scream filtered through a 2000s-era microphone.\n - *Encyclopædia Limus*, NLACakaNM Museum of History \n - https://cdn.discordapp.com/attachments/667820533454340112/745004791222239232/The_Venators_Encyclopedia21.png",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_unnervingfightingoperator: {
        "slimerange": [1000000, 3000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_armcannon,
        "displayname": "Unnerving Fighting Operator",
        "raredisplayname": "Unyielding Fierce Operator",
        "aliases": ["ufo", "alien", "unnervingfightingoperator", "unnerving"],
        "arcticvariant":"Unflinching Frozen Operator",
        "dhvariant": "Unworldly Ferocious Owl",
        "description": "\n\n> An enigmatic enemy of unknown species and origin. It feels strange to document these unusual beings, considering I know so little about them. \n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004817738367136/The_Venators_Encyclopedia22.png",
        "raredescription": "\n\n> An exponentially more powerful variation of the Unnerving Fighting Operator. These entities are somehow even harder to come by and gather information on than their less-powerful counterparts.\n - *The Venator's Encyclopedia*, The Venator\n - https://cdn.discordapp.com/attachments/667820533454340112/745004840295333969/The_Venators_Encyclopedia23.png",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_titanoslime: {
        "slimerange": [5000000, 7000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_stomp,
        "displayname": "Titanoslime",
        "raredisplayname": "Miscreated Titanoslime",
        "aliases": ["titano", "titanoslime", "biglizard"],
        "dhvariant": "Ghoulific Titanogreslime",
        "description": "\n\n> Titanic beasts, Titanoslimes are horrific additions to NLACakaNM's sauropod population. Created in labs by the now-dead N6, Titanoslimes were unleashed prior to the raid against the now-defunct Slimecorp. Nowadays, they've taken up their own niche in NLACakaNM's wild ecosystem.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        "raredescription": "\n\n> Malformed variants of their genetically-stable counterparts, Miscreated Titanoslimes came out of the lab vats *wrong*. Their specific deformities vary, but nonetheless, they are unparalleled in maiming citizens.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
    },
    enemy_type_mutated_titanoslime: {
        "slimerange": [10000000, 10000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_stomp_n6,
        "displayname": "N6 on a Mutated Titanoslime",
        "raredisplayname": "Miscreated Mutated Titanoslime",
        "aliases": ["n6", "mutatedtitanoslime", "mutated", "titanoslime", "bigtitano"]
    },
    enemy_type_piloslime: {
        "slimerange": [20000, 30000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_tusks,
        "displayname": "Piloslime",
        "raredisplayname": "Shiny Piloslime",
        "aliases": ["piloswine", "mammoslimejr", "pleboslime", "shinypiloslime"],
        "arcticvariant":"Terastallized Piloslime",
        "description": "\n\n> A Piloslime is covered by a thick coat of long hair for enduring freezing cold. It uses its tusks to dig up food that has been buried underground.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        "raredescription": "\n\n> Shiny Piloslimes are rarer variants of Piloslimes, with bright yellow coats. This shaggy coat makes it unable to see. It checks surroundings with its sensitive nose instead.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        # "arcticdescription": "\n\n> \n - *MT. SRXEK GUIDEBOOK*, Author Unknown",
    },
    enemy_type_spacecarp: {
        "slimerange": [100000, 100000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_gnash,
        "displayname": "Space Carp",
        "raredisplayname": "Space Patriarch",
        "aliases": ["carp", "space", "spacedad", "spacepatriarch", "ss13"],
        "dhvariant": "Space Gill-man",
    },
    enemy_type_mammoslimebull: {
        "slimerange": [100000, 100000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_tusks,
        "displayname": "Mammoslime Bull",
        "raredisplayname": "Apex Mammoslime",
        "aliases": ["mammoswinebull", "swinebull", "mammobull", "apex", "apexmammoslime"],
        "description": "\n\n> More hostile than their larger counterparts, Mammoslime Bulls are smaller, rowdier, more aggressive Mammoslimes. Their fur was frequently used for Pueblo clothing, so make sure to snag its pelt if you ever get the chance.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        "raredescription": "\n\n> Even *more* hostile than their less rare counterpart, Apex Mammoslimes are the fiercest Mammoslimes in all of NLACakaNM. Despite still being smaller than their larger Mammoslime counterparts, they are still known for overcoming them in a fight.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
    },
    enemy_type_microgullswarm: {
        "slimerange": [100000, 100000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_beak,
        "displayname": "Micro Gull Swarm",
        "raredisplayname": "Micro Gull Cloud",
        "aliases": ["microgull", "smallgull", "birdswarm", "gullcloud", "gullswarm"],
        "dhvariant": "MiCrow Swarm",
        "description": "\n\n> A bunch of little fucking birds. What else can be written about these?\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        "raredescription": "\n\n> When many Micro Gull Swarms meet, they form a Micro Gull Cloud. These masses of bird can act as one mind, making them a horrifically deadly phenomenon.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
    },
    enemy_type_thegull: {
		"slimerange": [3500000, 7000000],
		"ai": enemy_ai_attacker_a,
		"attacktype": enemy_attacktype_beak,
		"displayname": "The Gull",
		"raredisplayname": "The Land-Gull",
		"aliases": ["seagull", "thegull", "seabird", "cgull", "landgull"]
	},
    enemy_type_civilian: {
        "slimerange": [100001, 100001],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "Bloodthirsty Civilian",
        "raredisplayname": "Closet Serial Killer",
        "aliases": ["townsfolk", "citizen", "civilian", "bloodthirsty", "person"]
    },
    enemy_type_civilian_innocent: {
        "slimerange": [100001, 100001],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "Innocent Civilian",
        "raredisplayname": "Puppy-Eyed Youth",
        "aliases": ["townsfolk", "citizen", "civilian", "innocent", "person"]
    },
    enemy_type_slimeoidtrainer: {
        "slimerange": [10001, 10001],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "Slimeoid Trainer",
        "raredisplayname": "Slimeoid Champion",
        "aliases": ["slimeoidt", "st", "strainer", "champ", "trainer"],
        "dhvariant": "Costumed Slimeoid Trainer",
    },
    enemy_type_ug_slimeoidtrainer: {
        "slimerange": [10001, 10001],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "Suspicious Slimeoid Trainer",
        "raredisplayname": "Villainous Slimeoid Champion",
        "aliases": ["slimeoidt", "sst", "sstrainer", "champ", "sustrainer", "villain"],
        "dhvariant": "Double Costumed Slimeoid Trainer",
    },
    enemy_type_npc: {
        "slimerange": [100000, 100000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "NPC",
        "raredisplayname": "NPC Template",
        "aliases": []
    },
    enemy_type_policeofficer: {
        "slimerange": [100000, 500000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_cop,
        "displayname": "Police Officer",
        "raredisplayname": "Crazed Police Officer",
        "aliases": ["cop", "police", "policeofficer", "officer", "pig"]
    },
    enemy_type_bandito: {
        "slimerange": [300000, 600000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_wesson,
        "displayname": "Bandito",
        "raredisplayname": "Bandito Supreme",
        "aliases": ["bandit", "banditosupreme"],
        "dhvariant": "Candy Bandit",
    },
    enemy_type_raiderunderboss: {
        "slimerange": [1000000, 2000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_wesson,
        "displayname": "Raider Underboss",
        "raredisplayname": "Raider Overboss",
        "aliases": ["raiderboss", "underboss", "overboss"],
        "dhvariant": "Door-to-door Raider Underboss",
    },
    enemy_type_protester: {
        "slimerange": [10000, 20000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "Slimeunist Protester",
        "raredisplayname": "False Flag Protester",
        "aliases": ["falseflagprotester", "slimeunist", "protestor"]
    },
    enemy_type_antiprotestprotester: {
        "slimerange": [15000, 30000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "Anti-Protest Protester",
        "raredisplayname": "False Flag Anti-Protest Protester",
        "aliases": ["antiprotest", "antiprotester", "antiprotestor", "anti", "falseflagantiprotestprotester"]
    },
    enemy_type_deathclaw: {
        "slimerange": [5000000, 7000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_gnash,
        "displayname": "Deathclaw",
        "raredisplayname": "Legendary Deathclaw",
        "aliases": ["legendarydeathclaw"],
        "description": "\n\n> The Deathclaw is a mysterious cryptid that is rumored to haunt Little Chernobyl in times of great calamity. Little is known about its true nature, and its veracity is frequently debated by Slime historians. \n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        "raredescription": "\n\n> My God! My God! A Legendary Deathclaw has got my baby!\n - *Martha*, Mother (Later Arrested for Child Murder)",
    },
    enemy_type_mutatedbarrel: {
        "slimerange": [1000, 5000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_gunkshot,
        "displayname": "Bipedal Mutated Barrel",
        "raredisplayname": "Quadrupedal Mutated Barrel",
        "aliases": ["bipedalmutatedbarrel", "quadrupedalmutatedbarrel", "barrel"],
        "description": "\n\n> The Bipedal Mutated Barrel is a cryptid that originates from Little Chernobyl's Nuclear Power Plant, though how exactly it emerged isn't clear. It is said this nuclear barrel with legs is known to play with Little Chernobyl children on the haziest of nights.\n - *Encyclopædia Limus*, NLACakaNM Museum of History",
        "raredescription": "\n\n> The Bipedal Mutated Barrel's cryptid pet, the Quadrupedal Mutated Barrel is a ferocious dog in the shape of a nuclear barrel with legs. It is said it eats children who are too obedient to their parents.\n - *Encyclopædia Limus*, NLACakaNM Museum of History"
    },
    enemy_type_lesserwerewolf: {
        "slimerange": [100000, 2000000], # BIG range
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_gnash,
        "displayname": "Lesser Werewolf",
        "raredisplayname": "Greater Werewolf",
        "aliases": ["lesserwerewolf", "greaterwerewolf", "werewolf"]
    },
    enemy_type_skeletonranger: {
        "slimerange": [1000000, 2000000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_bonemerang,
        "displayname": "Skeleton Ranger",
        "raredisplayname": "Skeleton Warden",
        "aliases": ["sranger", "swarden", "skeletonwarden"],
    },
    enemy_type_alm: {
        "slimerange": [1000, 5000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_axe,
        "displayname": "Alm Fire Emblem",
        "raredisplayname": "Alm Fire Emblem Conqueror",
        "aliases": ["alm", "fireemblem"],
        "description": "https://cdn.fireemblemwiki.org/thumb/2/29/Portrait_alm_fe15.png/150px-Portrait_alm_fe15.png",
        "raredescription": "https://cdn.fireemblemwiki.org/d/d7/FESoV_Conqueror_concept.png",
    }, 
    enemy_type_slimernaliajuvie: {
        "slimerange": [1000000, 3000000],
        "ai": enemy_ai_attacker_b, 
        "attacktype": enemy_attacktype_bluntweapon,
        "displayname": "Festive Juvie",
        "raredisplayname": "Found Juvie",
        "aliases": ["juvie", "greenman", "foundjuvie", "found", "festive", "festivejuvie"],
    },
    enemy_type_vandal: {
        "slimerange": [600000, 1200000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_gunkshot,
        "displayname": "Rebellious Vandal",
        "raredisplayname": "Vicious Vandal",
        "aliases": ["vandal", "rebellious", "vicious", "rebelliousvandal", "viciousvandal"],
    },
    enemy_type_illegalimmigrant: {
        "slimerange": [750000, 1200000],
        "ai": enemy_ai_attacker_b,
        "attacktype": enemy_attacktype_bonemerang,
        "displayname": "Illegal Immigrant",
        "raredisplayname": "Legal Immigrant But They Are Missing Their Visa",
        "aliases": ["illegal", "legal", "immigrant", "visa", "australian", "illegalimmigrant", "legalimmigrantbuttheyaremissingtheirvisa"], 
    },
    enemy_type_arsonist: {
        "slimerange": [250000, 750000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_molotovbreath,
        "displayname": "Agitated Arsonist",
        "raredisplayname": "Agitated Larcenist",
        "aliases": ["agitated", "arsonist", "agitatedarsonist", "larcenist", "agitatedlarcenist"],
    },
    enemy_type_spiritofslimernaliapast: {
        "slimerange": [100000, 900000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_amateur,
        "displayname": "Spirit of Slimernalia Past",
        "raredisplayname": "Spirit of Slimernalia Present",
        "aliases": ["spirit", "slimernalia", "staydead", "past", "present", "spiritofslimernaliapast", "spiritofslimernaliapresent"],
    },
    enemy_type_slimernaliagangster: {
        "slimerange": [5000000, 8000000],
        "ai": enemy_ai_coward,
        "attacktype": enemy_attacktype_unarmed,
        "displayname": "Enlisted Gangster",
        "raredisplayname": "Enlisted Goon",
        "aliases": ["idiot", "enlistedgangster", "enlisted", "gangster", "goon", "enlistedgoon"],
    },
    enemy_type_drugdealer: {
        "slimerange": [40000, 100000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_unarmed,
        "displayname": "Drug Dealer",
        "raredisplayname": "Drug Stealer",
        "aliases": ["drug", "dealer", "drugdealer", "stealer", "drugstealer"],
    },
    enemy_type_slimeoidabuser: {
        "slimerange": [3000000, 5000000],
        "ai": enemy_ai_attacker_a,
        "attacktype": enemy_attacktype_raiderscythe,
        "displayname": "Slimeoid Abuser",
        "raredisplayname": "Negaslimeoid Abuser",
        "aliases": ["abuser", "slimeoid", "negaslimeoid", "slimeoidabuser", "negaslimeoidabuser"],
    },
    enemy_type_miserablemiser: {
        "slimerange": [4000000, 6000000],
        "ai": enemy_ai_defender,
        "attacktype": enemy_attacktype_wesson,
        "displayname": "Miserable Miser",
        "raredisplayname": "Miserable Scrooge",
        "aliases": ["miser", "miserable", "scrooge", "miserablemiser", "miserablescrooge"],
    },
}

# Raid boss names used to avoid raid boss reveals in ewutils.formatMessage
raid_boss_names = []
for enemy in enemy_data_table.keys():
    if enemy in raid_bosses:
        raid_boss_names.append(enemy_data_table[enemy]["displayname"])
        raid_boss_names.append(enemy_data_table[enemy]["raredisplayname"])

# Responses given by cowardly enemies when a non-ghost user is in their district.
    coward_responses = [
    "The {} calls out to you: *H-Hello. Are you one of those Gangsters everyone seems to be talking about?*",
    "The {} calls out to you: *You wouldn't hurt a {}, would you?*",
    "The {} calls out to you: *Why.. uh.. hello there? What brings you to these parts, stranger?*",
    "The {} calls out to you: *L-look at how much slime I have! I'm not even worth it for you to kill me!*",
    "The {} calls out to you: *I'm just a good little {}... never hurt nobody anywhere...*",
    ]

# Responses given by cowardly enemies when hurt.
    coward_responses_hurt = [
    "\nThe {} cries out in pain!: *Just wait until Juvieman hears about this!!*",
    "\nThe {} cries out in pain!: *You MONSTER!*",
    "\nThe {} cries out in pain!: *What the H-E-double-hockey-sticks is your problem?*",
    ]

# Letters that an enemy can identify themselves with
identifier_letters = [
    'A', 'B', 'C', 'D', 'E',
    'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
]

gvs_almanac = {
    'poketubers': 'Poketubers are mines that deal massive damage when a shambler tries to attack one of them. However, they must take 15 seconds to prime beforehand, otherwise they\'re sitting ducks. When given a Joybean, they will entrench their roots into the ground ahead of them, spawning more fully primed poketubers in random locations ahead of it.\nPoketuber used to be a big shot. His analysis channel with Dire Apples was the talk of the town, even getting big shots like Aushucks to turn their heads in amazement. Nowadays though, he\'s washed up, and has to shill his patreon just to get by. "God, just fucking step on me already and end it all", Poketuber thinks to himself every day.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743641434841808967/poketubers_seedpacket.png',
    'pulpgourds': 'Gaiaslimeoids anywhere on the field can drink out of Pulp Gourds, replenishing their HP and draining that Pulp Gourd\'s storage in the process. Pulp Gourds can only be refilled by Blood Cabbages. When given a Joybean, their healing effect is doubled.\nPulp Gourd is the faithful and humble servant of Blood Cabbage, aiding her in her experiments. "I would sooner walk into the fires of Hell than see a wound on your leaves, Miss Cabbage", says Pulp Gourd. "Ohohoho~, you spoil me, sir Gourd", replies Blood Cabbage. Other Gaiaslimeoids aren\'t sure what the nature of their relationship is, and frankly it weirds them out a bit.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258076152332339/pulpgourds_seedpacket.png',
    'sourpotatoes': 'Sour Potatoes are a great front-line attacker for any Garden Op. They can\'t dish out constant damage like a Pink Rowddish, but they make up for it by swallowing almost any shambler in front of it whole, killing it instantly. This immobilizes the Sour Potato for 10 seconds, however, leaving it vulnerable to attacks. When given a Joybean, they can launch out a ball of fire, which melts away the frozen slime trail left by Shambonis, in addition to dealing a fair amount of splash damage.\nIn a twist of fate, Sour Potatoes have turned into a popular pet across NLACakaNM. This is in opposition of the fact that Sour Potatoes are sentient, and aware of their own domestication. "Awww, who\'s a cute widdle doggy", a Juvenile says. "I can speak English you know. I\'m forming proper sentences, for fucks sake. Treat me with some dignity, *please*", says Sour Potato.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241053598908466/sourpotatoes_seedpacket.png',
    'bloodcabbages': 'Attacks coming from a Blood Cabbage are relatively weak compared to their Rowddish and Killiflower cohorts, but they have a special effect of draining health from enemy shamblers and redistributing it to their allies. They cannot heal themselves, however. When given a Joybean, their attacks will deal twice as much damage, and heal twice as much as a result. They can heal any Gaiaslimeoid within range, but will prioritize those that are low on health, saving Pulp Gourds for last.\nBlood Cabbage\'s obsession with the dark arts led her down an equally dark path in life. After pouring over countless forbidden tomes, she had found what she had been seeking, and used the hordes of undead Shamblers as her test subjects to measure her abilities. "Ahahaha... what a discovery! This ability will prove to be useful... whether my allies like it or not!"\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241003779227718/bloodcabbages_seedpacket.png',
    'joybeans': 'Joybeans act as an upgrade to other Gaiaslimeoids. They can either be planted onto blank tiles and used later when combined with other Gaiaslimeoids, or they can be planted on top of other Gaiaslimeoids. If two Joybeans combine, they explode into a fountain of sheer ecstasy, activating the Joybean effects of all Gaiaslimeoids within a short radius for 30 seconds. It is consumed upon use.\nJoybean is very excitable. When in the presence of another Gaiaslimeoid, she can\'t help but start hyperventilating at the thought of being near them, and is frequently unable to contain herself. "Kyaaaaaa~!" Joybean cries out, as she glomps onto fellow Gaiaslimeoids.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241010506891374/joybeans_seedpacket.png',
    'purplekilliflower': 'Purple Killiflowers shoot out toxic vape clouds when they !dab. This allows them to target shamblers up to 6 tiles in front of them, piercing multiple Shamblers in the process. When given a Joybean, it will deal twice as much damage.\n"Fuck you Dad! It\'s called The Vapors, and it\'s way better than any shitty comic book you\'ve ever read! God, I HATE YOU!", says Killiflower, as he slams the door shut behind him. Choking back tears, he mutters to himself: "Don\'t let him see you cry..."\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241012104921098/killiflower_seedpacket.png',
    'razornuts': 'Razornuts aren\'t as hard or long as Suganmanuts, but their sharpened edges will harm any Shambler that tries to attack it. If a Razornut is damaged, you can !plant another one on top of it to repair it. When given a Joybean, its death will cause an explosion of shrapnel, dealing a fair amount of damage within a large radius around it.\nWhen a Shambler bites into Razornut, he doesn\'t care. He lets it happen, just to *feel* something. "Go on, give me your best. You aren\'t half as strong as the thugs I\'ve mauled in the past", says Razonut. "This shell right here, it\'s ready for the apocalypse.", he continues.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241045348843530/razornuts_seedpacket.png',
    'pawpaw': 'When planted, a Pawpaw will explode after a short amount of time, dealing massive damage in a small radius. If a Pawpaw is planted on top of a Joybean, this will increase its range significantly.\nPawpaw has been places and seen shit you would not believe. The guilt of his war crimes will be taken with him to the grave. "It\'s a good day to die.", says Pawpaw.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258148239966308/pawpaw_seedpacket.png',
    'sludgeberries': 'Sludgeberries are a Gaiaslimeoid that will detonate into a sticky and immobilizing sludge, inflicting a stun effect on all shamblers within a short range. When given a Joybean, it will cover all Shamblers on the field in this sludge.\nThese Gaiaslimeoids are all the craze over at Pyrope Farms. "UM, G4RD3N G4NK3RS? SORRY, BUT W3 ONLY WORK UND3R DIR3CT ORD3RS FROM T3R3Z1 G4NG", says Sludgeberry.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241051401224192/sludgeberries_seedpacket.png',
    'suganmanuts': 'Suganmanuts\' large health pool allows it to provide a great amount of defensive utility in battle. If a Suganmanut is damaged, you can !plant another one on top of it to repair it. When given a Joybean, it will occasionally spit out its nut, ricocheting off of shamblers.\n"I swear I\'m not gay" says Suganmanuts. "I just like the taste". The look in his eye told a different story, however. That, and the 50 tabs of Grimedr he had open.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743240999492649071/suganmanuts_seedpacket.png',
    'pinkrowddishes': 'Pink Rowddishes attack by !thrash-ing about, dealing massive damage to all Shamblers within a short range in front of them. They can attack behind themselves as well. When given a Joybean, it will begin to violently scream. These screams act as an increase to its range, reaching three times as far as a basic attack.\nRowddishes are hot-blooded and looking to brawl. Though they have no eyes, they make up for it with intense reflexes. In some instances, they will even go as far as to lash out at the Garden Gankers who have planted them. "Back off, Juvie!", says Rowddish. "Unless you want me to turn you into a knuckle sandwich! Ha! Up-five", he says as he hi-fives himself. Even when there are no Shamblers around, Rowddishes will continue to pick fights with each other, frequently engaging in what are known as "No Hard Feelings Civil Wars".\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258274761015326/pinkrowddish_seedpacket.png',
    'dankwheat': 'Dankwheat tend to be a utility-focussed Gaiaslimeoid, dealing minimal damage, but whatever does enter their short attack radius that surrounds them will be slowed down by a status effect. When given a Joybean, it can reach further in front and in back of it for targets, and the status effect will also lower the damage output of its targets.\n"Dude, what\'s a text command?" one stalk of Dankwheat says. "Dude, what GAME are we even IN right now??", another adds. "Guys, wait, hold on, my seaweed joint is running out, can one of you spot me?", the third one chimes in. These guys can never seem to get their fucking heads straight, outside of the 22 minutes every Saturday that a new MLP episode is on the air.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241007025488023/dankwheat_seedpacket.png',
    'brightshade': 'Brightshades are an essential plant to have in any Garden Op. They provide Garden Gankers with precious gaiaslime, at a rate of 25 gaiaslime every 20 seconds. When given a Joybean, this output is doubled in effectiveness.\nIn her past, Brightshade was a beautiful singer, frequently selling out even to large crowds. When the Shamblers came to town, she decided to put her career on hold, however. She is a shining gem among Gaiaslimeoids, revered and loved by all, and by some, perhaps a bit too much...\n"I just got this Brightshade poster off of Amoozeon, and oh my fucking God, you can see her TITS."\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241005406486658/brightshade_seedpacket.png',
    'blacklimes': 'When a Black Lime gets bitten, its sour taste will repulse the shambler and redirect it to a different lane entirely. If a Black Lime is damaged, you can !plant another one on top of it to repair it. When given a Joybean, it will shoot out a damaging stream of lime juice, shuffling all shamblers within its lane, and it will also be healed fully.\nOther Gaiaslimeoids worry about Black Lime... what he might do, who he might become. They only hang out with him as a preventative measure. "He\'s... he\'s just different, you know?", says Brightshade as she watches Black Lime brutally torture disease-infested rodents from a safe distance.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241002319347873/blacklimes_seedpacket.png',
    'phosphorpoppies': 'Phosphorpoppies will give Shamblers a \'bad trip\' when it shoots out its Binaural Brainwaves, or when it gets eaten. This will cause Shamblers to either hit, miss, or backfire in their attacks. When given a Joybean, its Binaural Brainwaves will inflict this effect 100% of the time, otherwise the effect only has a chance to be inflicted.\nPhosphoroppy is a total klutz, but she tries her best. Her simple-minded innocence led to her becoming a fan-favorite among many of the Garden Gankers, but behind those swirly eyes remains a horrible tragedy. A psychadelic experience aided by one of the Dankwheat brothers caused her to overload and see things no Gaiaslimeoid was meant to see. It fractured her mind, but her heart is still in there, ready to take on the Shamblers with everything she\'s got.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258227696730152/phosphorpoppies_seedpacket.png',
    'direapples': 'Dire apples are a vital Gaiaslimeoid to have in any offensive setup. They can lob globules of acid or spit bullet seeds. When given a Joybean, their seed attacks will do more damage and will inflict an acidic burn on whatever shamblers it manages to hit.\n"How does a Gaiaslimeoid like me make the best of both worlds collide? Well, I could tell you, but I\'ve got a BIG meeting to catch." He speeds away in his sports car occupied by himself and several Phosphorpoppies. Only a puff of smoke is left behind.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241008828907660/direapples_seedpacket.png',
    'rustealeaves': 'Rustea Leaves are a grounded Gaiaslimeoid, and can attack only within a very short range of where they are planted. They are completely immune to conventional methods of Shambler offense, however, only being damaged by Gigashamblers, Shambonis, and UFO Shamblers. They can be planted on any tile, provided it\'s not already occupied by another Rustea Leaves. When given a Joybean, they will receive a significant boost in both health and damage output.\nRustea Leaves are the amalgamation of leftover shavings off of other metallic crops, culminating into one fearsome Gaiaslimeoid. He is the forgotten fourth member of the Metal Crop Bros, but despite all this, he manages to maintain a positive attitude. "You gotta work with tha hand yah dealt", he says. "These shamblahs ain\'t gonna moida themselves." Regardless of what he says though, he\'s still bitter about not being invited to the family reunion.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241049073254460/rustealeaves_seedpacket.png',
    'metallicaps': 'Metallicaps are a metallic upgrade Gaiaslimeoid, meaning that it can be planted on any tile, provided that a Steel Bean or Aushuck is not already occupying that tile. When planted on top of an attacking Gaiaslimeoid, it will provide a boost in damage, as well as an additional amount of damage in the form of a spores effect, which burns away the health of enemy shamblers. It cannot be given a Joybean. It is consumed upon use, much like a Joybean.\nMetallicap is a rebellious youth, and the youngest member of the Metal Crop Bros. His affinity for metal music drives his other brothers up the goddamn wall, given how often he will throw parties over at the house and blast his music through his custom-made boombox. "Rules? HA! There\'s only one rule in this house brah, and that is, *TO GET DOWN AND PARTY!!!*", he says.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241014118187059/metallicaps_seedpacket.png',
    'steelbeans': 'Steel Beans are a metallic upgrade Gaiaslimeoid, meaning that it can be planted on any tile, provided that a Metallicap or Aushuck is not already occupying that tile. When planted on top of a gaiaslimeoid, it will act as an additional layer of health that a shambler must get rid of before it can attack the Gaiaslimeoid being protected. If a Steel Bean is damaged, you can !plant another one on top of it to repair it. It cannot be given a Joybean.\nSteel Bean is the middle child of the Metal Crop Bros. He has a deep fascination with conspiracy theories, to the point where his brothers seriously worry about his mental state at times. "We\'re all in a simulation man, they\'re pulling our strings with commands and we just have to follow what\'s in the program." When asked to clarify what he meant by this, Steel Bean replied "You wouldn\'t get it..."\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241056048644126/steelbeans_seedpacket.png',
    'aushucks': 'Aushucks are a metallic upgrade Gaiaslimeoid, meaning that it can be planted on any tile, provided that a Metallicap or Steel Bean is not already occupying that tile. When planted on top of a Gaiaslimeoid, it will produce Gaiaslime at the same rate as a regular brightshade. It can be planted on top of any Gaiaslimeoid, including Brightshades. It cannot be given a Joybean. It is consumed upon use, much like a Joybean.\nAushuck is the eldest of the Metal Crop Bros. He got in on the ground floor with SlimeCoin after the last market crash and made a killing, and from then on he\'s been living the high life. His newfound wealth enables his smug personality, much to the ire of his younger brothers. Everything he owns is gold plated, including all his furniture and clothing. "Look at me, I fucking OWN this city", he says as he stands on the balcony of his luxury condo.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241000918450196/aushucks_seedpacket.png',
    'partypoppeppers': 'Party Poppeppers are a Gaiaslimeoid that were never used on the battlefield, as their seeds were not uncovered until long after the end of Garden Ops. \nParty Poppeppers are a real party animal, screaming through the night. When not being the life of the party, they\'re actually chillaxing and a pretty low energy, laid-back kind of dude. \nhttps://cdn.discordapp.com/attachments/875184852746514433/891796268706299925/gc_partypoppepper.png', # Love you Smearg UwU

    'defaultshambler': 'The Default Shambler is exactly what it sounds like. It has low defenses and low attack, and will slowly move towards the edge of the field.\n"Ughhhhhhhh, criiiiiiiinnnnngggggeeeee. Baaaaaasssseeeddddddd. Duuuuuddee I loooooovvveeee braaiiiiiiinnnnnnnzzzzz", says Default Shambler, as he lurches toward an enemy Gaiaslimeoid. they\'re all like this. Copy and paste this for every single type of Shambler, you aren\'t missing much.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241123576807435/defaultshambler_gravestone.png',
    'bucketshambler': 'The KFC Bucket shambler is exactly the same as a Default Shambler, it just has more HP.\nShamblers don\'t need to eat regular food, but they sometimes do, just for the enjoyment of chowing down on some nice fast food. They tend to go overboard, however, frequently placing the entire KFC bucket over their head just to get the last few crumbs down their gullet. This is how every KFC Bucket shambler is born, as they are too stupid to figure out how to take it off.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241141293416568/kfcbucket_shambler.png',
    'juveolanternshambler': 'The Juve-O\'-Lantern shambler is exactly the same as a Default Shambler, it just has significantly more HP.\nThe Juve-O\'-Lantern is crafty, at least by Shambler standards. He has taken a product of the Garden Gankers and used it against them. This increase in defense compensates for the lack of vision it provides, but to be fair Shamblers don\'t really need to worry about that when their only concern is with moving forward in a straight line.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241134977056858/juveolanternshambler_gravestone.png',
    'flagshambler': 'The Flag Shambler is exactly the same as a Default Shambler in terms of health and damage output, but it has the unique ability of boosting the damage of all shamblers in its lane when it is present.\nThe Flag Shambler is one of the best units to have in a Graveyard Op, if only for his enthusiasm for the cause. He\'s gone as far as releasing his own album dedicated to Shambler pride, including sleeper hits such as "Amazing Brainz" and "Take Me Home, Shambler Road".\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241129260089374/flagshambler_gravestone.png',
    'shambonidriver': 'The Shamboni is a specialized unit, killing anything in its path and leaving behind a frozen slime trail, of which Gaiaslimeoids cannot be planted on. There\'s a catch, however: If it drives over Rustea Leaves or a primed Poketuber, it will not survive the attack and explode instantly.\nBeing turned into a Shambler has given the Shamboni Driver a new lease on life. In his past, he worked long hours with little pay, cleaning the Ice Rink over at Slime\'s End like any other wagecuck, but now he is a brave soldier in Dr. Downpour\'s army of the undead. Drive on, Shamboni. We believe in you.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241174197731389/shambonidriver_gravestone.png',
    'mammoshambler': 'The Mammoshambler is a Shambler Mammoslime. It may be slow, but it\'s tough as hell. It can slide on the frozen slime trail left behind by Shambonis to move as fast as a normal Shambler.\nMammoslimes were already bereft of any intelligent thoughts, but being turned into a Shambler has just made things worse. It will frequently be unable to tell friend from foe, and leave many ally Shamblers caught in the crossfire when it slams its massive tusks into the ground. Despite their massive size, they are terrified of Microshamblers.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241144229691463/mammoshambler_gravestone.png',
    'gigashambler': 'The Gigashambler is a powerful attacking unit. It is very slow, but can practically one-shot anything in its path once it lands a hit. It will toss a Microshambler off of its back when it is below half of its maximum health.\nThe Gigashambler is what every shambler aspires to be. When he enters the field, you will know. You won\'t just *see* him, you\'ll *sense* him and his chad-like presence. He\'ll make your heart rock. He\'ll make your dick rock. He\'ll make your ass fucking shake, bro.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241132112085123/gigashambler_gravestone.png',
    'microshambler': 'The Microshambler is a smaller version of the Default Shambler. He may not have much health, but he can be a vital distraction or even tear up the backlines of a Gaiaslimeoid defense if left unattended. One punch from a Pink Rowddish will send him flying.\nIf Microshambler could speak in complete sentences, he would probably say something like "Being small has its benefits. I may not be able to ride all the rollercoasters I want, but I\'m light enough for Big Bro to carry me on his back and give me a good view of the battlefield."For lack of a better word, he\'s the \'brainz\' of the Gigashambler/Microshambler tag team.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743259271298416640/microshambler_gravestone.png',
    'shamblersaurusrex': 'The Shamblersaurus Rex is a Shambler Slimeasaurus Rex. It is fairly bulky and can dish out reasonable damage, but the main draw is its mighty roar, which will stun all Gaiaslimeoids on the field for a brief time, once it reaches below half of its maximum health\n"A pitiable creature. It has the potential to be the king of this city, but it\'s held back by its lust for meat." comments Dr. Downpour. In an effort to maximize the potential of the Shamblersaurus Rex, he re-wired its brain and body to be an omnivore, setting it free to rampage onward towards Gaiaslimeoids and sate its hunger.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241168204333116/shamblersaurusrex_gravestone.png',
    'shamblerdactyl': 'The Shamblerdactyl is a Shambler Slimeadactyl. It will not attack in a conventional manner, instead opting to swoop down from the skies and snatch Gaiaslimeoids away from the field, effectively killing them instantly. Sour Potatoes can swallow them whole before it can have the chance to land this attack, however, and Phosphorpoppies will thwart their attacks outright if they are nearby a Shamblerdactyl.\nNo one knows where Shamblerdactyls take their victims after they are whisked away into the skies. Shambologists theorize that they are taken to somewhere in outskirts where their nest lies and newborn Shamblerdactyls are born and raised. At least, they would, if they weren\'t so wall-eyed and prone to crashing into things.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241161350709308/shamblerdactyl_gravestone.png',
    'dinoshambler': 'The Dinoshambler is a Shambler Dinoslime. It will not attack in a conventional manner, instead opting to jump over all Gaiaslimeoids in its path. This allows it to be a considerable threat against Garden Gankers who do not put a stop to its agile movements, either by catching it with a Sour Potato, slowing it down with a Dankwheat, or blocking it outright with an erect Suganmanut.\nThe Dinoshambler remains a carnivorous entity, less modified and altered compared to the Shamblersaurus Rex. They make use of their springy legs to leap over short distances, and seek out the mouth-watering Garden Gankers hiding behind the less-desireable leafy appendages of all Gaiaslimeoids. "Chew on this, you knock-off Secreature!", a gangster might say as they shoot down Dinoshamblers who prey on their Garden Ganker allies.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241126185795636/dinoshambler_gravestone.png',
    'ufoshambler': 'The UFO Shambler is a Shambler Unnerving Fighting Operator. It will not attack in a conventional manner, preferring to launch ranged attacks in the form of grenades. If a grenade lands nearby a Pink Rowddish, it will be thrown back, resulting in damage taken by the UFO Shambler. If a UFO Shambler runs out of grenades, or if all Gaiaslimeoids within its lane are taken out, it will then begin to move forward like any other shambler and instantly take out any Gaiaslimeoid it finds with a short-range blaster attack.\nOf all the modified Secreatures in Dr. Downpour\'s arsenal, this was by far the trickiest to overturn. Not only did it have to be genetically modified, but technologically modified as well. If all the right steps aren\'t properly taken, there\'s a chance they might be able to contact their homeworld, and god help us all if it comes to that.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241176811044965/ufoshambler_gravestone.png',
    'brawldenboomer': 'The Brawlden Boomer is a Shambler with slightly above-average defenses, as he is protected by his Boombox. Once the song on his boombox finishes playing, it will explode, damaging all nearby Gaiaslimeoids. If it is destroyed by Gaiaslimeoids before that point, then he will become enraged, gaining a significant boost to his offensive capabilities. Certain attacks will pierce through his boombox and deal damage to him directly, such as the globs of acid from Dire Apples, or the toxic vape from Killiflowers.\n"Music... they don\'t make it... like they used to...", says The Brawlden Boomer. You can\'t tell if turning into a Shambler caused him to look and act the way he does, or if he was already like this.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241120724811816/brawldenboomer_gravestone.png',
    'juvieshambler': 'The Juvie Shambler is a Shambler Juvie. What is less obvious, however, is their method of attack: They mine underground, circumventing all forms of Gaiaslimeoid defense, with the exception of primed Poketubers, which they will detonate upon digging underneath them. If the reach the back of the field, they will begin to walk towards their starting point, taking out Gaiaslimeoids from behind.\nJuvie Shamblers are as cowardly as they come, perhaps even more so than before they had been Shambled. The process of bicarbination has left them traumatized and unable to confront even the weakest of gangsters, instead opting to safely eliminate Gaiaslimeoids through careful navigation under their roots. Fucking pussies.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241138399608852/juvieshambler_gravestone.png',
    'shambleballplayer': 'The Shambleball Player is a bulkier version of the Default Shambler, with a unique ability: Any Gaiaslimeoid in their path will be kicked into the column behind them, provided that there is enough room. Their efforts to punt Razonuts will always end in failure, however, due to the sharpened edges puncturing straight through their cleats and damaging them instead. Sour Potatoes will also devour them before their kicks can go through.\nMany people in NLACakaNM, shamblers and non-shamblers alike, are under the impression that Shambeball is a real sport. This is a farce, however. Shambleball can be a fun pass time, but it lacks any notion of rules or formations. As a result, many Shambleball players are found to be wearing conflicting uniforms, be it those used for Soccer, Football, or Basketball. Many of them don\'t even know what game they\'re playing, but their single-digit-IQ allows them to enjoy it all the more.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743259662815592533/shambleballplayer_gravestone.png',
    'shamblerwarlord': 'The Shambler Warlord is a Shambler Desert Warlord. He is a fairly strong Shambler, and additionally, he will sometimes call in a handful of Shambler Raiders to surround him and protect him from enemy fire.\nThe Shambler Warlord willingly joined Dr. Downpour\'s forces, so as to get back at the residents of NLACakaNM, who continue to invade his outposts and slaughter his underlings. "Sure, braiiinz, whatever, I\'m just here to get the fucking job done", says Shambler Warlord.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241171219906621/shamblerwarlord_gravestone.png',
    'shamblerraider': 'The Shambler Raider is a Shambler Desert Raider. He is exactly the same as a Default Shambler, summoned whenever he is called upon by the Shambler Warlord.\n"N-no, it\'s not true!", Shambler Raider says, clutching his scythe. "I-I don\'t like gardening, this is just for combat!". We all know the truth though, Shambler Raider. You don\'t have to hide it.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241165436092476/shamblerraider_gravestone.png',
    'blueeyesshamblerdragon': 'The Blue Eyes Shambler Dragon is Dr. Downpour\'s personal weapon of mass destruction. It can deal massive damage with balls of fire, summon any type of Shambler, spit out a Bicarbonate Rain weather balloon that heals all Shamblers on the field, and fly into the air for brief periods of time, protecting it from almost all methods of attack from Gaiaslimeoids.\nThe Blue Eyes Shambler Dragon is the culmination of Dr. Downpour\'s research throughout his time spent at SlimeCorp. Every smidgen of anger and vengeance towards his former colleagues was poured into the creation of one disastrous half-monster half-machine that has the potential to turn cities to ash, and spread the Modelovirus like wildfire.\n"Call it whatever you want, The Rain, The Modelovirus. Only the right stuff survived that nightmare... It set me free. It opened my eyes to the future of the city, and what it takes to reach that future. Night Star sent us to hell, but we are going even deeper. I will wage war in order to end this war, once and for all." -Dr. Downpour\nhttps://cdn.discordapp.com/attachments/436013056233963520/728419713633484930/blue_eyes_shambler_dragon.png'
}

rain_protection = [
    cosmetic_id_raincoat,
    weapon_id_umbrella
]

crop_icon_map = {
item_id_poketubers: emote_poketubers,
item_id_pulpgourds: emote_pulpgourds,
item_id_sourpotatoes: emote_sourpotatoes,
item_id_bloodcabbages: emote_bloodcabbages,
item_id_joybeans: emote_joybeans,
item_id_purplekilliflower: emote_killiflower,
item_id_razornuts: emote_razornuts,
item_id_pawpaw: emote_pawpaw,
item_id_sludgeberries: emote_sludgeberries,
item_id_suganmanuts: emote_suganmanuts,
item_id_pinkrowddishes: emote_pinkrowddishes,
item_id_dankwheat: emote_dankwheat,
item_id_brightshade: emote_brightshade,
item_id_blacklimes: emote_blacklimes,    
item_id_phosphorpoppies: emote_phosphorpoppies,
item_id_direapples: emote_direapples,
item_id_rustealeaves: emote_rustealeaves,
item_id_metallicaps: emote_metallicaps,
item_id_steelbeans: emote_steelbeans,
item_id_aushucks: emote_aushucks,
item_id_partypoppeppers: emote_partypoppeppers,
}

# Not actual world events - used for mining.
event_type_slimeglob = "slimeglob"
event_type_poudringlob = "poudringlob"

event_type_slimefrenzy = "slimefrenzy"
event_type_poudrinfrenzy = "poudrinfrenzy"
event_type_minecollapse = "minecollapse"
event_type_voidhole = "voidhole"
event_type_spookyghost = "spookyghost"
event_type_spookyskeleton = "spookyskeleton"
event_type_voidconnection = "voidconnection"
event_type_marriageceremony = "marriageceremony"

event_type_brickshit = "brickshit"
event_type_alarmclock = "alarmclock"

# POI Events
event_type_tornado = "tornado"
event_type_meteor_shower = "meteorshower"
event_type_smog_warning = "smogwarning"
event_type_poudrin_hail = "poudrinhail"
event_type_radiation_storm = "radiationstorm"
event_type_jape_storm = "japestorm"
event_type_firestorm = "firestorm"
event_type_raider_incursion = "raiderincursion"
event_type_slimeunist_protest = "slimeunistprotest"
event_type_dimensional_rift = "dimensionalrift"
event_type_fishing_frenzy = "fishingfrenzy"
event_type_gas_leak = "gasleak"
# For raids
event_type_raid_den = "raidden"

event_type_rally = "rally"
event_type_rally_end = "rallyend"


# In list format
random_poi_events = [
    event_type_tornado,
    event_type_meteor_shower,
    event_type_smog_warning,
    event_type_poudrin_hail,
    event_type_radiation_storm,
    event_type_jape_storm,
    event_type_firestorm,
    event_type_raider_incursion,
    event_type_slimeunist_protest,
    event_type_dimensional_rift,
    event_type_fishing_frenzy,
    event_type_gas_leak,
]

poi_events = random_poi_events + [event_type_raid_den, event_type_rally, event_type_rally_end]

# DH dates
day_map = {
    datetime.date(2023, 12, 7): 0,
    datetime.date(2023, 12, 8): 1,
    datetime.date(2023, 12, 9): 2,
    datetime.date(2023, 12, 10): 3,
    datetime.date(2023, 12, 1):  4,
    datetime.date(2023, 12, 2):  5,
    datetime.date(2023, 12, 3):  6,
    datetime.date(2023, 12, 4):  7,
    datetime.date(2023, 12, 5):  8,
    datetime.date(2023, 12, 6):  9,
    datetime.date(2023, 1, 1):  9,
    datetime.date(2023, 1, 2):  9,
    datetime.date(2023, 1, 3):  9,
}

# Events that need to be checked up on every time the market updates
# All hourly_events MUST include a "time" event_prop!
hourly_events = [event_type_brickshit, event_type_alarmclock]

halloween_tricks_tricker = [
    "You open the door and give {} a hearty '!SPOOK'. They lose {} slime!",
    "You slam open the door and give {} a knuckle sandwich. They lose {} slime!",
    "You hastily unlock the door and throw a bicarbonate-soda-flavored pie in {}'s face. They lose {} slime!",
    "You just break down the door and start stomping on {}'s fucking groin. The extreme pain makes them lose {} slime!",
]
halloween_tricks_trickee = [
    "{} opens the door and gives you a hearty '!SPOOK'. You lose {} slime!",
    "{} slams open the door and gives you a knuckle sandwich. You lose {} slime!",
    "{} hastily unlocks the door and throws a bicarbonate-soda-flavored pie in your face. You lose {} slime!",
    "{} just breaks down the door and starts stomping on your fucking groin. The extreme pain makes you lose {} slime!",
]

# links to SlimeCorp propaganda
propaganda = [
    'https://cdn.discordapp.com/attachments/431238867459375145/617526157239386113/image0.jpg',
    'https://cdn.discordapp.com/attachments/761984492868993031/761984545087946764/break_free_goon.png',
    'https://cdn.discordapp.com/attachments/761984492868993031/761984547549478942/corp_goon_1.png',
    'https://cdn.discordapp.com/attachments/761984492868993031/761984566562258984/saint_goon.png',
    'https://cdn.discordapp.com/attachments/761984492868993031/761984567249731664/D7xtNC8XYAI5uB9.png',
    'https://cdn.discordapp.com/attachments/761984492868993031/761984569460391967/DeQWu9iX0AA-F7H.png',
    'https://cdn.discordapp.com/attachments/761984492868993031/761984575228215316/securityforce2.png',
    'https://cdn.discordapp.com/attachments/761984492868993031/761984576205619220/slime_corp_designs.png',
]

# list of genres and aliases
book_genres = [
    "narrative",  # 0
    "historical",  # 1
    "comic",  # 2
    "porn",  # 3
    "instructional",  # 4
    "lore",  # 5
    "reference",  # 6
    "journal",  # 7
    "newspaper",  # 8
    "experimental",  # 9
    "surgical",  # 10
    "locked" #11
]

# rating flavor text
rating_flavor = [
    "",
    "Seething with hatred",
    "Teeming with disappointment",
    "pullulating with mild satisfaction",
    "Brimming with respect",
    "Glowing with admiration",
]

id_item_convert ={
    it_furniture:'id_furniture',
    it_cosmetic:'id_cosmetic',
    it_weapon:'weapon_type',
    it_food : 'id_food',
    it_item: 'id_item',
    it_questitem:'qitem_name'
}

sacrifice_rates = {
'scalp':[30, "You make a little effigy out of the scalp and toss it on the altar."],
'soul':[1000, "Literally without thinking at all, you decide to offer your soul to the devil in exchange for a chance at getting your soul. Your idiocy is rewarded with like a billion points."],
'slimepoudrin':[5, "Sure, slime makes sense as a sacrifice."],
'water':[-1, 'What the fuck kind of sacrifice is a glass of water? Not even slime, just kill me now.' ],
'sord':[-1, 'https://cdn.discordapp.com/attachments/608051831775428648/902359140607885392/sweets-meme.jpg \n!spook'],
'barbecuesauce':[-5, "The nameless dieties you're sacrificing to don't really like barbecue sauce."],
'butler':[150, "Human sacrifice? Let's go."],
'reanimatedcorpse':[300, "Human sacrifice? Let's go."],
'humancorpse':[150, "Human sacrifice? Let's go."],
'dragonsoul':[100, "Animal souls aren't as good as the real deal. You wouldn't fuck an animal, right? It's like that but with souls."],
'monsterbones':[30, "Animal sacrifice is good, but maybe a little too ethical for the eldritch horrors downstairs."],
'dinoslimemeat':[25, "Animal sacrifice is good, but maybe a little too ethical for the eldritch horrors downstairs."],
'bloodcabbages':[50, "Blood for the blood god."],
'bloodstone':[1200, "We are eternally grateful for your generous donation. We shall feed for centuries on it."],
'bloodcabbagecoleslaw':[-100, "You sacrifice cole slaw to the undead. Seriously, what the fuck were you thinking?"],
'coleslaw': [-100, "You sacrifice cole slaw to the undead. Seriously, what the fuck were you thinking?"],
'bloodtransfusion':[170, "Blood for the blood god."],
'normal':[1, "You toss your worldly posessions to the altar."],
'brick': [-5, "Can't dodge a valuable gift with a brick."],
'humanskeleton':[100, "Human sacrifice? Let's go."],
'dinoslimeskeleton':[650, "You throw the priceless piece of history to be immolated on the stone slab."],
'slimeadactylskeleton':[650, "You throw the priceless piece of history to be immolated on the stone slab."],
'mammoslimeskeleton':[650, "You throw the priceless piece of history to be immolated on the stone slab."],
'slimeasaurusskeleton':[650, "You throw the priceless piece of history to be immolated on the stone slab."],
'slimedragonskeleton':[650, "You throw the priceless piece of history to be immolated on the stone slab."],
'leatherchair':[153, "It's furniturized, but it oughta do the job well enough."],
'leatherlamp':[120, "It's furniturized, but it oughta do the job well enough."],
'leatherdesk':[150, "It's furniturized, but it oughta do the job well enough."],
'leatherbed':[390, "It's furniturized, but it oughta do the job well enough."],
'leathercouch':[350, "It's furniturized, but it oughta do the job well enough."],
'civilianscalp':[50, "You make a little effigy out of the scalp and toss it on the altar."]
}

zine_cost = 10000
minimum_pages = 1
maximum_pages = 30

# zine related commands that can be used in DMs
zine_commands = [
    cmd_beginmanuscript,
    cmd_beginmanuscript_alt_1,
    cmd_beginmanuscript_alt_2,
    cmd_setpenname,
    cmd_setpenname_alt_1,
    cmd_settitle,
    cmd_settitle_alt_1,
    cmd_setgenre,
    cmd_editpage,
    cmd_viewpage,
    cmd_checkmanuscript,
    cmd_publishmanuscript,
    cmd_readbook,
    cmd_nextpage,
    cmd_nextpage_alt_1,
    cmd_previouspage,
    cmd_previouspage_alt_1,
    cmd_previouspage_alt_2,
    cmd_rate,
    cmd_rate_alt_1,
    cmd_rate_alt_2,
    cmd_accept,
    cmd_refuse,
    cmd_setpages,
    cmd_setpages_alt_1,
    cmd_setpages_alt_2,
]
# lock states between two specific districts
lock_states = {
    "shipstate": ["ufoufo", "westoutskirts"]
}

region_lock_states = {
    "slimecorptunnel": ["lobbylock1", "lobbylock2"],
    "slimecorphotel": ["hotelfound"]
}



curse_words = {  # words that the player should be punished for saying via swear jar deduction. the higher number, the more the player gets punished.
    "fag": 20,
    "shit": 10,
    "asshole": 10,  # can not be shortened to 'ass' due to words like 'pass' or 'class'
    "dumbass": 10,
    "cunt": 30,
    "fuck": 10,
    "bitch": 10,
    "bastard": 5,
    "nigger": 80,
    "kike": 80,
    "cuck": 30,
    # "chink":50,
    "chinaman": 50,
    "gook": 50,
    "injun": 50,
    "bomboclaat": 80,
    "mick": 50,
    "pickaninny": 50,
    "tarbaby": 50,
    "towelhead": 50,
    "wetback": 50,
    "zipperhead": 50,
    "spic": 50,
    "dyke": 50,
    "tranny": 80,
    "dickhead": 20,
    "retard": 20,
    "buster": 100,
    "kraker": 100,
    "beaner": 50,
    "wanker": 10,
    "twat": 10,
}

curse_responses = [  # scold the player for swearing
    "Watch your language!",
    "Another one for the swear jar...",
    "Do you kiss your mother with that mouth?",
    "Wow, maybe next time be a little nicer, won't you?",
    "If you don't have anything nice to say, then don't say anything at all.",
    "Now that's just plain rude.",
    "And just like that, some of your precious SlimeCoin goes right down the drain.",
    "Calm down that attitude of yours, will you?",
    "Your bad manners have costed you a fraction of your SlimeCoin!",
    "Take your anger out on a juvenile, if you're so inclined to use such vulgar language.",
    # "You know, don't, say, s-swears."
]

captcha_dict = [
    # 3
    'GOO', 'MUD', 'DIE', 'WAR', 'BEN',
    'EYE', 'ARM', 'LEG', 'BOO', 'DAB',
    'KFC', 'GAY', 'LOL', 'GUN', 'MUK',
    'POW', 'WOW', 'POP', 'OWO', 'HIP',
    'END', 'HAT', 'CUP', '911', '711',
    'SIX', 'SMG', 'BOW', 'UWU',
    # 4
    'GOON', 'DOOR', 'CORP', 'SPAM', 'BLAM',
    'FISH', 'MINE', 'LOCK', 'OURS', 'ROCK',
    'DATA', 'LOOK', 'GOTO', 'COIN', 'GANG',
    'HEHE', 'WEED', 'LMAO', 'EPIC', 'NICE',
    'SOUL', 'KILL', 'FREE', 'GOOP', 'CAVE',
    'ZOOM', 'FIVE', 'NINE', 'BASS', 'FIRE',
    'TEXT', 'AWOO', 'GOKU', 'FOUR', 'VAPE',
    # 5
    'GUNKY', 'BOORU', 'ROWDY', 'GHOST', 'ORDER',
    'SCARE', 'BULLY', 'FERRY', 'SAINT', 'SLASH',
    'SLOSH', 'PARTY', 'BASED', 'TULPA', 'RELIC',
    'SLURP', 'MONTH', 'SEVEN', 'BRASS', 'MINES',
    'CHEMO', 'LIGHT', 'FURRY', 'PIZZA', 'ARENA',
    'LUCKY', 'RIFLE', '56709', 'SNIPE', 'SLIME',
    # 6
    'SLUDGE', 'KILLER', 'MUNCHY', 'BLAAAP', 'BARTER',
    'ARTIST', 'FUCKER', 'MINING', 'SURVEY', 'THRASH',
    'BEWARE', 'STOCKS', 'COWARD', 'CRINGE', 'INVEST',
    'BUSTAH', 'KILLAH', 'KATANA', 'GHOSTS', 'BASSED',
    'REVIVE', 'BATTLE', 'PAWPAW', 'SLEDGE', 'HAMMER',
    # 7
    'KINGPIN', 'ENDLESS', 'ATTACKS', 'FUCKERS', 'FISHING',
    'VIOLENT', 'SQUEEZE', 'LOBSTER', 'WESTERN', 'EASTERN',
    'REGIONS', 'DISCORD', 'KNUCKLE', 'MOLOTOV', 'SHAMBLE',
    'WARFARE', 'BIGIRON', 'POUDRIN', 'PATRIOT', 'MINIGUN',
    'MONSTER', 'DIVORCE', 'GARROTE', 'ASSAULT', 'PICKAXE',
    'HARPOON', 'HUNTING',
    # 8
    'GAMEPLAY', 'CONFLICT', 'EXCHANGE', 'FEEDBACK', 'GRENADES',
    'VIOLENCE', 'TACOBELL', 'PIZZAHUT', 'OUTSKIRT', 'WHATEVER',
    'WITHDRAW', 'SOUTHERN', 'NORTHERN', 'ASTATINE', 'SLIMEOID',
    'SHAMBLIN', 'STAYDEAD', 'DOWNTOWN', 'DISTRICT', 'BASEBALL',
    'BIGBONES', 'LONEWOLF', 'REVOLVER', 'COMMANDO', 'STINKEYE',
    # 9
    'APARTMENT', 'SURVIVORS', 'NEGASLIME', 'COMMUNITY', 'GIGASLIME',
    'DETENTION', 'CATHEDRAL', 'TOXINGTON', 'SLIMEGIRL', 'INVESTING',
    'SLIMECOIN', 'RATELIMIT', 'NARRATIVE', 'SHAMBLERS', 'KEENSMELL',
    'NUNCHUCKS', 'SLIMECORP', 'SMOGSBURG', 'SLIMEFEST', 'RAZORNUTS',
    'COMMANDER', 'FATCHANCE', 'DANKWHEAT',
    # 10
    'SLUDGECORE', 'LOREMASTER', 'ROUGHHOUSE', 'GLOCKSBURY', 'CALCULATED',
    'PLAYGROUND', 'NEWYONKERS', 'OLDYONKERS', 'VANDALPARK', 'SLIMERMAID',
    'SLIMEXODIA', 'WEBBEDFEET', 'NOSEFERATU', 'BINGEEATER', 'TRASHMOUTH',
    'DIREAPPLES', 'BLACKLIMES', 'POKETUBERS', 'PULPGOURDS', 'ROWDDISHES',
    'DRAGONCLAW', 'ARSONBROOK', 'SKATEBOARD', 'POPPEPPERS',
    # 27
    'STOPSCAVENGINGANDTOUCHGRASS', 'GETSERIOUSPSYCHOLOGICALHELP',
    'FEELTHETOUCHOFAWOMANINSTEAD', 'THISISNTVERYIMPRESSIVECHUMP',
    'YOUCOULDBEDOINGSOMUCHBETTER', 'GOGETAJOBINSTEADOFDOINGTHIS',
    'CONTESTARENEVERJUDGEDONTIME',
    # To the people who don't know how to count to 10 letters, I feel pity for your parents.
]

riflecap = ['UP', 'DOWN', 'LEFT', 'RIGHT']


race_humanoid = 'humanoid'
race_amphibian = 'amphibian'
race_food = 'food'
race_skeleton = 'skeleton'
race_robot = 'robot'
race_furry = 'furry'
race_scalie = 'scalie'
race_slimederived = 'slime-derived'
race_monster = 'monster'
race_critter = 'critter'
race_avian = 'avian'
race_insectoid = 'insectoid'
race_other = 'other'
race_forbidden = 'forbidden'
race_shambler = 'shambler'
race_cyborg = 'cyborg'
race_demon = 'demon'
race_clown = 'clown'


# define race info in one place
defined_races = {
    race_humanoid: {
        "race_prefix": "lame-ass ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as a boring humanoid. Your lame and uninspired figure allows you to do nothing but **{cmd}**.",
        "racial_cmd": cmd_exist,
        "soul_behavior" : "dances around in place, naive and slightly giddy."
    },
    race_amphibian: {
        "race_prefix": "slippery ",
        "race_suffix": "amphibious ",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as some denomination of amphibian. You may now **{cmd}** to let the world hear your fury.",
        "racial_cmd": cmd_ree,
        "soul_behavior" : "is vibrating and throwing a tantrum."
    },
    race_food: {
        "race_prefix": "",
        "race_suffix": "edible ",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as a member of the food race. If you must, you may now give in to your deepest desires, and **{cmd}**.",
        "racial_cmd": cmd_autocannibalize,
        "soul_behavior" : "lazily rolls around on the floor."
    },
    race_skeleton: {
        "race_prefix": "",
        "race_suffix": "skele",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as a being of bone. You may now **{cmd}** to intimidate your enemies or soothe yourself.",
        "racial_cmd": cmd_rattle,
        "soul_behavior" : "speeds around, bumping into walls!"
    },
    race_robot: {
        "race_prefix": "silicon-based ",
        "race_suffix": "robo",
        "acknowledgement_str": '\n```python\nplayer_data.race = "robot"	#todo: change to an ID\nplayer_data.unlock_command("{cmd}")```',
        "racial_cmd": cmd_beep,
        "soul_behavior" : "rotates slowly and ominously."
    },
    race_furry: {
        "race_prefix": "furry ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR reluctantly acknowledges you as a furry. Yes, you can **{cmd}** now, but please do it in private.",
        "racial_cmd": cmd_yiff,
        "soul_behavior" : "ripples its texture, making odd sounds."
    },
    race_scalie: {
        "race_prefix": "scaly ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as a scalie. You may now **{cmd}** at your enemies as a threat.",
        "racial_cmd": cmd_hiss,
        "soul_behavior":"plays around with its shape, contorting its wisps every which way."
    },
    race_slimederived: {
        "race_prefix": "goopy ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as some sort of slime-derived lifeform. **{cmd}** to your heart's content, you goopy bastard.",
        "racial_cmd": cmd_jiggle,
        "soul_behavior":"is giving off a pungent, synthetic smell."
    },
    race_monster: {
        "race_prefix": "monstrous ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as a monstrosity. Go on a **{cmd}**, you absolute beast.",
        "racial_cmd": cmd_rampage,
        "soul_behavior":"is looking for another soul it can terrorize."
    },
    race_critter: {
        "race_prefix": "small ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as a little critter. You may **{cmd}**s from others now. Adorable.",
        "racial_cmd": cmd_request_petting,
        "soul_behavior":"...wait, where is it?"
    },
    race_avian: {
        "race_prefix": "feathery ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as some kind of bird creature. You can now **{cmd}** to fly away for a quick escape.",
        "racial_cmd": cmd_flutter,
        "soul_behavior":"keeps trying to escape the top of the cylinder."
    },
    race_insectoid: {
        "race_prefix": "chitinny ",
        "race_suffix": "",
        "acknowledgement_str": 'ENDLESS WAR acknowledges you as an insectoid lifeform. You may now **{cmd}** alongside other creepy-crawlies of your ilk.',
        "racial_cmd": cmd_entomize,
        "soul_behavior":"is floating around in a weird loop."
    },
    race_shambler: {
        "race_prefix": "rotting ",
        "race_suffix": "",
        "acknowledgement_str": 'ENDLESS WAR acknowledges you as one of the dead, is disturbed by your presence. You may now **{cmd}** in the hordes of those like you',
        "racial_cmd": cmd_shamble,
        "soul_behavior":"is just happy it's apart from its owner."
    },
    race_forbidden: {
        "race_prefix": "mouthbreathing ",
        "race_suffix": "",
        "acknowledgement_str": 'In its infinite wisdom, ENDLESS WAR sees past your attempt at being funny and acknowledges you for what you _truly_ are: **a fucking idiot**.',
        "soul_behavior":"has melted, and is lying in a puddle on the floor."
    },
    race_cyborg: {
        "race_prefix": "",
        "race_suffix": "cybernetic ",
        "acknowledgement_str": "ENDLESS WAR reluctantly acknowledges your biological trancendence. You can now **{cmd}**. ",
        "racial_cmd": cmd_netrun,
        "soul_behavior":"is wearing sunglasses and you don't know how it got them."
    },
    race_demon: {
        "race_prefix": "",
        "race_suffix": "demonic ",
        "acknowledgement_str": "ENDLESS WAR acknowledges you as the hellspawn you are. You can now **{cmd}**. ",
        "racial_cmd": cmd_strike_deal,
        "soul_behavior":"has established dominance in here."
    },
        race_clown: {
        "race_prefix": "goofy ",
        "race_suffix": "",
        "acknowledgement_str": "ENDLESS WAR somewhat irritatedly acknowledges you as the lowest common denominator of the entertainment industry. You can now **{cmd}**. Congrats, dipshit.",
        "racial_cmd": cmd_honk,
        "soul_behavior":"is bothering bystanders with its various goofs and gaffes."
    },
    race_other: {  # Keep this one at the end, or else
        "race_prefix": "peculiar ",
        "race_suffix": "",
        "acknowledgement_str": 'ENDLESS WAR struggles to categorize you, and files you under "other". Your peculiar form can be used to **{cmd}** those around you.',
        "racial_cmd": cmd_confuse,
        "soul_behavior":"rattles seductively through the glass."
    },
}

# slime twitter stuff
tweet_color_by_lifestate = {
    life_state_corpse: '010101',
    life_state_juvenile: '33cc4a'
}

tweet_color_by_faction = {
    faction_killers: 'b585ff',
    faction_rowdys: 'f390b6',
    faction_slimecorp: 'ff0000'
}

# lists of all the discord server objects served by bot, identified by the server id
server_list = {}

"""
    store a server in a dictionary
"""


def update_server_list(server):
    server_list[server.id] = server


client_ref = None


def get_client():
    global client_ref
    return client_ref


"""
    save the discord client of this bot
"""


def set_client(cl):
    global client_ref
    client_ref = cl

    return client_ref


"""
    Default settings for the cache
"""


cacheable_types = ["EwItem"]

autoload_types = ["EwItem"]

obj_type_to_identifiers = {
    "EwItem": [{"id_item", "id_entry"}],
    # "EwPlayer": [{"id_user", "id_entry"}],
    # "EwUser": [
    #    {"id_user", "id_entry"},
    #    {"id_server"}
    # ],
}

obj_type_to_nested_props = {
    "EwItem": ["item_props"],
    # "EwEnemy": ["enemy_props"],
}

obj_type_indexes = {
    "EwItem": ["id_owner", "item_type"]
}

#scream = ""
#for i in range(1, 10000):
#    scream += "A"
#
#print(scream)

debugroom = None

debugpiers = None
debugfish_response = None
debugfish_goal = None

# debug5 = None


cmd_debug8 = None
cmd_debug9 = None
