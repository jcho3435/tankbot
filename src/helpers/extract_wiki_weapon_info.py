"""
Function to pull all necessary weapon data from the wiki
"""

import discord

import requests, re
import datetime
from lxml import html

from src.helpers.global_vars import WIKI_BASE_URL

def get_weapon_info(wepId: str) -> dict:
    res = requests.get(f"{WIKI_BASE_URL}/{wepId}")
    tree: html.HtmlElement = html.fromstring(res.content)

    wepHeader: html.HtmlElement = tree.xpath(f"//span[@id='{wepId}']")[0].getparent()
    wepInfoTable: html.HtmlElement = wepHeader.getnext()

    wepDesc = wepInfoTable.xpath(".//td[@class='weapondesc']")[0].text # WEAPON DESCRIPTION

    wepBoxElement: html.HtmlElement = wepInfoTable.xpath(".//div[@class='weapon-box']")[0]

    style = wepBoxElement.attrib.get("style", "")
    matched = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', style)
    bgColorHex = matched.group(1) if matched else None

    imgElement: html.HtmlElement = wepBoxElement.xpath(".//img")[0]
    imgUrl = imgElement.attrib.get("data-src", None)
    if not imgUrl:
        imgUrl = imgElement.attrib.get("src", "")

    return {"desc": wepDesc, "color": bgColorHex, "imgUrl": imgUrl, "updated": datetime.datetime.now().isoformat()}