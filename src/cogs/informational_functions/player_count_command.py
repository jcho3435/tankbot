import asyncio

import discord
from discord.ext import commands

from src.helpers.global_vars import player_count
from src.helpers.wiki_pull.get_player_count import update_player_count_var

async def player_count_command(ctx: commands.Context):
    await asyncio.to_thread(update_player_count_var)
    await ctx.send(player_count["player_count"])