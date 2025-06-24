import asyncio
from enum import Enum
from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands

from src.helpers.global_vars import xp_leaderboard, DEFAULT_EMBED_COLOR, DEFAULT_PREFIX
from src.helpers.wiki_pull.pull_xp_lb import update_xp_lb_var
from src.helpers.error_embed import build_error_embed
import src.helpers.db_query_helpers as db_query
from src.views.pagination import PaginationView

xp_lb_update_lock = asyncio.Lock()
XP_LB_TIME_BETWEEN_UPDATES = timedelta(hours=12)

class LeaderboardTypes(Enum):
    xp="xp"
    guess_the_weapon="guess_the_weapon"
    gtw="gtw"

class XPLBPageView(PaginationView):
    def __init__(self, ctx: commands.Context, current_page: int = 0):
        super().__init__(ctx, xp_leaderboard["data"], current_page=current_page, timeout=90)
        del self.data # data does not need to be saved for lb

    def build_embed(self) -> discord.Embed:
        start = self.current_page * self.per_page
        end = start + self.per_page
        embed = discord.Embed(title="XP Leaderboard", timestamp=datetime.now(timezone.utc), color=self.color, description=f"-# Leaderboard updates every 12 hours. Last update: <t:{int(datetime.fromisoformat(xp_leaderboard["updated"]).timestamp())}>\n")

        if xp_lb_update_lock.locked():
            embed.add_field(name="", value="-# Update in progress...", inline=False)

        embed.add_field(name="", value="", inline=False)

        rankField, nameField, xpField = "", "", ""
        players = xp_leaderboard["data"][start:end]
        for player in players:
            rankField += f"{player["rank"]}\n"
            nameField += f"{player["player"]}\n"
            xpField += f"{player["xp"]}\n"

        embed.add_field(name="Rank", value=rankField)
        embed.add_field(name="Player", value=nameField)
        embed.add_field(name="Total XP", value=xpField)
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.max_page + 1}")
        return embed
    
    def interaction_check(self, interaction):
        return super().interaction_check(interaction, "This isn't your leaderboard embed to use, smh.\n-# Use `/leaderboard` or `>>leaderboard`.")


#region lb command functions
async def xp_leaderboard_command(ctx: commands.Context, page: str):
    if not page.isdigit():
        raise commands.BadArgument(f"Invalid argument: `page` must be a number between 1 and 20 inclusive.")

    page = int(page)
    if page < 1 or page > 20:
        raise commands.BadArgument(f"Invalid argument: `page` must be a number between 1 and 20 inclusive.")

    updated = datetime.fromisoformat(xp_leaderboard["updated"])
    update = False
    if datetime.now() - updated > XP_LB_TIME_BETWEEN_UPDATES:
        update = True

    view = XPLBPageView(ctx, current_page=page-1)
    embed = view.build_embed()
    if update and len(embed.fields) == 4: # insert update in progress field
        embed.insert_field_at(0, name="", value="-# Update in progress...", inline=False)
    await ctx.send(embed=embed, view=view)

    if update:
        if not xp_lb_update_lock.locked():
            async with xp_lb_update_lock:
                await asyncio.to_thread(update_xp_lb_var)

async def gtw_leaderboard_command(ctx: commands.Context):
    embed = discord.Embed(title="Guess the Weapon Top 10", color=discord.Color.from_str(DEFAULT_EMBED_COLOR), timestamp=datetime.now(timezone.utc), description=f"-# Play Guess the Weapon by using the command `{DEFAULT_PREFIX}guess_the_weapon`!")
    data = []
    try:
        data = await db_query.safe_fetch(ctx.bot, "SELECT id, gtw_wins FROM users ORDER BY gtw_wins DESC LIMIT 10")
    except Exception as e:
        errorEmbed = build_error_embed("An unexpected error occurred!", ctx.author)
        await ctx.send(embed=errorEmbed)
        raise e
    
    rankField, userField, winsField = "\n".join([str(i) for i in range(1, 11)]), "", ""
    for entry in data:
        userField += f"<@{entry["id"]}>\n"
        winsField += f"{entry["gtw_wins"]}\n"

    embed.add_field(name="Rank", value=rankField)
    embed.add_field(name="User", value=userField)
    embed.add_field(name="Guess the Weapon Wins", value=winsField)

    await ctx.send(embed=embed)



#endregion
async def leaderboard_command(ctx: commands.Context, leaderboard_type: LeaderboardTypes, page: str):
    match leaderboard_type:
        case LeaderboardTypes.xp:
            await xp_leaderboard_command(ctx, page)
        case LeaderboardTypes.guess_the_weapon | LeaderboardTypes.gtw:
            await gtw_leaderboard_command(ctx)
        case _:
            await ctx.send("Well... I don't know how you're seeing this, but good job. This isn't supposed to be reachable.")