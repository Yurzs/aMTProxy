import asyncio
from protocols import RealProtocol


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: RealProtocol(loop),
        '0.0.0.0', 8080)

    async with server:
        await server.serve_forever()

asyncio.run(main())

