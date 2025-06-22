import os
from datetime import datetime
import discord
import aiomysql
from aiomysql import OperationalError, InterfaceError

from src.helpers.bot import Bot

MAX_RETRIES = 3
MAX_RECONNECTS = 10

async def create_pool():
    pool = await aiomysql.create_pool(
        host=os.getenv("DB_HOST"),
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        cursorclass=aiomysql.DictCursor,
        autocommit=False
    )
    return pool

async def safe_user_update(bot: Bot, user: discord.User, query: str, args: tuple = None) -> None:
    """
    Performs a safe DB update of a user, making sure the user exists, handling retries/reconnects, and handling errors.
    param `user` is a discord.User object referencing the user for which data is being updated.
    """
    tries, reconnects, lastException = 0, 0, None
    while tries < MAX_RETRIES and reconnects < MAX_RECONNECTS:
        conn: aiomysql.Connection = None
        try:
            conn = await bot.db_pool.acquire()
            async with conn.cursor() as cur:
                cur: aiomysql.Cursor
                await cur.execute("INSERT INTO Users (id, username) VALUES (%s, %s) ON DUPLICATE KEY UPDATE username=IF(Users.username <> %s, %s, Users.username)", (user.id, user.name, user.name, user.name)) # ty chatgpt. This query 1) Inserts user if not already in DB, and 2) Updates username

                if args:
                    await cur.execute(query, args)
                else:
                    await cur.execute(query)

                await conn.commit()
                break
        except (OperationalError, InterfaceError) as e:
            print(f"DB disconnection detected at {datetime.now().isoformat()}. Removing connection from pool.")
            if conn:
                conn.close()
            lastException = e
            reconnects += 1
        except Exception as e:
            print(f"Error in user update DB call on query: `{query}`\n{e}")
            if conn:
                try:
                    await conn.rollback()
                except Exception as rollback_err:
                    print("Rollback failed:", rollback_err)
            tries += 1
            lastException = e
        finally:
            if conn and not conn.closed:
                bot.db_pool.release(conn)
    
    if tries == MAX_RETRIES:
        import traceback
        traceback.print_exception(type(lastException), lastException, lastException.__traceback__)
        raise lastException
    
    if reconnects == MAX_RECONNECTS:
        print(f"Reached max attempts when trying to reconnect to DB. DB may be offline.")
        raise lastException


async def safe_fetch(bot: Bot, query: str, args: tuple = None) -> list:
    tries, reconnects, lastException = 0, 0, None
    while tries < MAX_RETRIES:
        conn: aiomysql.Connection = None
        try:
            conn = await bot.db_pool.acquire()
            async with conn.cursor() as cur:
                cur: aiomysql.Cursor

                if args:
                    await cur.execute(query, args)
                else:
                    await cur.execute(query)

                retVal = await cur.fetchall()
                await conn.rollback()
                return retVal
        except (OperationalError, InterfaceError) as e:
            print(f"DB disconnection detected at {datetime.now().isoformat()}. Removing connection from pool.")
            if conn:
                conn.close()
            lastException = e
            reconnects += 1
        except Exception as e:
            print("Error in user update in DB call\n" + str(e))
            if conn:
                try:
                    await conn.rollback()
                except Exception as rollback_err:
                    print("Rollback failed:", rollback_err)
            tries += 1
            lastException = e            
        finally:
            if conn and not conn.closed:
                bot.db_pool.release(conn)
    
    if tries == MAX_RETRIES:
        import traceback
        traceback.print_exception(type(lastException), lastException, lastException.__traceback__)
        raise lastException
    
    if reconnects == MAX_RECONNECTS:
        print(f"Reached max attempts when trying to reconnect to DB. DB may be offline.")
        raise lastException