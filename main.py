import discord
from discord.ext import commands, fancyhelp

import os, asyncio

# imports for type hinting
from src.cogs.misc import Miscellaneous 
import discord.ext.commands

DEFAULT_PREFIX = ">>"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX), intents=intents, help_command=fancyhelp.EmbeddedHelpCommand())

# On ready event
@bot.event
async def on_ready():
    print(f"{bot.user} bot started (ID: {bot.user.id})")

    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} slash command(s).")

# On command event
@bot.event
async def on_command(ctx):
    cog: Miscellaneous = bot.get_cog("Miscellaneous")
    if cog:
        cog.commandCount += 1

# On error event
@bot.event
async def on_command_error(ctx: discord.ext.commands.context.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"\u26A0\uFE0F Missing argument: `{error.param.name}`. Please check the command usage using `>>help {ctx.command}`.")
    else:
        raise error

# Load cogs
async def load():
    cogFiles = [
        "misc",
        "wiki",
    ]

    for file in cogFiles:
        await bot.load_extension(f"src.cogs.{file}")


asyncio.run(load())
bot.run(os.getenv("BOT_TOKEN"))