from discord.ext import commands
from discord import app_commands
import discord

from src.helpers.command_aliases import WEAPON_INFO_ALIASES, WEAPON_TIPS_ALIASES, XP_ALIASES
from src.helpers.global_vars import weapons
from src.cogs.wiki_functions.weapon_info_command import weapon_info_command
from src.cogs.wiki_functions.weapon_tips_command import weapon_tips_command

class QuickWiki(commands.Cog, name="Quick Wiki"):
    """Commands for quick wiki lookups."""

    def __init__(self, bot):
        self.bot = bot

    #region Commands
    # weapon info command
    @commands.hybrid_command(name="weapon_info", aliases=WEAPON_INFO_ALIASES)
    @app_commands.describe(weapon="Choose a weapon to get info on.")
    async def weapon_info(self, ctx: commands.Context, weapon: str):
        """Fetches and displays weapon information from the ShellShock Live wiki."""
        await weapon_info_command(ctx, weapon)

    @commands.hybrid_command(name="weapon_tips", aliases=WEAPON_TIPS_ALIASES)
    @app_commands.describe(weapon="Choose a weapon to get tips and trivia on.")
    async def weapon_tips(self, ctx: commands.Context, weapon: str):
        """Fetches and displays weapon tips and trivia from the ShellShock Live wiki. Cannot display videos from the wiki."""
        await weapon_tips_command(ctx, weapon)

    @commands.hybrid_command(name="xp", aliases=XP_ALIASES)
    @app_commands.describe(level="Choose a level or star amount to get xp requirements on.")
    async def xp(self, ctx: commands.Context, xp: str):
        """Fetches and displays xp information from the ShellShock Live wiki."""
        pass
    #endregion


    #region Autocompletes
    @weapon_info.autocomplete("weapon")
    @weapon_tips.autocomplete("weapon")
    async def weapon_autocomplete(self, interaction: discord.Interaction, current: str):
        maxLen, currLen = 10, 0
        choices = []
        current = current.lower()
        for w in weapons:
            if current in w:
                choices.append(app_commands.Choice(name=w, value=w))
                currLen += 1
                if currLen > maxLen:
                    return choices
                
        return choices
    
    #endregion

async def setup(bot: commands.Bot):
    await bot.add_cog(QuickWiki(bot))
    