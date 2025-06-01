import json

DEFAULT_PREFIX = ">>"
WIKI_BASE_URL = "https://shellshocklive.fandom.com/wiki"

# weapons
WEAPONS_JSON_FILE = "data/weapons.json"

with open(WEAPONS_JSON_FILE, "r+") as f:
    weaponData: dict = json.load(f)
    weapons = list(weaponData.keys())

# xp
XP_JSON_FILE = "data/xp_table.json"
with open(XP_JSON_FILE) as f:
    xp_table: dict = json.load(f)
    level_options = list(xp_table.keys()) + [f"{i}*" for i in range(1, 6)]