import asyncio
from asyncio.transports import BaseTransport


class TelegramProtocol(asyncio.Protocol):
    transport: BaseTransport
    task: asyncio.Task = None

    def __init__(self, loop, dispatcher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = loop
        self.dispatcher = dispatcher

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.task = asyncio.Task(self.async_handler(data), loop=self.loop)

    @asyncio.coroutine
    def async_handler(self, data):
        return (yield from self.dispatcher.reverse_handle(data))

    def connection_lost(self, exc) -> None:
        if self.task:
            self.task.cancel()
        self.dispatcher.real_protocol.close_connection()
