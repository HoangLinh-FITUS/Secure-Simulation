from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from . import RSA, SHA_256
from modules.types.customer import *

def generate_key(private_key: Base64Str, data: bytes) -> bytes:
    key = RSA.export_key(private_key)
    h = SHA256.new(data)
    return pkcs1_15.new(key).sign(h)

def verify(public_key: Base64Str, data: bytes, signature: bytes) -> bool:
    key = RSA.export_key(public_key)
    h = SHA256.new(data)
    
    try:
        pkcs1_15.new(key).verify(h, signature)
        print("The signature is valid.")
        return True
    except (ValueError, TypeError):
        print("The signature is not valid.")
        return False


if __name__ == "__main__":
    
    private_key, public_key = RSA.generate_key(2048)

    with open('test/file/small.pdf', 'rb') as f:
        data = f.read()

    with open('sign.sig', 'wb') as f:
        f.write(generate_key(private_key, data))

    with open('sign.sig', 'rb') as f:
        signature = f.read()
        verify(public_key, data, signature)
