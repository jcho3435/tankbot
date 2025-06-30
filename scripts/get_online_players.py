"""
Fetches online player count from steam API. Aside from setting the 
bot up on a new server, this should never need to be run.
"""

# this will be needed for all scripts
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(curr_dir, '..'))
sys.path.insert(0, root)

import json

from src.helpers.global_vars import PLAYER_COUNT_JSON_FILE
from src.helpers.wiki_pull.get_player_count import get_player_count_data


pulled = get_player_count_data()
data = {"old": pulled, "new": pulled}

with open(PLAYER_COUNT_JSON_FILE, "w+") as f:
    json.dump(data, f, indent=2)

print("Successfully wrote player count to file.")