from . import cfg as ewcfg
from ..model.status import EwHitzone
from ..model.status import EwStatusEffectDef
from ..model.status import EwTrauma

status_effect_list = [
    EwStatusEffectDef(
        id_status=ewcfg.status_burning_id,
        time_expire=ewcfg.time_expire_burn,
        str_acquire='{name_player}\'s body is engulfed in flames.',
        str_describe='They are burning.',
        str_describe_self='You are burning.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_acid_id,
        time_expire=ewcfg.time_expire_burn,
        str_acquire='{name_player}\'s body is drenched in acid.',
        str_describe='Their body is being melted down by acid.',
        str_describe_self='Your body is being melted down by acid.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_spored_id,
        time_expire=ewcfg.time_expire_burn,
        str_acquire='{name_player}\'s body is riddled with spores.',
        str_describe='Their body is being consumed by spores.',
        str_describe_self='Your body is being consumed by spores.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_badtrip_id,
        time_expire=5,
        str_acquire='{name_player} begins to suffer from a bad trip.',
        str_describe='They are suffering from the effects of a bad trip.',
        str_describe_self='You are suffering from a bad trip.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_stoned_id,
        time_expire=30,
        str_acquire='{name_player} starts to get stoned as fuck, brooooo.',
        str_describe='Their movements are sluggish and weak due to being stoned.',
        str_describe_self='Your movements are sluggish and weak due to being stoned.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_baked_id,
        time_expire=30,
        str_acquire='{name_player} has become absolutely *baked!*',
        str_describe='They can barely move a muscle due to how fucking baked they are.',
        str_describe_self='You can barely move a muscle due to how fucking baked you are.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_ghostbust_id,
        time_expire=86400,
        str_describe_self='The coleslaw in your stomach allows you to bust ghosts.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_busted_id,
        time_expire=86400,
        str_describe_self='You are busted and therefore cannot leave the sewers until your next !haunt.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_strangled_id,
        time_expire=5,
        str_describe='They are being strangled.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_stunned_id,
        str_describe='They are stunned.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_repelled_id,
        time_expire=ewcfg.time_expire_repel_base,
        str_acquire='You spray yourself with the FUCK ENERGY Body Spray.',
        str_describe='They smell like shit, much to the displeasure of slime beasts.',
        str_describe_self='You smell like shit, much to the displeasure of slime beasts.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_repelaftereffects_id,
        time_expire=2,
        str_acquire='You try and shake off the foul smell, but its stench still lingers, if only for a brief moment.',
        str_describe='Their surroundings give off a slightly foul odor.',
        str_describe_self='Your surroundings give off a slightly foul odor.'
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_high_id,
        time_expire=ewcfg.time_expire_high,
        str_describe="They are as high as a kite.",
        str_describe_self="You are as high as a kite."
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_thinned_id,
        time_expire=ewcfg.time_expire_high,
        str_describe="They are gassed up on paint thinner.",
        str_describe_self="You are gassed up on paint thinner."
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_huffed_id,
        time_expire=ewcfg.time_expire_poserhigh,
        str_describe="They have huffed spraypaint.",
        str_describe_self="You have huffed spraypaint."
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_evasive_id,
        time_expire=10,
        str_describe="They have assumed an evasive stance.",
        str_describe_self="You have assumed an evasive stance.",
        hit_chance_mod=-0.25
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_taunted_id,
        time_expire=10,
        str_describe="They are fuming with rage.",
        str_describe_self="You are fuming with rage.",
        hit_chance_mod_self=-0.25
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_aiming_id,
        time_expire=10,
        str_describe="They are taking careful aim.",
        str_describe_self="You are taking careful aim.",
        hit_chance_mod_self=0.1,
        crit_mod_self=0.2
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_sapfatigue_id,
        time_expire=60,
        str_describe="They are suffering from sap fatigue.",
        str_describe_self="You are suffering from sap fatigue.",
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_rerollfatigue_id,
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_injury_head_id,
        str_describe="Their head looks {severity}",
        str_describe_self="Your head looks {severity}",
        hit_chance_mod_self=-0.05,
        crit_mod_self=-0.1,
        hit_chance_mod=0.01,
        crit_mod=0.01,
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_injury_torso_id,
        str_describe="Their torso looks {severity}",
        str_describe_self="Your torso looks {severity}",
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_injury_arms_id,
        str_describe="Their arms look {severity}",
        str_describe_self="Your arms look {severity}",
        hit_chance_mod_self=-0.05,
        crit_mod_self=-0.1,
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_injury_legs_id,
        str_describe="Their legs look {severity}",
        str_describe_self="Your legs look {severity}",
        hit_chance_mod=0.06,
        crit_mod=0.03,
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_slapped_id,
        time_expire=300,
        str_acquire="You're tuckered out. Better not get slapped for awhile.",
        str_describe_self="You got ditch slapped recently and are really feeling it."
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_foodcoma_id,
        time_expire=300,
        str_acquire="Calorie-induced rage consumes you! You could drink gasoline and get shot and not feel a damn thing!",
        str_describe_self="You're in the middle of a raging food coma.",
        dmg_mod=0.6
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_n1,
        time_expire=86400,
        str_acquire="",
        str_describe_self="You are god's gift to malice.",
        str_describe="He is god's gift to malice.",
        dmg_mod=0.5,
        dmg_mod_self=2,
        hit_chance_mod_self=+.2,
        hit_chance_mod=-.35
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_n2,
        time_expire=86400,
        str_acquire="",
        str_describe_self="You shred like nobody's business.",
        str_describe="They shred like nobody's business.",
        dmg_mod=0.5,
        hit_chance_mod_self=0.2,
        hit_chance_mod=-0.5
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_n4,
        time_expire=86400,
        str_acquire="",
        str_describe_self="Sorry, you can't let them do that.",
        str_describe="Sorry, they can't let you do this.",
        dmg_mod=0,
        dmg_mod_self=0.5,
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_n8,
        time_expire=86400,
        str_acquire="",
        str_describe_self="You're itching to move on from this.",
        dmg_mod_self=0.5,
        dmg_mod=1.5,
        crit_mod_self=.3
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_n11,
        time_expire=86400,
        str_acquire="",
        str_describe_self="You're feeling like putting your cronies to the test.",
        str_describe="You're afraid of this guy.",
        dmg_mod=0.5,
        dmg_mod_self=1.5,
        crit_mod_self=.5
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_n12,
        time_expire=86400,
        str_acquire="",
        str_describe_self="Time to get nasty.",
        str_describe="She barely looks human.",
        dmg_mod=0.5,
        dmg_mod_self=1.7,
        crit_mod_self=.75
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_n13,
        time_expire=86400,
        str_acquire="",
        str_describe_self="They're really starting to get on your nerves.",
        str_describe="You're really starting to get on his nerves.",
        dmg_mod=0.5,
        dmg_mod_self=1.5,
        crit_mod_self=.5
    ),

    # EwStatusEffectDef(
    #	id_status = ewcfg.status_juviemode_id,
    #	time_expire = 86400,
    #	str_acquire = "",
    #	str_describe_self = "You're carrying slime under the legal limit."
    # ),
    EwStatusEffectDef(
        id_status=ewcfg.status_kevlarattire_id,
        time_expire=86400,
        str_acquire="",
        str_describe_self="You're dressed to the nines in the latest Kevlar work attire.",
        dmg_mod=0.8
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_hogtied_id,
        str_acquire="They're tied up like a hog on a summer sunday.",
        str_describe_self="You're tied up like a hog on a summer sunday."
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_pheromones_id,
        time_expire=ewcfg.time_expire_repel_base,
        str_acquire="You spray yourself with Kinkfish pheromones.",
        str_describe="They smell horrible, but strangely... alluring?",
        str_describe_self="You smell horrible, but strangely... alluring?"
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_enemy_barren_id,
        time_expire=86400,
        str_acquire="",
        str_describe="They don't have slime on them.",
        str_describe_self=""
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_enemy_juviemode_id,
        time_expire=86400,
        str_acquire="",
        str_describe="They're under the legal limit for slime. Guess they sucked the government's dick or something.",
        str_describe_self=""
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_enemy_hostile_id,
        time_expire=30,
        str_acquire="",
        str_describe="Oh shit, they're hostile!",
        str_describe_self=""
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_enemy_trainer_id,
        time_expire=86400,
        str_acquire="",
        str_describe="They've got a slimeoid. Looks ready for a battle...",
        str_describe_self=""
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_enemy_tanky_id,
        time_expire=86400,
        str_acquire="",
        str_describe="They look exceedingly difficult to kill.",
        str_describe_self="",
        dmg_mod=0.2,
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_enemy_dodgy_id,
        time_expire=86400,
        str_acquire="",
        str_describe="Their movements are erratic, they're incredibly difficult to hit.'",
        str_describe_self="",
        hit_chance_mod=-.8
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_dueling,
        time_expire=300,
        str_acquire="",
        str_describe="They're squared up for a duel...",
        str_describe_self="You're squared up for a duel..."
    ),
    EwStatusEffectDef(
        id_status=ewcfg.status_enemy_following_id,
        time_expire=86400,
        str_acquire="",
        str_describe="They're a little too attached to someone right now.",
        str_describe_self="",
    ),
EwStatusEffectDef(
        id_status=ewcfg.status_enemy_delay_id,
        time_expire=7,
        str_acquire="",
        str_describe="",
        str_describe_self="",
    ),
EwStatusEffectDef(
        id_status=ewcfg.status_braced_id,
        time_expire=30,
        str_acquire="",
        str_describe="They're bracing for impact and can't do any damage.",
        str_describe_self="You're bracing for impact and can't do any damage."# i know there are damage mods but they're not 100% multiplicative so this doesn't work sadly
    ),
]

status_effects_def_map = {}

for status in status_effect_list:
    status_effects_def_map[status.id_status] = status

# Places you might get !shot
hitzones = [
    EwHitzone(
        name="head",
        aliases=[
            "neck",
            "jaw",
            "face",
            "nose",
        ],
        id_injury=ewcfg.status_injury_head_id,
    ),
    EwHitzone(
        name="torso",
        aliases=[
            "upper back",
            "obliques",
            "solar plexus",
            "trapezius",
            "chest",
            "gut",
            "abdomen",
            "lower back",
        ],
        id_injury=ewcfg.status_injury_torso_id,
    ),
    EwHitzone(
        name="leg",
        aliases=[
            "foot",
            "kneecap",
            "Achilles' tendon",
            "ankle",
            "thigh",
            "calf",
        ],
        id_injury=ewcfg.status_injury_legs_id,
    ),
    EwHitzone(
        name="arm",
        aliases=[
            "hand",
            "wrist",
            "shoulder",
            "elbow",
        ],
        id_injury=ewcfg.status_injury_arms_id,
    ),
]

hitzone_list = []
hitzone_map = {}

for hz in hitzones:
    hitzone_list.append(hz.name)
    hitzone_map[hz.name] = hz

    for alias in hz.aliases:
        hitzone_list.append(alias)
        hitzone_map[alias] = hz

    hitzone_map[hz.id_injury] = hz

trauma_list = [
    EwTrauma(
        id_trauma=ewcfg.trauma_id_suicide,
        str_trauma_self="You are suffering from a tragic case of cowardice.",
        str_trauma="They are suffering from a tragic case of cowardice.",
        trauma_class=ewcfg.trauma_class_damage,
    ),
    EwTrauma(
        id_trauma=ewcfg.trauma_id_backfire,
        str_trauma_self="You are suffering from a chronic case of stupidity.",
        str_trauma="They are suffering from a chronic case of stupidity.",
        trauma_class=ewcfg.trauma_class_damage
    ),
    EwTrauma(
        id_trauma=ewcfg.trauma_id_betrayal,
        str_trauma_self="You look anxious around your teammates, wary of betrayal.",
        str_trauma="They look anxious around their teammates, wary of betrayal.",
        trauma_class=ewcfg.trauma_class_movespeed,
    ),
    EwTrauma(
        id_trauma=ewcfg.trauma_id_environment,
        str_trauma_self="Your death could have resulted from any number of situations, mostly related to your own idiocy.",
        str_trauma="Their death could have come from any number of situations, mostly related to their own idiocy.",
        trauma_class=ewcfg.trauma_class_slimegain,
    ),
    # Player weapon trauma
    EwTrauma(  # 1
        id_trauma=ewcfg.weapon_id_revolver,
        str_trauma_self="You have scarring on both temples, which occasionally bleeds.",
        str_trauma="They have scarring on both temples, which occasionally bleeds.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 2
        id_trauma=ewcfg.weapon_id_dualpistols,
        str_trauma_self="You have several stitches embroidered into your chest over your numerous bullet wounds.",
        str_trauma="They have several stitches embroidered into their chest over their numerous bullet wounds.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 3
        id_trauma=ewcfg.weapon_id_shotgun,
        str_trauma_self="You have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
        str_trauma="They have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 4
        id_trauma=ewcfg.weapon_id_rifle,
        str_trauma_self="Your torso is riddled with scarred-over bulletholes.",
        str_trauma="Their torso is riddled with scarred-over bulletholes.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 5
        id_trauma=ewcfg.weapon_id_smg,
        str_trauma_self="Your copious amount of bullet holes trigger onlookers’ Trypophobia.",
        str_trauma="Their copious amount of bullet holes trigger onlookers’ Trypophobia.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 6
        id_trauma=ewcfg.weapon_id_minigun,
        str_trauma_self="What little is left of your body has large holes punched through it, resembling a slice of swiss cheese.",
        str_trauma="What little is left of their body has large holes punched through it, resembling a slice of swiss cheese.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 7
        id_trauma=ewcfg.weapon_id_bat,
        str_trauma_self="Your head appears to be slightly concave on one side.",
        str_trauma="Their head appears to be slightly concave on one side.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 8
        id_trauma=ewcfg.weapon_id_brassknuckles,
        str_trauma_self="You've got two black eyes, missing teeth, and a profoundly crooked nose.",
        str_trauma="They've got two black eyes, missing teeth, and a profoundly crooked nose.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 9
        id_trauma=ewcfg.weapon_id_katana,
        str_trauma_self="A single clean scar runs across the entire length of your body.",
        str_trauma="A single clean scar runs across the entire length of their body.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 10
        id_trauma=ewcfg.weapon_id_broadsword,
        str_trauma_self="A large dent resembling that of a half-chopped down tree appears on the top of your head.",
        str_trauma="A dent resembling that of a half-chopped down tree appears on the top of their head.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 11
        id_trauma=ewcfg.weapon_id_nunchucks,
        str_trauma_self="You are covered in deep bruises. You hate martial arts of all kinds.",
        str_trauma="They are covered in deep bruises. They hate martial arts of all kinds.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 12
        id_trauma=ewcfg.weapon_id_scythe,
        str_trauma_self="You are wrapped tightly in bandages that hold your two halves together.",
        str_trauma="They are wrapped tightly in bandages that hold their two halves together.",
        trauma_class=ewcfg.trauma_class_movespeed,
    ),
    EwTrauma(  # 13
        id_trauma=ewcfg.weapon_id_yoyo,
        str_trauma_self="Simple yo-yo tricks caught even in your peripheral vision triggers intense PTSD flashbacks.",
        str_trauma="Simple yo-yo tricks caught even in their peripheral vision triggers intense PTSD flashbacks.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 14
        id_trauma=ewcfg.weapon_id_knives,
        str_trauma_self="You are covered in scarred-over lacerations and puncture wounds.",
        str_trauma="They are covered in scarred-over lacerations and puncture wounds.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 15
        id_trauma=ewcfg.weapon_id_molotov,
        str_trauma_self="You're wrapped in bandages. What skin is showing appears burn-scarred.",
        str_trauma="They're wrapped in bandages. What skin is showing appears burn-scarred.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 16
        id_trauma=ewcfg.weapon_id_grenades,
        str_trauma_self="Blast scars and burned skin are spread unevenly across your body.",
        str_trauma="Blast scars and burned skin are spread unevenly across their body.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 17
        id_trauma=ewcfg.weapon_id_garrote,
        str_trauma_self="There is noticeable bruising and scarring around your neck.",
        str_trauma="There is noticeable bruising and scarring around their neck.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 18
        id_trauma=ewcfg.weapon_id_pickaxe,
        str_trauma_self="There is a deep, precise indent in the crown of your skull. How embarrassing!",
        str_trauma="There is a deep, precise indent in the crown of their skull. How embarrassing!",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 19
        id_trauma=ewcfg.weapon_id_fishingrod,
        str_trauma_self="There is a piercing on the side of your mouth. How embarrassing!",
        str_trauma="There is a piercing on the side of their mouth. How embarrassing!",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 20
        id_trauma=ewcfg.weapon_id_bass,
        str_trauma_self="There is a large concave dome in the side of your head.",
        str_trauma="There is a large concave dome in the side of their head.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 21
        id_trauma=ewcfg.weapon_id_umbrella,
        str_trauma_self="You have a large hole in your chest.",
        str_trauma="They have a large hole in their chest.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 22
        id_trauma=ewcfg.weapon_id_bow,
        str_trauma_self="There is a pixelated arrow in the side of your head.",
        str_trauma="There is a pixelated arrow in the side of their head.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 23
        id_trauma=ewcfg.weapon_id_dclaw,
        str_trauma_self="Three smoldering claw marks are burned into your flesh, the flames `won't seem to extinguish.",
        str_trauma="Three smoldering claw marks are burned into their flesh, the flames won't seem to extinguish.",
        trauma_class=ewcfg.trauma_class_sapregeneration,
    ),
    EwTrauma(  # 24
        id_trauma=ewcfg.weapon_id_staff,
        str_trauma_self="Parts of your skin look necrotic, and you look like you haven't slept in days.",
        str_trauma="Parts of their skin look necrotic, and they look like they haven't slept in days.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 25
        id_trauma=ewcfg.weapon_id_hoe,
        str_trauma_self="You have a perfectly straight scar right on your neck.",
        str_trauma="They have a perfectly straight scar right on their neck.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 26
        id_trauma=ewcfg.weapon_id_pitchfork,
        str_trauma_self="You have three evenly sized holes on your upper body.",
        str_trauma="They have three evenly sized holes on their upper body.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 27
        id_trauma=ewcfg.weapon_id_shovel,
        str_trauma_self="You have a cartoonishly large dent on your head.",
        str_trauma="They have a cartoonishly large dent on their head.",
        trauma_class=ewcfg.trauma_class_sapregeneration,
    ),
    EwTrauma(  # 28
        id_trauma=ewcfg.weapon_id_slimeringcan,
        str_trauma_self="Your throat is swollen.",
        str_trauma="Their throat is swollen.",
        trauma_class=ewcfg.trauma_class_sapregeneration,
    ),
    EwTrauma(  # 29
        id_trauma=ewcfg.weapon_id_fingernails,
        str_trauma_self="Criscrossed slash marks cover your body.",
        str_trauma="Criscrossed slash marks cover their body.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 30
        id_trauma=ewcfg.weapon_id_spraycan,
        str_trauma_self="Your breath smells awful, and you talk in a wheeze.",
        str_trauma="Their breath smells awful, and they talk in a wheeze.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 31
        id_trauma=ewcfg.weapon_id_paintroller,
        str_trauma_self="Mishhapen welts cover the top of your head.",
        str_trauma="Misshhapen welts cover the top of their head.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 32
        id_trauma=ewcfg.weapon_id_paintgun,
        str_trauma_self="Your stitched-up form looks barely held together.",
        str_trauma="Their stitched-up form looks barely held together.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 33
        id_trauma=ewcfg.weapon_id_paintbrush,
        str_trauma_self="Your eyes are bloodshot, and splinters stick out of your torso.",
        str_trauma="Their eyes are bloodshot, and splinters stick out of their torso.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 34
        id_trauma=ewcfg.weapon_id_thinnerbomb,
        str_trauma_self="Light scars run across your face, which is a disturbing blue discoloration.",
        str_trauma="Light scars run across their face, which is a disturbing blue discoloration.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 35
        id_trauma=ewcfg.weapon_id_watercolors,
        str_trauma_self="You are a dumb suicidal idiot and despise watercolors as a concept.",
        str_trauma="They are a dumb suicidal idiot and despise watercolors as a concept.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 36
        id_trauma=ewcfg.weapon_id_roomba,
        str_trauma_self="Your skin is stretched amd misshapen, flabby and tight in different spots.",
        str_trauma="Their skin is stretched amd misshapen, flabby and tight in different spots.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 37
        id_trauma=ewcfg.weapon_id_chainsaw,
        str_trauma_self="Your body is made almost exclusively out of scar tissue.",
        str_trauma="Their body is made almost exclusively out of scar tissue.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 38
        id_trauma=ewcfg.weapon_id_laywaster,
        str_trauma_self="Your body is melting and mishhapen, like your skin was made of drenched paper mache.",
        str_trauma="Their body is melting and mishhapen, like their skin was made of drenched paper mache.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 39
        id_trauma=ewcfg.weapon_id_diamondpickaxe,
        str_trauma_self="There is a deep, precise indent in the crown of your skull. How embarrassing!",
        str_trauma="There is a deep, precise indent in the crown of their skull. How embarrassing!",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 40
        id_trauma=ewcfg.weapon_id_awp,
        str_trauma_self="Your head contains a hole where there should be an eye, removed with surgical precision.",
        str_trauma="Their head contains a hole where there should be an eye, removed with surgical precision.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 41
        id_trauma=ewcfg.weapon_id_huntingrifle,
        str_trauma_self="Your head contains a hole where there should be an eye, removed with surgical precision.",
        str_trauma="Their head contains a hole where there should be an eye, removed with surgical precision.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 42
        id_trauma=ewcfg.weapon_id_monofilamentwhip,
        str_trauma_self="Your body is riddled with scars, circled around limbs which don't seem to be reattached correctly.",
        str_trauma="Their body is riddled with scars, circled around limbs which don't seem to be reattached correctly.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 43
        id_trauma=ewcfg.weapon_id_slimeoidwhistle,
        str_trauma_self="You hesitate to even acknowledge your own slimeoid.",
        str_trauma="They hesitate to even acknowledge their own slimeoid.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 44
        id_trauma=ewcfg.weapon_id_fists,
        str_trauma_self="You've still got a black eye from that pummeling.",
        str_trauma="They've still got a black eye from that pummeling.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 45
        id_trauma=ewcfg.weapon_id_sledgehammer,
        str_trauma_self="Your head is dented in with a huge crater.",
        str_trauma="Their head is dented in with a huge crater.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 46
        id_trauma=ewcfg.weapon_id_skateboard,
        str_trauma_self="The sight of skate tricks makes you cower in fear.",
        str_trauma="The sight of skate tricks makes them cower in fear.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 47
        id_trauma=ewcfg.weapon_id_missilelauncher,
        str_trauma_self="You still haven't found the missing body part from your last encounter.",
        str_trauma="It looks like they are still searching for a missing body part.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 48
        id_trauma=ewcfg.weapon_id_pistol,
        str_trauma_self = "You have several small holes in your chest.",
        str_trauma = "They have several small holes in their chest.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 49
        id_trauma=ewcfg.weapon_id_combatknife,
        str_trauma_self = "You are covered in several cut wound scars.",
        str_trauma = "They are covered in several cut wound scars.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 50
        id_trauma=ewcfg.weapon_id_machete,
        str_trauma_self = "Your body has been loosely stitched back together.",
        str_trauma = "Their body has been loosely stitched back together.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 51
        id_trauma=ewcfg.weapon_id_boomerang,
        str_trauma_self = "You have several long cut scars across your body.",
        str_trauma = "They have several long cut scars across their body.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    # Enemy weapon  trauma
    EwTrauma(  # 1
        id_trauma="fangs",
        str_trauma_self="You have bite marks littered throughout your body.",
        str_trauma="They have bite marks littered throughout their body.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 2
        id_trauma="talons",
        str_trauma_self="A large section of scars litter your abdomen.",
        str_trauma="A large section of scars litter their abdomen.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 4
        id_trauma="gunk shot",
        str_trauma_self="Several locations on your body have decayed from the aftermath of horrific radiation.",
        str_trauma="Several locations on their body have decayed from the aftermath of horrific radiation.",
        trauma_class=ewcfg.trauma_class_sapregeneration,
    ),
    EwTrauma(  # 5
        id_trauma="tusks",
        str_trauma_self="You have one large scarred-over hole on your upper body.",
        str_trauma="They have one large scarred-over hole on their upper body.",
        trauma_class=ewcfg.trauma_class_bleeding,
    ),
    EwTrauma(  # 6
        id_trauma="molotov breath",
        str_trauma_self="You're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
        str_trauma="They're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 7
        id_trauma="arm cannon",
        str_trauma_self="There's a deep bruising right in the middle of your forehead.",
        str_trauma="There's a deep bruising right in the middle of their forehead.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 8
        id_trauma="axe",
        str_trauma_self="There's a hefty amount of bandages covering the top of your head",
        str_trauma="There's a hefty amount of bandages covering the top of their head",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 9
        id_trauma="hooves",
        str_trauma_self="Your chest is somewhat concave.",
        str_trauma="Their chest is somewhat concave.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 10
        id_trauma='amateur',
        str_trauma_self="You can still feel the circular scar inside your throat. Embarrassing...",
        str_trauma="They can still feel the circular scar inside their throat. Embarrassing...",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 17
        id_trauma='whistle',
        str_trauma_self="You hesitate to even acknowledge your own slimeoid.",
        str_trauma="They hesitate to even acknowledge their own slimeoid.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 40
        id_trauma=ewcfg.weapon_id_fists,
        str_trauma_self="You've still got a black eye from that pummeling.",
        str_trauma="They've still got a black eye from that pummeling.",
        trauma_class=ewcfg.trauma_class_hunger,
    ),
    EwTrauma(  # 17
        id_trauma=ewcfg.weapon_id_sledgehammer,
        str_trauma_self="Your head is dented in with a huge crater.",
        str_trauma="Their head is dented in with a huge crater.",
        trauma_class=ewcfg.trauma_class_accuracy,
    ),
    EwTrauma(  # 18
        id_trauma=ewcfg.weapon_id_skateboard,
        str_trauma_self="The sight of skate tricks makes you cower in fear.",
        str_trauma="The sight of skate tricks makes them cower in fear.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 19
        id_trauma=ewcfg.weapon_id_juvierang,
        str_trauma_self="Your head is cleaved in with an L-shaped imprint. Loser!",
        str_trauma="Their head is cleaved in with an L-shaped imprint. Loser!",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 48
        id_trauma=ewcfg.weapon_id_missilelauncher,
        str_trauma_self="You still haven't found the missing body part from your last encounter.",
        str_trauma="It looks like they are still searching for a missing body part.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 20
        id_trauma=ewcfg.weapon_id_pistol,
        str_trauma_self = "You have several small holes in your chest.",
        str_trauma = "They have several small holes in their chest.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 21
        id_trauma=ewcfg.weapon_id_combatknife,
        str_trauma_self = "You are covered in several cut wound scars.",
        str_trauma = "They are covered in several cut wound scars.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 22
        id_trauma=ewcfg.weapon_id_machete,
        str_trauma_self = "Your body has been loosely stitched back together.",
        str_trauma = "Their body has been loosely stitched back together.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    ),
    EwTrauma(  # 23
        id_trauma=ewcfg.weapon_id_boomerang,
        str_trauma_self = "You have several long cut scars across your body.",
        str_trauma = "They have several long cut scars across their body.",
        trauma_class=ewcfg.trauma_class_sapregeneration
    )
]

trauma_map = {}

for trauma in trauma_list:
    trauma_map[trauma.id_trauma] = trauma
