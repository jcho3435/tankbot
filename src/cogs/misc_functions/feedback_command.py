from datetime import datetime, timedelta, timezone

from discord.ext import commands
import discord

from src.helpers.global_vars import DEFAULT_EMBED_COLOR
from src.helpers.error_embed import build_error_embed
from src.helpers import db_query_helpers as db_query

timeBetweenSubmit = timedelta(hours=24)

class FeedbackForm(discord.ui.Modal, title="Feedback - Suggestions - Bug Reports"):
    subject = discord.ui.TextInput(label="Subject", required=False, max_length=150)
    feedback = discord.ui.TextInput(label="Feedback/Suggestion/Bug Report", style=discord.TextStyle.paragraph)

    def __init__(self, view: 'FeedbackButtonView'):
        super().__init__()
        self.view = view
        self.ctx = view.ctx

    async def on_submit(self, interaction: discord.Interaction):
        if self.view.lastSubmit and (datetime.now() - self.view.lastSubmit < timeBetweenSubmit):
            embed = build_error_embed(f"You submitted a form too recently! Please wait until <t:{int((self.view.lastSubmit + timeBetweenSubmit).timestamp())}> before submitting again.\n\n-# You tried to double submit, didn't you?...", interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return 
        
        try:
            await db_query.safe_user_update(self.ctx.bot, self.ctx.author, "INSERT INTO feedback (userid, subject, body) VALUES (%s, %s, %s)", (self.ctx.author.id, self.subject.value if self.subject.value else None, self.feedback.value))
        except Exception as e:
            print("Exception occurred in form submission.")
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)

            await interaction.response.send_message(embed=build_error_embed("An unexpected error occurred!", self.ctx.author))
            raise(e)

        self.view.lastSubmit = datetime.now()

        embed = discord.Embed(title="Form submitted!", color=discord.Color.from_str("#2bcc3d"), timestamp=datetime.now(timezone.utc), description="Thank you for your submission!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class FeedbackButtonView(discord.ui.View):
    def __init__(self, ctx: commands.Context, lastSubmit: datetime = None, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.lastSubmit = lastSubmit
        self.ctx = ctx

    @discord.ui.button(label="Give Feedback", style=discord.ButtonStyle.primary)
    async def feedback_form(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackForm(self))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            embed = build_error_embed("This isn't your embed. Find your own, smh.", interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        if self.lastSubmit and (datetime.now() - self.lastSubmit < timeBetweenSubmit):
            embed = build_error_embed(f"You submitted a form too recently! Please wait until <t:{int((self.lastSubmit + timeBetweenSubmit).timestamp())}> before submitting again.", interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

async def feedback_command(ctx: commands.Context):
    lastSubmit: datetime | None = None
    data = await db_query.safe_fetch(ctx.bot, "SELECT UNIX_TIMESTAMP(date) time FROM feedback WHERE userid=%s ORDER BY date DESC LIMIT 1", (ctx.author.id,))
    if data:
        data = data[0]
        lastSubmit = datetime.fromtimestamp(data["time"])
    
    embed = discord.Embed(title="Feedback - Suggestions - Bug Reports", timestamp=datetime.now(timezone.utc), color=discord.Color.from_str(DEFAULT_EMBED_COLOR), description="Help improve the bot by providing feedback, suggestions, and bug reports!")
    embed.add_field(name="", value="-# Note: Abuse of the submission form may result in a temporary or permanent ban from using the bot. Abuse includes spam, inappropriate content, etc.")
    embed.add_field(name="", value="", inline=False)

    if lastSubmit:
        embed.add_field(name="", value=f"Form last submitted on <t:{data["time"]}>.")
        embed.add_field(name="", value="", inline=False)
        if datetime.now() - lastSubmit < timeBetweenSubmit:
            embed.add_field(name="", value=f"\u26A0\uFE0F You submitted a form too recently! Please wait until <t:{int((lastSubmit + timeBetweenSubmit).timestamp())}> before submitting again.")
            embed.add_field(name="", value="", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, view=FeedbackButtonView(ctx, lastSubmit))
    else:
        await ctx.send(embed=embed, view=FeedbackButtonView(ctx))