import json, os
import discord

from typing import List

TEST_GUILD = discord.Object(id=os.getenv("TEST_GUILD"))

DEFAULT_PREFIX = ">>"
WIKI_BASE_URL = "https://shellshocklive.fandom.com/wiki"

DEFAULT_EMBED_COLOR = "#00A6FF"


def load_json_file(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        return json.load(f)
    
# weapons
WEAPONS_JSON_FILE = "data/weapons.json"
weaponData: dict = load_json_file(WEAPONS_JSON_FILE)
weapons: List[str] = list(weaponData.keys())

# xp table
XP_TABLE_JSON_FILE = "data/xp_table.json"
xp_table: dict = load_json_file(XP_TABLE_JSON_FILE)
level_options: List[str] = list(xp_table.keys()) + [f"{i}*" for i in range(1, 6)]

# xp leaderboard
XP_LEADERBOARD_JSON_FILE = "data/xp_lb.json"
xp_leaderboard: dict = load_json_file(XP_LEADERBOARD_JSON_FILE)

# player count
PLAYER_COUNT_JSON_FILE = "data/player_count.json"
player_count: dict = load_json_file(PLAYER_COUNT_JSON_FILE)

# recent game news
NEWS_JSON_FILE = "data/news.json"
news: dict = load_json_file(NEWS_JSON_FILE)