import logging
import socket
from MTProtoPacket import MTProxy
from config import Config
import select

secret = '11111'


class MTProtoProxyServer():
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('10.8.0.4', 8445))
            self.sock.listen(1)
            while True:
                (clientsocket, address) = self.sock.accept ()
                Clients(clientsocket)
        else:
            self.sock = sock


class TelegramSocket:
    def __init__(self):
        self.sock = socket.socket (
            socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

class Clients:
    def __init__(self,user_socket):
        connected = True
        telegram = TelegramSocket ()
        telegram.connect ('149.154.175.50', Config.TelegramPort)
        while connected:
            ready_user = select.select ([user_socket], [], [], 0.5)
            ready_telegram = select.select ([telegram.sock], [], [], 0.5)
            if ready_user[0]:
                data_from_client = user_socket.recv (4096)
                print ('Data from user')
                print(data_from_client)
            if ready_telegram[0]:
                data_from_telegram = telegram.sock.recv(4096)
                print('Data from telegram')
                print(data_from_telegram)
            if not ready_telegram[0] and ready_user[0]:
                continue
            if not data_from_client:
                if not data_from_telegram:
                    continue
                else:
                    print(data_from_telegram)
                    raw_data = MTProxy.MTProtoPacket.serverside_deobfuscated2(self=None,
                                                                              enc_data=data_from_telegram)
                    print('RAW telegram data')
                    print(raw_data)
                    encrypted_data = MTProxy.MTProtoPacket.serverside_obfuscated2(self=None,
                                                                                  raw_data=raw_data,
                                                                                  secret=secret)
                    user_socket.send(encrypted_data)
                    print ('Sent this to telegram')
                    print(encrypted_data)
                    ready_telegram = [False]

            else:
                raw_data = MTProxy.MTProtoPacket.serverside_deobfuscated2(self=None,
                                                                          enc_data=data_from_client,
                                                                          secret=secret)
                print ('RAW telegram data')
                print (raw_data)
                encrypted_data = MTProxy.MTProtoPacket.serverside_obfuscated2(self=None,
                                                                     raw_data=raw_data)
                telegram.sock.send(encrypted_data)
                print('Sent this to client')
                print(encrypted_data)
                ready_user = [False]


server = MTProtoProxyServer()
