import discord
from discord.ext import commands

import datetime

from src.helpers.global_vars import WIKI_BASE_URL
from src.helpers.weapons import weapons, weaponData
from src.helpers.extract_wiki_weapon_info import get_weapon_info

def construct_wep_info_embed(weapon: str, sourceUrl: str, description: str, imageUrl: str, color: discord.Color, stats: dict) -> discord.Embed:
    """
    Helper function to construct weapon embeds. This method
    should not be directly called outside of this file.
    """

    embed = discord.Embed(title=weapon, url=sourceUrl, timestamp=datetime.datetime.now(), color=color)
    embed.set_thumbnail(url=imageUrl)
    embed.add_field(name="Description", value=description, inline=False)
    embed.add_field(name="", value="", inline=False) # create space

    for k, v in stats.items():
        embed.add_field(name=k, value=v)

    # add extra fields for centering
    neededFields = 3 - (len(stats.keys()) % 3)
    for i in range(neededFields):
        embed.add_field(name="", value="")

    return embed

async def weapon_info_command(ctx: commands.Context, weapon: str):
    if weapon not in weapons:
        raise commands.BadArgument("Invalid argument")
    
    wepData: dict = weaponData[weapon]

    #update weapon if necessary
    updated = datetime.datetime.fromisoformat(wepData["updated"])
    delta = datetime.datetime.now() - updated
    if delta.days >= 10:
        maxTries, t, lastException = 3, 0, ""
        while t < maxTries:
            try:
                wepWikiData = get_weapon_info(wepData["wepId"])
                wepData.update(wepWikiData)
                break
            except Exception as e:
                t += 1
                lastException = e

        if t == maxTries:
            print(f"Failed to fetch weapon data from the wiki: (wepId - {wepData["wepId"]}). Proceeding with showing old weapon data.")
            print(f"Exception: {lastException}")
        else:
            with open("data/weapons.json", "w+") as f:
                import json
                json.dump(weaponData, f, indent=2)
    
    #create embed
    wepId: str = wepData["wepId"]
    embed = construct_wep_info_embed(
        weapon = wepId.replace("_", " "), 
        sourceUrl = f"{WIKI_BASE_URL}/{wepId}", 
        description = wepData["desc"], 
        imageUrl = wepData["imgUrl"], 
        color = discord.Color.from_str(wepData["color"]), 
        stats = wepData["stats"])

    await ctx.send(embed=embed)