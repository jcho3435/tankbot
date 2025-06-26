from rapidfuzz import fuzz, process

import discord
from discord import app_commands
from discord.ext import commands

from src.helpers.command_aliases import LEADERBOARD_ALIASES, PROFILE_ALIASES, SEARCH_ALIASES, SET_PROFILE_ALIASES, PLAYER_COUNT_ALIASES 
from src.helpers.global_vars import DEFAULT_PREFIX
from src.cogs.informational_functions.leaderboard_command import leaderboard_command, LeaderboardTypes
from src.cogs.informational_functions.profile_command import profile_command
from src.cogs.informational_functions.set_profile_command import set_profile_command, FieldOptions
from src.cogs.informational_functions.player_count_command import player_count_command
from src.cogs.informational_functions.search_command import search_command, SEARCH_OUTPUT_DICT

class Informational(commands.Cog, name="Informational"):
    """Informational commands."""

    searchSelections = list(SEARCH_OUTPUT_DICT.keys())

    def __init__(self, bot):
        self.bot = bot
    
    # leaderboard 
    @commands.hybrid_command(aliases=LEADERBOARD_ALIASES)
    @app_commands.describe(page="Leaderboard page (default = 1). Accepted values: [1, 20].")
    async def leaderboard(self, ctx: commands.Context, leaderboard_type: LeaderboardTypes, page: str = "1"):
        """Displays leaderboard data for the chosen leaderboard type."""
        await leaderboard_command(ctx, leaderboard_type, page)


    # profile
    @commands.hybrid_command(
            aliases=PROFILE_ALIASES,
            help=f"Displays a user's profile. Some profile data can be set with `{DEFAULT_PREFIX}set_profile`."
    )
    @app_commands.describe(user="A user mention.")
    async def profile(self, ctx: commands.Context, user: discord.User = None):
        await profile_command(ctx, user)

    
    # set profile
    @commands.hybrid_command(
            aliases=SET_PROFILE_ALIASES,
            help=f"Set profile data for certain fields. Use `{DEFAULT_PREFIX}search set_profile` for detailed information."
    )
    @app_commands.describe(field="The field that you would like to set.")
    @app_commands.describe(value="The value to set for for the provided field. Value constraints depend on the field being set.")
    async def set_profile(self, ctx: commands.Context, field: FieldOptions, *, value: str = None):
        await set_profile_command(ctx, field, value)

    
    # player count
    @commands.hybrid_command(aliases=PLAYER_COUNT_ALIASES)
    async def player_count(self, ctx: commands.Context):
        await player_count_command(ctx)


    # search
    @commands.hybrid_command(aliases=SEARCH_ALIASES)
    @app_commands.describe(query="The command or feature to get more information about.")
    async def search(self, ctx: commands.Context, query: str):
        """A more detailed help command. Search for commands and other bot-related features.""" # This command's output is hard coded
        await search_command(ctx, query)



    #region autocompletes
    @search.autocomplete("query")
    async def search_autocomplete(self, interaction: discord.Interaction, current: str):
        current = current.lower()
        
        selections = self.searchSelections
        
        results = process.extract(
            query=current,
            choices=selections,
            scorer=fuzz.partial_ratio,
            limit=8,
            score_cutoff=100
        ) if current else [(el, 0, 0) for el in selections[:8]]
        
        return [
            app_commands.Choice(name=match, value=match)
            for match, _, _ in results
        ]

    #endregion

    #region error handlers
    @set_profile.error # This will catch the error and pass it to the on_command_error event
    @leaderboard.error
    async def catch_enum_cast_error(self, ctx: commands.Context, error: commands.CommandError):
        return

    #endregion



async def setup(bot: commands.Bot):
    await bot.add_cog(Informational(bot))
    