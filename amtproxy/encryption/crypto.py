from hashlib import sha256

from .aes import AES_CTR


class DecryptionKey:
    def __init__(self, key, secret):
        dec_key = sha256()
        dec_key.update(key)
        dec_key.update(secret)
        self.key = dec_key.digest()

    def __call__(self):
        return self.key


class EncryptionKey:
    def __init__(self, key, secret):
        enc_key = sha256()
        enc_key.update(key)
        enc_key.update(secret)
        self.key = enc_key.digest()

    def __call__(self):
        return self.key


class Decryptor:
    def __init__(self, raw_bytes, secret):
        self.secret = bytes.fromhex(secret)
        self.decryption_key = DecryptionKey(raw_bytes[8:40], self.secret)
        self.aes = AES_CTR(self.decryption_key(), raw_bytes[40:56])

    async def __call__(self, data):
        return await self.aes.decrypt(data)


class Encryptor:
    def __init__(self, raw_bytes, secret):
        self.secret = bytes.fromhex(secret)
        self.encryption_key = EncryptionKey(raw_bytes[8:56][::-1][0:32], self.secret)
        self.aes = AES_CTR(self.encryption_key(), raw_bytes[8:56][::-1][32:48])

    async def __call__(self, data):
        return await self.aes.encrypt(data)
