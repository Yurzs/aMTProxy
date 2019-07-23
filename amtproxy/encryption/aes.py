import pyaes


class AES_CTR:
    def __init__(self, key, iv):
        assert isinstance(key, bytes), 'Key should be instance of bytes'
        self._aes = pyaes.AESModeOfOperationCTR(key)
        assert isinstance(iv, bytes), 'IV should be instance of bytes'
        assert len(iv) == 16, 'IV length must be 16 bytes'
        self._aes._counter._counter = list(iv)

    async def encrypt(self, data):
        return self._aes.encrypt(data)

    async def decrypt(self, data):
        return self._aes.decrypt(data)
