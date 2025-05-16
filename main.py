import discord
from discord.ext import commands, fancyhelp

import os, asyncio

from src.helpers.command_preprocessing import preprocess_command
from src.helpers.global_vars import DEFAULT_PREFIX

# imports for type hinting
from src.cogs.misc_functions.misc import Miscellaneous 
import discord.ext.commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX), intents=intents, help_command=fancyhelp.EmbeddedHelpCommand())

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
    cog: Miscellaneous = bot.get_cog("Miscellaneous") 
    if cog:
        cog.commandCount += 1 # Maybe replace this with a setter function, an incrementer function, or something else, then have this as a static field

# On error event
@bot.event
async def on_command_error(ctx: discord.ext.commands.context.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"\u26A0\uFE0F Missing argument: `{error.param.name}`. Please check the command usage using `>>help {ctx.command}`.")
    elif isinstance(error, commands.BadArgument) and error.args[-1].startswith("Invalid option"):
            await ctx.send(f"\u26A0\uFE0F Invalid argument: Please use the slash command `/{ctx.command}` to see the available argument options.")
    else:
        raise error

# on message event
@bot.event
async def on_message(message: discord.message.Message):
    if message.author.bot:
        return
    if not message.content.startswith(DEFAULT_PREFIX):
        return
    
    message.content = preprocess_command(message.content) # preprocess commands, i.e. ensure all letters are lowercase, properly insert underscores in some args, etc.

    await bot.process_commands(message)

#endregion


# Load cogs
async def load():
    cogFiles = [
        "misc",
        "wiki",
    ]

    for file in cogFiles:
        await bot.load_extension(f"src.cogs.{file}_functions.{file}")


asyncio.run(load())
bot.run(os.getenv("BOT_TOKEN"))