import datetime

from discord import app_commands
from discord.ext import commands
import discord

async def guess_the_weapon(ctx: commands.Context, rounds: str):
    isError = False
    if not rounds.isdigit():
        isError = True
    rounds = int(rounds)
    if rounds < 1 or rounds > 5:
        isError = True
    if isError:
        raise commands.BadArgument(f"Invalid argument: `rounds` must be a numeric value between 1 and 5 inclusive.")

    # game starts
    if ctx.channel.id in ctx.bot.guessTheWepGames:
        await ctx.send("There is already an active game in this channel!\n-# Use `>>quit` or `/quit` to quit the game. (Only the person who started the game can quit)")
    else:
        ctx.bot.guessTheWepGames[ctx.channel.id] = {"rounds": rounds, "start_time": datetime.datetime.now(), "author_id": ctx.author.id}
        await ctx.send(f"Starting: {rounds} rounds of Guess the Weapon.\n-# The person who started the game can end the game at any time using `>>quit` or `/quit`")
    