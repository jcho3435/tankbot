from filelock import FileLock
import requests
import datetime, json

from src.helpers.global_vars import PLAYER_COUNT_JSON_FILE, player_count

def get_player_count_data():
    res = requests.get("https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=326460").json()
    data = {"updated": datetime.datetime.now().isoformat(), "player_count": res["response"]["player_count"]}

    return data

def update_player_count_var():
    maxTries, t, lastException = 3, 0, ""
    while t < maxTries:
        try:
            dataDict = get_player_count_data()
            player_count.update(dataDict)
            break
        except Exception as e:
            t += 1
            lastException = e

    if t == maxTries:
        raise lastException
    
    lock = FileLock(PLAYER_COUNT_JSON_FILE + ".lock", timeout=10)
    with lock:
        with open(PLAYER_COUNT_JSON_FILE, "w+") as f:
            json.dump(player_count, f, indent=2)