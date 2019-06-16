import os
import asyncpg

DATABASE_URL = os.environ['DATABASE_URL']


async def connection():
    conn = await asyncpg.connect(DATABASE_URL, ssl=True)
    print(conn)
    await conn.close()

