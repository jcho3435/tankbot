import json

DEFAULT_PREFIX = ">>"
WIKI_BASE_URL = "https://shellshocklive.fandom.com/wiki"


def load_json_file(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
# weapons
WEAPONS_JSON_FILE = "data/weapons.json"
weaponData = load_json_file(WEAPONS_JSON_FILE)
weapons = list(weaponData.keys())

# xp
XP_JSON_FILE = "data/xp_table.json"
xp_table = load_json_file(XP_JSON_FILE)
level_options = list(xp_table.keys()) + [f"{i}*" for i in range(1, 6)]