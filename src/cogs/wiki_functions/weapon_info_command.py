import discord
from discord.ext import commands
from lxml import html

import datetime, requests, re

from src.helpers.global_vars import WIKI_BASE_URL
from src.helpers.weapons import weapons, weaponData

def construct_wep_info_embed(weapon: str, sourceUrl: str, description: str, imageUrl: str, color: discord.Color, stats) -> discord.Embed:
    """
    Helper function to construct weapon embeds. This method
    should not be directly called outside of this file.
    """

    embed = discord.Embed(title=weapon, url=sourceUrl, timestamp=datetime.datetime.now(), color=color)
    embed.add_field(name="Description", value=description)
    embed.set_thumbnail(url=imageUrl)

    return embed

async def weapon_info_command(ctx: commands.Context, weapon: str):
    if weapon not in weapons:
        raise commands.BadArgument("Invalid argument")
    
    #create embed
    wepData = weaponData[weapon]
    wepId = wepData["wepId"]
    embed = construct_wep_info_embed(wepId, f"{WIKI_BASE_URL}/{wepId}", wepData["desc"], wepData["imgUrl"], discord.Color.from_str(wepData["color"]), None)

    await ctx.send(embed=embed)