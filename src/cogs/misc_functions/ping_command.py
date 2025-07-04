import time

from discord.ext import commands
import discord

async def ping_command(ctx: commands.Context):
    user_bot_latency = round((discord.utils.utcnow() - ctx.message.created_at).total_seconds() * 1000)
    start = time.perf_counter()
    message = await ctx.send("Pinging...")
    end = time.perf_counter()
    rest_latency = round((end - start) * 1000)
    ws_latency = round(ctx.bot.latency * 1000)
    await message.edit(content=f"Pong!\n\n`WebSocket RTT: {ws_latency} ms`\n`REST API latency: {rest_latency} ms`\n`User to Bot latency: {user_bot_latency} ms`")
