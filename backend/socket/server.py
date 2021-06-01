import logging
import asyncio

import asyncpg


LOG_FILE = '/logs/socket.log'
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)

HOST = '172.17.0.1'
PORT = 5432
USERNAME = "admin"
PASSWORD = "iP}hg*$0tIX8"
DATABASE_NAME = "alertifa"


async def handle_client(reader: asyncio.StreamReader,
                        writer: asyncio.StreamWriter) -> None:
    message = await reader.readexactly(64)
    conn = await asyncpg.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE_NAME
    )
    rows = await conn.fetch('''
        SELECT * FROM channels;
    ''')
    for i in rows:
        print(i)
    # with open("/logs/result.txt", "a") as file:
    #     file.write(message.decode('utf-8'))
    # print(message)

async def main():
    logging.info("Connected")
    server = await asyncio.start_server(
        handle_client, '0.0.0.0', 9000
    )
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main() )
