from modules.types.customer import *
from modules.crypto import AES, RSA
from Crypto.Random import get_random_bytes
from modules.account.file import *
from modules.config import logger 

def encrypt(file: DataFile, public_key: Base64Str) -> tuple[list[Base64Str], Base64Str]:
 
    aes_key = get_random_bytes(16)
    key_enc = RSA.encrypt(public_key, aes_key.hex())
    logger.security.info('Mã hóa AES_KEY bằng public key - thành công')
    
    data_enc = []
    for i, block_i in enumerate(file):
        try:
            enc = AES.encrypt(aes_key, block_i.hex())
            logger.security.info('Mã hóa từng block thứ {} của file bằng AES - thành công'.format(i))
        except:
            logger.security.warning('Mã hóa từng block thứ {} của file bằng AES - thất bại'.format(i))

        data_enc.append(enc)
    
    
    return data_enc, key_enc

def decrypt(file_enc: list[Base64Str], aes_key_enc: str, private_key: Base64Str) -> bytes:
    
    aes_key_enc      = RSA.decrypt(private_key, aes_key_enc)
    aes_key_enc      = bytes.fromhex(aes_key_enc)

    logger.security.info('giải mã AES_KEY bằng private key - thành công')
    
    file = ""
    for i, block_i in enumerate(file_enc):
        try:
            f = AES.decrypt(aes_key_enc, block_i)
            logger.security.info('giải mã block thứ {} của file bằng AES - thành công'.format(i))
        except:
            logger.security.warning('giải mã block thứ {} của file bằng AES - thất bại'.format(i))
        file += f


    return bytes.fromhex(file)


