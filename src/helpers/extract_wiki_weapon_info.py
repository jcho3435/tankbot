"""
Function to pull all necessary weapon data from the wiki
"""

import discord

import requests, re
import datetime
from lxml import html

from src.helpers.global_vars import WIKI_BASE_URL

#imports for typing
from typing import List

IGNORED_STATS_FIELDS = ["Requirements"]

def get_weapon_info(wepId: str) -> dict:
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