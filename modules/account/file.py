import os
from modules.crypto import FILE
from modules.types.customer import *
from modules.crypto import AES
from modules.config import logger 

def check_file_large(filename: str):
    return os.path.getsize(filename) > 1024 * 1024 * 5 # 5MB

def read(filename: str):
    with open(filename, 'rb') as f:
        size_bytes = 1000000 # bytes
        if not check_file_large(filename):
            size_bytes = -1
        
        file_data: DataFile = []
        while True:
            data = f.read(size_bytes)
            if not data: break
            file_data.append(data)

    return file_data

def send(filename: str, public_key: Base64Str):
    data_file = read(filename)
    data_enc, data_key_enc = FILE.encrypt(data_file, public_key)
    return data_enc, data_key_enc


def receive(data_enc: list[Base64Str], data_key_enc: str, private_key_password_enc: Base64Str, password: str):
    private_key = AES.decrypt(password.encode(), private_key_password_enc)
    private_key = Base64Str.from_string(private_key)
    
    logger.security.info('AES giải mã private key bằng password - thành công')
    
    original_data = FILE.decrypt(data_enc, data_key_enc, private_key)
    return original_data

