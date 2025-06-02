import discord
from discord.ext import commands, fancyhelp

import os, asyncio
import datetime

from src.helpers.command_preprocessing import preprocess_command
from src.helpers.global_vars import DEFAULT_PREFIX

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
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"\u26A0\uFE0F Missing argument: `{error.param.name}`. Please check the command usage using `>>help {ctx.command}`.")
    elif isinstance(error, commands.BadArgument) and error.args[-1].startswith("Invalid argument"):
        await ctx.send(f"\u26A0\uFE0F Invalid argument: Please use the slash command `/{ctx.command}` to see the available argument options.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"\u26A0\uFE0F Command not recognized: Use `/help` or `{DEFAULT_PREFIX}help` to see a list of commands.")
    else:
        raise error

# on message event
@bot.event
async def on_message(message: discord.message.Message):
    if message.author.bot: # skip bot responses
        return
    
    if message.channel.id in bot.guessTheWepGames and not message.content.startswith(DEFAULT_PREFIX): # handle guess the wep games
        print("message received!")
        return

    if message.content.startswith(DEFAULT_PREFIX): # commands
        message.content = preprocess_command(message.content) # preprocess commands, i.e. ensure all letters are lowercase, properly insert underscores in some args, etc.
        await bot.process_commands(message)
    
    

#endregion


# Load cogs
async def load():
    cogFiles = [
        "misc",
        "wiki",
        "game"
    ]

    for file in cogFiles:
        await bot.load_extension(f"src.cogs.{file}_functions.{file}")

asyncio.run(load())
bot.run(os.getenv("BOT_TOKEN"))