import asyncio
from ..dispatcher import Dispatcher


class RealProtocol(asyncio.Protocol):
    transport: asyncio.transports.BaseTransport
    task: asyncio.Task = None

    def __init__(self, loop, secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = loop
        self.dispatcher = Dispatcher(loop, self, secret)

    def connection_made(self, transport):
        self.transport = transport


    def data_received(self, data):
        self.task = asyncio.Task(self.async_handler(data), loop=self.loop)


    @asyncio.coroutine
    def async_handler(self, data):
        return (yield from self.dispatcher.handle(data))

    def connection_lost(self, exc) -> None:
        if self.task:
            self.task.cancel()
        try:
            self.dispatcher.telegram_transport.close()
        except AttributeError:
            pass

    def close_connection(self):
        self.transport.close()
