from datetime import datetime, timezone
import re

from src.helpers.global_vars import xp_table, WIKI_BASE_URL, DEFAULT_PREFIX
from src.views.pagination import PaginationView

from discord.ext import commands
import discord

class XPPageView(PaginationView):
    def __init__(self, ctx: commands.Context):
        # only keeping xp_table.keys in order to save space
        super().__init__(ctx, list(xp_table.keys()))
        del self.data # This does not need to be tracked for xp table

    def build_embed(self) -> discord.Embed:
        start = self.current_page * self.per_page
        end = start + self.per_page
        embed = discord.Embed(url=f"{WIKI_BASE_URL}/XP", title="XP Table", timestamp=datetime.now(), color=self.color)

        levelField, cumulativeField, nextLevelField = "", "", ""
        keys = list(xp_table.keys())[start:end]
        for key in keys:
            levelField += f"{key}\n"
            cumulativeField += f"{xp_table[key]['cumulative']}\n"
            nextLevelField += f"{xp_table[key]['next_level']}\n"

        embed.add_field(name="Level", value=levelField)
        embed.add_field(name="Cumulative XP", value=cumulativeField)
        embed.add_field(name="XP to next level", value=nextLevelField)
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.max_page + 1}")
        return embed
    
    def interaction_check(self, interaction):
        return super().interaction_check(interaction, "Find your own xp table to use, bud.\n-# Use `/xp` or `>>xp`.")

async def xp_table_command(ctx: commands.Context, level: str):
    if not level:
        view = XPPageView(ctx)
        embed = view.build_embed()
        await ctx.send(embed=embed, view=view)
    else:
        # preprocess for star levels and valid levels
        pattern = r"100\*{1,5}|[1-5](\*|stars?)"
        if level.isdigit():
            l = int(level)
            if l < 1 or l > 100:
                raise commands.BadArgument(f"Invalid argument: Please use the slash command `/{ctx.command}` or `{DEFAULT_PREFIX}search {ctx.command}` to see the available argument options.")
        elif re.fullmatch(pattern, level):
            if re.fullmatch(r"100\*{1,5}", level):
                level = level.replace("*", "\u2605")
            if re.fullmatch(r"[1-5](\*|stars?)", level):
                c = level[0]
                level = f"100{'\u2605'*int(c)}"
        else:
            raise commands.BadArgument(f"Invalid argument: Please use the slash command `/{ctx.command}` or `{DEFAULT_PREFIX}search {ctx.command}` to see the available argument options.")
        
        embed = discord.Embed(url=f"{WIKI_BASE_URL}/XP", title="XP_table", timestamp=datetime.now(timezone.utc), color = discord.Color.from_str("#A8A8A8"))
        embed.add_field(name="Level", value=level)
        embed.add_field(name="Cumulative XP", value=xp_table[level]["cumulative"])
        embed.add_field(name="XP to next level", value=xp_table[level]["next_level"])

        await ctx.send(embed=embed)
