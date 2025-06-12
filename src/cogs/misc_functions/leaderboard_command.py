import asyncio, datetime

import discord
from discord.ext import commands

from src.helpers.global_vars import xp_leaderboard
from src.helpers.wiki_pull.pull_xp_lb import update_xp_lb_var
from src.views.pagination import PaginationView

xp_lb_update_lock = asyncio.Lock()
TIME_BETWEEN_UPDATES = datetime.timedelta(hours=12)

class LBPageView(PaginationView):
    def __init__(self, ctx: commands.Context, current_page: int = 0):
        super().__init__(ctx, xp_leaderboard["data"], current_page=current_page, timeout=90)
        del self.data # data does not need to be saved for lb

    def build_embed(self) -> discord.Embed:
        start = self.current_page * self.per_page
        end = start + self.per_page
        embed = discord.Embed(title="XP Leaderboard", timestamp=datetime.datetime.now(), color=self.color, description=f"-# Leaderboard updates every 12 hours. Last update: <t:{int(datetime.datetime.fromisoformat(xp_leaderboard["updated"]).timestamp())}>\n")

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

async def leaderboard_command(ctx: commands.Context, page: str):
    if not page.isdigit():
        raise commands.BadArgument(f"Invalid argument: `page` must be a number between 1 and 20 inclusive.")

    page = int(page)
    if page < 1 or page > 20:
        raise commands.BadArgument(f"Invalid argument: `page` must be a number between 1 and 20 inclusive.")

    updated = datetime.datetime.fromisoformat(xp_leaderboard["updated"])
    update = False
    if datetime.datetime.now() - updated > TIME_BETWEEN_UPDATES:
        update = True

    view = LBPageView(ctx, current_page=page-1)
    embed = view.build_embed()
    if update and len(embed.fields) == 4: # insert update in progress field
        embed.insert_field_at(0, name="", value="-# Update in progress...", inline=False)
    await ctx.send(embed=embed, view=view)

    if update:
        if not xp_lb_update_lock.locked():
            async with xp_lb_update_lock:
                await asyncio.to_thread(update_xp_lb_var)