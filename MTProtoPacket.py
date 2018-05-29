from hashlib import sha256
from AESEncryptor import AESModeCTR
from config import Config
import random
import asyncio

TG_DC = [
    "149.154.175.50", "149.154.167.51", "149.154.175.100",
    "149.154.167.91", "149.154.171.5"
]


class MTProxy:
    class MTProtoPacket:

        async def from_client_to_telegram(self, enc_data, secret):
            obf_dec_key_bytes = bytes(enc_data[0:64])
            obf_dec_key = obf_dec_key_bytes[8:40]  # 8 - 39 bytes [32]
            obf_dec_iv = obf_dec_key_bytes[40:56]  # 40 - 55 bytes [16]
            secret = bytes.fromhex(secret)
            dec_key = sha256()
            dec_key.update(obf_dec_key)
            dec_key.update(secret)
            obf_dec_key = dec_key.digest()
            decryptor = AESModeCTR(key=obf_dec_key,
                                   iv=obf_dec_iv)

            obf_enc_key_bytes = bytes(enc_data[8:56])[::-1]
            obf_enc_key = obf_dec_key_bytes[0:32]
            obf_enc_iv = obf_dec_key_bytes[32:48]
            enc_key = sha256()
            enc_key.update(obf_enc_key)
            enc_key.update(secret)
            obf_enc_key = enc_key.digest()
            encryptor = AESModeCTR(key=obf_enc_key,
                                   iv=obf_enc_iv)

            raw_data = decryptor.decrypt (enc_data)

            dc_idx = int.from_bytes (raw_data[60:62], "little") - 1
            if dc_idx < 0 or dc_idx >= len(TG_DC):
                raise Exception
            dc = TG_DC[dc_idx]
            if b'\xef\xef\xef\xef' == raw_data[56:60]:
                return dc, decryptor, encryptor
            else:
                raise Exception

        async def from_telegram_to_client(self,dc,secret):
            tg_reader, tg_writer = await asyncio.open_connection(dc, TG_DC)

            obf_dec_key_bytes = bytearray([random.randrange(0, 256) for i in range(64)])
            obf_dec_key_bytes[56] = obf_dec_key_bytes[57] = obf_dec_key_bytes[58] = obf_dec_key_bytes[59] = 0xef
            obf_dec_key_iv = bytes (obf_dec_key_bytes[8:56])[::-1]
            obf_dec_key = obf_dec_key_iv[0:32]
            obf_dec_iv = obf_dec_key_iv[32:48]
            decryptor = AESModeCTR(key=obf_dec_key,
                                   iv=obf_dec_iv)

            obf_enc_key_bytes = bytes (obf_dec_key_bytes)[::-1]
            obf_enc_key = obf_enc_key_bytes[8:40]  # 8 - 39 bytes [32]
            obf_enc_iv = obf_enc_key_bytes[40:56]  # 40 - 55 bytes [16]
            secret = bytes.fromhex (secret)
            enc_key = sha256 ()
            enc_key.update(obf_enc_key)
            enc_key.update(secret)
            obf_enc_key = enc_key.digest ()
            encryptor = AESModeCTR(key=obf_enc_key,
                                   iv=obf_enc_iv)
            enc_data = obf_dec_key_bytes[:56] + encryptor.encrypt(bytes(obf_dec_key_bytes))[56:]

            tg_writer.write(enc_data)
            await tg_writer.drain()

            return encryptor, decryptor, tg_reader, tg_writer
