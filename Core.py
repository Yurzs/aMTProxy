import logging
import socket
from MTProtoPacket import MTProxy
from time import time
from collections import deque
import asyncio

SECRET = '4b3e3c2f99046f92a61bab6775848577'

class MTProtoproxy:
    class Server:
        def __init__(self):
            loop = asyncio.get_event_loop()
            client = MTProtoproxy.Client()
            task = asyncio.start_server( client.client_connector,
                                        "0.0.0.0", 8445, loop=loop)
            server = loop.run_until_complete(task)

            try:
                loop.run_forever()
            except KeyboardInterrupt:
                pass

            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()

    class Client:
        async def client_connector(self,reader,writer):
            try:
                await self.loop(reader, writer)
            except (asyncio.IncompleteReadError, ConnectionResetError):
                writer.close()

        async def sockets_connector(self,reader,writer,decryptor,encryptor):
            try:
                while True:
                    data = reader.read()
                    if not data:
                        writer.write_eof()
                        await writer.drain()
                        writer.close()
                        raise Exception
                    else:
                        dec_data = decryptor.decrypt(data)
                        data = encryptor.encrypt(dec_data)
                        writer.write(data)
                        await writer.drain()
            except (ConnectionResetError, BrokenPipeError, OSError,
                    AttributeError):
                writer.close()
            except Exception:
                return

        async def loop(self, cli_reader, cli_writer):
            cli_data = await MTProxy.MTProtoPacket.from_client_to_telegram(self = None,
                                                                           enc_data=await cli_reader.read(),
                                                                           secret=SECRET)
            if not cli_data:
                cli_writer.close()
                raise Exception

            dc, cli_decryptor, cli_encryptor = cli_data

            tg_data = await MTProxy.MTProtoPacket.from_telegram_to_client(self=None,
                                                                          dc=dc,
                                                                          secret=SECRET)
            if not tg_data:
                cli_writer.close()

            tg_encryptor, tg_decryptor, tg_reader, tg_writer = tg_data

            asyncio.ensure_future(self.sockets_connector(tg_reader, cli_writer, tg_decryptor, cli_encryptor))
            asyncio.ensure_future(self.sockets_connector(cli_reader, tg_writer, cli_decryptor, tg_encryptor))

if __name__ == "__main__":
    MTProtoproxy.Server()
