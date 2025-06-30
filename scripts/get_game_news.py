"""
Fetches game news from steam API. Aside from setting the 
bot up on a new server, or if you want to do a quick manual
update, this should never need to be run.
"""

# this will be needed for all scripts
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(curr_dir, '..'))
sys.path.insert(0, root)

import json
import requests

res = requests.get("https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=326460&count=5").json()
news = res["appnews"]["newsitems"]

for item in news:
    print(item["title"])