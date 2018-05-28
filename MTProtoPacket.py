from AESEncryptor import AESModeCTR
import os
from hashlib import sha256
import numpy
import hexdump

class MTProxy:
    class MTProtoPacket:
        def __init__(self):
            pass

        def to_client_obfuscated2(self, raw_data, secret):
            obf_enc_key_bytes = bytes(os.urandom(64))
            obf_enc_key = obf_enc_key_bytes[8:40]  # 8 - 39 bytes [32]
            obf_enc_iv = obf_enc_key_bytes[40:56]  # 40 - 55 bytes [16]
            secret = bytes.fromhex(secret)
            dec_key = sha256 ()
            dec_key.update (obf_enc_key)
            dec_key.update (secret)
            obf_enc_key = dec_key.digest ()
            encryptor = AESModeCTR(key=obf_enc_key,
                                   iv=obf_enc_iv)
            enc_data = encryptor.encrypt(raw_data)
            return enc_data

        def from_client_deobfuscated2(self, enc_data, secret):
            obf_dec_key_bytes = bytes(enc_data[0:64])
            obf_dec_key = obf_dec_key_bytes[8:40]  # 8 - 39 bytes [32]
            obf_dec_iv = obf_dec_key_bytes[40:56]  # 40 - 55 bytes [16]
            secret = bytes.fromhex(secret)
            dec_key = sha256()
            dec_key.update(obf_dec_key)
            dec_key.update(secret)
            obf_dec_key = dec_key.digest()
            encryptor = AESModeCTR (key=obf_dec_key,
                                    iv=obf_dec_iv)
            raw_data = encryptor.decrypt(enc_data)
            return raw_data

        def from_telegram_deobfuscated2(self, enc_data):
            obf_dec_key_bytes = bytes(enc_data[0:48])[::-1]  # reversed
            obf_dec_key = obf_dec_key_bytes[0:32]  # 0 - 32 bytes [32]
            obf_dec_iv = obf_dec_key_bytes[32:48]  # 32 - 48 bytes [16]
            encryptor = AESModeCTR(key=obf_dec_key,
                                   iv=obf_dec_iv)
            raw_data = encryptor.decrypt(enc_data)
            return raw_data

        def to_telegram_obfuscated2(self, raw_data):
            obf_enc_key_bytes = os.urandom(64)
            obf_enc_key = obf_enc_key_bytes[8:40]  # 8 - 40 bytes [32]
            obf_enc_iv = obf_enc_key_bytes[40:56]  # 40 - 56 bytes [16]
            encryptor = AESModeCTR (key=obf_enc_key,
                                    iv=obf_enc_iv)
            enc_data = encryptor.encrypt(raw_data)
            return enc_data


