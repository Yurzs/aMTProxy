import logging
import socket
from MTProtoPacket import MTProxy
from config import Config
import select
import hexdump
secret = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'


class MTProtoProxyServer():
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('192.168.1.3', 8445))
            self.sock.listen(1)
            while True:
                (clientsocket, address) = self.sock.accept ()
                Clients(clientsocket)
        else:
            self.sock = sock


class TelegramSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

class Clients:
    def __init__(self,user_socket):
        connected = True
        telegram = TelegramSocket ()
        telegram.connect('149.154.175.100', Config.telegramPort)
        while connected:
            ready_user = select.select([user_socket], [], [], 0.25)
            ready_telegram = select.select([telegram.sock], [], [], 0.25)
            if ready_user[0]:
                data_from_client = user_socket.recv (4096)
                if data_from_client == b'':
                    user_socket.close()
                    connected = False
                    break
            elif ready_telegram[0]:
                data_from_telegram = telegram.sock.recv(4096)
            if not ready_telegram[0] and ready_user[0]:
                continue
            if not data_from_client:
                if not data_from_telegram:
                    break
                else:
                    print('Recieved from telegram')
                    print(data_from_telegram)
                    print(hexdump.hexdump(data_from_telegram))
                    raw_data = MTProxy.MTProtoPacket.from_telegram_deobfuscated2(self=None,
                                                                              enc_data=data_from_telegram)
                    print('RAW telegram data')
                    print(raw_data[55:60])
                    print(hexdump.hexdump(raw_data))
                    encrypted_data = MTProxy.MTProtoPacket.to_client_obfuscated2(self=None,
                                                                                  raw_data=raw_data,
                                                                                  secret=secret)
                    user_socket.send(encrypted_data)
                    print('Sent this to client')
                    print(hexdump.hexdump(encrypted_data))
                    print(len(encrypted_data))
                    ready_telegram = [False]

            else:
                print('Recieved from client')
                raw_data = MTProxy.MTProtoPacket.from_client_deobfuscated2(self=None,
                                                               enc_data=data_from_client,
                                                               secret=secret)
                print('RAW client data')
                print(hexdump.hexdump(raw_data))
                encrypted_data = MTProxy.MTProtoPacket.to_telegram_obfuscated2(self=None,
                                                                              raw_data=raw_data)
                print(telegram.sock.send(encrypted_data))
                print('Sent this to telegram')
                print(len(encrypted_data))
                print(hexdump.hexdump (encrypted_data))
                ready_user = [False]


server = MTProtoProxyServer()
