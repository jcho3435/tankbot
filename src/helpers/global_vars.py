import json

DEFAULT_PREFIX = ">>"
WIKI_BASE_URL = "https://shellshocklive.fandom.com/wiki"
WEAPONS_JSON_FILE = "data/weapons.json"

with open(WEAPONS_JSON_FILE, "r+") as f:
    weaponData: dict = json.load(f)
    weapons = weaponData.keys()