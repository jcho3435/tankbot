from datetime import datetime, timedelta

from discord.ext import commands

def format_uptime(delta: timedelta) -> str:
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")

    return " ".join(parts)

async def uptime_command(ctx: commands.Context):
    time = datetime.now() - ctx.bot.startTime
    await ctx.send(f"The bot has been online for **{format_uptime(time)}**!")