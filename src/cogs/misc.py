from discord import app_commands
from discord.ext import commands
import datetime

from src.helpers.format_uptime import format_uptime

import discord.ext.commands # imported for type hinting


class Miscellaneous(commands.Cog, name="Miscellaneous"):
    """Random miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot
        self.commandCount = 0
        self.startTime = datetime.datetime.now()

    # Ugly work around for help slash command
    @app_commands.command(name="help", description="Get command information.")
    async def slash_help(self, interaction: discord.Interaction, command: str = None):
        await interaction.response.send_message("Your help embed is being prepared. If no embed is generated, please use the prefix command `>>help` instead.") 

        help_command = self.bot.help_command

        class FakeContext: # fake context object to trick fancyhelp into working
            def __init__(self, interaction: discord.Interaction):
                self.interaction = interaction
                self.bot = interaction.client
                self.channel = interaction.channel
                self.clean_prefix = ">>"

        help_command.context = FakeContext(interaction)

        if command:
            cmd = self.bot.get_command(command)
            await help_command.send_command_help(cmd)
        else:
            mapping = help_command.get_bot_mapping()
            await help_command.send_bot_help(mapping)
    
    # command count
    @commands.hybrid_command(aliases=["command-count", "commandcount"])
    async def command_count(self, ctx: discord.ext.commands.context.Context):
        """Responds with the number of commands that have been run since the last time the bot went offline."""
        await ctx.send(f"**{self.commandCount}** command(s) have been sent since the bot last went went offline.")

    # uptime
    @commands.hybrid_command()
    async def uptime(self, ctx: discord.ext.commands.context.Context):
        """Responds with the amount of time elapsed since the bot has last come online."""
        time = datetime.datetime.now() - self.startTime
        await ctx.send(f"The bot has been online for **{format_uptime(time)}**!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Miscellaneous(bot))
    