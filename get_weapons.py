"""
This is a script that will pull all weapons from the ShellShock Live wiki page, and creates a list
variable for them in src/helpers/weapons.py. This script should only be run when new weapons are added 
to the game. Also, if the structure of the wiki page is ever updated, then this script might also need
to be updated.

NOTE: An enum is not used for weapons because of variable naming issues (weapons that start with digits)
NOTE: Spaces in weapon names must be replaced with underscores for the sake of the wiki
"""

import requests
from src.helpers.global_vars import WIKI_BASE_URL

from lxml import html

from typing import List

res = requests.get(f"{WIKI_BASE_URL}/weapons")
tree: html.HtmlElement = html.fromstring(res.content)

wepTable: html.HtmlElement = tree.xpath("//table[@id='weapontable']")[0]
wepList: List[html.HtmlElement] = wepTable.xpath(".//span[@style='color:white;']")

weapons: List[str] = [wep.text for wep in wepList]

with open("./src/helpers/weapons.py", "w+") as f:
    f.write("weapons = [\n") # create enum class

    for wep in weapons: 
        f.write(
            f'\t"{wep.lower().replace(" ", "_").replace("-", "_")}",\n'
        ) # replaces all spaces and hyphens with underscores

    f.write("]")


# Store the webpage into weapons.html
# with open("weapons.html", "w", encoding="utf-8") as f:
#     f.write(res.text)
