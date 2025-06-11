from discord.ext import commands
from discord import app_commands
import discord

from src.helpers.command_aliases import WEAPON_INFO_ALIASES, WEAPON_TIPS_ALIASES, WEAPON_TREE_ALIASES, XP_ALIASES
from src.helpers.global_vars import weapons, level_options
from src.cogs.wiki_functions.weapon_info_command import weapon_info_command
from src.cogs.wiki_functions.weapon_tips_command import weapon_tips_command
from src.cogs.wiki_functions.weapon_tree_command import weapon_tree_command
from src.cogs.wiki_functions.xp_table_command import xp_table_command

class QuickWiki(commands.Cog, name="Quick Wiki"):
    """Commands for quick wiki lookups."""

    def __init__(self, bot):
        self.bot = bot

    #region Commands
    # weapon info command
    @commands.hybrid_command(aliases=WEAPON_INFO_ALIASES)
    @app_commands.describe(weapon="Choose a weapon to get info on.")
    async def weapon_info(self, ctx: commands.Context, weapon: str):
        """Fetches and displays weapon information from the ShellShock Live wiki."""
        await weapon_info_command(ctx, weapon)


    # weapon tips command
    @commands.hybrid_command(
        aliases=WEAPON_TIPS_ALIASES, 
        help="Fetches and displays weapon tips and trivia from the ShellShock Live wiki. Cannot display videos from the wiki.",
        description="Fetches and displays weapon tips and trivia from the ShellShock Live wiki."
    )
    @app_commands.describe(weapon="Choose a weapon to get tips and trivia on.")
    async def weapon_tips(self, ctx: commands.Context, weapon: str):
        await weapon_tips_command(ctx, weapon)

    @commands.hybrid_command(aliases=WEAPON_TREE_ALIASES)
    @app_commands.describe(weapon="Choose a weapon to get the weapon tree of.")
    async def weapon_tree(self, ctx: commands.Context, weapon: str):
        """Fetches and displays weapon tree info """
        await weapon_tree_command(ctx, weapon)

    # xp command
    @commands.hybrid_command(name="xp", aliases=XP_ALIASES)
    @app_commands.describe(level="Choose a level or star amount to get xp requirements on.")
    async def xp(self, ctx: commands.Context, level: str = None):
        """Fetches and displays xp information from the ShellShock Live wiki."""
        await xp_table_command(ctx, level)

    #endregion


    #region Autocompletes
    @weapon_info.autocomplete("weapon")
    @weapon_tips.autocomplete("weapon")
    @weapon_tree.autocomplete("weapon")
    @xp.autocomplete("level")
    async def weapon_autocomplete(self, interaction: discord.Interaction, current: str):
        maxLen, currLen = 10, 0
        choices = []
        current = current.lower()
        command = interaction.command.name
        
        # decise which list of selections to use
        selections = None
        if command in ["weapon_info", "weapon_tips", "weapon_tree"]:
            selections = weapons
        elif command in ["xp"]:
            selections = level_options
        else:
            raise Exception(f"Failed to find valid command: {command}\n")
        
        for s in selections:
            if current in s:
                choices.append(app_commands.Choice(name=s, value=s))
                currLen += 1
                if currLen >= maxLen:
                    return choices
                
        return choices

    #endregion

async def setup(bot: commands.Bot):
    await bot.add_cog(QuickWiki(bot))
    