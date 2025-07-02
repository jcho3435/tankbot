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

from src.helpers.global_vars import DEFAULT_EMBED_COLOR


async def db_setup():
    conn = await aiomysql.connect(
        host=os.getenv("DB_HOST"),
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        cursorclass=aiomysql.DictCursor,
    )

    async with conn.cursor() as cur:
        cur: aiomysql.Cursor

        await cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS Users (
                id BIGINT PRIMARY KEY,
                username VARCHAR(32),
                commands INT DEFAULT 0,
                gtw_wins INT DEFAULT 0,
                profile_color CHAR(7) DEFAULT '{DEFAULT_EMBED_COLOR}',
                xp INT DEFAULT NULL
            );
            """
        )
        await conn.commit()
        print("Successfully created the Users table.")

        await cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS Feedback (
                id INT PRIMARY KEY AUTO_INCREMENT,
                userid BIGINT NOT NULL,
                subject VARCHAR(150),
                body VARCHAR(4000) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (userid) REFERENCES users(id)
            )
            """
        )
        await conn.commit()
        print("Successfully created the Feedback table.")

    await conn.ensure_closed()

asyncio.run(db_setup())






# DB SCHEMA

# Users
# ---------
# id
# username
# commands
# gtw_wins
# profile_color
# xp