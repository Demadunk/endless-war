from ew.static import cfg as ewcfg
from . import slimetwittercmds

cmd_map = {

    # Send a tweet
    ewcfg.cmd_tweet: slimetwittercmds.tweet,
    ewcfg.cmd_qrt: slimetwittercmds.quote_retweet,
    ewcfg.cmd_qrt_alt1: slimetwittercmds.quote_retweet,

    # Get Verified
    ewcfg.cmd_verification: slimetwittercmds.verification,
    ewcfg.cmd_verification_alt: slimetwittercmds.verification,

}

dm_cmd_map = {

    # !tweet 
    # ewcfg.cmd_tweet: slimetwittercmds.tweet,
    # Removed due to bypassing things such as bans, kicks, and mutes.
}
