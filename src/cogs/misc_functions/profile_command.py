import datetime

from src.helpers import db_query_helpers as db_query
from src.helpers.global_vars import DEFAULT_EMBED_COLOR
from src.helpers.error_embed import build_error_embed

import discord
from discord.ext import commands

def build_profile_embed(ctx: commands.Context, user: discord.User, data: dict) -> discord.Embed:
    embed = discord.Embed(title="\u00AC Profile", timestamp=datetime.datetime.now(), color=discord.Color.from_str(DEFAULT_EMBED_COLOR))
    if not data:
        embed.add_field(name="", value="`There is no data for this user!`")
        return embed
    
    embed.set_thumbnail(url=user.display_avatar)

    data = data[0]

    profileStr = f"\u2794 Username: **{user.name}**\n\n"
    profileStr += f"\u2794 Display name: **{user.display_name}**\n\n"
    profileStr += f"\u2794 Lifetime commands used: **{data["commands"]}**\n\n"
    profileStr += f"\u2794 Guess the Weapon wins: **{data["gtw_wins"]}**\n\n"

    embed.add_field(name="", value=profileStr)
    embed.add_field(name="", value="")
    embed.set_footer(icon_url=ctx.author.display_avatar, text=f"Invoked by {ctx.author.display_name}")
    return embed

async def profile_command(ctx: commands.Context, user: discord.User):
    data = []
    user = user if user else ctx.author
    user_id = user.id

    try:
        data = await db_query.safe_fetch(ctx.bot, "SELECT commands, gtw_wins FROM Users WHERE id=%s", (user_id,))
    except Exception as e:
        errorEmbed = build_error_embed("An unexpected error occurred!", ctx.author)
        await ctx.send(embed=errorEmbed)
        raise e
    
    embed = build_profile_embed(ctx, user, data)
    await ctx.send(embed=embed)