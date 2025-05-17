from discord.ext import commands
from discord import app_commands
import discord

from src.helpers.command_aliases import WEAPON_INFO_ALIASES
from src.helpers.weapons import weapons
from src.cogs.wiki_functions.weapon_info_command import weapon_info_command

class WikiLookup(commands.Cog, name="Wiki Lookup"):
    """Commands for quick wiki lookups."""

    def __init__(self, bot):
        self.bot = bot

    #region Commands
    # weapon info command
    @commands.hybrid_command(name="weapon_info", aliases=WEAPON_INFO_ALIASES)
    @app_commands.describe(weapon="Choose a weapon to get info on.")
    async def weapon_info(self, ctx: commands.Context, weapon: str):
        await weapon_info_command(ctx, weapon)

    #endregion


    #region Autocompletes
    @weapon_info.autocomplete("weapon")
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
    await bot.add_cog(WikiLookup(bot))
    