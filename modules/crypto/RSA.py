from modules.types.customer import *
from Crypto.PublicKey import RSA 
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Cipher import PKCS1_OAEP
from typing import Tuple 

def generate_key(len_bit: int) -> Tuple[Base64Str, Base64Str]:
    key = RSA.generate(len_bit)
    private_key = key
    public_key = key.publickey()
    return Base64Str(private_key.export_key()), \
           Base64Str(public_key.export_key())

def encrypt(public_key: Base64Str, plaintext: str) -> Base64Str:
    public_key: RsaKey = RSA.import_key(public_key.decode())

    plaintext = plaintext.encode()
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted = cipher_rsa.encrypt(plaintext)
    return Base64Str(encrypted)
    
def decrypt(private_key: Base64Str, ciphertext: Base64Str) -> str:
    private_key: RsaKey = RSA.import_key(private_key.decode())

    ciphertext: bytes = ciphertext.decode()
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted = cipher_rsa.decrypt(ciphertext)
    return decrypted.decode()

def export_key(key: Base64Str) -> RsaKey:
    return RSA.import_key(key.decode())
    
if __name__ == '__main__':
    private_key, public_key = generate_key(2048)

    enc = encrypt(public_key, 'nguyễn văn an')
    print('[ENCRYPT]: ', enc)
    print(decrypt(private_key, enc))