from ew.static import cfg as ewcfg
from . import prankcmds

cmd_map = {
    # Swilldermuk -- Please make swilldermuk specific cmd/util files on reimplementation
    ewcfg.cmd_gambit: prankcmds.gambit,
    ewcfg.cmd_credence: prankcmds.credence, #debug
    ewcfg.cmd_reset_prank_stats: prankcmds.reset_prank_stats, #debug
    ewcfg.cmd_set_gambit: prankcmds.set_gambit, #debug
    ewcfg.cmd_pointandlaugh: prankcmds.point_and_laugh,

}

apt_dm_cmd_map = {

    ewcfg.cmd_gambit:prankcmds.gambit,
    ewcfg.cmd_credence: prankcmds.credence,

}