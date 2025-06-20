import datetime
import aiomysql

from discord.ext import commands

class Bot(commands.Bot):
    # static globals
    commandCount = 0
    startTime = datetime.datetime.now()
    guessTheWepGames = {}
    db_pool: aiomysql.Pool = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def close(self):
        print("Closing DB connection.")
        if self.db_pool:
            self.db_pool.close()
            await self.db_pool.wait_closed()
        await super().close()