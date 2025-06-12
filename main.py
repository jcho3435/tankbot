import discord
from discord.ext import commands, fancyhelp

import os, asyncio
import datetime

from src.helpers.command_preprocessing import preprocess_command
from src.helpers.global_vars import DEFAULT_PREFIX
from src.helpers.error_embed import build_error_embed
from src.cogs.games_functions.guess_the_weapon import handle_guess

# imports for type hinting
import discord.ext.commands


class Bot(commands.Bot):
    # static globals
    commandCount = 0
    startTime = datetime.datetime.now()
    guessTheWepGames = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX), intents=intents, help_command=fancyhelp.EmbeddedHelpCommand())

#region event handlers
# On ready event
@bot.event
async def on_ready():
    print(f"{bot.user} bot started (ID: {bot.user.id})")

    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} slash command(s).")

# On command event
@bot.event
async def on_command(ctx):
    bot.commandCount += 1

# On error event
@bot.event
async def on_command_error(ctx: discord.ext.commands.context.Context, error):
    errorMessage = ""
    if isinstance(error, commands.MissingRequiredArgument):
        errorMessage = f"Missing argument: `{error.param.name}`. Please check the command usage using `>>help {ctx.command}`."
    elif isinstance(error, commands.BadArgument) and error.args[-1].startswith("Invalid argument"):
        errorMessage = error.args[-1]
    elif isinstance(error, commands.CommandNotFound):
        errorMessage = f"Command not recognized: Use `/help` or `{DEFAULT_PREFIX}help` to see a list of commands."
    else:
        raise error
    
    await ctx.send(embed=build_error_embed(errorMessage, ctx.author))

# on message event
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: # skip bot responses
        return
    
    if message.channel.id in bot.guessTheWepGames and not message.content.startswith(DEFAULT_PREFIX): # handle guess the wep games
        await handle_guess(message, bot.guessTheWepGames)
        return

    if message.content.startswith(DEFAULT_PREFIX): # commands
        message.content = preprocess_command(message.content) # preprocess commands, i.e. ensure all letters are lowercase, properly insert underscores in some args, etc.
        await bot.process_commands(message)
    
    

#endregion


# Load cogs
async def load():
    cogFiles = [
        "wiki",
        "games",
        "misc"
    ]

    for file in cogFiles:
        await bot.load_extension(f"src.cogs.{file}_functions.{file}")

asyncio.run(load())
bot.run(os.getenv("BOT_TOKEN"))