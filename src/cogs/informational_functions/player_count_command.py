import asyncio

import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

from src.helpers.global_vars import player_count, DEFAULT_EMBED_COLOR
from src.helpers.error_embed import build_error_embed
from src.helpers.wiki_pull.get_player_count import update_player_count_var

timeBetweenUpdates = timedelta(seconds=30)

def get_time_difference_str(diff: timedelta):
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours += days*24

    if hours > 0:
        return f"{hours} Hour(s)"
    if minutes > 0:
        return f"{minutes} minute(s)"
    return f"{seconds} second(s)"

async def player_count_command(ctx: commands.Context):
    lastUpdate = datetime.fromisoformat(player_count["new"]["updated"])
    if datetime.now() - lastUpdate > timeBetweenUpdates:
        try:
            await asyncio.to_thread(update_player_count_var)
        except Exception as e:
            embed = build_error_embed(f"Unexpected error: Unable to fetch online player count. Please check the online player count [here](https://steamdb.info/app/326460/charts/)!")
            await ctx.send(embed=embed)
            raise e
    
    embed = discord.Embed(title="Player Count", url="https://steamdb.info/app/326460/charts/", description=f"-# Last updated: <t:{int(datetime.fromisoformat(player_count["new"]["updated"]).timestamp())}>" ,timestamp=datetime.now(timezone.utc), color=discord.Color.from_str(DEFAULT_EMBED_COLOR))
    embed.add_field(name="Players Online", value=str(player_count["new"]["player_count"]))

    tchange = datetime.fromisoformat(player_count["new"]["updated"]) - datetime.fromisoformat(player_count["old"]["updated"])
    tchange = get_time_difference_str(tchange)
    pchange = str(player_count["new"]["player_count"]-player_count["old"]["player_count"])
    if pchange[0] != "-":
        pchange = "+" + pchange
    embed.add_field(name=f"Change Over Last {tchange}", value=pchange)
    embed.add_field(name="", value="", inline=False)
    await ctx.send(embed=embed)