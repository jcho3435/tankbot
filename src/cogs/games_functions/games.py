from discord import app_commands
from discord.ext import commands

from src.helpers.command_aliases import GUESS_THE_WEAPON_ALIASES
from src.cogs.games_functions.guess_the_weapon import guess_the_weapon_start
from src.cogs.games_functions.quit_command import quit_command

class Games(commands.Cog, name="Games"):
    """Text based games."""

    def __init__(self, bot):
        self.bot = bot
    
    # guess_the_weapon
    @commands.hybrid_command(aliases=GUESS_THE_WEAPON_ALIASES)
    @app_commands.describe(rounds="Number of rounds (1-5). Default = 1")
    async def guess_the_weapon(self, ctx: commands.Context, rounds: str = "1"):
        """Start a game of guess the weapon. Times out after 2 minutes with no interaction."""
        await guess_the_weapon_start(ctx, rounds)


    # quit all games
    @commands.hybrid_command()
    async def quit(self, ctx: commands.Context):
        """Quit all active games you have started in the current channel"""
        await quit_command(ctx)

async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
    