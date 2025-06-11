from discord import app_commands
from discord.ext import commands
import discord

from src.cogs.games_functions.guess_the_weapon import clean_games

async def quit(ctx: commands.Context):
    clean_games(ctx.channel.id, ctx.bot.guessTheWepGames)
    
    if ctx.channel.id in ctx.bot.guessTheWepGames:
        if ctx.author.id == ctx.bot.guessTheWepGames[ctx.channel.id]["author_id"]:
            ctx.bot.guessTheWepGames.pop(ctx.channel.id)
            await ctx.send("Guess the weapon game has been ended!")
        else:
            await ctx.send("You have no active games to quit in this channel!")
            
    else:
        await ctx.send("There are no active games to quit in this channel!")
