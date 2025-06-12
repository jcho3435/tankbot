"""
Function to pull all necessary weapon data from the wiki
"""

import requests, re, json
from filelock import FileLock
import datetime
from lxml import html

from src.helpers.global_vars import WIKI_BASE_URL, WEAPONS_JSON_FILE
from src.helpers.global_vars import weaponData

#imports for typing
from typing import List

EXTERNAL_STATS_FIELDS = ["Requirements"]
TIPS_AND_TRIVIA_IDS = ["Tips_&_Trivia", "Tips", "Trivia", "Tips_And_Trivia"]

def escape_special_chars(s: str) -> str:
    chars = "_*~"
    for c in chars:
        s = s.replace(c, f"\\{c}")

    return s

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

    lock = FileLock(WEAPONS_JSON_FILE + ".lock", timeout=10)
    with lock:
        with open(WEAPONS_JSON_FILE, "w+") as f:
            json.dump(weaponData, f, indent=2)


def get_weapon_info(wepId: str) -> dict:
    """
    Returns a dict of info for a weapon.

    params:
        wepId (str): The weapon id, which is used to locate the weapon on the wiki.
    """
    res = requests.get(f"{WIKI_BASE_URL}/{wepId}")

    #extract base request url
    urlPath = res.request.path_url
    baseWepUrl = WIKI_BASE_URL.strip("/wiki") + urlPath
    tree: html.HtmlElement = html.fromstring(res.content)
    res.close()

    wepHeader: html.HtmlElement = tree.xpath(f"//span[@id='{wepId}']")[0].getparent()
    wepInfoTable: html.HtmlElement = wepHeader.getnext()

    wepDesc = escape_special_chars(wepInfoTable.xpath("string(.//td[@class='weapondesc'])").strip()) # WEAPON DESCRIPTION

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
    ext_stats = {k: None for k in EXTERNAL_STATS_FIELDS}
    for tr in wepStatsRows:
        tds: List[html.HtmlElement] = tr.xpath("./td")
        label = tds[0].xpath("string(.)").strip()
        if label in EXTERNAL_STATS_FIELDS:
            ext_stats[label] = escape_special_chars(tds[1].xpath("string(.)").strip())
            continue
        stats[label] = escape_special_chars(tds[1].xpath("string(.)").strip())

    # extract tips and trivia
    tipsDict = {"sectionId": None, "content": []}

    tipsHeader: html.HtmlElement = None
    tipsList: List[html.HtmlElement] = []
    for headerId in TIPS_AND_TRIVIA_IDS:
        tipsSpan = tree.xpath(f"//span[@id='{headerId}']")
        if tipsSpan:
            tipsHeader = tipsSpan[0].getparent()
            tipsDict["sectionId"] = headerId
            tipsList = tipsHeader.getnext()
            break
    
    for tip in tipsList:  # this is done to avoid excessive nesting of statements
        figure: html.HtmlElement = tip.find('figure')
        text = ""

        if figure is not None:
            if figure.tail:
                text = figure.tail.strip()
            tip.remove(figure)
        else:
            text = tip.xpath("string(.)").strip()

        tipsDict["content"].append(text)

    retVal = {
        "desc": wepDesc, 
        "color": bgColorHex, 
        "imgUrl": imgUrl, 
        "baseWikiUrl": baseWepUrl,
        "stats": stats,
        "tips": tipsDict
    }
    retVal.update({k.lower(): v for k, v in ext_stats.items()})
    retVal.update({"updated": datetime.datetime.now().isoformat()})

    return retVal