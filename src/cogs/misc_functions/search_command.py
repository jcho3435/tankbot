from datetime import datetime, timezone

from rapidfuzz import process, fuzz

from src.helpers.global_vars import DEFAULT_EMBED_COLOR, DEFAULT_PREFIX
from src.helpers import command_aliases as aliases
from src.cogs.misc_functions.set_profile_command import DEFAULT_COLORS

import discord
from discord.ext import commands

SEARCH_OUTPUT_DICT = {
    # Help
    "help": {
        "desc": "If a command is provided, shows a short description of the command, including the parameters and aliases. Otherwise, shows a list of all commands on the bot.\n\nUse `>>search parameters` to see a full explanation of command parameter syntax.",
        "syntax": f"{DEFAULT_PREFIX}help [command | category]",
        "[command | category]": "A command, command alias, or category name. Case insensitive."
    },

    # Quick Wiki
    "weapon_info": {
        "desc": "Fetches and displays weapon information from the ShellShock Live wiki. New weapon data is automatically pulled from the wiki every 10 days.",
        "syntax": f"{DEFAULT_PREFIX}weapon_info <weapon>",
        "<weapon>": "The name of a weapon from ShellShock Live. Case insensitive."
    },
    "weapon_tips": {
        "desc": "Fetches and displays weapon tips and trivia information from the ShellShock Live wiki. Cannot display videos from the wiki. New tips and trivia data is automatically pulled from the wiki every 10 days.",
        "syntax": f"{DEFAULT_PREFIX}weapon_tips <weapon>",
        "<weapon>": "The name of a weapon from ShellShock Live. Case insensitive."
    },
    "weapon_tree": {
        "desc": "Fetches and displays weapon progression information from the ShellShock Live Wiki. New tips and trivia data is automatically pulled from the wiki every 10 days.",
        "syntax": f"{DEFAULT_PREFIX}weapon_tree <weapon>",
        "<weapon>": "The name of a weapon from ShellShock Live. Case insensitive."
    },
    "xp": {
        "desc": "Fetches and displays XP information from the ShellShock Live wiki. Displays a table of all levels if no level parameter is provided.",
        "syntax": f"{DEFAULT_PREFIX}xp [level]",
        "[level]": "A level in the range 1-100 or a star level. For star levels, the following patterns are accepted: `100***`, `3 star`, `3 stars`, or `3*`."
    },

    # Games
    "guess_the_weapon": {
        "desc": "Starts a game of Guess the Weapon with up to 5 rounds. Only one game of Guess the Weapon can be active per text channel, and the user who started the game can use `>>quit` to exit the game in that channel.\n\n" +
                "Rules: The first person who guesses the correct weapon wins the round! Any user can guess a weapon at any time. Guesses are case insensitive.\n\n" +
                "\u2022 A new hint is revealed after incorrect guesses made 7.5+ seconds after the previous hint.\n" +
                "\u2022 The weapon color is revealed after 30 seconds.\n" +
                "\u2022 The game ends automatically after 2 minutes of no interaction, or if a round lasts 5 minutes without anyone guessing correctly.",
        "syntax": f"{DEFAULT_PREFIX}guess_the_weapon [rounds=1]",
        "[rounds=1]": "The number of rounds of Guess the Weapon that you want to start. Must be a value between 1-5 inclusive. `Default: 1`."
    },
    "quit": {
        "desc": "Quits all active games you have started in the current channel.",
        "syntax": f"{DEFAULT_PREFIX}quit"
    },

    # Miscellaneous
    "command_count": {
        "desc": "Responds with the number of commands that have been run globally since the last time the bot went offline.",
        "syntax": f"{DEFAULT_PREFIX}command_count"
    },
    "uptime": {
        "desc": "Responds with the amount of time that has elapsed since the bot has last come online.\n`d = days`\n`h = hours`\n`m = minutes`\n`s = seconds`",
        "syntax": f"{DEFAULT_PREFIX}uptime"
    },
    "leaderboard": {
        "desc": "Displays a table of leaderboard data for the top 200 players by XP, pulled from the Steam leaderboards. Leaderboard updates every 12 hours.",
        "syntax": f"{DEFAULT_PREFIX}leaderboard [page=1]",
        "[page=1]": "The starting page number for the leaderboards table. Must be a value between 1-20 inclusive. `Default: 1`."
    },
    "profile": {
        "desc": f"Displays a user's profile. If no parameter is given, then it displays the profile of the user who runs the command.\n\nSome profile data can be set manually. See `{DEFAULT_PREFIX}set_profile`",
        "syntax": f"{DEFAULT_PREFIX}profile [user]",
        "[user]": "A user mention, e.g. `@Tank Game#0362`."
    },
    "set_profile": {
        "desc": "Allows users to set their own profile data for certain fields.",
        "syntax": f"{DEFAULT_PREFIX}set_profile <field> [value]",
        "<field>": "The field to be set. Possible fields:\n" +
                   "**\u2022 `color`**: the user's embed color on the profile command\n" +
                   "**\u2022 `xp`**: the user's ShellShock Live XP",
        "[value]": "The value to set for the provided field. Value constrains are dependent upon the field.\nFor all fields, value can be left **empty** to **reset** the field to its default value.\n" +
                   f"**\u2022 `color`**: A valid hex code for a color preceded by the `#` symbol, or a preset color name (`{DEFAULT_PREFIX}search colors`). `Default: {DEFAULT_EMBED_COLOR}`\n" +
                   "**\u2022 `xp`**: A positive integer value without commas. `Default: Unset`"
    },
    "search": {
        "desc": f"A more detailed help command. Search for commands and other bot-related features. Use `{DEFAULT_PREFIX}search options` for a full list of all search options.",
        "syntax": f"{DEFAULT_PREFIX}search <query>",
        "<query>": f"A command, feature, etc. that the bot supports. See a full list of options by using `{DEFAULT_PREFIX}search options`"
    },

    # Others
    "parameters": {
        "desc": "Parameters displayed in `[]` are optional while parameters displayed in `<>` are required. The `|` symbol represents \"or\". For example, `[command | category]` means there is an optional parameter that can be a command or a category.\n\nSome parameters have a default value. That is shown using `=`. For example, a parameter `[rounds=1`] is an optional parameter called `rounds` that defaults to a value of 1 if no value is provided when the command is called."
    },
    "aliases": {
        "desc": f"Aliases are alternate names, either for commands or for search parameters. For example, `s` is an alias of `search`, so `{DEFAULT_PREFIX}s` and `{DEFAULT_PREFIX}search` do the same thing."
    },
    "colors": {
        "desc": "Default color names recognized by the bot:\n\n" + 
                "\n".join("   ".join(f"**`{color}`** `({hex})`" for color, hex in list(DEFAULT_COLORS.items())[i:i+3]) for i in range(0, len(DEFAULT_COLORS), 3)) # dont question what is happening here lmao
    },


    # HARDCODED
    "options": {
        "desc": "THIS SHOULD NEVER BE DISPLAYED. OUTPUT FOR THIS OPTION SHOULD BE HARDCODED."
    }
}

SEARCH_ALIASES = {
    "parameters": ["param", "params", "parameter"],
    "aliases": ["alias"],
    "colors": ["color"],

    # HARDCODED
    "options": ["option"]
}

def build_options_embed() -> discord.Embed:
    embed = discord.Embed(title=f"Search > options", color=discord.Color.from_str(DEFAULT_EMBED_COLOR))
    extraOptions = list(SEARCH_ALIASES.keys())
    commandOptions = list(SEARCH_OUTPUT_DICT.keys())
    for option in extraOptions:
        commandOptions.remove(option)
    commandsStrs = ["", "", ""]
    for i in range(len(commandOptions)):
        commandsStrs[i % 3] += f"**\u2022** `{commandOptions[i]}`\n"

    embed.add_field(name="Commands", value="", inline=False)
    for s in commandsStrs:
        embed.add_field(name="", value=s)

    embed.add_field(name="", value="", inline=False)
    extrasStrs = ["", "", ""]
    for i in range(len(extraOptions)):
        extrasStrs[i % 3] += f"**\u2022** `{extraOptions[i]}`\n"

    embed.add_field(name="Others", value="", inline=False)
    for s in extrasStrs:
            embed.add_field(name="", value=s)
    return embed

async def search_command(ctx: commands.Context, query: str):
    # HARDCODED OUTPUTS
    if query in ["option", "options"]:
        embed = build_options_embed()
        await ctx.send(embed=embed)
        return
    
    varnames = [name for name in dir(aliases) if name.isupper()]
    aliasFound = False
    for name in varnames:
        command_aliases = getattr(aliases, name)
        if query in command_aliases:
            query = name.removesuffix("_ALIASES").lower()
            aliasFound = True
            break
    
    if not aliasFound:
        for s, query_aliases in SEARCH_ALIASES.items():
            if query in query_aliases:
                query = s
                break
    
    try:
        res: dict = SEARCH_OUTPUT_DICT[query]
    except:
        options = SEARCH_OUTPUT_DICT.keys()
        matches = process.extract(query, options, scorer=fuzz.ratio, score_cutoff=55, limit=10)
        embed = None
        if not matches:
            embed = discord.Embed(title=f"Search > {query}", color=discord.Color.from_str("#FF0000"), timestamp=datetime.now(timezone.utc), description=f"No search results found for `{query}`!")
        else:
            embed = discord.Embed(title=f"Search > {query}", color=discord.Color.from_str("#FFFF00"), timestamp=datetime.now(timezone.utc), description=f"No matches found. Did you mean to search for one of the following?")
            desc = ""
            for match, _, _ in matches:
                desc += f"`{match}`\n"
            embed.add_field(name="", value=desc)
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title=f"Search > {query}", color=discord.Color.from_str(DEFAULT_EMBED_COLOR), description=res["desc"])
    if "syntax" in res:
        embed.add_field(name="Command Syntax", value=f"```{res["syntax"]}```")

    params = list(res.keys())[2:]
    for param in params:
        embed.add_field(name=f"Parameter: `{param}`", value=res[param], inline=False)

    command_aliases = []
    try:
        command_aliases = getattr(aliases, query.upper() + "_ALIASES")
    except:
        try:
            command_aliases = SEARCH_ALIASES[query]
        except:
            pass # No aliases

    if command_aliases:
        aliasStr = ", ".join(command_aliases)
        embed.add_field(name="Aliases", value=f"```{aliasStr}```")

    await ctx.send(embed=embed)