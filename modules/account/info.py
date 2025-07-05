import datetime

from modules.crypto import RSA, AES, SHA_256
from modules.database import user_keys as user_keys_db, users as users_db
from modules.config import settings
from modules.database.db_manager import * 
from modules.types.customer import *
from modules.auth import controller
from modules.config import logger 


def insert_key(email: str, password: str, pin: str):
    private_key, public_key = RSA.generate_key(settings.LEN_KEY)
    logger.security.info(f'{email} - RSA sinh private key vs public key - thành công')

    try:
        encrypt_private_key_pwd_AES = AES.encrypt(password.encode(), private_key)
        logger.security.info(f'{email} - AES Mã hóa private key bằng password - thành công')
    except:
        logger.security.warning(f'{email} AES Mã hóa private key bằng password - thất bại')

    try:
        encrypt_private_key_pin_AES = AES.encrypt(pin.encode(), private_key)
        logger.security.info(f'{email} - AES Mã hóa private key bằng mã khôi phục - thành công')
    except:
        logger.security.warning(f'{email} - AES Mã hóa private key bằng mã khôi phục - thất bại')

    user_keys_db.insert(
        user_keys_db.Data(
            email                   = email,
            public_key              = public_key,
            private_key_password    = encrypt_private_key_pwd_AES,
            private_key_recovery    = encrypt_private_key_pin_AES,
            ngay_tao                = datetime.datetime.now().strftime('%c')
        )
    )

def change_key(email: str, password: str, pin: str):
    auth = controller.AuthController(email, password)
    
    if not auth.check_account():            raise Exception('Sai password')
    if not auth.check_recover_account(pin):    raise Exception('Sai ma khoi phuc')

    
    user_keys_db.delete(email)
    insert_key(email, password, pin)

    logger.security.info(f'{email} - Thay đổi khóa private key vs public key - thành công')

def update_new_password(email: str, new_password: str, 
                        pin: str = None, old_password: str = None):
    
    infor_user_keys = user_keys_db.find_email(email)
    if not len(infor_user_keys): 
        raise Exception('Thay đổi password thất bại')
    
    private_key_password: Base64Str = Base64Str.from_string(infor_user_keys[0][2])
    private_key_recovery: Base64Str = Base64Str.from_string(infor_user_keys[0][3])
    
    if pin:
        try:
            private_key_AES = AES.decrypt(pin.encode(), private_key_recovery)
            logger.security.info(f'{email} - AES giải mã private_key bằng mã khôi phục - thành công')
        except:
            logger.security.warning(f'{email} - AES giải mã private_key bằng mã khôi phục - thất bại')
    else:
        try:
            private_key_AES = AES.decrypt(old_password.encode(), private_key_password)
            logger.security.info(f'{email} - AES giải mã private_key bằng mật khẩu - thành công')
        except:
            logger.security.warning(f'{email} - AES giải mã private_key bằng mật khẩu - thất bại')
    
    try:
        encrypt_private_key_pwd = AES.encrypt(new_password.encode(), private_key_AES)
        logger.security.info(f'{email} - AES Mã hóa private key bằng password mới - thành công')
    except:
        logger.security.warning(f'{email} - AES Mã hóa private key bằng password mới - thất bại')

    infor_user = users_db.find_email(email)

    try:
        new_password_enc = SHA_256.hash_text(new_password)
        logger.security.info(f'{email} - SHA_256 Mã hóa new_password - thành công')
    except:
        logger.security.warning(f'{email} - SHA_256 Mã hóa new_password - thất bại')

    
    data_tmp = users_db.Data(*infor_user[0])
    data_tmp.passphrase = new_password_enc

    users_db.update(data_tmp)

    user_keys_db.update(
        user_keys_db.Data(
            email                   = infor_user_keys[0][0],
            public_key              = infor_user_keys[0][1],
            private_key_password    = encrypt_private_key_pwd,
            private_key_recovery    = infor_user_keys[0][3],
            ngay_tao                = infor_user_keys[0][4],
            thoi_han                = infor_user_keys[0][5],
            len_key                 = infor_user_keys[0][6]
    ))
