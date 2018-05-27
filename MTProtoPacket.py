from hashlib import sha256
import numpy
from AesEncryptor import AESencryptor

class MTProxy():
    class MTProtoPacket():
        def __init__(self):
            self.encryptCountBuf = bytearray()
            self.decryptCountBuf = bytearray()
            self.encryptNum = 0
            self.decryptNum = 0

        class ProtocolType():
            none = 0
            AbridgedObfuscated2 = 1
            IntermediateObfuscated2 = 2

        def EncryptObfuscated2(self,data,length):
            return self.AesCtr128Encrypt(data,length)

        def DecryptObfuscated2(self,buffer, length):
            return self.AesCtr128Decrypt(buffer, length)

        def AesCtr128Encrypt(self,buffer,length):
            output = bytearray(length=length)
            for i in range(length):
                if self.encryptNum == 0:
                    ecountBuf = 'aa' ###TODO ADD NUMPY LAST BLOCK TRANSFORMATION
                    self.ivec = reversed(self.ivec)
                    bigInteger = int(numpy.concatenate,bytearray({ 0x00 })) +1
                    bigIntegerArray = bytearray(bigInteger)
                    self.ivec = bigIntegerArray[0:min(len(self.ivec),len(bigIntegerArray))]
                    self.ivec = reversed(self.ivec)
                output[i] = bytearray(buffer[i] ^ self.encryptCountBuf[self.encryptNum])
                number = (self.encryptNum + 1) % 16;
            return output

        def AesCtr128Decrypt(self,buffer,length):
            output = bytearray (length=length)
            for i in range (length):
                if self.decryptNum == 0:
                    ecountBuf = 'aa' ###TODO ADD NUMPY LAST BLOCK TRANSFORMATION
                    ivdc = reversed (self.ivdc)
                    bigInteger = int (numpy.concatenate, bytearray ({0x00})) + 1
                    bigIntegerArray = bytearray (bigInteger)
                    self.ivdc = bigIntegerArray[0:min (len (self.ivdc), len (bigIntegerArray))]
                    self.ivdc = reversed (self.ivdc)
                output[i] = bytearray (buffer[i] ^ self.decryptCountBuf[self.decryptNum])
                number = (self.decryptNum + 1) % 16;
            return output

        def SetInitBufferObfuscated2(self, buffer, secret):
            reversed_buffer = buffer[8:48]
            reversed_buffer = reversed (reversed_buffer)
            key = buffer[8:32]
            key_reversed = reversed_buffer[0:32]
            hex_secret = bytearray.fromhex (secret.decode ("hex"))
            key = sha256 (numpy.concatenate(key,hex_secret))
            key_reversed = sha256(numpy.concatenate(key_reversed,hex_secret))

            self.encrypt_key = key_reversed
            self.encryptIv = reversed_buffer[32:16]
            self.decrypt_key = key
            self.decryptIv = buffer[40:16]

            self.cryptoTransformEncrypt = AESencryptor(key=self.encrypt_key)
            self.cryptoTransformDecrypt = AESencryptor(key=self.decrypt_key)

            decrypted_buffer = self.DecryptObfuscated2(buffer, len(buffer))
            for i in range(len(decrypted_buffer)):
                if i > 55:
                    continue
                buffer[i] = decrypted_buffer[i]

            protocol_result = buffer[56:-4]
            if protocol_result[0] == 0xef and\
               protocol_result[1] == 0xef and\
               protocol_result[2] == 0xef and\
               protocol_result[3] == 0xef:
                self.protocol_type = self.ProtocolType.AbridgedObfuscated2
            elif protocol_result[0] == 0xee and\
                 protocol_result[1] == 0xee and\
                 protocol_result[2] == 0xee and\
                 protocol_result[3] == 0xee:
                self.protocol_type = self.ProtocolType.IntermediateObfuscated2
            else:
                self.protocol_type = self.ProtocolType.none

        def GetInitBufferObfuscated2(self,protocol_type):
            self.protocol_type = protocol_type
            buffer = bytearray(length=64)
            done = False
            while not done:
                buffer = numpy.random.random(64)
                val = (buffer[3] << 24) | (buffer[2] << 16) | (buffer[1] << 8) | (buffer[0])
                val2 = (buffer[7] << 24) | (buffer[6] << 16) | (buffer[5] << 8) | (buffer[4])
                if buffer[0] != 0xef and val != 0x44414548 and val != 0x54534f50 and val != 0x20544547 and val != 0x4954504f and val2 != 0x00000000:
                    if protocol_type == 1:
                        buffer[56] = buffer[57] = buffer[58] = buffer[59] = 0xef
                        done = True
                    if protocol_type == 2:
                        buffer[56] = buffer[57] = buffer[58] = buffer[59] = 0xee
                        done = True
                    if protocol_type == 0:
                        return None
                break
            keyIvEncrypt = buffer[8:48]
            self.encryptKey = keyIvEncrypt[0:32]
            self.encryptIv = keyIvEncrypt[32:16]

            keyIvEncrypt = reversed(keyIvEncrypt)
            self.decryptKey = keyIvEncrypt[0:32]
            self.decryptIv = keyIvEncrypt[32:16]

            self.cryptoTransformEncrypt = AESencryptor(self.encryptKey)
            self.cryptoTransformDecrypt = AESencryptor(self.decryptKey)

            encrypted_buffer = self.EncryptObfuscated2(buffer, len(buffer))
            for i in range(len(encrypted_buffer)):
                if i > 55:
                    continue
                buffer[i] = encrypted_buffer[i]
            return buffer




