from modules.types.customer import *
import hashlib 
import uuid

def hash_text(plaintext: str) -> Base64Str: 
    salt = uuid.uuid4().hex
    hash = hashlib.sha256(salt.encode() + plaintext.encode()).hexdigest() + ":" + salt
    return Base64Str(hash)

def verify(ciphertext: Base64Str, plaintext: str):
    hash, salt = (ciphertext.decode().decode()).split(':')
    return hashlib.sha256(salt.encode() + plaintext.encode()).hexdigest() == hash
