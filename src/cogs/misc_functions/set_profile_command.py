import datetime

from src.helpers import db_query_helpers as db_query
from src.helpers.global_vars import DEFAULT_EMBED_COLOR
from src.helpers.error_embed import build_error_embed

import discord
from discord.ext import commands

async def set_profile_command(ctx: commands.Context, field: str, value: str):
    await ctx.send("Command under construction")

    # try:
    #     data = await db_query.safe_fetch(ctx.bot, "SELECT commands, gtw_wins, profile_color, xp FROM Users WHERE id=%s", (user_id,))
    # except Exception as e:
    #     errorEmbed = build_error_embed("An unexpected error occurred!", ctx.author)
    #     await ctx.send(embed=errorEmbed)
    #     raise e