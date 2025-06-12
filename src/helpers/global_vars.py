import json

DEFAULT_PREFIX = ">>"
WIKI_BASE_URL = "https://shellshocklive.fandom.com/wiki"


def load_json_file(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
# weapons
WEAPONS_JSON_FILE = "data/weapons.json"
weaponData: dict = load_json_file(WEAPONS_JSON_FILE)
weapons = list(weaponData.keys())

# xp table
XP_TABLE_JSON_FILE = "data/xp_table.json"
xp_table: dict = load_json_file(XP_TABLE_JSON_FILE)
level_options = list(xp_table.keys()) + [f"{i}*" for i in range(1, 6)]

# xp leaderboard
XP_LEADERBOARD_JSON_FILE = "data/xp_lb.json"
xp_leaderboard: dict = load_json_file(XP_LEADERBOARD_JSON_FILE)