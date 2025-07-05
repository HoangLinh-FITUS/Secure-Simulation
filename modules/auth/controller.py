from modules.database import users as users_db
from modules.crypto import SHA_256
from modules.types.customer import Base64Str

import datetime 
import re 

class AuthController:
    def __init__(self, email, passphrase):
        self.email = email
        self.passphrase = passphrase 

    def check_email(self) -> bool:
        res = users_db.find_email(email=self.email)
        return bool(len(res))
    
    def check_account(self) -> bool:
        users = users_db.find_email(email=self.email)
        if not len(users):
            return False
        
        password_enc_db: Base64Str = Base64Str.from_string(users[0][5])
        if not SHA_256.verify(password_enc_db, self.passphrase):
            results = []
            return False
        
        return True
    
    def check_strong_password(self) -> bool:
        
        if len(self.passphrase) < 8 or len(self.passphrase) > 16:                    
            return False
        
        if not re.search('\d', self.passphrase):        return False
        if not re.search('[a-z]', self.passphrase):     return False
        if not re.search('[A-Z]', self.passphrase):     return False
        if not re.search('[^\w\s]', self.passphrase):   return False
        
        return True
    
    def check_password_matches(self, nhaplai_passphrase: str) -> bool:
        return self.passphrase == nhaplai_passphrase
    
    def check_recover_account(self, ma_khoi_phuc: str) -> bool:
        users = users_db.find_email(self.email)
        if not len(users):
            return False

        ma_khoi_phuc_enc: Base64Str = Base64Str.from_string(users[0][6])
        if not SHA_256.verify(ma_khoi_phuc_enc, ma_khoi_phuc):
            return False 

        return True

    def is_block(self):
        users = users_db.find_email(self.email) 
        if not len(users):
            raise Exception('khong ton tai user')
        user = users_db.Data(*users[0])
        return user.is_block
    
    def time_block(self) -> int: # seconds 
        if not self.is_block():
            raise Exception('tai khoan khong bi block')
        
        users = users_db.find_email(self.email) 
        if not len(users):
            raise Exception('khong ton tai user')
        
        user = users_db.Data(*users[0])
        second = datetime.datetime.strptime(user.thoi_han_block, '%c') - datetime.datetime.now()
        
        if second < datetime.timedelta(0): return -1
        return second.seconds
        