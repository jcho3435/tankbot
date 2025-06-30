"""
Fetches game news from steam API. Aside from setting the 
bot up on a new server, or if you want to do a quick manual
update, this should never need to be run.

All news: https://store.steampowered.com/news/app/326460
"""

# this will be needed for all scripts
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(curr_dir, '..'))
sys.path.insert(0, root)

import json
from src.helpers.global_vars import NEWS_JSON_FILE
from src.helpers.wiki_pull.get_news import get_news_data

data = get_news_data()

with open(NEWS_JSON_FILE, "w+") as f:
    json.dump(data, f, indent=2)

print(f"Successfully wrote {len(data["data"])} news entries to {NEWS_JSON_FILE}.")