import datetime

import discord

def build_error_embed(message, author: discord.User = None) -> discord.Embed:
    embed = discord.Embed(title="\u26A0\uFE0F Error", description=message, color=discord.Color.from_str("#FF0000"), timestamp=datetime.datetime.now())
    if author:
        embed.set_author(name=author.display_name, icon_url=author.display_avatar)
    return embed
