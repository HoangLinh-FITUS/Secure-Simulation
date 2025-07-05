import pyotp 
import time
from modules.utils.qrcode import create_qr

class TOTP:
    def __init__(self):
        # self.secret = pyotp.random_base32()
        self.secret = "base32secret3232"
        

    def create_totp_url(self, name: str, issuer_name: str) -> str:
        self.totp = pyotp.TOTP(self.secret)  
        print(self.totp.now())
        url = self.totp.provisioning_uri(name, issuer_name)
        return url 
    
    def verify(self, totp_input) -> bool:
        return self.totp.verify(totp_input)

    def time_remaining(self) -> int:
        return int(self.totp.interval - (time.time() % self.totp.interval))


