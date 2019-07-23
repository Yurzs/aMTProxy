import asyncio
from amtproxy.dispatcher import Dispatcher


class RealProtocol(asyncio.Protocol):
    def __init__(self, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = loop
        self.dispatcher = Dispatcher(loop, self)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        task = asyncio.Task(self.async_handler(data), loop=self.loop)


    @asyncio.coroutine
    def async_handler(self, data):
        return (yield from self.dispatcher.handle(data))

    def connection_lost(self, exc) -> None:
        try:
            self.dispatcher.telegram_transport.close()
        except AttributeError:
            pass

    def close_connection(self):
        self.transport.close()