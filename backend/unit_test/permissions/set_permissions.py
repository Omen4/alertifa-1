import asyncio
import asyncpg


HOST = 'db'
PORT = 5432
USERNAME = "admin"
PASSWORD = "iP}hg*$0tIX8"
DATABASE_NAME = "alertifa"

async def main():
    conn = await asyncpg.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE_NAME
    )
    await conn.execute('''
        INSERT INTO permissions (user_id, channel_id, role_id)
        VALUES (1, 100000000000000000, 4);
    ''')
    await conn.execute('''
        INSERT INTO permissions (user_id, channel_id, role_id)
        VALUES (1, 788063937056210946, 2);
    ''')
    await conn.execute('''
        INSERT INTO permissions (user_id, channel_id, role_id)
        VALUES (3, 100000000000000000, 2);
    ''')
    await conn.execute('''
        INSERT INTO permissions (user_id, channel_id, role_id)
        VALUES (3, 788063937056210946, 2);
    ''')
    await conn.execute('''
        INSERT INTO permissions (user_id, channel_id, role_id)
        VALUES (4, 100000000000000000, 3);
    ''')
    await conn.close()
    print("Set permissions: Done")

asyncio.run(main())
