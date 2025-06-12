r"""
This is a script that will pull the first 200 positions of the XP leaderboard from steam's
leaderboard web page, and store the data in data/xp_lb.json. 

NOTE: This script should be run from the root of the project, e.g. C://path/to/project/Tank\ Game
"""

# this will be needed for all scripts
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(curr_dir, '..'))
sys.path.insert(0, root)

from src.helpers.global_vars import XP_LEADERBOARD_JSON_FILE
from src.helpers.wiki_pull.pull_xp_lb import get_xp_lb_data
import json

dataDict = get_xp_lb_data()

with open(XP_LEADERBOARD_JSON_FILE, "w+") as f:
    json.dump(dataDict, f, indent=2)

print(f"Successfully wrote {len(dataDict["data"])} players' data to {XP_LEADERBOARD_JSON_FILE}")