import json
from src.helpers.global_vars import WEAPONS_JSON_FILE

with open(WEAPONS_JSON_FILE, "r+") as f:
    weaponData: dict = json.load(f)
    weapons = weaponData.keys()