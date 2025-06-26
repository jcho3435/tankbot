from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands, fancyhelp

import os, asyncio

from src.helpers.bot import Bot
from src.helpers.command_preprocessing import preprocess_command
from src.helpers.global_vars import DEFAULT_PREFIX, TEST_GUILD
from src.helpers.error_embed import build_error_embed
from src.helpers import db_query_helpers as db_query
from src.cogs.games_functions.guess_the_weapon import handle_guess

# imports for type hinting
import discord.ext.commands


intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX), intents=intents, help_command=fancyhelp.EmbeddedHelpCommand())

#region event handlers
# On ready event
@bot.event
async def on_ready():
    # try:
    #     bot.tree.clear_commands(guild=None)
    #     print("Cleared commands")
    # except Exception as e:
    #     print(e)
    print(f"{bot.user} bot started (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print("Error while syncing commands:", str(e))
    print(f"Synced {len(synced)} slash command(s).")
    print()

# On command event
@bot.event
async def on_command(ctx: commands.Context):
    bot.commandCount += 1
    await db_query.safe_user_update(bot, ctx.author, "UPDATE Users SET commands=commands+1 WHERE id=%s;", (ctx.author.id,))

# On error event
@bot.event
async def on_command_error(ctx: discord.ext.commands.context.Context, error):
    errorMessage = ""
    if isinstance(error, commands.MissingRequiredArgument):
        errorMessage = f"Missing argument: `{error.param.name}`. Please check the command usage using `{DEFAULT_PREFIX}help {ctx.command}` or `{DEFAULT_PREFIX}search {ctx.command}`."
    elif isinstance(error, commands.BadArgument) and error.args[-1].startswith("Invalid argument"):
        errorMessage = error.args[-1]
    elif isinstance(error, commands.BadArgument):
        errorMessage = f"Invalid argument. Please use the slash command `/{ctx.command}` or `{DEFAULT_PREFIX}search {ctx.command}` to see the available argument options."
    elif isinstance(error, commands.CommandNotFound):
        errorMessage = f"Command not recognized: Use `/help` or `{DEFAULT_PREFIX}help` to see a list of commands."
    elif isinstance(error, commands.UserNotFound):
        errorMessage = f"Command argument must be a user mention."
    else:
        import traceback
        traceback.print_exception(type(error), error, error.__traceback__)
        return
    
    await ctx.send(embed=build_error_embed(errorMessage, ctx.author))

# on message event
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: # skip bot responses
        return
    
    if message.channel.id in bot.guessTheWepGames and not message.content.startswith(DEFAULT_PREFIX): # handle guess the wep games
        await handle_guess(message, bot)
        return

    if message.content.startswith(DEFAULT_PREFIX): # commands
        message.content = preprocess_command(message.content) # preprocess commands, i.e. ensure all letters are lowercase, properly insert underscores in some args, etc.
        await bot.process_commands(message)
    
    

#endregion


# Connect to DB and load cogs
async def bot_startup():
    # db connection
    try:
        bot.db_pool = await db_query.create_pool()
    except Exception as e:
        print("Error in connecting to DB\n" + str(e))
        await bot.close()
        return
    
    print("Successfully connected to db.")

    # cogs
    cogFiles = [
        "wiki",
        "informational",
        "games",
        "misc",
    ]

    for file in cogFiles:
        await bot.load_extension(f"src.cogs.{file}_functions.{file}")

    # start bot
    try:
        await bot.start(os.getenv("BOT_TOKEN"))
    finally:
        await bot.close()

try:
    asyncio.run(bot_startup())
except KeyboardInterrupt:
    print("Caught keyboard interrupt.")