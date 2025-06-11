import discord
from discord.ext import commands

import datetime

from src.helpers.global_vars import WIKI_BASE_URL
from src.helpers.global_vars import weapons, weaponData
from src.helpers.custom_emojis import WEAPON_ICONS

def construct_wep_tree_embed(wepList: list) -> discord.Embed:
    """
    Helper function to construct weapon tree embeds. This method
    should not be directly called outside of this file.
    """
    firstWepData = weaponData[wepList[0]]

    embed = discord.Embed(title=f"{firstWepData["wepId"].replace("_", " ")} Weapon Progression", url=firstWepData["baseWikiUrl"], color=discord.Color.from_str(firstWepData["color"]), timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=firstWepData["imgUrl"])
    embed.add_field(name="", value="", inline=False)

    tier = 1
    for wep in wepList:
        wepData = weaponData[wep]
        embed.add_field(value=f"**Tier {tier}**", name="")
        embed.add_field(value=f"**[{wepData["wepId"].replace("_", " ")}]({WIKI_BASE_URL}/{wepData["wepId"]})**", name="")
        embed.add_field(value=f"**Unlock: {wepData["requirements"]}**", name="")
        tier += 1

    embed.add_field(name="", value="", inline=False)

    return embed

async def weapon_tree_command(ctx: commands.Context, weapon: str):
    if weapon not in weapons:
        raise commands.BadArgument(f"Invalid argument: Please use the slash command `/{ctx.command}` to see the available argument options.")
    
    # no need to pull data from the wiki for this weapon
    # find all weapons related to the primary weapon
    wepList = [weapon]
    i = weapons.index(weapon)
    targetBaseUrl = weaponData[weapon]["baseWikiUrl"]

    ci = i - 1
    while ci >= 0 and weaponData[weapons[ci]]["baseWikiUrl"] == targetBaseUrl:
        wepList.insert(0, weapons[ci])
        ci -= 1
    
    ci = i + 1
    while ci < len(weapons) and weaponData[weapons[ci]]["baseWikiUrl"] == targetBaseUrl:
        wepList.append(weapons[ci])
        ci += 1

    embed = construct_wep_tree_embed(wepList)
    await ctx.send(embed=embed)