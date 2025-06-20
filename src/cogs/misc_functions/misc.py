from discord import app_commands
from discord.ext import commands
import discord

import datetime

from src.helpers.format_uptime import format_uptime
from src.helpers.command_aliases import COMMAND_COUNT_ALIASES, LEADERBOARD_ALIASES, PROFILE_ALIASES, SEARCH_ALIASES
from src.cogs.misc_functions.help_command import help_command
from src.cogs.misc_functions.leaderboard_command import leaderboard_command
from src.cogs.misc_functions.profile_command import profile_command
from src.cogs.misc_functions.search_command import search_command

class Miscellaneous(commands.Cog, name="Miscellaneous"):
    """Random miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    # Ugly workaround for help slash command
    @app_commands.command(name="help", description="Get command information.")
    async def slash_help(self, interaction: discord.Interaction, command: str = None):
        """Shows a list of commands, or shows information about a specified command."""
        await interaction.response.send_message("Your help embed is being prepared. If no embed is generated, please use the prefix command `>>help` instead.")
        await help_command(self, interaction, command)

    
    # command count
    @commands.hybrid_command(aliases=COMMAND_COUNT_ALIASES)
    async def command_count(self, ctx: commands.Context):
        """Responds with the number of commands that have been run since the last time the bot went offline."""
        await ctx.send(f"**{ctx.bot.commandCount}** command(s) have been sent since the bot last went went offline.")


    # uptime
    @commands.hybrid_command()
    async def uptime(self, ctx: commands.Context):
        """Responds with the amount of time elapsed since the bot has last come online."""
        time = datetime.datetime.now() - ctx.bot.startTime
        await ctx.send(f"The bot has been online for **{format_uptime(time)}**!")


    # leaderboard 
    @commands.hybrid_command(
        aliases=LEADERBOARD_ALIASES,
        help="Displays leaderboard data for the top 200 players by XP. Leaderboard updates every 12 hours.",
        description="Displays leaderboard data for the top 200 players by XP."
    )
    @app_commands.describe(page="Leaderboard page (default = 1). Accepted values: [1, 20].")
    async def leaderboard(self, ctx: commands.Context, page: str = "1"):
        await leaderboard_command(ctx, page)

    
    # profile
    @commands.hybrid_command(aliases=PROFILE_ALIASES)
    @app_commands.describe(user="A user mention.")
    async def profile(self, ctx: commands.Context, user: discord.User = None):
        """Displays a user's profile."""
        await profile_command(ctx, user)


    # search
    @commands.hybrid_command(aliases=SEARCH_ALIASES)
    async def search(self, ctx: commands.Context, query: str):
        """A more detailed help command. Search for commands, flags, and other bot-related features.""" # This command's output is hard coded
        await search_command(ctx, query)

async def setup(bot: commands.Bot):
    await bot.add_cog(Miscellaneous(bot))
    