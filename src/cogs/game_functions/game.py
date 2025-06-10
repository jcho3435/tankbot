from discord import app_commands
from discord.ext import commands
import discord

from src.helpers.command_aliases import GUESS_THE_WEAPON_ALIASES
from src.cogs.game_functions.guess_the_weapon import guess_the_weapon
from src.cogs.game_functions.quit import quit

class Games(commands.Cog, name="Games"):
    """Text based games."""

    def __init__(self, bot):
        self.bot = bot
    
    # guess_the_weapon
    @commands.hybrid_command(aliases=GUESS_THE_WEAPON_ALIASES)
    @app_commands.describe(rounds="Number of rounds (1-5). Default = 1")
    async def guess_the_weapon(self, ctx: commands.Context, rounds: str = "1"):
        """Start a game of guess the weapon."""
        await guess_the_weapon(ctx, rounds)


    # quit all games
    @commands.hybrid_command()
    async def quit(self, ctx: commands.Context):
        """Quit all active games you have started in the current channel"""
        await quit(ctx)

async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
    