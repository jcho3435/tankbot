import discord
from discord.ext import commands

from src.helpers.error_embed import build_error_embed
from src.helpers.global_vars import DEFAULT_EMBED_COLOR

from typing import Iterable

class PaginationView(discord.ui.View):
    def __init__(self, ctx: commands.Context, data: Iterable, per_page: int = 10, current_page: int = 0, color: discord.Color = discord.Color.from_str(DEFAULT_EMBED_COLOR), timeout: int = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.per_page = per_page
        self.color = color
        self.data = data
        self.max_page = (len(data) - 1) // per_page
        self.current_page = current_page if current_page <= self.max_page else self.max_page

    def build_embed(self) -> discord.Embed:
        raise NotImplementedError("Subclasses must override build_embed() to return an embed.")

    async def update(self, interaction: discord.Interaction):
        embed = self.build_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="\u23EE", style=discord.ButtonStyle.primary)
    async def firstPage(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = 0
        await self.update(interaction)

    @discord.ui.button(label="\u25C0", style=discord.ButtonStyle.primary)
    async def previousPage(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="\u25B6", style=discord.ButtonStyle.primary)
    async def nextPage(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_page:
            self.current_page += 1
            await self.update(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="\u23ED", style=discord.ButtonStyle.primary)
    async def lastPage(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = self.max_page
        await self.update(interaction)

    async def interaction_check(self, interaction: discord.Interaction, message: str):
        if interaction.user.id != self.ctx.author.id:
            embed = build_error_embed(message, interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True