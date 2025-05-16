from discord.ext import commands
from discord import app_commands
import discord

from src.helpers.weapons import weapons
from src.helpers.command_aliases import WEAPON_INFO_ALIASES
        
class WikiLookup(commands.Cog, name="Wiki Lookup"):
    """Commands for quick wiki lookups."""

    def __init__(self, bot):
        self.bot = bot

    #region Commands
    # Test command
    @commands.hybrid_command(name="weapon_info", aliases=WEAPON_INFO_ALIASES)
    @app_commands.describe(weapon="Choose a weapon to get info on.")
    async def weapon_info(self, ctx: commands.Context, weapon: str):
        if weapon not in weapons:
            raise commands.BadArgument("Invalid option")
        await ctx.send(f"You chose: {weapon}")

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
    