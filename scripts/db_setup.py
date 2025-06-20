"""
DB setup - this file may be changing a lot.
"""

# this will be needed for all scripts
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(curr_dir, '..'))
sys.path.insert(0, root)

import asyncio, os
import aiomysql

from src.helpers.db_query_helpers import get_connection

async def db_setup():
    conn = await get_connection()

    async with conn.cursor() as cur:
        cur: aiomysql.Cursor

        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
                id BIGINT PRIMARY KEY,
                username VARCHAR(32),
                commands INT DEFAULT 0,
                gtw_wins INT DEFAULT 0
            );
            """
        )
        await conn.commit()
        print("Successfully created the Users table.")

    conn.close()

asyncio.run(db_setup())






# DB SCHEMA

# Users
# ---------
# id
# username
# commands
# gtw_wins