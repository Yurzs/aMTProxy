import asyncio
from amtproxy.protocols import RealProtocol


async def main(port=8080):
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: RealProtocol(loop),
        '0.0.0.0', port)

    async with server:
        await server.serve_forever()


def start(port=None):
    asyncio.run(main(port))


if __name__ == '__main__':
    asyncio.run(main())

