import json

with open("data/weapons.json", "r+") as f:
    weaponData: dict = json.load(f)
    weapons = weaponData.keys()