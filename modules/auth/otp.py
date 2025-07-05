import string, random, datetime
from modules.database import users as users_db
import smtplib
import os 
from dotenv import load_dotenv

load_dotenv()

class OTP:

    def __init__(self, len: int, expired_seconds: int):
        self.len            = len
        self.expired        = expired_seconds
        self.gen_code       = self.generate_code(len) 
        self.time_start     = datetime.datetime.now()
        self.time_end       = (datetime.datetime.now() + datetime.timedelta(seconds=self.expired))

    def generate_code(self, len: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=len))

    def send_otp(self, userFrom: users_db.Data, userTo: users_db.Data) -> bool:

        data = {
            "code": self.gen_code,
            'date': self.time_start.strftime("%c"),
            "expired": self.time_end.strftime("%c")
        }

        print("FROM: ", userFrom.email)
        print(userFrom.passphrase)
        print("TO: ", userTo.email)

        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            
            smtp.login(userFrom.email, userFrom.passphrase)
            msg = f"""
            code: {data['code']}  
            date: {data['date']}
            expired: {data['expired']}"""
            smtp.sendmail(userFrom.email, userTo.email, msg)
        except:
            print('gui mail that bai')
            return False
        finally:
            smtp.quit()
        
        print('gui mail thanh cong')
        return True
    
    def verify(self, pin_code_input: str) -> bool:
        return self.gen_code == pin_code_input
    
    def check_expired(self) -> bool:
        return datetime.datetime.now() <= self.time_end


