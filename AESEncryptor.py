import pyaes


class AESModeCTR:
    def __init__(self, key, iv):
        assert isinstance(key, bytes)
        self._aes = pyaes.AESModeOfOperationCTR(key)

        assert isinstance(iv, bytes)
        assert len(iv) == 16
        self._aes._counter._counter = list(iv)

    def encrypt(self, data):
        return self._aes.encrypt(data)

    def decrypt(self, data):
        return self._aes.decrypt(data)

