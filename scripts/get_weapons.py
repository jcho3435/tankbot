r"""
This is a script that will pull all weapons from the ShellShock Live wiki page, and stores them in 
json format in data/weapons.json. This script should only need to be run every once in a while, 
when the wiki has potentially had updates, or when new weapons are added to the wiki. Also, if the 
structure of the wiki page is ever updated, then this script might also need to be updated.

NOTE: Spaces in weapon names must be replaced with underscores for the sake of the wiki.
NOTE: This script should be run from the root of the project, e.g. C://path/to/project/Tank\ Game
"""

# this will be needed for all scripts
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(curr_dir, '..'))
sys.path.insert(0, root)


from lxml import html
import requests
from tqdm import tqdm
import json

from src.helpers.global_vars import WIKI_BASE_URL, WEAPONS_JSON_FILE
from src.helpers.wiki_pull.extract_wiki_weapon_info import get_weapon_info

from typing import List

res = requests.get(f"{WIKI_BASE_URL}/weapons")
tree: html.HtmlElement = html.fromstring(res.content)
res.close()

wepTable: html.HtmlElement = tree.xpath("//table[@id='weapontable']")[0]
wepList: List[html.HtmlElement] = wepTable.xpath(".//span[@style='color:white;']")

weapons: List[str] = [wep.text for wep in wepList]

# Weapons should be stored as 
# {"weapon_name": 
#   {
#      "wepId": "Weapon-Name", "desc": "weapon description", "imageUrl": "wepImageUrl",
#      "baseWikiUrl": "baseUrl", "color": "#HEXCOL", "stats": {...},
#      "tips": {"sectionId": "ID", "content": [...]}, "requirements": "some req",
#      "updated": "ISO format datetime string"
#   }
#  "weapon_name2": {...}
# }


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