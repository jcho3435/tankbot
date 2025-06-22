from src.helpers.global_vars import XP_LEADERBOARD_JSON_FILE, xp_leaderboard

from filelock import FileLock
from lxml import html
import requests
import json
from datetime import datetime

from typing import List

XP_LB_URL = "https://steamcommunity.com/stats/326460/leaderboards/743177"

def get_xp_lb_data() -> dict:
    """Pulls xp leaderboard data from the steam leaderboards page and returns a dict, {updated: updatetime, data: [...]}"""
    data = []

    for sr in range(1, 200, 15):
        url = XP_LB_URL + f"?sr={sr}"

        res = requests.get(url)
        tree: html.HtmlElement = html.fromstring(res.content)
        res.close()
        statsDiv: html.HtmlElement = tree.xpath("//div[@id='stats']")[0]

        entries: List[html.HtmlElement] = statsDiv.xpath(".//div[@class='lbentry']")
        if sr == 196: # hard coded because of how the steam lb page works
            entries = entries[-5:]
        for entry in entries:
            strRank: str = entry.xpath(".//div[@class='rR']")[0].text_content().strip()
            rank = int(strRank[1:])

            player = entry.xpath(".//div[@class='playerLink']")[0].text_content().strip()
            playerXp = entry.xpath(".//div[@class='score']")[0].text_content().strip()

            data.append({"rank": rank, "player": player, "xp": playerXp})

    data.sort(key=lambda el: el["rank"]) # redundant sort on rank

    return {"updated": datetime.now().isoformat(), "data": data}


def update_xp_lb_var():
    maxTries, t, lastException = 3, 0, ""
    while t < maxTries:
        try:
            dataDict = get_xp_lb_data()
            xp_leaderboard.clear()
            xp_leaderboard.update(dataDict)
            break
        except Exception as e:
            t += 1
            lastException = e

    if t == maxTries:
        raise lastException
    
    lock = FileLock(XP_LEADERBOARD_JSON_FILE + ".lock", timeout=10)
    with lock:
        with open(XP_LEADERBOARD_JSON_FILE, "w+") as f:
            json.dump(xp_leaderboard, f, indent=2)