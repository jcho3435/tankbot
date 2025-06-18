import os
import aiomysql

async def get_connection() -> aiomysql.Connection:
    """Creates a connection to the DB and returns it."""
    conn = await aiomysql.connect(
        host=os.getenv("DB_HOST"),
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        cursorclass=aiomysql.DictCursor
    )
    return conn

def user_exists(cur: aiomysql.Cursor, user_id: int) -> bool:
    pass

def safe_user_update(cur: aiomysql.Cursor, user_id: int, query: str, args: tuple | list = None) -> None:
    pass

def safe_user_fetch(cur: aiomysql.Cursor, user_id: int, query: str, args: tuple = None) -> dict:
    pass