"""
Function to pull all necessary weapon data from the wiki
"""

import requests, re, json
import datetime
from lxml import html

from src.helpers.global_vars import WIKI_BASE_URL, WEAPONS_JSON_FILE
from src.helpers.weapons import weaponData

#imports for typing
from typing import List

IGNORED_STATS_FIELDS = ["Requirements"]

def update_weapon_info(weapon: str) -> None:
    """
    Pulls updated  info for a single weapon from the wiki and stores it in data/weapons.json.

    params:
        weapon (str): The processed weapon name (all lower, spaces and hyphens replaced with underscores)
    
    returns: None
    """
    wepData = weaponData[weapon]
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
        raise lastException
    else:
        with open(WEAPONS_JSON_FILE, "w+") as f:
            json.dump(weaponData, f, indent=2)


def get_weapon_info(wepId: str) -> dict:
    """
    Returns a dict of info for a weapon.

    params:
        wepId (str): The weapon id, which is used to locate the weapon on the wiki.
    """
    res = requests.get(f"{WIKI_BASE_URL}/{wepId}")
    tree: html.HtmlElement = html.fromstring(res.content)

    wepHeader: html.HtmlElement = tree.xpath(f"//span[@id='{wepId}']")[0].getparent()
    wepInfoTable: html.HtmlElement = wepHeader.getnext()

    wepDesc = wepInfoTable.xpath("string(.//td[@class='weapondesc'])").strip() # WEAPON DESCRIPTION

    wepBoxElement: html.HtmlElement = wepInfoTable.xpath(".//div[@class='weapon-box']")[0]

    # extract weapon color
    style = wepBoxElement.attrib.get("style", "")
    matched = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', style)
    bgColorHex = matched.group(1) if matched else None

    # extract weapon image
    imgElement: html.HtmlElement = wepBoxElement.xpath(".//img")[0]
    imgUrl = imgElement.attrib.get("data-src", None)
    if not imgUrl:
        imgUrl = imgElement.attrib.get("src", "")

    # extract weapon stats
    wepStatsTable: html.HtmlElement = wepInfoTable.xpath(".//table[@class='weaponstats']/tbody")[0]
    wepStatsRows: List[html.HtmlElement] = wepStatsTable.xpath("./tr")
    stats = {}
    for tr in wepStatsRows:
        tds: List[html.HtmlElement] = tr.xpath("./td")
        label = tds[0].xpath("string(.)").strip()
        if label in IGNORED_STATS_FIELDS:
            continue
        stats[label] = tds[1].xpath("string(.)").strip()

    return {
        "desc": wepDesc, 
        "color": bgColorHex, 
        "imgUrl": imgUrl, 
        "stats": stats,
        "updated": datetime.datetime.now().isoformat()
    }