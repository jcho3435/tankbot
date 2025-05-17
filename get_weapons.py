"""
This is a script that will pull all weapons from the ShellShock Live wiki page, and stores them in 
json format in data/weapons.json. This script should only need to be run every once in a while, 
when the wiki has potentially had updates, or when new weapons are added to the wiki. Also, if the 
structure of the wiki page is ever updated, then this script might also need to be updated.

NOTE: Spaces in weapon names must be replaced with underscores for the sake of the wiki.
"""

from lxml import html
import requests
from tqdm import tqdm
import json

from src.helpers.global_vars import WIKI_BASE_URL
from src.helpers.extract_wiki_weapon_info import get_weapon_info

from typing import List

WEAPONS_JSON_FILE = "data/weapons.json"

res = requests.get(f"{WIKI_BASE_URL}/weapons")
tree: html.HtmlElement = html.fromstring(res.content)

wepTable: html.HtmlElement = tree.xpath("//table[@id='weapontable']")[0]
wepList: List[html.HtmlElement] = wepTable.xpath(".//span[@style='color:white;']")

weapons: List[str] = [wep.text for wep in wepList]

# Weapons should be stored as 
# {"weapon_name": {"wepId": "Weapon-Name", "desc": "weapon description", "imageUrl": "wepImageUrl", "color": "#HEXCOL", "stats": {...}}, "updated": "ISO format datetime string"}

dataDict = {}
wepCount = len(weapons)
for i in tqdm(range(wepCount)): 
    wep = weapons[i]
    wepData = {"wepId": wep.replace(" ", "_")}
    
    maxTries, t, lastException = 3, 0, ""
    while t < maxTries:
        try:
            wepWikiData = get_weapon_info(wepData["wepId"])
            wepData.update(wepWikiData)
            break
        except Exception as e:
            t += 1
            lastException = e

    if t == maxTries:
        print(f"Failed to fetch weapon data from the wiki: (wepId - {wepData["wepId"]})")
        raise lastException

    processedWep = wep.lower().replace(" ", "_").replace("-", "_") # replaces all spaces and hyphens with underscores
    dataDict[processedWep] = wepData

with open(WEAPONS_JSON_FILE, "w+") as f:
    json.dump(dataDict, f, indent=2)

print(f"Successfully wrote {wepCount} weapons' data to {WEAPONS_JSON_FILE}")






# Store the webpage into weapons.html
# with open("weapons.html", "w", encoding="utf-8") as f:
#     f.write(res.text)