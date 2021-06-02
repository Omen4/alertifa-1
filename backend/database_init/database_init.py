#!/usr/bin/env python3
import pickle
import asyncio

import asyncpg


HOST = 'alertifa_postgres'
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

    tables = await conn.fetch('''
        SELECT table_name
        FROM information_schema.tables
        WHERE table_type='BASE TABLE'
        AND table_schema='public';
    ''')
    for t in tables:
        await conn.execute(f'''DROP TABLE {t[0]} CASCADE;''')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id BIGSERIAL,
            created_at TIMESTAMPTZ DEFAULT Now(),
            updated_at TIMESTAMPTZ DEFAULT Now(),
            name VARCHAR,
            description VARCHAR,
            PRIMARY KEY (id)
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL,
            created_at TIMESTAMPTZ DEFAULT Now(),
            updated_at TIMESTAMPTZ DEFAULT Now(),
            user_name VARCHAR NOT NULL,
            email VARCHAR,
            bio VARCHAR,
            hashed_password VARCHAR,
            salt VARCHAR,
            jwt_id BIGINT DEFAULT 1,
            is_admin BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id)
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id BIGSERIAL,
            reference_id BIGINT,
            user_id BIGINT,
            created_at TIMESTAMPTZ DEFAULT Now(),
            updated_at TIMESTAMPTZ DEFAULT NULL,
            body VARCHAR,
            notification BIGINT DEFAULT 0,
            type BIGINT DEFAULT 0,
            PRIMARY KEY (id),
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON UPDATE CASCADE
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            message_id BIGINT,
            channel_id BIGINT,
            PRIMARY KEY (message_id, channel_id),
            FOREIGN KEY (message_id)
                REFERENCES messages(id)
                ON UPDATE CASCADE,
            FOREIGN KEY (channel_id)
                REFERENCES channels(id)
                ON UPDATE CASCADE
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id BIGINT,
            name VARCHAR,
            PRIMARY KEY (id)
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            user_id BIGINT,
            channel_id BIGINT,
            role_id BIGINT NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT Now(),
            updated_at TIMESTAMPTZ DEFAULT Now(),
            PRIMARY KEY (user_id, channel_id),
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON UPDATE CASCADE,
            FOREIGN KEY (channel_id)
                REFERENCES channels(id)
                ON UPDATE CASCADE,
            FOREIGN KEY (role_id)
                REFERENCES roles(id)
                ON UPDATE CASCADE
        );
    ''')
    print("Database INIT: Done")


asyncio.run(main())
