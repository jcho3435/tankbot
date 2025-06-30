import asyncio

import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

from src.helpers.global_vars import news, DEFAULT_EMBED_COLOR
from src.helpers.wiki_pull.get_news import update_news_var

timeBetweenUpdates = timedelta(days=1)

async def recent_news_command(ctx: commands.Context):
    lastUpdate = datetime.fromisoformat(news["updated"])
    if datetime.now() - lastUpdate > timeBetweenUpdates:
        try:
            await asyncio.to_thread(update_news_var)
        except Exception as e:
            print("Error in updating news var:", e)
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)
            print("Proceeding with old data")

    embed = discord.Embed(title="Most Recent ShellShock Live News", timestamp=datetime.now(timezone.utc), color=discord.Color.from_str(DEFAULT_EMBED_COLOR))
    
    embed.add_field(name="Post", value="")
    embed.add_field(name="Author", value="")
    embed.add_field(name="Published", value="")

    for ent in news["data"]:
        embed.add_field(name="", value=f"**\u2022** \u200B [{ent["title"]}]({ent["url"]})")
        embed.add_field(name="", value=f"{ent["author"]}")
        embed.add_field(name="", value=f"<t:{ent["date"]}>")


    embed.add_field(name="", value="", inline=False)

    await ctx.send(embed=embed)