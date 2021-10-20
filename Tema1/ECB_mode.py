from Cryptodome.Cipher import AES
 
class ECB_mode:
    def __init__(self, k):
        self.key = k

    def encrypt(self, plaintext):
        ciphertext = b''
        while plaintext:
            block = plaintext[0:16]
            block = block + b'\0' * (16 - len(block))  # padding if necessary
            plaintext = plaintext[16:]
            cipher = AES.new(self.key, AES.MODE_ECB)
            enc_block = cipher.encrypt(block)
            ciphertext += enc_block
        return ciphertext
    
    def decrypt(self, ciphertext):
        plaintext = b''
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]
            cipher = AES.new(self.key, AES.MODE_ECB)
            dec_block = cipher.decrypt(block)
            plaintext += dec_block
        return plaintext
 