#!/usr/bin/env python3
import pickle
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

    # with open("test_data.pckl", "rb") as f:
    with open("/src/test_data.pckl", "rb") as f:
        (channels, users, messages, conversations, roles, permissions) = pickle.load(f)
    await conn.copy_records_to_table(
        table_name="channels",
        records=channels,
        columns=['id', 'name']
    )
    await conn.copy_records_to_table(
        table_name="users",
        records=users,
        columns=['id', 'user_name']
    )
    await conn.copy_records_to_table(
        table_name="messages",
        records=messages,
        columns=['id', 'user_id', 'body', 'created_at', 'reference_id']
    )
    await conn.copy_records_to_table(
        table_name="conversations",
        records=conversations,
        columns=['message_id', 'channel_id']
    )
    await conn.copy_records_to_table(
        table_name="roles",
        records=roles,
        columns=['id', 'name']
    )
    
    await conn.copy_records_to_table(
        table_name="permissions",
        records=permissions,
        columns=['user_id', 'channel_id', 'role_id']
    )
    # await conn.execute('''
    #     INSERT INTO users (id, user_name, email, hashed_password, salt, is_admin)
    #     VALUES (1, 'yul','yulquen@protonmail.com','$2b$12$js/5WUAorlHn/mOYZofI/Oeqil3dWp33jQzq3ZV8khqXoiLm/O1Le',  '$2b$12$Tnol7FDwbyhWgR3meoXKEe', TRUE);
    # ''')
    # await conn.execute('''
    #     INSERT INTO permissions (user_id, channel_id, role_id)
    #     VALUES (1, 100000000000000000, 4);
    # ''')
    # await conn.execute('''
    #     INSERT INTO permissions (user_id, channel_id, role_id)
    #     VALUES (1, 788063937056210946, 4);
    # ''')
    # await conn.execute('''
    #     INSERT INTO permissions (user_id, channel_id, role_id)
    #     VALUES (1, 800740277500379171, 4);
    # ''')

    await conn.close()
    print("Database population: Done")

asyncio.run(main())