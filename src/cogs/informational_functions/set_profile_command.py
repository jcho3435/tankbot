import re
from datetime import datetime, timezone

from enum import Enum

from src.helpers import db_query_helpers as db_query
from src.helpers.global_vars import DEFAULT_EMBED_COLOR, xp_leaderboard
from src.helpers.error_embed import build_error_embed

import discord
from discord.ext import commands

#region enum
class FieldOptions(Enum):
    color="color"
    xp="xp"

#endregion

DEFAULT_COLORS = {
    "magenta": "#FF00FF",
    "pink": "#FFB6B6",
    "red": "#FF0000",
    "dark red": "#8B0000",
    "orange": "#FFA500",
    "yellow": "#FFFF00",
    "lime": "#00FF00",
    "green": "#00B000",
    "dark green": "#006400",
    "cyan": "#00FFFF",
    "blue": "#0000FF",
    "dark blue": "#00008B",
    "purple": "#800080",
}

#region set_field_functions
async def set_color_value(ctx: commands.Context, value: str):
    if not value:
        try:
            await db_query.safe_user_update(ctx.bot, ctx.author, "UPDATE users SET profile_color=DEFAULT WHERE id=%s", (ctx.author.id,))
        except Exception as e:
            errorEmbed = build_error_embed("An unexpected error occurred!", ctx.author)
            await ctx.send(embed=errorEmbed)
            raise e
    else:
        pattern = r'#[a-fA-F0-9]{6}'
        if not re.fullmatch(pattern, value):
            if value in DEFAULT_COLORS:
                value = DEFAULT_COLORS[value]
            else:
                raise commands.BadArgument(f"Invalid argument: `value` must be a valid hex code color starting with `#`. E.g. `{DEFAULT_EMBED_COLOR}`.")
        
        try:
            await db_query.safe_user_update(ctx.bot, ctx.author, "UPDATE users SET profile_color=%s WHERE id=%s", (value, ctx.author.id))
        except Exception as e:
            errorEmbed = build_error_embed("An unexpected error occurred!", ctx.author)
            await ctx.send(embed=errorEmbed)
            raise e
        
    await ctx.message.add_reaction("\u2705")

async def set_xp_value(ctx: commands.Context, value: str):
    if not value:
        try:
            await db_query.safe_user_update(ctx.bot, ctx.author, "UPDATE users SET xp=DEFAULT WHERE id=%s", (ctx.author.id,))
        except Exception as e:
            errorEmbed = build_error_embed("An unexpected error occurred!", ctx.author)
            await ctx.send(embed=errorEmbed)
            raise e
    else:
        if not value.isdigit():
            raise commands.BadArgument(f"Invalid argument: `value` must be a positive integer without commas.")
        value = int(value)
        if value < 0:
            raise commands.BadArgument(f"Invalid argument: `value` must be a positive integer without commas.")
        
        if value > (int(xp_leaderboard["data"][0]["xp"].replace(",", "")) + 1000000): # Assuming rank 1 will not be getting 1 million xp between leaderboard updates
            embed = discord.Embed(title="Everyone, point and laugh.", color=discord.Color.from_str("#FF0000"), timestamp=datetime.now(timezone.utc))
            embed.add_field(name="You know what you've done. Shame on you.", value="")
            embed.set_image(url="https://media.tenor.com/0Kx3rafiiZYAAAAC/shame-on.gif")
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            embed.set_footer(text=f"Invoked shamefully by {ctx.author.display_name}", icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed)
            return
        
        try:
            await db_query.safe_user_update(ctx.bot, ctx.author, "UPDATE users SET xp=%s WHERE id=%s", (value, ctx.author.id))
        except Exception as e:
            errorEmbed = build_error_embed("An unexpected error occurred!", ctx.author)
            await ctx.send(embed=errorEmbed)
            raise e
        
    await ctx.message.add_reaction("\u2705")



#endregion

async def set_profile_command(ctx: commands.Context, field: FieldOptions, value: str):
    match field:
        case FieldOptions.color:
            await set_color_value(ctx, value)
        case FieldOptions.xp:
            await set_xp_value(ctx, value)
        case _:
            await ctx.send("Well... I don't know how you're seeing this, but good job. This isn't supposed to be reachable.")
