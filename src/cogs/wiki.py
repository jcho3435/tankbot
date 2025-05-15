from discord.ext import commands
from enum import Enum

import discord.ext.commands # imported for type hinting

class MyEnum(Enum):
    VAL1 = "val1"
    VAL2 = "val2"
    VAL3 = "val3"
        
class WikiLookup(commands.Cog, name="Wiki Lookup"):
    """Random miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    # Test command
    @commands.hybrid_command()
    async def test(self, ctx: discord.ext.commands.context.Context, arg1: MyEnum):
        await ctx.send(f"Hello, {ctx.author.display_name}! Here is your arg: {arg1.name}, {arg1.value}")

async def setup(bot: commands.Bot):
    await bot.add_cog(WikiLookup(bot))
    