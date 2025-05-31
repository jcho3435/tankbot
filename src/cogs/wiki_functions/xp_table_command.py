import datetime, re

from src.helpers.global_vars import xp_table, WIKI_BASE_URL

from discord.ext import commands
import discord

async def xp_table_command(ctx: commands.Context, level: str):
    embed = discord.Embed(url=f"{WIKI_BASE_URL}/XP", title="XP_table", timestamp=datetime.datetime.now())
    if not level:
        levelField = ""
        cumulativeField = ""
        nextLevelField = ""
        for i in range(10):
            
            levelField += f"{i+1}\n"
            cumulativeField += f"{xp_table[f"{i+1}"]["cumulative"]}\n"
            nextLevelField += f"{xp_table[f"{i+1}"]["next_level"]}\n"

        embed.add_field(name="Level", value=levelField)
        embed.add_field(name="Cumulative XP", value=cumulativeField)
        embed.add_field(name="XP to next level", value=nextLevelField)
        # HANDLE PAGINATION
    else:
        # preprocess for star levels and valid levels
        pattern = r"100\*{1,5}|[1-5](\*|stars?)"
        if level.isdigit():
            level = level.strip("0")
            l = int(level)
            if l < 1 or l > 100:
                raise commands.BadArgument("Invalid argument")
        elif re.fullmatch(pattern, level):
            if re.fullmatch(r"100\*{1,5}", level):
                level = level.replace("*", "\u2605")
            if re.fullmatch(r"[1-5](\*|stars?)", level):
                c = level[0]
                level = f"100{'\u2605'*int(c)}"
        else:
            raise commands.BadArgument("Invalid argument")

        embed.add_field(name="Level", value=level)
        embed.add_field(name="Cumulative XP", value=xp_table[level]["cumulative"])
        embed.add_field(name="XP to next level", value=xp_table[level]["next_level"])


    await ctx.send(embed=embed)