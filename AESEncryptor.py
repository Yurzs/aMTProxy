from Crypto.Cipher import AES


class AESencryptorCTR:
    def __init__(self, key,iv,counter,number):
        self.key = key
        self.iv = iv
        self.cnter_cb_called = 0
        self.counter = counter
        self.number = number

    def encrypt(self, raw):
        cipher = AES.new (self.key, AES.MODE_CTR, counter=lambda :self.iv)
        return cipher.encrypt (raw)

    def decrypt(self, enc):
        cipher = AES.new (self.key, AES.MODE_CTR, counter=lambda :self.iv)
        return cipher.decrypt (enc)

