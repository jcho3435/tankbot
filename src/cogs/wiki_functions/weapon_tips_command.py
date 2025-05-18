import discord
from discord.ext import commands

from src.helpers.global_vars import weapons, weaponData
from src.helpers.extract_wiki_weapon_info import update_weapon_info
from src.helpers.global_vars import WIKI_BASE_URL

import datetime

# imports for type hinting
from typing import List

def construct_weapon_tips_embed(weapon: str) -> discord.Embed:
    """
    Helper function to construct weapon tips embeds. This method
    should not be directly called outside of this file.
    """
    wepData = weaponData[weapon]
    wepId: str = wepData["wepId"]
    color = discord.Color.from_str(wepData["color"])
    imageUrl = wepData["imgUrl"]

    embed = discord.Embed(title=f"{wepId.replace("_", " ")} Tips and Trivia", timestamp=datetime.datetime.now(), color=color)
    embed.set_thumbnail(url=imageUrl)

    # return early if there is not tips/trivia section
    if not wepData["tips"]["sectionId"]:
        embed.add_field(name="No data", value="Oops! Looks like the wiki doesn't have any Tips & Tricks section for this weapon!")
        embed.url = f"{WIKI_BASE_URL}/{wepId}"
        return embed

    embed.url = f"{WIKI_BASE_URL}/{wepId}#{wepData["tips"]["sectionId"]}"

    tips: List[str] = wepData["tips"]["content"]
    for tip in tips:
        embed.add_field(name = "", value=f"\u2022 {tip}", inline=False)

    embed.set_footer(text="Incorrect or missing information? Help improve the ShellShock Live Wiki!\n")

    return embed

async def weapon_tips_command(ctx: commands.Context, weapon: str):
    if weapon not in weapons:
        raise commands.BadArgument("Invalid argument")
    
    wepData: dict = weaponData[weapon]

    #update weapon if necessary
    updated = datetime.datetime.fromisoformat(wepData["updated"])
    delta = datetime.datetime.now() - updated
    if delta.days >= 10:
        try:
            update_weapon_info(weapon)
        except Exception as e:
            print(f"Error in pulling updated weapon info from wiki (wep: {weapon}). Proceeding with old data.")
            print("Error:", e)
    
    embed = construct_weapon_tips_embed(weapon)

    await ctx.send(embed=embed)