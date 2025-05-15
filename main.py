import discord
from src.client import BotClient
import os

intents = discord.Intents.default()
intents.message_content = True
client = BotClient(intents=intents)
client.run(os.getenv("BOT_TOKEN"))