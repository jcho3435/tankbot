from filelock import FileLock
import requests
import datetime, json
from typing import List

from src.helpers.global_vars import news, NEWS_JSON_FILE

def get_news_data():
    res = requests.get("https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=326460&count=5").json()
    news: List[dict] = res["appnews"]["newsitems"]

    keysToPop = ["gid", "is_external_url", "contents", "feed_type", "feedname", "appid", "feedlabel", "tags"]
    for item in news:
        for key in keysToPop:
            item.pop(key, None)

    data = {
        "data": news,
        "updated": datetime.datetime.now().isoformat()
    }

    return data

def update_news_var(): 
    maxTries, t, lastException = 3, 0, ""
    while t < maxTries:
        try:
            dataDict = get_news_data
            news.clear()
            news.update(dataDict)
            break
        except Exception as e:
            t += 1
            lastException = e

    if t == maxTries:
        raise lastException
    
    lock = FileLock(NEWS_JSON_FILE + ".lock", timeout=10)
    with lock:
        with open(NEWS_JSON_FILE, "w+") as f:
            json.dump(news, f, indent=2)