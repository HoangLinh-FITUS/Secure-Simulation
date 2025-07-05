from modules.types.customer import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(data: bytes) -> bytes:
    padding_length = 16 - len(data) % 16
    padding = bytes([padding_length] * padding_length)
    return data + padding

def encrypt(key_AES: bytes, plaintext: str) -> Base64Str:

    key_AES = pad(key_AES)
    cipher  = AES.new(key_AES, AES.MODE_GCM)

    nonce = cipher.nonce 
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())

    return Base64Str(
        ciphertext.hex() + ":" + tag.hex() + ":" + nonce.hex()
    )

def decrypt(key_AES: bytes, ciphertext: Base64Str) -> tuple[str, bool]:
    ciphertext = ciphertext.decode().decode()
    key_AES = pad(key_AES)
    
    ciphertext, tag, nonce = map(bytes.fromhex, ciphertext.split(':'))

    cipher_key = AES.new(key_AES, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher_key.decrypt(ciphertext)

    try:
        cipher_key.verify(tag)
        return plaintext.decode('utf-8')
    except ValueError:
        raise Exception('khong giai ma dc')


