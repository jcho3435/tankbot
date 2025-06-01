from discord import app_commands
from discord.ext import commands
import discord

from src.helpers.command_aliases import GUESS_THE_WEAPON_ALIASES

class Games(commands.Cog, name="Games"):
    """Text based games."""

    def __init__(self, bot):
        self.bot = bot
    
    # command count
    @commands.hybrid_command(aliases=GUESS_THE_WEAPON_ALIASES)
    async def guess_the_weapon(self, ctx: commands.Context, rounds: str = "1"):
        """Start a game of guess the weapon."""
        await ctx.send(f"{rounds} games started.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
    