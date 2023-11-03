#Values are sorted by the chance to the drop an item, and then the minimum and maximum amount of times to drop that item.
from ..model.hunting import EwAttackType
from ..model.hunting import EwNpc
from . import cfg as ewcfg
from . import community_cfg as commcfg

from ew.utils import npcutils
from . import poi as poi_static

npc_list = [
    EwNpc(
        id_npc="thedrinkster",  # unique id for each npc
        active = False,  # whether an npc spawns
        str_name = "The Drinkster",  # Name of the NPC
        poi_list = [ewcfg.poi_id_downtown],  # list of locations an NPC roams in
        dialogue = {"talk":["...", "Feeling kind of thirsty..."],
                    "give":["Thanks, buddy! I'll take it, but honestly I'd rather have something to drink."],
                    "loop":["...", "Feeling kind of thirsty..."]},  # list of dialogue an npc can use
        func_ai = npcutils.drinkster_npc_action,  # function the enemy's AI uses
        image_profile = "https://rfck.app/npc/drinkster_thumb.png",  # image link to add to dialogue embeds
        defaultslime = 2036231,
        defaultlevel = 22,
        slimeoid_name = "Orange Crush",
        rewards = [
        {ewcfg.item_id_slimepoudrin: [5, 1, 1]}
        ],
        starting_statuses=[ewcfg.status_enemy_juviemode_id, ewcfg.status_enemy_trainer_id]
    ),
EwNpc(
        id_npc="thehostiledrinkster",  # unique id for each npc
        active = False,  # whether an npc spawns
        str_name = "The Hostile Drinkster",  # Name of the NPC
        poi_list = [ewcfg.poi_id_downtown],  # list of locations an NPC roams in
        dialogue = {"talk":["heyyyy. stupid hoser pucknick bitches. i'm gonna steal your drink. huehuehuehuehuehuehuehue"],
                    "hit":["FUCK YOU YOU MADE ME SPILL MY DRINK!"],
                    "die": ["OH SHIT"]},  # list of dialogue an npc can use
        func_ai = npcutils.generic_npc_action,  # function the enemy's AI uses
        image_profile = "https://www.cupholdersplus.com/mm5/graphics/00000001/BD-Shorty-Drinkster-Bench-Seat-Console-Fiesta_540x540.jpg",  # image link to add to dialogue embeds
        defaultslime = 200,
        defaultlevel = 1,
        rewards = [
        {ewcfg.item_id_slimepoudrin: [5, 1, 1]},
        {ewcfg.rarity_patrician: [20, 1, 1]},
        {ewcfg.item_id_monsterbones: [100, 1, 1]},
        ],
        starting_statuses=[ewcfg.status_enemy_barren_id, ewcfg.status_enemy_hostile_id]
    ),
EwNpc(
    id_npc = "shortsguy",
    active = False,
    str_name = "Shorts Guy",
    description = "Some people get into gang violence. Others are drawn to the stock market or maybe fishing. This goddamn idiot found shorts in the bodega one day and it's been love ever since.",
    poi_list = [],  # list of locations an NPC roams in
    dialogue = {"talk":["Shorts are so comfortable and easy to wear. Why don't you try wearing some?", "I've bought about 10 pairs of shorts today. Want one?", "It's the perfect kind of day to go for a walk in some nice shorts.", "Shorts, shorts, shorts, can't get enough of them!", "Trying my best to make shorts into a fashion craze.", "Mama always said life is like a fresh pair of shorts."],
                "hit":["You're just jealous of my shorts!"],
                "die":["Not the shorts!"]},
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/927511712473702411/994771357940334684/unknown.png", # Mischief said "I'll come up with one later" so I took creative liberty
    defaultslime = 28561,
    defaultlevel = 13,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [75, 1, 2]},
    {'shorts': [50, 1, 1]},
    {'shortshorts': [50, 1, 1]},
    {'shortshortshorts': [50, 1, 1]},
    {'autographedshorts': [10, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_barren_id, ewcfg.status_enemy_trainer_id, '2leveltrainer', ewcfg.status_enemy_trainer_id] # Didn't specify whether hostile or not - considering the guy in Pokemon is, I'd assume so?
),
EwNpc(
    id_npc = "pork",
    active = False,
    str_name = "Pork, NLACPD",
    description = "Good thing you spotted in time. This isn't any old officer. This guy's got a sadist streak a million miles wide.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["Howdy, there.", "Don't you just love that sound when you asphyxiate some perp? Good times...", "Golly, I'm so hungry could eat a whole person.", "You seen any of these gang types around?"],
                "loop":["hrm...", "I'm hungry.", "Whew-wee.", "I could go for some blood. Good drinkin'..."],
                "hit":["NLACPD! Hold it!", "Kill 'em dead!", "Shucks! He's got a weapon!"],
                "die":["Ergh. Call in a squad, chief, I'm spent. Bring some donuts to the office, too."],
                "give":["What a morsel..."]
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/npc/pork.png",
    defaultslime = 6911000,
    defaultlevel = 40,
    rarity=7,
    rewards = [
    {"jellyfilleddoughnut": [100, 2, 3],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=['7leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 10000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False,
    slimeoid_name='Chocolate Donut',
    is_threat=True
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "riot",
    active = False,
    str_name = "Riot, NLACPD",
    description = "A fresh-faced officer with a penchant for destruction. Do you recognize the voice under there? Nah, can't be.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["WHO ARE YOU?", "IM GONNA RIP THESE CRIMINALS' FINGERS OFF. JUST NEED TO FIND ONE.", "I CAN SMELL THAT JUSTICE IN THE AIR. SMELLS LIKE GUNPOWDER.", "CAN YOU LEAVE FOR A SEC? I WANT TO KICK SOMETHING REAL QUICK."],
                "loop":["IT'S HOT IN THIS SUIT...", "DO I GET TO KILL YOU? NO, MAYBE LATER.", "HEY DISPATCH, THIS IS RIOT. DID I LEAVE MY TASER BACK THERE? ACTUALLY, FORGET IT. I DON'T NEED THAT."],
                "hit":["RED ALERT!", "ZUCK THIS FUCKING HOOD RAT!!", "GRAAAHH!!"],
                "die":["CALLING FOR BACKUP! DISPATCH BETTER FUCKIN' HURRY!"],
                "give":["GIMME THAT!"]
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/npc/riot.png",
    defaultslime = 4911000,
    defaultlevel = 40,
    rarity=7,
    rewards = [
    {"jellyfilleddoughnut": [50, 1, 1],
    "gasmask":[50, 1, 1],
     "heavymetalarmor":[20, 1, 1],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=['5leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    is_threat=True,
    condition = lambda user_data, enemy_data: True if user_data.crime > 1000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False,

    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "sleuth",
    active = False,
    str_name = "Sleuth, NLACPD",
    description = "A well known police detective that goes way back with the department. It's NLACakaNM, so he has plenty to keep himself occupied.",
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["I'm a PI, bud. No need to get all panicky.", "I see your hands reaching into your pockets. A rookie like you shouldn't try anythin funny.", "At this point, getting killed's about as inconvenient as missing the train. You still shouldn't try it, squirt.", "This city..."],
                "loop":["This might be easier if they gave me some god damn forensic supplies.", "Dispatch, there's someone over here. They're looking at me funny.", "Can't believe they put me on homicide desk. It's not relevant no more."],
                "hit":["Now you've done it, punk!", "Bilge rat!", "Get back here!"],
                "die":["Son of a bitch. To dispatch, come to my location. Somebody got me..."],
                "give":["What, this some sorta clue?"]
                },
    func_ai = npcutils.police_npc_action,
    image_profile = "https://rfck.app/npc/sleuth.png",
    defaultslime = 5911000,
    defaultlevel = 40,
    is_threat=True,
    rarity=7,
    rewards = [
    {"jellyfilleddoughnut": [20, 1, 1],
    "revolver":[50, 1, 1],
     "trenchcoat":[50, 1, 1],
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=['6leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 25000 or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False,
    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "mrc",
    active = False,
    str_name = "Mr. C, NLACPD Chief of Police",
    description = 'The city\'s Chief of Police. Not much is known about them, but you hear they\'re pretty intimidating. You might not get this chance again, you should gank this sonavabitch!',
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["..."],
                "hit":["You'll regret this."],
                "die":["Dispatch, send all available high level officers. We need to make an example of someone."],
                "give":["We'll have our officers look over this."]
                },
    func_ai = npcutils.police_chief_npc_action,
    image_profile = "https://rfck.app/npc/mrc.png",
    defaultslime = 3000000,
    defaultlevel = 80,
    is_threat=True,
    rarity=1,
    rewards = [
    {
     "officercopbadge":[100, 1, 1]}
    ],
    starting_statuses=[ewcfg.status_enemy_barren_id, '9leveltrainer', ewcfg.status_enemy_trainer_id],
    attacktype = 'police',
    condition = lambda user_data, enemy_data: True if user_data.crime > 2250000 else False,

    #if the cop is trigger happy or if you're above a certain crime level
),
EwNpc(
    id_npc = "recalcitrantfawn",
    active = True,
    str_name = "RF",
    description = 'This little guy made a big splash in the Rowdys when they first joined up. They ended up getting Consort in record time thanks to the inexplicable appearance of a bunch of  consort-themed fetch quests. If you kill him? Oh boy, he\'ll really lose his marbles.',
    poi_list = [ewcfg.poi_id_rowdyroughhouse],
    dialogue = {"talk":["!!!", "👋",  "🤙", "()*RF gives you a high five.*"],
                "loop":["()*RF just checked a trash can. Can't jump in there, too full.*", "()*RF is anxious and jumping around! You must've caught them by suprise.*", "()*RF seems distracted by that brick over there*", "()*RF does a little happy dance.*"],
                "rowdyroughhouseloop": ["RF looks at the top of the Rowdy Roughhouse with a sense of pride."],
                "outsidethe711loop": ["RF repeatedly presses the button to the fuck energy machine."],
                "hit":["RF gears up for battle."],
                "die":["*It looks like RF really wasn't cut out to be a Rowdy.* {}".format(ewcfg.emote_slimeskull)]
                },
    func_ai = npcutils.condition_hostile_action,
    image_profile = "https://rfck.app/npc/rf1.png",
    defaultslime = 6479,
    defaultlevel = 12,
    is_threat=True,
    rewards = [
    {'rfconsortmarble': [5, 1, 1]}
    ],
    starting_statuses = ['4leveltrainer', ewcfg.status_enemy_trainer_id],
    condition= lambda user_data, enemy_data: True if (user_data.faction == 'killers' and user_data.life_state == ewcfg.life_state_enlisted) or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False #attacks killers, or anyone when hostile
),
EwNpc(
    id_npc = "pinkerton",
    active = False,
    str_name = "Pinkerton",
    description = "A disheveled homeless man wearing a tarp cloak over ruined body armor. Pinkerton was once a member of the NLACakaNMPD's Vandal Squad, thuggish brutes who disguised as homeless people to get the drop on poor, innocent graffiti artists. Decades of slime-fueled gang violence have made him a shell of his former self.",
    poi_list = poi_static.capturable_districts, # Change to whatever ew\static\poi is imported as
    dialogue = {"talk":["()*Pinkerton barks some incomprehensible nonsense that may have once been police radio shorthand. You slowly back away so as not to anger him further.*", "()*You think Pinkerton lost the ability to speak long ago.*"],
                "loop":["()*Pinkerton peers out from a back alley, suspiciously eyeing passersby.*", "()*Pinkerton is busying himself with a broken radio, trying to call backup that has long since disappeared.*", "()*Pinkerton's eye twitches, his hand tentatively reaching for his piece.*"],
                "hit":["HYARGH-!!", "RRGH-", "()*Pinkerton snaps to attention, readying his revolver*"],
                "rarehit":["()*Pinkerton lets out a bestial roar, lunging to grab and throw you in a perfect-arch German suplex!*"],
                "die":["()*The last of the Vandal Squad falls.*"]
                },
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://cdn.discordapp.com/attachments/927511712473702411/996283670631546931/rivers_cuomo_pinkerton.png", # No PFP given again
    defaultslime = 1900000,
    defaultlevel = 23,
    is_threat=True,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [100, 2, 6]},
    {'pairofsunglasses': [100, 1, 1]},
    {'reinforcedkfcbucket': [5, 1, 1]},
    {ewcfg.item_id_454casullround: [80, 1, 1]},
    {'crop': [100, 1, 3]}
    ],
    starting_statuses = ['6leveltrainer', ewcfg.status_enemy_trainer_id],
    ),
EwNpc(
    id_npc = "chad",
    active = True,
    str_name = "Chad", # Full name "Alpha Chad"
    poi_list = [ewcfg.poi_id_downtown, ewcfg.poi_id_rowdyroughhouse],
    dialogue = {"talk":["Look alive there, pal!", "We're all gonna make it, or so I've been told."],
                "hit":["Well, looks like things are going that way.", "Let's do this."],
                "die":["Back to the sauce I go..."],
                },
    func_ai = npcutils.condition_hostile_action,
    image_profile = "https://rfck.app/npc/kimblynpcchad.png",
    defaultslime = 2560000,
    is_threat=True,
    defaultlevel = 40,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [1, 1, 1]},
    {'cookingapron': [5, 1, 1]},
    {'crop': [1, 1, 3]}
    ],
    starting_statuses = ['5leveltrainer', ewcfg.status_enemy_trainer_id],
    condition=lambda user_data, enemy_data: True if (user_data.faction == 'killers' and user_data.life_state == ewcfg.life_state_enlisted) or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False
    # attacks killers, or anyone when hostile
),
EwNpc(
    id_npc = "kimbly",
    active = True,
    str_name = "Kimbly", # Full name "Kimbly Loksed"
    poi_list = [ewcfg.poi_id_downtown],
    dialogue = {"first":["Wha- Oh hey there!"],
                "talk":["Is there always supposed to be this much slime on the streets? "],
                "hit":["Oh jeez! Looks like I'll have to deal you a hand!"],
                "die":["Someone... Please check on my plushies..."],
                },
    func_ai = npcutils.generic_npc_action,
    image_profile = "https://rfck.app/npc/kimblynpcKimbly.png",
    defaultslime = 1550000,
    defaultlevel = 35,
    rewards = [
    {ewcfg.item_id_gameguide: [100, 1, 1]},
    {'crop': [1, 1, 3]}
    ],
    starting_statuses = [ewcfg.status_enemy_barren_id, '3leveltrainer', ewcfg.status_enemy_trainer_id],
),
EwNpc(
    id_npc = "mozz",
    active = True,
    str_name = "Mozz",
    description = "Eww. Looks like somebody smelted a stuffed crust pizza wrong. Better let the thing just go about its business.",
    poi_list = [ewcfg.poi_id_downtown, ewcfg.poi_id_rowdyroughhouse],
    dialogue = {"talk":["()It starts to snarl at you! Oh shit!", "WRYYYYYYYYYY!"],
                "loop":["*slurp smack*", "AJAJAJA!!", "*munch munch*", "...", "WRYYYYYYYYYY! *Yawn...*"],
                "hit":["!!", "HCK!"],
                "die":["()The creature melts into a pizza puddle on the ground...", "WEHHHHHHH!"],
                "give":["()Mozz takes your spoiled food and runs away with it!"]
                },
    func_ai = npcutils.mozz_action,
    image_profile = "https://rfck.app/npc/mozz.png",
    defaultslime = 9999000,
    defaultlevel = 1,
    rarity=5,
    is_threat=True,
    attacktype = 'pizzagraspers',
    rewards = [
    {ewcfg.item_id_octuplestuffedcrust:[100, 1, 1],
     ewcfg.item_id_quadruplestuffedcrust:[100, 2, 4],
     ewcfg.item_id_doublestuffedcrust:[100, 2, 4],
     'funpizza': [1, 1, 1]}
     ],
    starting_statuses=[ewcfg.status_enemy_tanky_id, ewcfg.status_enemy_dodgy_id, ewcfg.status_enemy_barren_id],
),
EwNpc(
    id_npc = "avgr",
    active = True,
    str_name = "Angry Video Game Rowdy", 
    poi_list = poi_static.capturable_districts,
    dialogue = {"talk":["What were they thinking with this shitload of fuck?", "Let me ask a question: what do you get when you take a podcast that's ASS and you make it into a game? You get a piece of shit!", "Go purple for putrid gameplay.", "WHAT WERE THEY THINKING!?", "I think I'm going to play Super Mario World! Fuck yeah! That game's awesome!", "This game's a MUD, and playing it is just like muddying your shoes in dogshit!", "https://www.youtube.com/watch?v=JFvtk5toGJg&t=373s", "**ASS!**", "I can't take this many references...", "It's a sad thing when the best thing in the game is playing roulette!", "First the developers nerf my ass by making me slower to hit people, THEN they don't let me get more slime? WHAT WERE THEY THINKING!?", "Fuck this, I'm leaving the server. Or at least I would if I wasn't a fucking NPC! FUCK!! THIS IS TORTURE!"],
                "hit":["**GODDAMNIT!**", "**FUCKING BULLSHIT!**", "**SHIT!** Come on!"],
                "die":["This game sucks.", "Ah-duh, ah-duh, duh, that's all, fucks!"],
                "give":["This is as useful as a Tiger Electronics game.", "I don't want your BULLSHIT!"],
                "data":["Eugh.", "Talk about desperate.","!Data? More like !playafuckingbettergame!!"] ,
                },
    func_ai = npcutils.condition_hostile_action,
    image_profile = "https://cdn.discordapp.com/attachments/699776308850327698/1151696956956102756/AngryVideoGameRowdy.png",
    defaultslime = 4000000,
    is_threat=True,
    defaultlevel = 50,
    rewards = [
    {ewcfg.item_id_slimepoudrin: [5, 1, 1]},
    {'pairofpoindexterglasses': [10, 1, 1]},
    ],
    slimeoid_name = "Glitch Gremlin",
    starting_statuses = ['9leveltrainer', ewcfg.status_enemy_trainer_id],
    condition=lambda user_data, enemy_data: True if (user_data.faction == 'killers' and user_data.life_state == ewcfg.life_state_enlisted) or ewcfg.status_enemy_hostile_id in enemy_data.getStatusEffects() else False
),
]

for npc in npc_list:
    npc.starting_statuses.append(ewcfg.status_enemy_delay_id)

active_npcs_map = {}
spawn_probability_list = []


for npc in npc_list:
    if npc.active:
        active_npcs_map[npc.id_npc] = npc
        #print(npc.rarity)
        for x in range(min(npc.rarity, 10)): #the rarity determines frequency in the list, and thus spawn frequency, capped at 10
            spawn_probability_list.append(npc.id_npc)