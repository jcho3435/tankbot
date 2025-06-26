from rapidfuzz import fuzz, process

from discord import app_commands
from discord.ext import commands
import discord

from src.helpers.command_aliases import COMMAND_COUNT_ALIASES, INVITE_ALIASES
from src.helpers.global_vars import DEFAULT_PREFIX
from src.cogs.misc_functions.help_command import help_command
from src.cogs.misc_functions.uptime_command import uptime_command


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
        """Responds with the amount of time that has elapsed since the bot has last come online."""
        await uptime_command(ctx)



    @commands.hybrid_command(aliases=INVITE_ALIASES)
    async def invite(self, ctx: commands.Context):
        """Get the bot's invite link."""
        await ctx.send(f"Click [here](https://discord.com/oauth2/authorize?client_id=1372529262065750117&permissions=563364485254208&integration_type=0&scope=bot) to invite the bot!")



async def setup(bot: commands.Bot):
    await bot.add_cog(Miscellaneous(bot))
    