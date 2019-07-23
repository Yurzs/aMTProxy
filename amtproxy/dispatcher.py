from amtproxy.encryption.crypto import Encryptor, Decryptor
from amtproxy.config import secret, telegram_ips, mtproto_footprint, obf_footprint
from amtproxy.exceptions import WrongServerID
from amtproxy.protocols.telegram import TelegramProtocol


class Dispatcher:
    def __init__(self, loop, real_protocol):
        self.loop = loop
        self.real_protocol = real_protocol
        self.telegram_protocol = None
        self.telegram_transport = None
        self.encryptor = None
        self.decryptor = None

    async def handle(self, raw_data: bytes):
        if not self.encryptor or not self.decryptor:
            self.decryptor = Decryptor(raw_data, secret)
            self.encryptor = Encryptor(raw_data, secret)
            self.decoded_data = await self.decryptor(raw_data)
            server_id = int.from_bytes(self.decoded_data[60:62], 'little') - 1
            if server_id < 0 or server_id > len(telegram_ips):
                raise WrongServerID(f'Got id {server_id}')
            self.telegram_server_ip = telegram_ips[server_id]
            assert self.decoded_data[56:60] == mtproto_footprint or self.decoded_data[56:60] == obf_footprint, self.decoded_data[56:60]
        if not self.telegram_protocol or not self.telegram_transport:
            self.telegram_transport, self.telegram_protocol = await self.loop.create_connection(lambda: TelegramProtocol(self.loop, self),
                self.telegram_server_ip, 443)
            self.telegram_transport.write(self.decoded_data)
            return
        self.telegram_transport.write(await self.decryptor(raw_data))

    async def reverse_handle(self, raw_data):
        self.real_protocol.transport.write(await self.encryptor(raw_data))