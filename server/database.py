import os
import asyncpg

DATABASE_URL = os.environ['DATABASE_URL']


async def connection():
    conn = await asyncpg.connect(DATABASE_URL)
    print(conn)
    await conn.close()

