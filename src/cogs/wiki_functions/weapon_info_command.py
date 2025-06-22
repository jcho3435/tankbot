import discord
from discord.ext import commands

from datetime import datetime, timezone
import asyncio

from src.helpers.global_vars import WIKI_BASE_URL, DEFAULT_PREFIX, weapons, weaponData
from src.helpers.wiki_pull.extract_wiki_weapon_info import update_weapon_info

def construct_wep_info_embed(weapon: str) -> discord.Embed:
    """
    Helper function to construct weapon info embeds. This method
    should not be directly called outside of this file.
    """
    wepData = weaponData[weapon]
    wepId: str = wepData["wepId"]

    sourceUrl =  f"{WIKI_BASE_URL}/{wepId}"
    description = wepData["desc"]
    imageUrl = wepData["imgUrl"]
    color = discord.Color.from_str(wepData["color"])
    stats = wepData["stats"]

    embed = discord.Embed(title=wepId.replace("_", " "), url=sourceUrl, timestamp=datetime.now(timezone.utc), color=color)
    embed.set_thumbnail(url=imageUrl)
    embed.add_field(name="Description", value=description, inline=False)
    embed.add_field(name="", value="", inline=False) # create space

    for k, v in stats.items():
        embed.add_field(name=k, value=v)

    # add extra fields for centering
    neededFields = 3 - (len(stats.keys()) % 3)
    for i in range(neededFields):
        embed.add_field(name="", value="")

    embed.set_footer(text="Incorrect or missing information? Help improve the ShellShock Live Wiki!")

    return embed

async def weapon_info_command(ctx: commands.Context, weapon: str):
    if weapon not in weapons:
        raise commands.BadArgument(f"Invalid argument: Please use the slash command `/{ctx.command}` or `{DEFAULT_PREFIX}search {ctx.command}` to see the available argument options.")
    
    wepData: dict = weaponData[weapon]

    #update weapon if necessary
    updated = datetime.fromisoformat(wepData["updated"])
    delta = datetime.now() - updated
    if delta.days >= 10:
        try:
            await asyncio.to_thread(update_weapon_info, weapon) # the asyncio thread call is necessary to stop the blocking of the main thread
        except Exception as e:
            print(f"Error in pulling updated weapon info from wiki (wep: {weapon}). Proceeding with old data.")
            print("Error:", e)
    
    #create embed
    embed = construct_wep_info_embed(weapon)

    await ctx.send(embed=embed)