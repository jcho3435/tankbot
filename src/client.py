import discord
import time

DEFAULT_PREFIX = "t!"

class BotClient(discord.Client):
    async def on_ready(self):
        print(f"Bot started at {time.time()}\n{self.user}")

    async def on_message(self, message: discord.message.Message): # Read message based commands
        if not message.content.startswith(DEFAULT_PREFIX):
            return
        
        if message.author == self.user:
            return
        
        command = message.content[2:].strip()
        
        await message.channel.send(f"Hello, {message.author}")