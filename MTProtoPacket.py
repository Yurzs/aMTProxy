from hashlib import sha256
import numpy
from AESEncryptor import AESencryptor,AESencryptorCTR
import os


class MTProxy:
    class MTProtoPacket:
        def __init__(self):
            pass

        def obfuscated2(self,raw_data):
            obf_enc_key_bytes = os.urandom(64)
            obf_enc_key = obf_enc_key_bytes[7:39]  # 8 - 39 bytes [32]
            obf_enc_iv = obf_enc_key_bytes[39:55]  # 40 - 55 bytes [16]
            encryptor = AESencryptorCTR(key=obf_enc_key,
                                        iv=obf_enc_iv,
                                        counter=0,
                                        number=0)
            enc_data = encryptor.encrypt(raw_data)

            return obf_enc_key_bytes + enc_data

        def deobfuscated2(self,enc_data):
            obf_dec_key_bytes = bytes(enc_data[0:64])[::-1]
            obf_dec_key = obf_dec_key_bytes[7:39]  # 8 - 39 bytes [32]
            obf_dec_iv = obf_dec_key_bytes[39:55]  # 40 - 55 bytes [16]
            encryptor = AESencryptorCTR (key=obf_dec_key,
                                         iv=obf_dec_iv,
                                         counter=0,
                                         number=0)
            raw_data = encryptor.decrypt(enc_data[64:])
            return raw_data

        def serverside_deobfuscated2(self, enc_data):
            obf_dec_key = enc_data[7:39]  # 8 - 39 bytes [32]
            obf_dec_iv = enc_data[39:55]  # 40 - 55 bytes [16]
            encryptor = AESencryptorCTR(key=obf_dec_key,
                                        iv=obf_dec_iv,
                                        counter=0,
                                        number=0)
            raw_data = encryptor.decrypt(enc_data[64:])
            return raw_data

        def serverside_obfuscated2(self, raw_data):
            obf_enc_key_bytes = os.urandom (64)
            obf_enc_key = (obf_enc_key_bytes[7:39])  # 8 - 39 bytes [32]
            obf_enc_iv = (obf_enc_key_bytes[39:55])
            obf_enc_key_bytes = obf_enc_key_bytes[::-1]

            encryptor = AESencryptorCTR (key=obf_enc_key,
                                         iv=obf_enc_iv,
                                         counter=0,
                                         number=0)
            enc_data = encryptor.encrypt (raw_data)

            return obf_enc_key_bytes + enc_data
