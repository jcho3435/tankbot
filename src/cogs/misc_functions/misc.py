from discord import app_commands
from discord.ext import commands
import discord

import datetime

from src.helpers.format_uptime import format_uptime
from src.helpers.command_aliases import COMMAND_COUNT_ALIASES
from src.cogs.misc_functions.help_command import help_command

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

async def setup(bot: commands.Bot):
    await bot.add_cog(Miscellaneous(bot))
    