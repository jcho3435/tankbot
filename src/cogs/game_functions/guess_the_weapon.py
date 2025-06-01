from discord import app_commands
from discord.ext import commands
import discord

async def guess_the_weapon(ctx: commands.Context, rounds: str):
    rounds = int(rounds)
    await ctx.send("TEST")