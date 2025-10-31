import asyncio
import asyncpg
import os

async def test():
    conn = await asyncpg.connect(
        user="data_service_user",
        password="data_service_password",
        database="data_service_db",
        host="127.0.0.1",
        port=5432,
    )
    print(await conn.fetch("SELECT 1"))
    await conn.close()

asyncio.run(test())
