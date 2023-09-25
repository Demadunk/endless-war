from ew.static import cfg as ewcfg
from . import cmdcmds

cmd_map = {

    # Show the current slime score of a player.
    ewcfg.cmd_score: cmdcmds.score,
    ewcfg.cmd_score_alt1: cmdcmds.score,
    ewcfg.cmd_score_alt2: cmdcmds.score,
    ewcfg.cmd_score_alt3: cmdcmds.score,
    ewcfg.cmd_score_alt4: cmdcmds.score,

    # Show a player's combat data.
    ewcfg.cmd_data: cmdcmds.data,

    # Show a player's mutations.
    ewcfg.cmd_mutations: cmdcmds.mutations,
    ewcfg.cmd_mutations_alt_1: cmdcmds.mutations,
    ewcfg.cmd_mutations_alt_2: cmdcmds.mutations,

    # Check how hungry you are.
    ewcfg.cmd_hunger: cmdcmds.hunger,

    # check what time it is, and the weather
    ewcfg.cmd_time: cmdcmds.weather,
    ewcfg.cmd_clock: cmdcmds.weather,
    ewcfg.cmd_weather: cmdcmds.weather,

    # check the weather forecast
    ewcfg.cmd_forecast: cmdcmds.forecast,
    ewcfg.cmd_forecast_alt1: cmdcmds.forecast,

    # check goonscape stats
    ewcfg.cmd_goonscape_stats: cmdcmds.display_goonscape_stats,

    # Rowdys thrash and Killers dab.
    ewcfg.cmd_thrash: cmdcmds.thrash,
    ewcfg.cmd_dab: cmdcmds.dab,

    # Ghosts can BOO
    ewcfg.cmd_boo: cmdcmds.boo,



    # Juvies can dance
    ewcfg.cmd_dance: cmdcmds.dance,
    ewcfg.cmd_dance_alt: cmdcmds.dance,

    # Terezi Gang can flip coins
    ewcfg.cmd_coinflip: cmdcmds.coinflip,

    # Die wielders can die
    ewcfg.cmd_rolldie: cmdcmds.rolldie,

    # Bass weilders can jam out
    ewcfg.cmd_jam: cmdcmds.jam,
    ewcfg.cmd_stunt: cmdcmds.stunt,
    ewcfg.cmd_stuntalt1: cmdcmds.stunt,
    ewcfg.cmd_stuntalt2: cmdcmds.stunt,

    # Show the total of positive slime in the world.
    ewcfg.cmd_endlesswar: cmdcmds.endlesswar,

    # Slimefest
    ewcfg.cmd_slimefest: cmdcmds.slimefest,

    # Show the number of swears in the global swear jar.
    # ewcfg.cmd_swear_jar: cmds.swearjar,

    # throw an item off the cliff
    # TODO -- Find out how to put this in item cmds without circular imports
    ewcfg.cmd_toss: cmdcmds.toss_off_cliff,

    # throw yourself off the cliff
    ewcfg.cmd_jump: cmdcmds.jump,
    ewcfg.cmd_jump_alt1: cmdcmds.jump,

    # throw someone else off the cliff -- could be in wep
    ewcfg.cmd_push: cmdcmds.push,
    ewcfg.cmd_push_alt_1: cmdcmds.push,
    ewcfg.cmd_push_alt_2: cmdcmds.push,

    # drink from the fountain
    ewcfg.cmd_purify: cmdcmds.purify,

    # look at the flag
    ewcfg.cmd_checkflag: cmdcmds.check_flag,

    # TODO - adapt these for every challenge/confrimation
    # Used in russianroulette and slimeoidbattle.
    ewcfg.cmd_accept: cmdcmds.accept,
    ewcfg.cmd_refuse: cmdcmds.refuse,
    ewcfg.cmd_yes: cmdcmds.confirm,
    ewcfg.cmd_no: cmdcmds.cancel,

    # More confirmation cmds, but for ads
    ewcfg.cmd_confirm: cmdcmds.confirm,
    ewcfg.cmd_cancel: cmdcmds.cancel,

    # link to the world maps
    ewcfg.cmd_map: cmdcmds.map,
    ewcfg.cmd_transportmap: cmdcmds.transportmap,
    ewcfg.cmd_transportmap_alt1: cmdcmds.transportmap,

    # Check your fashion ratings
    ewcfg.cmd_fashion: cmdcmds.fashion,
    ewcfg.cmd_fashion_alt1: cmdcmds.fashion,

    # Admin/debug commands

    ewcfg.cmd_checkstats: cmdcmds.check_stats,
    ewcfg.cmd_makebp: cmdcmds.make_bp,
    ewcfg.cmd_ping_me: cmdcmds.ping_me,
    ewcfg.cmd_addstatuseffect: cmdcmds.assign_status_effect,
    ewcfg.cmd_promote: cmdcmds.promote,
    ewcfg.cmd_checkbot: cmdcmds.check_bot,

    # force print the leaderboard
    ewcfg.cmd_post_leaderboard: cmdcmds.post_leaderboard,

    # Ban/pardon from gameplay
    ewcfg.cmd_arrest: cmdcmds.arrest,
    ewcfg.cmd_release: cmdcmds.release,
    ewcfg.cmd_release_alt1: cmdcmds.release,
    ewcfg.cmd_manual_unban: cmdcmds.unban_manual,

    # recycle your trash at the slimecorp recycling plant
    ewcfg.cmd_recycle: cmdcmds.recycle,
    ewcfg.cmd_recycle_alt1: cmdcmds.recycle,

    # Show guide pages or available commands
    ewcfg.cmd_help: cmdcmds.help,
    ewcfg.cmd_help_alt3: cmdcmds.help,
    ewcfg.cmd_commands: cmdcmds.commands,
    ewcfg.cmd_commands_alt1: cmdcmds.commands,

    # Pure flavor response
    ewcfg.cmd_howl: cmdcmds.cmd_howl,
    ewcfg.cmd_howl_alt1: cmdcmds.cmd_howl,
    ewcfg.cmd_moan: cmdcmds.cmd_moan,
    ewcfg.cmd_harvest: cmdcmds.harvest,
    ewcfg.cmd_salute: cmdcmds.salute,
    ewcfg.cmd_unsalute: cmdcmds.unsalute,
    ewcfg.cmd_hurl: cmdcmds.hurl,

    # Link to various external things
    ewcfg.cmd_news: cmdcmds.patchnotes,
    ewcfg.cmd_patchnotes: cmdcmds.patchnotes,
    ewcfg.cmd_wiki: cmdcmds.wiki,
    ewcfg.cmd_booru: cmdcmds.booru,
    ewcfg.cmd_bandcamp: cmdcmds.bandcamp,
    ewcfg.cmd_tutorial: cmdcmds.tutorial,
    ewcfg.cmd_leaderboard: cmdcmds.leaderboard,
    ewcfg.cmd_leaderboard_alt1: cmdcmds.leaderboard,
    ewcfg.cmd_crime:cmdcmds.crime,
    # LOL
    ewcfg.cmd_lol: cmdcmds.lol,

    # Shuts down the bot with sys.exit()
    # or kills non admins
    ewcfg.cmd_shutdownbot: cmdcmds.shut_down_bot,

    ewcfg.cmd_set_debug_option: cmdcmds.set_debug_option,


    # Praying at the base of ENDLESS WAR.
    ewcfg.cmd_pray: cmdcmds.pray,


    # PRANK people
    ewcfg.cmd_prank: cmdcmds.prank,

    # Check GvS almanac - obsolete, but contains a large amount of flavor text and lore for plants, Garden Gankers, and Shamblers, as well as art.
    ewcfg.cmd_gvs_almanac: cmdcmds.almanac,


    # Check your weapon masteries
    ewcfg.cmd_mastery: cmdcmds.check_mastery,

    # SlimeCorp security officers can post propaganda
    # ewcfg.cmd_propaganda: ewcmd.propaganda,

    # Show the player's slime coin.
    ewcfg.cmd_slimecoin: cmdcmds.slimecoin,
    ewcfg.cmd_slimecoin_alt1: cmdcmds.slimecoin,
    ewcfg.cmd_slimecoin_alt2: cmdcmds.slimecoin,
    ewcfg.cmd_slimecoin_alt3: cmdcmds.slimecoin,

    # show player's current shares in a company
    ewcfg.cmd_shares: cmdcmds.shares,
    ewcfg.cmd_shares_alt1: cmdcmds.shares,

    # Prints all cached data to the console
    ewcfg.cmd_log_caches: cmdcmds.print_cache,

    # Used for toggling of caches
    ewcfg.cmd_toggle_caches: cmdcmds.toggle_cache,

    # Verify that the cache is functional
    ewcfg.cmd_verify_cache: cmdcmds.verify_cache,

    # Testing command for retrieving members
    ewcfg.cmd_user_search: cmdcmds.user_search,

    # Admin command for cleaning stats db
    ewcfg.cmd_clean_stats: cmdcmds.clear_zero_stats,

    # *sigh*
    ewcfg.cmd_cockdraw: cmdcmds.cockdraw,
    ewcfg.cmd_measurecock: cmdcmds.cockdraw,
    ewcfg.cmd_dual_key_ban:cmdcmds.dual_key_ban,
    ewcfg.cmd_dual_key_ban_alt1: cmdcmds.dual_key_ban,
    ewcfg.cmd_dual_key_release:cmdcmds.dual_key_release,
    ewcfg.cmd_dual_key_release_alt1: cmdcmds.dual_key_release,
    ewcfg.cmd_setslime: cmdcmds.set_slime,
    ewcfg.cmd_windowshop: cmdcmds.windowshop,

    # Debug for world events
    ewcfg.cmd_createpoievent: cmdcmds.manual_poi_event_create,
    ewcfg.cmd_listworldevents: cmdcmds.list_worldevents,
    ewcfg.cmd_listworldevents_alt1: cmdcmds.list_worldevents,
    ewcfg.cmd_endworldevent: cmdcmds.end_worldevent,
    ewcfg.cmd_fun: cmdcmds.fun,
    ewcfg.cmd_loopdiagnostic: cmdcmds.loop_diagnostic
}
if ewcfg.dh_active:
    cmd_map[ewcfg.cmd_spook] = cmdcmds.spook

if ewcfg.slimernalia_active:
    # Slimernalia -- Moved unwrap to item cmds. Please move wrap upon reimplementation
    cmd_map[ewcfg.cmd_festivity] = cmdcmds.festivity
    cmd_map[ewcfg.cmd_wrap] = cmdcmds.wrap
    cmd_map[ewcfg.cmd_festivitystage] = cmdcmds.slimernaliastage
    cmd_map[ewcfg.cmd_setfestivitystage] = cmdcmds.setslimernaliastage
    cmd_map[ewcfg.cmd_announcefestivitystage] = cmdcmds.announceslimernaliastage



dm_cmd_map = {

    # !help
    ewcfg.cmd_help: cmdcmds.help,
    ewcfg.cmd_help_alt3: cmdcmds.help,

    # !commands
    ewcfg.cmd_commands_alt1: cmdcmds.commands,
    ewcfg.cmd_commands: cmdcmds.commands,

}

apt_dm_cmd_map = {

    # !howl
    ewcfg.cmd_howl: cmdcmds.cmd_howl,
    ewcfg.cmd_howl_alt1: cmdcmds.cmd_howl,

    # !moan
    ewcfg.cmd_moan: cmdcmds.cmd_moan,

    # Show a player's combat data.
    ewcfg.cmd_data: cmdcmds.data,

    # Check how hungry you are.
    ewcfg.cmd_hunger: cmdcmds.hunger,

    # Show the current slime score of a player.
    ewcfg.cmd_score: cmdcmds.score,
    ewcfg.cmd_score_alt1: cmdcmds.score,
    ewcfg.cmd_score_alt2: cmdcmds.score,
    ewcfg.cmd_score_alt3: cmdcmds.score,
    ewcfg.cmd_score_alt4: cmdcmds.score,

    # !booru
    ewcfg.cmd_booru: cmdcmds.booru,

    # !wiki
    ewcfg.cmd_wiki: cmdcmds.wiki,


    # !unsalute
    ewcfg.cmd_unsalute: cmdcmds.unsalute,

    # !salute
    ewcfg.cmd_salute: cmdcmds.salute,

    # vomit
    ewcfg.cmd_hurl: cmdcmds.hurl,

    # link to the world map
    ewcfg.cmd_map: cmdcmds.map,

    # check what time it is, and the weather
    ewcfg.cmd_time: cmdcmds.weather,
    ewcfg.cmd_clock: cmdcmds.weather,
    ewcfg.cmd_weather: cmdcmds.weather,

    # check the weather forecast
    ewcfg.cmd_forecast: cmdcmds.forecast,
    ewcfg.cmd_forecast_alt1: cmdcmds.forecast,

    # Check patchnotes
    ewcfg.cmd_news: cmdcmds.patchnotes,
    ewcfg.cmd_patchnotes: cmdcmds.patchnotes,

    # gives +10Gigaslime - but NOT in DMs
    # ewcfg.cmd_harvest: cmdcmds.harvest,

    # show what commands are currently available
    ewcfg.cmd_commands_alt1: cmdcmds.commands,
    ewcfg.cmd_commands: cmdcmds.commands,

    # Show the player's slime coin.
    ewcfg.cmd_slimecoin: cmdcmds.slimecoin,
    ewcfg.cmd_slimecoin_alt1: cmdcmds.slimecoin,
    ewcfg.cmd_slimecoin_alt2: cmdcmds.slimecoin,
    ewcfg.cmd_slimecoin_alt3: cmdcmds.slimecoin,

}
