import datetime, random

import discord
from discord.ext import commands

from src.helpers.global_vars import weapons, weaponData
from src.helpers import db_query_helpers as db_query
from src.helpers.bot import Bot

timeout = datetime.timedelta(minutes=2)
maxRoundTime = datetime.timedelta(minutes=5)
timeBetweenHints = datetime.timedelta(seconds=7.5)
timeUntilColor = datetime.timedelta(seconds=30)

#region Helper functions
def clean_games(channelId: str, guessTheWepGames: dict,):
    if channelId in guessTheWepGames:
        gameInfo = guessTheWepGames[channelId]
        lastInteraction = gameInfo["last_interaction"]
        if datetime.datetime.now() - lastInteraction > timeout:
            guessTheWepGames.pop(channelId)

def initialize_game(ctx: commands.Context, rounds: int) -> dict:
    """Returns a dict representing the game state"""
    wep = random.choice(weapons)
    wepInfo = weaponData[wep]
    hintOptions = ["desc"] + [cat for cat in wepInfo["stats"]]
    hint = random.choice(hintOptions)
    hintOptions.remove(hint)
    return {
        "rounds": rounds, 
        "current_round": 1, 
        "author_id": ctx.author.id, 
        "author_name": ctx.author.display_name,
        "author_avatar": ctx.author.display_avatar,
        "weapon": wep,
        "seen_weapons": [],
        "hints": [hint],
        "hint_options": hintOptions,
        "last_interaction": datetime.datetime.now(), 
        "last_hint_time":datetime.datetime.now(),
        "round_start_time": datetime.datetime.now()
    }

def build_game_embed(gameInfo: dict):
    embed = discord.Embed(title="Guess The Weapon!", timestamp=datetime.datetime.now(), description=f"-# A new hint is revealed after incorrect guesses made {timeBetweenHints.total_seconds()}+ seconds after the previous hint.")
    embed.set_author(name=f"Started by {gameInfo["author_name"]}", icon_url=gameInfo["author_avatar"])
    
    embed.add_field(name="", value="", inline=False)

    weaponInfo = weaponData[gameInfo["weapon"]]
    hint_no = 1
    for hint in gameInfo["hints"]:
        hintDesc = weaponInfo[hint] if hint in weaponInfo else weaponInfo["stats"][hint]

        if hint == "desc": # 
            hint = "Description"

        embed.add_field(name=f"Hint {hint_no}: {hint}", value=hintDesc, inline=False)
        hint_no += 1

    embed.add_field(name="", value="", inline=False)

    if datetime.datetime.now() - gameInfo["round_start_time"] > timeUntilColor:
        embed.color = discord.Color.from_str(weaponInfo["color"])
    
    embed.set_footer(text=f"Round {gameInfo["current_round"]}/{gameInfo["rounds"]}")

    return embed
#endregion


async def guess_the_weapon_start(ctx: commands.Context, rounds: str):
    if not rounds.isdigit():
        raise commands.BadArgument(f"Invalid argument: `rounds` must be a numeric value between 1 and 5 inclusive.")
    
    rounds = int(rounds)
    if rounds < 1 or rounds > 5:
        raise commands.BadArgument(f"Invalid argument: `rounds` must be a numeric value between 1 and 5 inclusive.")
        

    # game starts
    clean_games(ctx.channel.id, ctx.bot.guessTheWepGames)
    if ctx.channel.id in ctx.bot.guessTheWepGames:
        await ctx.send("There is already an active game in this channel!\n-# Use `>>quit` or `/quit` to quit the game. (Only the person who started the game can quit)")
    else:
        ctx.bot.guessTheWepGames[ctx.channel.id] = initialize_game(ctx, rounds)
        embed = build_game_embed(ctx.bot.guessTheWepGames[ctx.channel.id])
        await ctx.send(f"Starting `{rounds}` rounds of Guess the Weapon.\n-# The person who started the game can end the game at any time using `>>quit` or `/quit`", embed=embed)
    


async def handle_correct_guess(message: discord.Message, bot: Bot):
    """This function should not be called anywhere outside of this file"""
    guessTheWepGames = bot.guessTheWepGames

    gameInfo = guessTheWepGames[message.channel.id]
    await message.channel.send(f"{message.author.display_name} guessed correctly! The weapon was `{weaponData[gameInfo["weapon"]]["wepId"].replace("_", " ")}`")
    
    await db_query.safe_user_update(bot, message.author, "UPDATE Users SET gtw_wins=gtw_wins+1 WHERE id=%s", (message.author.id,))

    if gameInfo["current_round"] == gameInfo["rounds"]:
        guessTheWepGames.pop(message.channel.id)
        return

    gameInfo["current_round"] += 1
    gameInfo["seen_weapons"].append(gameInfo["weapon"])

    newWep = random.choice(weapons)
    while newWep in gameInfo["seen_weapons"]:
        newWep = random.choice(weapons)
    gameInfo["weapon"] = newWep

    gameInfo["round_start_time"] = gameInfo["last_hint_time"] = datetime.datetime.now()
    
    wepInfo = weaponData[newWep]
    hintOptions = ["desc"] + [cat for cat in wepInfo["stats"]]
    hint = random.choice(hintOptions)
    hintOptions.remove(hint)

    gameInfo["hints"] = [hint]
    gameInfo["hint_options"] = hintOptions

    await message.channel.send(embed=build_game_embed(gameInfo))

# assume this is only called if a game is active in the channel
async def handle_guess(message: discord.Message, bot: Bot):
    channelId, guess = message.channel.id, message.content.lower()
    guessTheWepGames = bot.guessTheWepGames

    clean_games(channelId, guessTheWepGames)
    if channelId not in guessTheWepGames:
        return

    gameInfo = guessTheWepGames[channelId]
    if datetime.datetime.now() - gameInfo["round_start_time"] > maxRoundTime:
        await message.channel.send("Max round time for `Guess the Weapon` has elapsed. Game has been forcibly quit.")
        guessTheWepGames.pop(channelId)
        return

    gameInfo["last_interaction"] = datetime.datetime.now()

    # Check for correct guess
    wep: str = gameInfo["weapon"].replace("-", "").replace("_", "")
    guess = guess.strip().replace(" ", "").replace("-", "").replace("_", "")

    if wep == guess: # correct guess
        await handle_correct_guess(message, bot)
    else: # incorrect guess
        await message.add_reaction("\u274C") # this is the :x: emoji
        if datetime.datetime.now() - gameInfo["last_hint_time"] > timeBetweenHints:
            hint = random.choice(gameInfo["hint_options"])
            gameInfo["hint_options"].remove(hint)
            gameInfo["hints"].append(hint)
            gameInfo["last_hint_time"] = datetime.datetime.now()

            msg = "**A new hint is now available!**"
            if not gameInfo["hint_options"]: # no more hint options
                gameInfo["last_hint_time"] = datetime.datetime.now() + maxRoundTime
                msg += "\n-# This is the final hint!"
            
            await message.channel.send(msg, embed=build_game_embed(gameInfo))