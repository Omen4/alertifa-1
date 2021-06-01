import asyncio


ADDRESS = '127.0.0.1'


async def main():
    reader, writer = await asyncio.open_connection(ADDRESS, 9000)
    writer.write(b"TEST" * 16)
    await writer.drain()

asyncio.run(main())
