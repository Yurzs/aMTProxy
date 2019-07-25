import asyncio

from .protocols.real import RealProtocol


async def main(port=8080, secret='1234567890abc1234567890abcef1234'):
    loop = asyncio.get_running_loop()
    print(f'MTProxy is starting on port {port}\nWith secret {secret}')
    server = await loop.create_server(
        lambda: RealProtocol(loop, secret),
        '0.0.0.0', port)

    async with server:
        await server.serve_forever()


def start_server(port=None, secret=None):
    args = {'port': port, 'secret': secret}
    asyncio.run(main(**{k: v for k, v in args.items() if v}))


if __name__ == '__main__':
    asyncio.run(main())
