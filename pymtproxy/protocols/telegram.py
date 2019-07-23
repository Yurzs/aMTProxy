import asyncio


class TelegramProtocol(asyncio.Protocol):
    
    def __init__(self, loop, dispatcher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = loop
        self.dispatcher = dispatcher

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        task = asyncio.Task(self.async_handler(data), loop=self.loop)

    @asyncio.coroutine
    def async_handler(self, data):
        return (yield from self.dispatcher.reverse_handle(data))

    def connection_lost(self, exc) -> None:
        self.dispatcher.real_protocol.close_connection()