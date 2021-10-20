from Cryptodome.Cipher import AES 
 
def get_xor_result(v1, v2):
    return bytes(a ^ b for (a, b) in zip(v1, v2))

class CFB_mode:
    def __init__(self, iv, k):
        self.initialization_vector = iv
        self.key = k
    def encrypt(self, plaintext):
        ciphertext = b''
        iv = self.initialization_vector
        while plaintext:
            block = plaintext[0:16]
            block = block + b'\0' * (16 - len(block))
            plaintext = plaintext[16:]
            cipher = AES.new(self.key, AES.MODE_ECB)
            enc_block = cipher.encrypt(iv)
            enc_block = get_xor_result(enc_block, block)
            ciphertext += enc_block
            iv = enc_block
        return ciphertext
    
    def decrypt(self, ciphertext):
        plaintext = b''
        iv = self.initialization_vector
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]
            cipher = AES.new(self.key, AES.MODE_ECB)
            dec_block = cipher.encrypt(iv)
            dec_block = get_xor_result(dec_block, block)
            plaintext += dec_block
            iv = block
        return plaintext
 