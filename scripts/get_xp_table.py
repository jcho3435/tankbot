r"""
This is a script that will pull the full XP table from the ShellShock Live wiki, and store it
in data/xp_data.json. This script should only need to be run if for some reason there is an
issue with the current data, or if the XP table is ever updated (new levels added to SSL). 
Also, if the structure of the wiki page is ever updated, then this script might also need 
to be updated.

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
import json

from src.helpers.global_vars import WIKI_BASE_URL, XP_TABLE_JSON_FILE

from typing import List

res = requests.get(f"{WIKI_BASE_URL}/XP")
tree: html.HtmlElement = html.fromstring(res.content)
res.close()

xpTable: html.HtmlElement = tree.xpath("//table[@class='wikitable']")[0]
xpList: List[html.HtmlElement] = xpTable.xpath("./tbody/tr")[1:]

# star data is stored as 100\u2605\u2605
# note that there are no spaces between 100 and the stars
dataDict = {}
for row in xpList:
    row_data: List[html.HtmlElement] = row.xpath("./td")

    dataDict[row_data[0].text.replace(" ", "").strip()] = {"cumulative": row_data[1].text.strip(), "next_level": row_data[2].text.strip()}

with open(XP_TABLE_JSON_FILE, "w+") as f:
    json.dump(dataDict, f, indent=2)

print(f"Successfully wrote xp table data to {XP_TABLE_JSON_FILE}")
