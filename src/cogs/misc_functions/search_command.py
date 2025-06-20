import datetime

from src.helpers.global_vars import DEFAULT_EMBED_COLOR, DEFAULT_PREFIX
from src.helpers import command_aliases as aliases

import discord
from discord.ext import commands

SEARCH_OUTPUT_DICT = {
    # Help
    "help": {
        "desc": "If a command is provided, shows a short description of the command, including the parameters and aliases. Otherwise, shows a list of all commands on the bot.\n\nUse `>>search parameters` to see a full explanation of parameter syntax.",
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
        "desc": "Fetches and displays XP information from the ShellShock Live wiki. Displays a table of all levels of no level parameter is provided.",
        "syntax": f"{DEFAULT_PREFIX}xp [level]",
        "[level]": "A level in the range 1-100. For star levels, the following patterns are accepted: `100***`, `3 star`, `3 stars`, or `3*`."
    },

    # Games
    "guess_the_weapon": {
        "desc": "",
        "syntax": f"{DEFAULT_PREFIX}guess_the_weapon [rounds=1]",
    },
    "quit": {

    },

    # Miscellaneous
    "command_count": {

    },
    "uptime": {

    },
    "leaderboard": {

    },
    "profile": {

    },
    "search": {

    },

    # Others
    "parameters": {
        "desc": "Parameters displayed in `[]` are optional while parameters displayed in `<>` are required. The `|` symbol represents \"or\". For example, `[command | category]` means there is an optional parameter that can be a command or a category.\n\n" # TODO: FIX THIS
    }
}

SEARCH_ALIASES = {
    "parameters": ["param", "params", "parameter"]
}

async def search_command(ctx: commands.Context, query: str):
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
        embed = discord.Embed(title="No results!", color=discord.Color.from_str("#FF0000"), timestamp=datetime.datetime.now(), description=f"No search results found for {query}!")
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title=f"Search > {query}", color=discord.Color.from_str(DEFAULT_EMBED_COLOR), description=res["desc"])
    if "syntax" in res:
        embed.add_field(name="Syntax", value=f"```{res["syntax"]}```")

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