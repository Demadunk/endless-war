from . import cfg as ewcfg
from . import cosmetics

from ..model.item import EwSmeltingRecipe

smelting_recipe_list = [
    EwSmeltingRecipe(
        id_recipe="coolcosmetic",
        str_name="a cool cosmetic",
        alias=[
            "cool",
            "coolhat",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 4,
            ewcfg.item_id_cool_material: 1,
        },
        products=cosmetics.cosmetic_style_names.get("cool")
    ),
    EwSmeltingRecipe(
        id_recipe="toughcosmetic",
        str_name="a tough cosmetic",
        alias=[
            "tough",
            "toughhat",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 4,
            ewcfg.item_id_tough_material: 1,
        },
        products=cosmetics.cosmetic_style_names.get("tough")
    ),
    EwSmeltingRecipe(
        id_recipe="smartcosmetic",
        str_name="a smart cosmetic",
        alias=[
            "smart",
            "smarthat",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 4,
            ewcfg.item_id_smart_material: 1,
        },
        products=cosmetics.cosmetic_style_names.get("smart")
    ),
    EwSmeltingRecipe(
        id_recipe="beautifulcosmetic",
        str_name="a beautiful cosmetic",
        alias=[
            "beautiful",
            "beautifulhat",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 4,
            ewcfg.item_id_beautiful_material: 1,
        },
        products=cosmetics.cosmetic_style_names.get("beautiful")
    ),
    EwSmeltingRecipe(
        id_recipe="cutecosmetic",
        str_name="a cute cosmetic",
        alias=[
            "cute",
            "cutehat",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 4,
            ewcfg.item_id_cute_material: 1,
        },
        products=cosmetics.cosmetic_style_names.get("cute")
    ),
    EwSmeltingRecipe(
        id_recipe="evilcosmetic",
        str_name="an evil cosmetic",
        alias=[
            "evil",
            "evilhat",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 4,
            ewcfg.item_id_evil_material: 1,
        },
        products=cosmetics.cosmetic_style_names.get("evil")
    ),
    EwSmeltingRecipe(
        id_recipe="knightarmor",
        str_name="a set of Knight Armor",
        alias=[
            "armor",
        ],
        ingredients={
            ewcfg.item_id_ironingot: 2,
        },
        products=["knightarmor"]
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_monstersoup,
        str_name="a bowl of Monster Soup",
        alias=[
            "soup",
            "meatsoup",
            "stew",
            "meatstew",
            "monstersoup",
            "monster soup",
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 5,
            ewcfg.item_id_dinoslimemeat: 1,
        },
        products=[ewcfg.item_id_monstersoup],
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_quadruplestuffedcrust,
        str_name="a Quadruple Stuffed Crust",
        alias=[
            "qsc",
            "quadruple",
            "quadruplestuffed",
        ],
        ingredients={
            ewcfg.item_id_doublestuffedcrust: 2,
        },
        products=[ewcfg.item_id_quadruplestuffedcrust],
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_octuplestuffedcrust,
        str_name="an Octuple Stuffed Crust",
        alias=[
            "osc",
            "octuple",
            "octuplestuffed",
        ],
        ingredients={
            ewcfg.item_id_quadruplestuffedcrust: 2,
        },
        products=[ewcfg.item_id_octuplestuffedcrust],
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_sexdecuplestuffedcrust,
        str_name="a Sexdecuple Stuffed Crust",
        alias=[
            "sdsc",
            "sexdecuple",
            "sexdecuplestuffed",
        ],
        ingredients={
            ewcfg.item_id_octuplestuffedcrust: 2,
        },
        products=[ewcfg.item_id_sexdecuplestuffedcrust],
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_duotrigintuplestuffedcrust,
        str_name="a Duotrigintuple Stuffed Crust",
        alias=[
            "dtsc",
            "duotrigintuple",
            "duotrigintuplestuffed",
        ],
        ingredients={
            ewcfg.item_id_sexdecuplestuffedcrust: 2,
        },
        products=[ewcfg.item_id_duotrigintuplestuffedcrust],
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_quattuorsexagintuplestuffedcrust,
        str_name="a Quattuorsexagintuple Stuffed Crust",
        alias=[
            "qssc",
            "quattuorsexagintuple",
            "quattuorsexagintuplestuffed",
        ],
        ingredients={
            ewcfg.item_id_duotrigintuplestuffedcrust: 2
        },
        products=[ewcfg.item_id_quattuorsexagintuplestuffedcrust],
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_forbiddenstuffedcrust,
        str_name="a Forbidden Stuffed Crust",
        alias=[
            "fsc",
            "forbiddenstuffedcrust",
        ],
        ingredients={
            ewcfg.item_id_quattuorsexagintuplestuffedcrust: 2,
            ewcfg.item_id_forbidden111: 1,
        },
        products=[ewcfg.item_id_forbiddenstuffedcrust],
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.item_id_forbidden111,
        str_name="The Forbidden {}".format(ewcfg.emote_111),
        alias=[
            "forbiddenone",
            "forbidden",
            "sealed",
            "exodia",
            "oneoneone",
            "forbidden111",
            ":111:",
        ],
        ingredients={
            'leftleg': 1,
            'rightleg': 1,
            'slimexodia': 1,
            'rightarm': 1,
            'leftarm': 1,
        },
        products=[ewcfg.item_id_forbidden111]
    ),
    EwSmeltingRecipe(
        id_recipe="pickaxe",
        str_name="a Poudrin Pickaxe",
        alias=[
            "pp",  # LOL
            "poudrinpick",
            "poudrinpickaxe",
            "pick",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 3,
            ewcfg.item_id_stick: 2
        },
        products=[ewcfg.weapon_id_pickaxe]
    ),
    EwSmeltingRecipe(
        id_recipe="diamondpickaxe",
        str_name="a Diamond Pickaxe",
        alias=[
            "dpick",
            "diamondpickaxe",
            "diamondpick",
            "dp",
        ],
        ingredients={
            ewcfg.item_id_minecraftdiamond: 10, #100 megaslime worth
            ewcfg.item_id_stick: 2,
        },
        products=[ewcfg.weapon_id_diamondpickaxe]
    ),
    EwSmeltingRecipe(
        id_recipe="minecraftdiamond",
        str_name="a minecraft diamond",
        alias=[
            "diamond",
            "mcd",
            "mcdiamond",
            "minecraftdiamond",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 1000, #10 megaslime worth
        },
        products=[ewcfg.item_id_minecraftdiamond]
    ),
    EwSmeltingRecipe(
        id_recipe="faggot",
        str_name="a Faggot",
        alias=[
            "f",
            "fag",
        ],
        ingredients={
            ewcfg.item_id_stick: 3,
        },
        products=[ewcfg.item_id_faggot]
    ),
    EwSmeltingRecipe(
        id_recipe="doublefaggot",
        str_name="a Double Faggot",
        alias=[
            "df",
            "dfag",
        ],
        ingredients={
            ewcfg.item_id_faggot: 2,
        },
        products=[ewcfg.item_id_doublefaggot]
    ),
    EwSmeltingRecipe(
        id_recipe="dinoslimesteak",
        str_name="a cooked piece of Dinoslime meat",
        alias=[
            "cookedmeat",
            "dss",
        ],
        ingredients={
            ewcfg.item_id_faggot: 1,
            ewcfg.item_id_dinoslimemeat: 1,
        },
        products=[ewcfg.item_id_dinoslimesteak]
    ),
    EwSmeltingRecipe(
        id_recipe="fishingrod",
        str_name="a fishing rod",
        alias=[
            "fish",
            "fishing",
            "rod",
            "fr",
        ],
        ingredients={
            ewcfg.item_id_string: 2,
            ewcfg.item_id_stick: 3,
        },
        products=[ewcfg.weapon_id_fishingrod]
    ),
    EwSmeltingRecipe(
        id_recipe="bass",
        str_name="a Bass Guitar",
        alias=[
            "bassguitar",
        ],
        ingredients={
            'thebassedgod': 1,
            ewcfg.item_id_string: 4,
        },
        products=[ewcfg.weapon_id_bass]
    ),
    EwSmeltingRecipe(
        id_recipe="bow",
        str_name="a Minecraft Bow",
        alias=[
            "minecraft bow",
        ],
        ingredients={
            ewcfg.item_id_stick: 3,
            ewcfg.item_id_string: 3,
        },
        products=[ewcfg.weapon_id_bow]
    ),
    EwSmeltingRecipe(
        id_recipe="ironingot",
        str_name="an Iron Ingot",
        alias=[
            "ingot",
            "metal",
            "ironingot",
            "iron ingot",
        ],
        ingredients={
            ewcfg.item_id_tincan: 10,
            ewcfg.item_id_faggot: 1,
        },
        products=[ewcfg.item_id_ironingot]
    ),
    EwSmeltingRecipe(
        id_recipe="tanningknife",
        str_name="a small tanning knife",
        alias=[
            "knife",
            "tanningknife",
            "tanning",
        ],
        ingredients={
            ewcfg.item_id_ironingot: 1,
        },
        products=[ewcfg.item_id_tanningknife]
    ),
    EwSmeltingRecipe(
        id_recipe="leather",
        str_name="a piece of leather",
        alias=[
            "leather",
        ],
        ingredients={
            ewcfg.item_id_oldboot: 10,
        },
        products=[ewcfg.item_id_leather]
    ),
    EwSmeltingRecipe(
        id_recipe="bloodstone",
        str_name="a chunk of bloodstone",
        alias=[
            "bloodstone",
            "bstone",
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 100,
            'scalp':100,
            #'soul':1,
        },
        products=[ewcfg.item_id_bloodstone]
    ),
    EwSmeltingRecipe(
        id_recipe="dclaw",
        str_name="a Dragon Claw",
        alias=[
            "dragonclaw",
            "claw",
            "dclaw",
        ],
        ingredients={
            ewcfg.item_id_dragonsoul: 1,
            ewcfg.item_id_slimepoudrin: 5,
            ewcfg.item_id_ironingot: 1,
            ewcfg.item_id_leather: 1,
        },
        products=[ewcfg.weapon_id_dclaw]
    ),
        EwSmeltingRecipe(
        id_recipe="monowhip",
        str_name="a monofilamentwhip",
        alias=[
            "monowhip",
            "monofilamentwhip",
            "whip",
        ],
        ingredients={
            ewcfg.item_id_monofilamentfragment: 25,
            ewcfg.item_id_ironingot: 1,
        },
        products=[ewcfg.weapon_id_monofilamentwhip]
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.weapon_id_staff,
        str_name="an eldritch staff",
        alias=[
            "eldritchstaff",
            "spookystaff",
            "reprehensiblerod",
            "wickedwand",
            "frighteningfaggot",
        ],
        ingredients={
            ewcfg.item_id_doublefaggot: 1,
            ewcfg.item_id_negapoudrin: 1,
        },
        products=[ewcfg.weapon_id_staff]
    ),
    EwSmeltingRecipe(
        id_recipe=ewcfg.weapon_id_slimeoidwhistle,
        str_name="a slimeoid whistle",
        alias=[
            "whistle",
            "slimewhistle",
            "slimeflute",
            "tooter",
        ],
        ingredients={
            ewcfg.item_id_cute_material: 3,
            ewcfg.item_id_slimepoudrin: 1,
        },
        products=[ewcfg.weapon_id_slimeoidwhistle]
    ),
    EwSmeltingRecipe(
        id_recipe="leathercouch",
        str_name="a leather couch",
        alias=[
            "humancouch",
        ],
        ingredients={
            'couch': 1,
            'scalp': 10,
        },
        products=['leathercouch']
    ),
    EwSmeltingRecipe(
        id_recipe="leatherchair",
        str_name="a leather chair",
        alias=[
            "humanchair",
        ],
        ingredients={
            'chair': 1,
            'scalp': 5,
        },
        products=['leatherchair']
    ),
    EwSmeltingRecipe(
        id_recipe="leatherlamp",
        str_name="a leather coated lamp",
        alias=[
            "humanlamp",
        ],
        ingredients={
            'lamp': 1,
            'scalp': 3,
        },
        products=['leatherlamp']
    ),
    EwSmeltingRecipe(
        id_recipe="leatherdesk",
        str_name="a leather desk",
        alias=[
            "humandesk",
        ],
        ingredients={
            'desk': 1,
            'scalp': 4,
        },
        products=['leatherdesk']
    ),
    EwSmeltingRecipe(
        id_recipe="leatherbed",
        str_name="a leather bed",
        alias=[
            "humanbed",
        ],
        ingredients={
            'bed': 1,
            'scalp': 12,
        },
        products=['leatherbed']
    ),
    EwSmeltingRecipe(
        id_recipe="seaweedjoint",
        str_name="a seaweed joint",
        alias=[
            "joint",
            "seaweed",
            "weed",
            "doobie",
            "blunt",
        ],
        ingredients={
            ewcfg.item_id_seaweed: 3,
            ewcfg.item_id_dankwheat: 1,
            ewcfg.item_id_slimepoudrin: 1,
        },
        products=[ewcfg.item_id_seaweedjoint]
    ),
    EwSmeltingRecipe(
        id_recipe="slimepoudrin",
        str_name="a slime poudrin",
        alias=[
            "poudrin",
            "poud",
            "pou",
            "poodrin",
        ],
        ingredients={
            ewcfg.item_id_royaltypoudrin: 2
        },
        products=[ewcfg.item_id_slimepoudrin]
    ),
    EwSmeltingRecipe(
        id_recipe="humancorpse",
        str_name="a corpse",
        alias=[
            "stiff",
            "corpse",
            "deadperson",
            "cadaver",
        ],
        ingredients={
            'scalp': 20,
            ewcfg.item_id_dinoslimemeat: 2,
            ewcfg.item_id_string: 2
        },
        products=['humancorpse']
    ),
    EwSmeltingRecipe(
        id_recipe="popeonarope",
        str_name="a pope on a rope",
        alias=[
            "pope",
            "francis",
            "deadpope",
            "sacrilege",
        ],
        ingredients={
            'humancorpse': 1,
            'diadem': 1,
            'scarf': 1,
            'confessionbooth': 1
        },
        products=['popeonarope']
    ),
    EwSmeltingRecipe(
        id_recipe="reanimatedcorpse",
        str_name="a reanimated corpse",
        alias=[
            "frankenstein",
            "reanimate",
            "revenant",
        ],
        ingredients={
            'humancorpse': 1,
            'soul': 1,
        },
        products=['reanimatedcorpse']
    ),
    EwSmeltingRecipe(
        id_recipe="soul",
        str_name="a soul",
        alias=[
            "spirit",
            "essence",
            "hippiebullshit",
        ],
        ingredients={
            'reanimatedcorpse': 1,
        },
        products=['soul']
    ),
    EwSmeltingRecipe(
        id_recipe="humanskeleton",
        str_name="a human skeleton",
        ingredients={
            'bone': 206,
        },
        products=['humanskeleton']
    ),
    EwSmeltingRecipe(
        id_recipe="monsterskeleton",
        str_name="a wild beast's skeleton",
        ingredients={
            ewcfg.item_id_monsterbones: 200,
        },
        products=['dinoslimeskeleton', 'slimeadactylskeleton', 'mammoslimeskeleton', 'slimeasaurusskeleton', 'slimedragonskeleton']
    ),
    EwSmeltingRecipe(
        id_recipe="handmadechair",
        str_name="a handmade chair",
        alias=[
            "woodchair",
            "carvedchair",
            "woodenchair",
            "ornatechair",
        ],
        ingredients={
            ewcfg.item_id_stick: 5,
            ewcfg.weapon_id_bat: 2,
        },
        products=['ornatechair', 'shittychair']
    ),
    EwSmeltingRecipe(
        id_recipe="handmadebench",
        str_name="a handmade bench",
        alias=[
            "woodbench",
            "carvedbench",
            "woodenbench",
            "ornatebench",
        ],
        ingredients={
            ewcfg.item_id_stick: 10,
            ewcfg.weapon_id_bat: 4,
        },
        products=['ornatebench', 'shittybench']
    ),
    EwSmeltingRecipe(
        id_recipe="handmadebed",
        str_name="a handmade bed",
        alias=[
            "woodbed",
            "carvedbed",
            "woodenbed",
            "ornatebed",
        ],
        ingredients={
            ewcfg.item_id_stick: 12,
            ewcfg.weapon_id_bat: 3,
        },
        products=['ornatebed', 'shittybed']
    ),
    EwSmeltingRecipe(
        id_recipe="handmadedesk",
        str_name="a handmade desk",
        alias=[
            "wooddesk",
            "carveddesk",
            "woodendesk",
            "ornatedesk",
        ],
        ingredients={
            ewcfg.item_id_stick: 4,
            ewcfg.weapon_id_bat: 1,
        },
        products=['ornatedesk', 'shittydesk']
    ),
    EwSmeltingRecipe(
        id_recipe="clarinet",
        str_name="a clarinet",
        alias=[
            "flute",
            "bennygoodmanthing",
            "vuvuzela",
        ],
        ingredients={
            'bat': 1,
            'razornuts': 1,
            'knives': 1,
            'blacklimes': 1,
            'direappleciderfuckenergy': 1,
            'sweetfish': 1,
        },
        products=['craftsmansclarinet', 'woodenvuvuzela']
    ),
    EwSmeltingRecipe(
        id_recipe="guitar",
        str_name="a solid poudrin guitar",
        alias=[
            "poudringuitar",
            "electricguitar",
            "solidpoudringuitar",
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 150,
            ewcfg.item_id_string: 6,
        },
        products=['solidpoudringuitar']
    ),
    EwSmeltingRecipe(
        id_recipe="drums",
        str_name="a beast skin drums",
        alias=[
            "beastskindrums",
            "drumset",
            "drum",
        ],
        ingredients={
            'dinoslimemeat': 5,
            'dinoslimesteak': 2,
            'scalp': 5,
            'string': 3,
            'stick': 2,
        },
        products=['beastskindrums']
    ),
    EwSmeltingRecipe(
        id_recipe="xylophone",
        str_name="a fish bone xylophone",
        alias=[
            "xylo",
            "metallophone",
            "fishbonexylophone",
        ],
        ingredients={
            'nuclearbream': 1,
            'largebonedlionfish': 2,
            'plebefish': 3,
            'sweetfish': 1,
            'stick': 1,
        },
        products=['fishbonexylophone']
    ),
    EwSmeltingRecipe(
        id_recipe="maracas",
        str_name="a gourd maracas",
        alias=[
            "gourdmaracas",
            "shakers",
            "rattle",
        ],
        ingredients={
            'pulpgourds': 1,
            'suganmanuts': 1,
            'sludgeberries': 1,
            'razornuts': 1,
            'joybeans': 1,
            'phosphorpoppies': 1,
        },
        products=['gourdmaracas']
    ),
    EwSmeltingRecipe(
        id_recipe="saxophone",
        str_name="a saxophone",
        alias=[
            "sax",
            "saxamaphone",
        ],
        ingredients={
            ewcfg.weapon_id_shotgun: 1,
            'earlbrowntea': 1,
            ewcfg.item_id_metallicapheads: 4,
            ewcfg.item_id_cute_material: 10,
            ewcfg.item_id_aushuckstalks: 1,
            ewcfg.item_id_slimepoudrin: 5,
        },
        products=['saxophone']
    ),
    EwSmeltingRecipe(
        id_recipe="cornet",
        str_name="a cornet",
        alias=[
            "trumpet",
            "horn",
            "trump",
        ],
        ingredients={
            ewcfg.weapon_id_slimeringcan: 1,
            'goobalibre': 1,
            ewcfg.item_id_steelbeanpods: 2,
            ewcfg.item_id_tough_material: 10,
            ewcfg.item_id_aushuckstalks: 2,
            ewcfg.item_id_slimepoudrin: 6,
        },
        products=['cornet']
    ),
    EwSmeltingRecipe(
        id_recipe="trombone",
        str_name="a trombone",
        alias=[
            "tbone",
            "bestinstrument",
            "sackbut",
        ],
        ingredients={
            ewcfg.weapon_id_shotgun: 2,
            'manhattanproject': 1,
            ewcfg.item_id_metallicapheads: 1,
            ewcfg.item_id_smart_material: 10,
            ewcfg.item_id_aushuckstalks: 3,
            ewcfg.item_id_slimepoudrin: 10,
        },
        products=['trombone']
    ),
    EwSmeltingRecipe(
        id_recipe="ferroslimeoidotamatone",
        str_name="a ferroslimeoid Otamatone",
        alias=[
            "otamatone",
            "otamatone DX",
            "ferroslimeoidotamatone",
        ],
        ingredients={
            'ferroslimeoid': 1,
            ewcfg.item_id_metallicapheads: 1,
            ewcfg.item_id_ironingot: 1,
            ewcfg.item_id_cute_material: 5,
            ewcfg.item_id_aushuckstalks: 1,
        },
        products=['ferroslimeoidotamatone']
    ),
    EwSmeltingRecipe(
        id_recipe="whitedye",
        str_name="a vial of White Dye",
        alias=[
            'white',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_poketubereyes: 1,
        },
        products=[ewcfg.item_id_dye_white]
    ),
    EwSmeltingRecipe(
        id_recipe="yellowdye",
        str_name="a vial of Yellow Dye",
        alias=[
            'yellow',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_pulpgourdpulp: 1,
        },
        products=[ewcfg.item_id_dye_yellow]
    ),
    EwSmeltingRecipe(
        id_recipe="orangedye",
        str_name="a vial of Orange Dye",
        alias=[
            'orange',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_sourpotatoskins: 1,
        },
        products=[ewcfg.item_id_dye_orange]
    ),
    EwSmeltingRecipe(
        id_recipe="reddye",
        str_name="a vial of Red Dye",
        alias=[
            'red',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_bloodcabbageleaves: 1,
        },
        products=[ewcfg.item_id_dye_red]
    ),
    EwSmeltingRecipe(
        id_recipe="magentadye",
        str_name="a vial of Magenta Dye",
        alias=[
            'magenta',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_joybeanvines: 1,
        },
        products=[ewcfg.item_id_dye_magenta]
    ),
    EwSmeltingRecipe(
        id_recipe="purpledye",
        str_name="a vial of Purple Dye",
        alias=[
            'purple',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_purplekilliflowerflorets: 1,
        },
        products=[ewcfg.item_id_dye_purple]
    ),
    EwSmeltingRecipe(
        id_recipe="bluedye",
        str_name="a vial of Blue Dye",
        alias=[
            'blue',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_razornutshells: 1,
        },
        products=[ewcfg.item_id_dye_blue]
    ),
    EwSmeltingRecipe(
        id_recipe="greendye",
        str_name="a vial of Green Dye",
        alias=[
            'green',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_pawpawflesh: 1,
        },
        products=[ewcfg.item_id_dye_green]
    ),
    EwSmeltingRecipe(
        id_recipe="tealdye",
        str_name="a vial of Teal Dye",
        alias=[
            'teal',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_sludgeberrysludge: 1,
        },
        products=[ewcfg.item_id_dye_teal]
    ),
    EwSmeltingRecipe(
        id_recipe="rainbowdye",
        str_name="a vial of ***Rainbow Dye***",
        alias=[
            'rainbow',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_suganmanutfruit: 1,
        },
        products=[ewcfg.item_id_dye_rainbow]
    ),
    EwSmeltingRecipe(
        id_recipe="pinkdye",
        str_name="a vial of Pink Dye",
        alias=[
            'pink',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_pinkrowddishroot: 1,
        },
        products=[ewcfg.item_id_dye_pink]
    ),
    EwSmeltingRecipe(
        id_recipe="greydye",
        str_name="a vial of Grey Dye",
        alias=[
            'grey',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_dankwheatchaff: 1,
        },
        products=[ewcfg.item_id_dye_grey]
    ),
    EwSmeltingRecipe(
        id_recipe="cobaltdye",
        str_name="a vial of Cobalt Dye",
        alias=[
            'cobalt',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_brightshadeberries: 1,
        },
        products=[ewcfg.item_id_dye_cobalt]
    ),
    EwSmeltingRecipe(
        id_recipe="blackdye",
        str_name="a vial of Black Dye",
        alias=[
            'black',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_blacklimeade: 1,
        },
        products=[ewcfg.item_id_dye_black]
    ),
    EwSmeltingRecipe(
        id_recipe="limedye",
        str_name="a vial of Lime Dye",
        alias=[
            'lime',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_phosphorpoppypetals: 1,
        },
        products=[ewcfg.item_id_dye_lime]
    ),
    EwSmeltingRecipe(
        id_recipe="cyandye",
        str_name="a vial of Cyan Dye",
        alias=[
            'cyan',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_direapplestems: 1,
        },
        products=[ewcfg.item_id_dye_cyan]
    ),
    EwSmeltingRecipe(
        id_recipe="browndye",
        str_name="a vial of Brown dye",
        alias=[
            'brown',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_rustealeafblades: 1,
        },
        products=[ewcfg.item_id_dye_brown]
    ),
    EwSmeltingRecipe(
        id_recipe="copperpaint",
        str_name="a bucket of Copper Paint",
        alias=[
            'copper',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_metallicapheads: 1,
        },
        products=[ewcfg.item_id_paint_copper]
    ),
    EwSmeltingRecipe(
        id_recipe="chromepaint",
        str_name="a bucket of Chrome Paint",
        alias=[
            'chrome',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_steelbeanpods: 1,
        },
        products=[ewcfg.item_id_paint_chrome]
    ),
    EwSmeltingRecipe(
        id_recipe="goldpaint",
        str_name="a bucket of Gold Paint",
        alias=[
            'gold',
        ],
        ingredients={
            ewcfg.item_id_dyesolution: 1,
            ewcfg.item_id_aushuckstalks: 1,
        },
        products=[ewcfg.item_id_paint_gold]
    ),
    EwSmeltingRecipe(
        id_recipe="jellyfilleddoughnut",
        str_name="a Jelly Filled Donut",
        alias=[
            'donut',
            'doughnut',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_poketubereyes: 1,
        },
        products=["jellyfilleddoughnut"]
    ),
    EwSmeltingRecipe(
        id_recipe="pulpgourdpie",
        str_name="a plate of Pulp Gourd Pie",
        alias=[
            'pie',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_pulpgourdpulp: 1,
        },
        products=['pulpgourdpie']
    ),
    EwSmeltingRecipe(
        id_recipe="sourpotatofrenchfries",
        str_name="a plate of Sour Potato French Fries",
        alias=[
            'fries',
            'frenchfries',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_sourpotatoskins: 1,
        },
        products=['sourpotatofrenchfries']
    ),
    EwSmeltingRecipe(
        id_recipe="bloodcabbagecoleslaw",
        str_name="a tub of Blood Cabbage Coleslaw",
        alias=[
            'coleslaw',
            'redcoleslaw',
            'blood',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_bloodcabbageleaves: 1,
        },
        products=['bloodcabbagecoleslaw']
    ),
    EwSmeltingRecipe(
        id_recipe="joybeanpastemochi",
        str_name="a pile of Joybean Paste Mochi",
        alias=[
            'mochi',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_joybeanvines: 1,
        },
        products=['joybeanpastemochi']
    ),
    EwSmeltingRecipe(
        id_recipe="purplekilliflowercrustpizza",
        str_name="a plate of Purple Killiflower Crust Pizza",
        alias=[
            'pizza',
            'cauliflowercrustpizza',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_purplekilliflowerflorets: 1,
        },
        products=['purplekilliflowercrustpizza']
    ),
    EwSmeltingRecipe(
        id_recipe="razornutbutter",
        str_name="a tub of Razornut Butter",
        alias=[
            'butter',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_razornutshells: 1,
        },
        products=['razornutbutter']
    ),
    EwSmeltingRecipe(
        id_recipe="pawpawfood",
        str_name="a plate of Pawpaw Food",
        alias=[
            'food',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_pawpawflesh: 1,
        },
        products=['pawpawfood']
    ),
    EwSmeltingRecipe(
        id_recipe="sludgeberrypancakes",
        str_name="a plate of Sludgeberry Pancakes",
        alias=[
            'pancakes',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_sludgeberrysludge: 1,
        },
        products=['sludgeberrypancakes']
    ),
    EwSmeltingRecipe(
        id_recipe="yourfavoritefood",
        str_name="a plate of ***Your Favorite Food***",
        alias=[
            'favoritefood',
            'favefood',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_suganmanutfruit: 1,
        },
        products=['yourfavoritefood']
    ),
    EwSmeltingRecipe(
        id_recipe="pinkrowdatouille",
        str_name="a plate of Pink Rowdatouille",
        alias=[
            'rowdatouille',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_pinkrowddishroot: 1,
        },
        products=['pinkrowdatouille']
    ),
    EwSmeltingRecipe(
        id_recipe="dankwheattoast",
        str_name="a plate of Dankwheat Toast",
        alias=[
            'toast',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_dankwheatchaff: 1,
        },
        products=['dankwheattoast']
    ),
    EwSmeltingRecipe(
        id_recipe="brightshadeseeds",
        str_name="some Brightshade Seeds",
        alias=[
            'seeds',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_brightshadeberries: 1,
        },
        products=['brightshadeseeds']
    ),
    EwSmeltingRecipe(
        id_recipe="blacklimesour",
        str_name="some Black Lime Sours",
        alias=[
            'sours',
            'sour',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_blacklimeade: 1,
        },
        products=['blacklimesour']
    ),
    EwSmeltingRecipe(
        id_recipe="phosphorpoppiesmuffin",
        str_name="a Phosphorpoppies Muffin",
        alias=[
            'muffin',
            'muffins',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_phosphorpoppypetals: 1,
        },
        products=['phosphorpoppiesmuffin']
    ),
    EwSmeltingRecipe(
        id_recipe="direapplejuice",
        str_name="a bottle of Dire Apple Juice",
        alias=[
            'juice',
            'applejuice',
            'appyjuice',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_direapplestems: 1,
        },
        products=['direapplejuice']
    ),
    EwSmeltingRecipe(
        id_recipe="earlbrowntea",
        str_name="a cup of Earl Brown Tea",
        alias=[
            'tea',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_rustealeafblades: 1,
        },
        products=['earlbrowntea']
    ),
    EwSmeltingRecipe(
        id_recipe="badshroomz",
        str_name="some Bad Shroomz",
        alias=[
            'shrooms',
            'mushrooms',
            'shroomz',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_metallicapheads: 1,
        },
        products=['badshroomz']
    ),
    EwSmeltingRecipe(
        id_recipe="chromaccino",
        str_name="a Chromaccino",
        alias=[
            'cappuccino',
            'chroma',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_steelbeanpods: 1,
        },
        products=['chromaccino']
    ),
    EwSmeltingRecipe(
        id_recipe="moltenpopcorn",
        str_name="a bag of Molten Popcorn",
        alias=[
            'popcorn',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_aushuckstalks: 1,
        },
        products=['moltenpopcorn']
    ),
    EwSmeltingRecipe(
        id_recipe="stuffedpoppepper",
        str_name="a Stuffed Poppepper",
        alias=[
            'stuffedpepper',
            'stuffedpartypoppepper',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_driedpartypoppeppers: 1,
        },
        products=['stuffedpoppepper']
    ),
    EwSmeltingRecipe(
        id_recipe="captainshat",
        str_name="a Captain's Hat",
        alias=[
            'captain',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_poketubereyes: 1,
        },
        products=['captainshat']
    ),
    EwSmeltingRecipe(
        id_recipe="juveolantern",
        str_name="a Juve-O' Lantern",
        alias=[
            'juve',
            'jackolantern',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_pulpgourdpulp: 1,
        },
        products=['juveolantern']
    ),
    EwSmeltingRecipe(
        id_recipe="bowlerhat",
        str_name="a Bowler Hat",
        alias=[
            'bowler',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_sourpotatoskins: 1,
        },
        products=['bowlerhat']
    ),
    EwSmeltingRecipe(
        id_recipe="cabbagetreehat",
        str_name="a Cabbage Tree Hat",
        alias=[
            'cabbagehat',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_bloodcabbageleaves: 1,
        },
        products=['cabbagetreehat']
    ),
    EwSmeltingRecipe(
        id_recipe="braces",
        str_name="some Braces",
        alias=[
            'headgear',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_joybeanvines: 1,
        },
        products=['braces']
    ),
    EwSmeltingRecipe(
        id_recipe="hoodie",
        str_name="a Hoodie",
        alias=[
            'hood',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_purplekilliflowerflorets: 1,
        },
        products=['hoodie']
    ),
    EwSmeltingRecipe(
        id_recipe="copbadge",
        str_name="a Cop Badge",
        alias=[
            'badge',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_razornutshells: 1,
        },
        products=['copbadge']
    ),
    EwSmeltingRecipe(
        id_recipe="strawhat",
        str_name="a Straw Hat",
        alias=[
            'straw',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_pawpawflesh: 1,
        },
        products=['strawhat']
    ),
    EwSmeltingRecipe(
        id_recipe="cosplayhorns",
        str_name="a pair of Cosplay Horns",
        alias=[
            'horns',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_sludgeberrysludge: 1,
        },
        products=['cosplayhorns']
    ),
    EwSmeltingRecipe(
        id_recipe="yourfavoritehat",
        str_name="***Your Favorite Hat***",
        alias=[
            'favoritehat',
            'favehat',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_suganmanutfruit: 1,
        },
        products=['yourfavoritehat']
    ),
    EwSmeltingRecipe(
        id_recipe="pajamaonesie",
        str_name="a Pajama Onesie",
        alias=[
            'pajamas',
            'onesie',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_pinkrowddishroot: 1,
        },
        products=['pajamaonesie']
    ),
    EwSmeltingRecipe(
        id_recipe="pairofcircularsunglasses",
        str_name="a Pair Of Circular Sunglasses",
        alias=[
            'digibroglasses',
            'circleglasses',
            'circularglasses',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_dankwheatchaff: 1,
        },
        products=['pairofcircularsunglasses']
    ),
    EwSmeltingRecipe(
        id_recipe="flowercrown",
        str_name="a Flower Crown",
        alias=[
            'flower',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_brightshadeberries: 1,
        },
        products=['flowercrown']
    ),
    EwSmeltingRecipe(
        id_recipe="spikedbracelets",
        str_name="a pair of Spiked Bracelets",
        alias=[
            'spiked',
            'bracelets',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_blacklimeade: 1,
        },
        products=['spikedbracelets']
    ),
    EwSmeltingRecipe(
        id_recipe="slimecorppin",
        str_name="a SlimeCorp Pin",
        alias=[
            'corppin',
            'shillpin',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_phosphorpoppypetals: 1,
        },
        products=['slimecorppin']
    ),
    EwSmeltingRecipe(
        id_recipe="overalls",
        str_name="a pair of Overalls",
        alias=[
            'trousers',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_direapplestems: 1,
        },
        products=['overalls']
    ),
    EwSmeltingRecipe(
        id_recipe="rustynail",
        str_name="a Rusty Nail",
        alias=[
            'nail',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_rustealeafblades: 1,
        },
        products=['rustynail']
    ),
    EwSmeltingRecipe(
        id_recipe="fullmetaljacket",
        str_name="a Full Metal Jacket",
        alias=[
            'jacket',
            'metaljacket',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_metallicapheads: 1,
        },
        products=['fullmetaljacket']
    ),
    EwSmeltingRecipe(
        id_recipe="tinfoilhat",
        str_name="a Tinfoil Hat",
        alias=[
            'tinfoil',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_steelbeanpods: 1,
        },
        products=['tinfoilhat']
    ),
    EwSmeltingRecipe(
        id_recipe="resplendentcoronet",
        str_name="a Resplendent Coronet",
        alias=[
            'crown',
            'goldcrown',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_aushuckstalks: 1,
        },
        products=['resplendentcoronet']
    ),
    EwSmeltingRecipe(
        id_recipe="partyhat",
        str_name="a Party Hat",
        alias=[
            'party',
            'celebrationhat',
        ],
        ingredients={
            ewcfg.item_id_textiles: 1,
            ewcfg.item_id_driedpartypoppeppers: 1,
        },
        products=['partyhat']
    ),
    EwSmeltingRecipe(
        id_recipe="stick",
        str_name="a stick",
        alias=[
            'wood',
        ],
        ingredients={
            ewcfg.item_id_direapplestems: 3,
        },
        products=[ewcfg.item_id_stick]
    ),
    EwSmeltingRecipe(
        id_recipe="rollerblades",
        str_name="a pair of rollerblades",
        alias=[
            'rollerblades',
            'inlineskates',
            'skates',
            'jsr',
        ],
        ingredients={
            ewcfg.item_id_oldboot: 2,
            ewcfg.item_id_slimepoudrin: 8,
            ewcfg.item_id_leather: 1,
            ewcfg.item_id_string: 2,
        },
        products=["rollerblades"]
    ),
    EwSmeltingRecipe(
        id_recipe="ferroslimeoid",
        str_name="a ferroslimeoid",
        alias=[
            'ferroslimeoid',
            'magnet',
        ],
        ingredients={
            ewcfg.item_id_tincan: 1,  
            ewcfg.item_id_slimepoudrin: 2,
        },
        products=["ferroslimeoid"]
    ),
    EwSmeltingRecipe(
        id_recipe="pheromones",
        str_name="a bottle of pheromones",
        alias=[
            'kinkfishpheromones',
            'antirepel',
        ],
        ingredients={
            'kinkfish': 1,
        },
        products=['pheromones']
    ),
    EwSmeltingRecipe(
        id_recipe="huntingrifle",
        str_name="a hunting rifle",
        alias=[
            'hrifle',
            'huntersrifle',
            'huntergun',
        ],
        ingredients={
            ewcfg.item_id_bustedrifle: 1,
            ewcfg.item_id_repairkit: 1,
        },
        products=[ewcfg.weapon_id_huntingrifle]
    ),
    EwSmeltingRecipe(
        id_recipe="phoenixdownpillow",
        str_name="phoenix down pillow",
        alias=[
            'phoenixpillow',
            'downpillow',
            'pheonixpillow',
        ],
        ingredients={
            ewcfg.item_id_phoenixdown: 5,
        },
        products=['phoenixdownpillow']
    ),
    EwSmeltingRecipe(
        id_recipe="partypopper",
        str_name="party popper",
        alias=[
            'ppopper',
            'partyp',
            'party popper',
        ],
        ingredients={
            'partypoppeppers': 1,
        },
        products=['partypopper']
    ),
    EwSmeltingRecipe(
        id_recipe="skinsuit",
        str_name="skinsuit",
        alias=[
            'alien skinsuit',
            'alien costume',
            'aliencostume',
        ],
        ingredients={
            'alienscalp': 10,
        },
        products=['skinsuit']
    ),
    EwSmeltingRecipe(
        id_recipe="pizzaball",
        str_name="a Pizzaball",
        alias=[
            "pb",
            "pizzaball",
        ],
        ingredients={
            ewcfg.item_id_quattuorsexagintuplestuffedcrust: 3,
        },
        products=["pizzaball"],
    ),
    EwSmeltingRecipe(
        id_recipe="batterypack",
        str_name="battery pack",
        alias=[
            'battery pack',
            'battery string',
            'bigbattery',
            'big battery',
        ],
        ingredients={
            'alienbattery': 5,
        },
        products=['batterypack']
    ),
    EwSmeltingRecipe(
        id_recipe="alienbattery",
        str_name="alien battery",
        alias=[
            'battery',
            'AA',
        ],
        ingredients={
            'tangeloidraygun': 1,
        },
        products=['alienbattery']
    ),
    EwSmeltingRecipe(
        id_recipe="purpledrink",
        str_name="purple drink",
        alias=[
            'purpledrank',
        ],
        ingredients={
            'reddrink': 1,
            'bluedrink': 1,
        },
        products=['purpledrink']
    ),
    EwSmeltingRecipe(
        id_recipe="skateboard",
        str_name="skateboard",
        alias=[
            'sk8b04rd',
            'sk8r',
            'board',
        ],
        ingredients={
            ewcfg.weapon_id_bat: 2,
            ewcfg.item_id_ironingot: 1,
            ewcfg.item_id_leather: 1,
            'rollerblades': 1,
        },
        products=[ewcfg.weapon_id_skateboard]
    ),
    EwSmeltingRecipe(
        id_recipe="monsterbonebevor",
        str_name="Monster Bone Bevor",
        alias=[
            'mbbevor',
            'Monster Bone Bevor',
            'Bevor',
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 150,
        },
        products=['monsterbonebevor']
    ),
    EwSmeltingRecipe(
        id_recipe="monsterbonegauntlets",
        str_name="Monster Bone Gauntlets",
        alias=[
            'mbgaultets',
            'Monsterbonegauntlet',
            'Gauntlets',
            'Gauntlet',
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 150,
        },
        products=['monsterbonegauntlets']
    ),
    EwSmeltingRecipe(
        id_recipe="monsterbonefullplate",
        str_name="Monster Bone Fullplate",
        alias=[
            'mbfullplate',
            'Monster Bone Fullplate',
            'Fullplate',
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 200,
        },
        products=['monsterbonefullplate']
    ),
    EwSmeltingRecipe(
        id_recipe="monsterbonegreaves",
        str_name="Monster Bone Greaves",
        alias=[
            'mbgreaves',
            'Monster Bone Greaves',
            'Greaves',
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 150,
        },
        products=['monsterbonegreaves']
    ),
    EwSmeltingRecipe(
        id_recipe="monsterbonesabatons",
        str_name="Monster Bone Sabatons",
        alias=[
            'mbsabatons',
            'Monster Bone Sabatons',
            'Sabatons',
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 150,
        },
        products=['monsterbonesabatons']
    ),
    EwSmeltingRecipe(
        id_recipe="monsterbonearmor",
        str_name="Monster Bone Armor",
        alias=[
            'monsterbonearmor',
            'Monster Bone Armor',
            'Bonearmor',
        ],
        ingredients={
            'monsterbonebevor': 1,
            'monsterbonegauntlets': 1, 
            'monsterbonefullplate': 1, 
            'monsterbonegreaves': 1, 
            'monsterbonesabatons': 1,
        },
        products=['monsterbonearmor']
    ),
    EwSmeltingRecipe(
        id_recipe="diamondhelmet",
        str_name="Diamond Helmet",
        alias=[
            'diamondhelmet',
            'Diamond Helmet',
            'dhelmet',
        ],
        ingredients={
            ewcfg.item_id_minecraftdiamond: 1,
        },
        products=['diamondhelmet']
    ),
    EwSmeltingRecipe(
        id_recipe="diamondchestplate",
        str_name="Diamond Chestplate",
        alias=[
            'diamondchestplate',
            'Diamond Chestplate',
            'dchestplate',
        ],
        ingredients={
            ewcfg.item_id_minecraftdiamond: 1,
        },
        products=['diamondchestplate']
    ),
    EwSmeltingRecipe(
        id_recipe="diamondleggings",
        str_name="Diamond Leggings",
        alias=[
            'diamondleggings',
            'Diamond Leggings',
            'dleggings',
        ],
        ingredients={
            ewcfg.item_id_minecraftdiamond: 1,
        },
        products=['diamondleggings']
    ),
    EwSmeltingRecipe(
        id_recipe="diamondboots",
        str_name="Diamond Boots",
        alias=[
            'diamondboots',
            'Diamond Boots',
            'dboots',
        ],
        ingredients={
            ewcfg.item_id_minecraftdiamond: 1,
        },
        products=['diamondboots']
    ),
    EwSmeltingRecipe(
        id_recipe="trenchcoat",
        str_name="Trench coat",
        alias=[
            'trenchcoat',
            'trench',
            'tcoat',
        ],
        ingredients={
            ewcfg.item_id_negapoudrin: 1,
            ewcfg.item_id_textiles: 1, 
            ewcfg.item_id_leather: 1,
        },
        products=['trenchcoat']
    ),  
    EwSmeltingRecipe(
        id_recipe="rippedjeans",
        str_name="Ripped Jeans",
        alias=[
            'ripmyjeansplease',
            'ripjeans',
            'rippedjeans',
        ],
        ingredients={
            'jeans': 1,
        },
        products=['rippedjeans']
    ),  
    EwSmeltingRecipe(
        id_recipe="shortshorts",
        str_name="Short Shorts",
        alias=[
            'shortshorts',
            'shortenmyshorts',
            'short2',
        ],
        ingredients={
            ewcfg.item_id_tanningknife: 1,
            'shorts': 1,
        },
        products=['shortshorts']
    ),  
    EwSmeltingRecipe(
        id_recipe="shortshortshorts",
        str_name="Short Short Shorts",
        alias=[
            'shortmyshortsagain',
            'shortshortshorts',
            'short3',
        ],
        ingredients={
            ewcfg.item_id_tanningknife: 1,
            'shortshorts': 1,
        },
        products=['shortshortshorts']
    ),  
    EwSmeltingRecipe(
        id_recipe="monsterbonecodpiece",
        str_name="Monster Bone Codpiece",
        alias=[
            'mbcodpiece',
            'monstercodpiece',
            'compensatingforsomething',
            'Monster Bone Codpiece',
        ],
        ingredients={
            ewcfg.item_id_monsterbones: 300,
        },
        products=['monsterbonecodpiece']
    ),  
    EwSmeltingRecipe(
        id_recipe="tomatotinsuit",
        str_name="Tomato Tin Suit",
        alias=[
            'tinsuit',
            'tomatosuit',
            'tomatotinsuit',
        ],
        ingredients={
            ewcfg.item_id_tincan: 10,
            'cannedtomatosoup': 5,
        },
        products=['tomatotinsuit']
    ),
    EwSmeltingRecipe(
        id_recipe="heavymetalarmor",
        str_name="Heavy Metal Armor",
        alias=[
            'heavyarmor',
            'heavymetalarmor',
            'hmarmor',
        ],
        ingredients={
            'knightarmor': 3,
        },
        products=['heavymetalarmor']
    ),
EwSmeltingRecipe(
        id_recipe="ectocooler",
        str_name="Hi-C Ecto Cooler",
        alias=[
            'hicectocooler',
            'hic',
            'hi-c',
        ],
        ingredients={
            ewcfg.item_id_ectoplasm: 5,
            'direapplefrickenergy': 1,
        },
        products=['ectocooler']
    ),
    EwSmeltingRecipe(
        id_recipe="druggumbo",
        str_name="Drug Gumbo",
        alias=[
            'drugsoup',
            'zugisacrackhead',
        ],
        ingredients={
            ewcfg.item_id_foodbase: 1,
            ewcfg.item_id_dankwheatchaff: 1,
            ewcfg.item_id_seaweed: 1,
            'purpledrink': 1,
            'coleslaw': 1,
            'justcumfuckenergy': 1,
            ewcfg.item_id_gmaxfuckenergybodyspray: 1,
            'pileofmysteriouspowder': 1,
            'armageddonspritzer': 1,
            ewcfg.item_id_pheromones: 1,
            ewcfg.item_id_carpotoxin: 1,
            'cigarette': 1,
            'cigarettebutt': 1,
            'cigar': 1,
            ewcfg.item_id_spent_pod: 1,
            ewcfg.item_id_usedneedle: 1,
        },
        products=['druggumbo']
    ),
    EwSmeltingRecipe(
        id_recipe="maidoutfit",
        str_name = "Maid outfit",
        alias=[
            'maid suit',
            'maid dress',
            'maid outfit'
        ],
        ingredients = {
            ewcfg.item_id_ghostlycloth : 3,
            ewcfg.item_id_negapoudrin : 3,
            ewcfg.item_id_cute_material : 2,
            ewcfg.item_id_ghosttoken : 2,
        },
        products=['maidoutfit']
    ),
    EwSmeltingRecipe(
        id_recipe = "cigaretteholder",
        str_name = "Cigarette Holder",
        alias =[
            'cigholder',
            'cighold',
            'cigstickonastick'
        ],
        ingredients={
            'cigarette': 1,
            ewcfg.item_id_stick: 2,
            ewcfg.item_id_ghosttoken : 1
        },
        products=['cigaretteholder']
    ),
    EwSmeltingRecipe(
        id_recipe = "widebrimmedhat",
        str_name ='Wide Brimmed Hat',
        alias = [
            'vampirehat',
            'sunhat',
            'moonhat'
        ],
        ingredients = {
            ewcfg.item_id_ghostlycloth: 3,
            ewcfg.item_id_blacklimeade : 2,
            ewcfg.item_id_ghosttoken : 1
        },
        products=['widebrimmedhat']
    ),
    EwSmeltingRecipe(
        id_recipe = 'drapeddress',
        str_name = 'Draped Evening Dress',
        alias = [
            'bigdress',
            'drapeddress',
            'eveningdress',
        ],
        ingredients = {
            ewcfg.item_id_ghostlycloth : 4,
            ewcfg.item_id_negapoudrin : 1,
            ewcfg.item_id_faggot : 1,
            ewcfg.item_id_ghosttoken : 1
        },
        products = ['drapeddress']
    ),
    EwSmeltingRecipe(
        id_recipe="bulletnecklace",
        str_name="a bullet necklace",
        alias=[
            'bulletneck',
            'bnecklace',
            'pinkerton',
            'weezer',
        ],
        ingredients={
            ewcfg.item_id_454casullround: 1,
            ewcfg.item_id_leather: 1,
            ewcfg.item_id_ironingot: 2,
        },
        products=["bulletnecklace"]
),
EwSmeltingRecipe(
        id_recipe="moonshoes",
        str_name="Moon Shoes",
        alias=[
            'moonshoe',
        ],
        ingredients={
            ewcfg.item_id_moonrock: 25,
            ewcfg.item_id_oldboot: 2,
        },
        products=['moonshoes']
    ),
    EwSmeltingRecipe(
        id_recipe="rabbitsuit",
        str_name="Rabbit Suit",
        alias=[
            'playboysuit',
        ],
        ingredients={
            ewcfg.item_id_beautiful_material: 5,
            ewcfg.item_id_monofilamentfragment: 10,
            ewcfg.item_id_leather: 1,
            ewcfg.item_id_pheromones: 1,
            ewcfg.item_id_lasso: 1,
            ewcfg.item_id_textiles: 1,
        },
        products=['rabbitsuit']
    ),
    EwSmeltingRecipe(
        id_recipe="heelys",
        str_name="Heelys",
        alias=[
            'heel wheels',
        ],
        ingredients={
            ewcfg.item_id_textiles: 5,
            ewcfg.item_id_oldboot: 2,
        },
        products=['heelys'] 
    ),
    EwSmeltingRecipe(
        id_recipe="poudrinonastringhat",
        str_name="Poudrin on a String Hat",
        alias=[
            'moredunce',
        ],
        ingredients={
            ewcfg.item_id_stick: 1,
            ewcfg.item_id_slimepoudrin: 1,
            'duncecap': 1,
        },
        products=['poudrinonastringhat'] 
    ),
    EwSmeltingRecipe(
        id_recipe="witchoutfit",
        str_name="Witch Outfit",
        alias=[
            'witchs clothes',
            'witch',
        ],
        ingredients={
            ewcfg.item_id_textiles: 5,
            ewcfg.weapon_id_pitchfork: 1,
            ewcfg.item_id_dankwheat: 3,
            ewcfg.item_id_smart_material: 1,
        },
        products=['witchoutfit']
    ),
    EwSmeltingRecipe(
        id_recipe="heartearrings",
        str_name="Heart Earrings",
        alias=[
            'heartear',
        ],
        ingredients={
            ewcfg.item_id_tincan: 5,
            ewcfg.item_id_cute_material: 1,
            ewcfg.item_id_textiles: 1,
        },
        products=['heartearrings']
    ),
    EwSmeltingRecipe(
        id_recipe="starearrings",
        str_name="Star Earrings",
        alias=[
            'starear',
        ],
        ingredients={
            ewcfg.item_id_tincan: 5,
            ewcfg.item_id_beautiful_material: 1,
            ewcfg.item_id_textiles: 1,
        },
        products=['starearrings']
    ),
    EwSmeltingRecipe(
        id_recipe="moonearrings",
        str_name="Moon Earrings",
        alias=[
            'moonear',
        ],
        ingredients={
            ewcfg.item_id_moonrock: 2,
            ewcfg.item_id_cool_material: 1,
            ewcfg.item_id_textiles: 1,
        },
        products=['moonearrings']
    ),
    EwSmeltingRecipe(
        id_recipe="invertedpentacleearrings",
        str_name="Inverted Pentacle Earrings",
        alias=[
            'evilear',
            'pentaear',
            'invertear',
        ],
        ingredients={
            ewcfg.item_id_tincan: 5,
            ewcfg.item_id_evil_material: 1,
            ewcfg.item_id_textiles: 1,
        },
        products=['invertedpentacleearrings']
    ),
    EwSmeltingRecipe(
        id_recipe="slimecorpearrings",
        str_name="Slimecorp Earrings",
        alias=[
            'shillear',
        ],
        ingredients={
            'slimecorppin': 2,
            ewcfg.item_id_smart_material: 1,
            ewcfg.item_id_textiles: 1,
        },
        products=['slimecorpearrings']
    ),
    EwSmeltingRecipe(
        id_recipe="rivetearrings",
        str_name="Rivet Earrings",
        alias=[
            'rivetear',
            'rivet',
        ],
        ingredients={
            ewcfg.item_id_ironingot: 1,
            ewcfg.item_id_tough_material: 1,
            ewcfg.item_id_textiles: 1,
        },
        products=['rivetearrings']
    ),
    EwSmeltingRecipe(
        id_recipe="alienleather",
        str_name="Alien Leather",
        alias=[
            'grayleather',
        ],
        ingredients={
            'alienscalp': 100,
            ewcfg.item_id_tanningknife: 1,
        },
        products=['alienleather']
    ),
    EwSmeltingRecipe(
        id_recipe="monofilamentcloth",
        str_name="Monofilament Cloth",
        alias=[
            'monocloth',
        ],
        ingredients={
            ewcfg.item_id_monofilamentfragment: 50,
            ewcfg.item_id_textiles: 1,
        },
        products=['monofilamentcloth']
    ),
    EwSmeltingRecipe(
        id_recipe="alienluxuryhandbag",
        str_name="Alien Luxury Hand Bag",
        alias=[
            'alienhandbag',
        ],
        ingredients={
            ewcfg.item_id_alienleather: 2,
            ewcfg.item_id_textiles: 3,
        },
        products=['alienluxuryhandbag']
    ),
    EwSmeltingRecipe(
        id_recipe="alienleathermidcalfboots",
        str_name="Alien Midcalf Boots",
        alias=[
            'alienboots',
        ],
        ingredients={
            ewcfg.item_id_alienleather: 4,
            ewcfg.item_id_textiles: 3,
        },
        products=['alienleathermidcalfboots']
    ),
    EwSmeltingRecipe(
        id_recipe="monofilamentkaleidoscopejacquard",
        str_name="Mono Kaleidoscope Jacquard",
        alias=[
            'monojacket',
            'monojacquard',
        ],
        ingredients={
            ewcfg.item_id_monofilamentcloth: 5,
            ewcfg.item_id_textiles: 3,
        },
        products=['monofilamentkaleidoscopejacquard']
    ),
    EwSmeltingRecipe(
        id_recipe="monofilamentpalazzo",
        str_name="Mono Palazzo",
        alias=[
            'monopalazzo',
        ],
        ingredients={
            ewcfg.item_id_monofilamentcloth: 3,
            ewcfg.item_id_textiles: 3,
        },
        products=['monofilamentpalazzo']
    ),
    EwSmeltingRecipe(
        id_recipe="futuredesk",
        str_name="Future Desk",
        alias=[
            'smartdesk',
        ],
        ingredients={
            ewcfg.item_id_monofilamentcloth: 2,
            ewcfg.item_id_alienleather: 2,
        },
        products=['futuredesk']
    ),
    EwSmeltingRecipe(
        id_recipe="futurelamp",
        str_name="Future Lamp",
        alias=[
            'smartlamp',
        ],
        ingredients={
            ewcfg.item_id_monofilamentcloth: 1,
            ewcfg.item_id_alienleather: 3,
        },
        products=['futurelamp']
    ),
    EwSmeltingRecipe(
        id_recipe="futurebed",
        str_name="Future Bed",
        alias=[
            'smartbed',
        ],
        ingredients={
            ewcfg.item_id_monofilamentcloth: 4,
            ewcfg.item_id_alienleather: 2,
        },
        products=['futurebed']
    ),
    EwSmeltingRecipe(
        id_recipe="futurecouch",
        str_name="Future Couch",
        alias=[
            'wallcouch',
        ],
        ingredients={
            ewcfg.item_id_monofilamentcloth: 2,
            ewcfg.item_id_alienleather: 5,
        },
        products=['futurecouch']
    ),
    EwSmeltingRecipe(
        id_recipe="edibleslime",
        str_name="Bottle of Edible Slime",
        alias=[
            'slimeedibles',
        ],
        ingredients={
            ewcfg.item_id_slimepoudrin: 50,
            "pileofmysteriouspowder": 3,
            "pawpaw": 5,
            "foodbase": 1,
            ewcfg.item_id_emptyslimebottle: 1,
        },
        products=['edibleslime']
    ),
    EwSmeltingRecipe(
        id_recipe = "wrappingpapersexywear",
        str_name = "Wrapping Paper Sexywear",
        alias = [
            "itsaslimernaliadiaster"
        ],
        ingredients = {
            'wrappingpaperhat': 100,
            ewcfg.item_id_giftribbon: 1,
        },
        products = ['wrappingpapersexywear']
    ),
    EwSmeltingRecipe(
        id_recipe="hummel",
        str_name="A Hummel",
        ingredients={
            ewcfg.item_id_giftribbon: 5,
            'brick': 25,
        },
    products=['endlesswarhummel', 'rowdyfuckerhummel', 'copkillerhummel', 'phoeubushummel', 'doubleheadlessdoublehorsemanhummel', 'deadcopshummel', 'slimexodiahummel']
    ),
    EwSmeltingRecipe(
        id_recipe = "giftpipebomb",
        str_name = "Gift Pipebomb",
        alias = [
            "themysterioustickingnoise",
            "pipebomb",
            "fakegift",            
        ],
        ingredients = {
            ewcfg.weapon_id_grenades: 1,
            ewcfg.item_id_giftribbon: 1,
        },
        products = ['giftpipebomb']
    ),
    EwSmeltingRecipe(
        id_recipe = "candycane",
        str_name = "Candy Cane?",
        alias = [
            "pennecandycane",
            "defectivecandycane",            
        ],
        ingredients = {
            ewcfg.item_id_foodbase: 3,
        },
        products = ['candycane']
    ),
    EwSmeltingRecipe(
        id_recipe = "slimeglobe",
        str_name = "Slimeglobe",
        alias = [
            "snowglobe"
        ],
        ingredients = {
            ewcfg.item_id_slimepoudrin: 50,
            ewcfg.item_id_giftribbon: 5,
        },
        products = ['slimeglobe']
    ),
    EwSmeltingRecipe(
        id_recipe = "furrobe",
        str_name = "Fur Robe",
        alias = [
            "santacoat"
        ],
        ingredients = {
            ewcfg.item_id_giftribbon: 3,
            ewcfg.item_id_textiles: 1,
        },
        products = ['furrobe']
    ),
    EwSmeltingRecipe(
        id_recipe = "wearablelights",
        str_name = "Wearable Lights",
        alias = [
            "thatmomentinachristmasfilmwherethedadgetsstuckinchristmaslightsanditssupposedtobefunnyithinkjimcarrywasinit",
            "itwasnationallampoonschristmasvacation"
            "thedudewasntevenelectrocutedlikeonthedvdcoverartworstmoviezerooutoften"
            "wearablefestivelights"
        ],
        ingredients = {
            ewcfg.item_id_giftribbon: 3,
            ewcfg.item_id_textiles: 1,
        },
        products = ['wearablelights']
    ),
]


if ewcfg.dh_active:
    smelting_recipe_list.extend([ #Accepts only one addition, so if someone wants to add more: change append to extend.
    EwSmeltingRecipe(
        id_recipe = "ticket",
        str_name = "Ticket to the White Line",
        alias = [
            "tickettohell",
        ],
        ingredients = {
            ewcfg.item_id_doublehalloweengrist: 100,
        },
    products = ['ticket']
    ),
])

# smelting_recipe_list += ewdebug.debugrecipes

# A map of id_recipe to EwSmeltingRecipe objects.
smelting_recipe_map = {}

# A list of recipe names
recipe_names = []

# Populate recipe map, including all aliases.
for recipe in smelting_recipe_list:

    # print("==============================\n\n{}\n――――――――――――――――――――――――――――――\nTo craft {}, you'll need...\n".format(recipe.str_name, recipe.str_name))
    # for ingredient in recipe.ingredients.keys():
    # 	print('{} {}'.format(recipe.ingredients[ingredient], ingredient))
    # print('')

    smelting_recipe_map[recipe.id_recipe] = recipe
    recipe_names.append(recipe.id_recipe)

    for alias in recipe.alias:
        smelting_recipe_map[alias] = recipe
