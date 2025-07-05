import os 
from dotenv import load_dotenv

from PySide6.QtWidgets import * 
from PySide6.QtCore import * 
from PySide6.QtGui import * 

from modules.auth.otp import OTP as auth_otp
from modules.database import users as users_db
from modules.config import logger
import gui


load_dotenv()


class OTPWorker(QThread):
    finished = Signal(bool)
    def __init__(self, otp: auth_otp, userFrom: users_db.Data, userTo: users_db.Data):
        super().__init__()
        self.userFrom   = userFrom
        self.userTo     = userTo
        self.otp        = otp

    def run(self):
        send_success = self.otp.send_otp(
            userFrom = self.userFrom,
            userTo   = self.userTo
        )

        self.finished.emit(send_success)

class OTP(QMessageBox):
    
    OTP_LEN             = 6
    OTP_EXPIRED         = 30 # second

    def __init__(self, email_to: str) -> None:
    
        emailFrom       = os.getenv('EMAIL_SEND')
        passphraseFrom  = os.getenv('PASSPHRASE')

        self.mfa_success = False

        self.an_wait = gui.announce.Waiting()
        self.an_wait.show()

        self.otp = auth_otp(len=OTP.OTP_LEN, expired_seconds=OTP.OTP_EXPIRED)
        self.otpworker = OTPWorker(
            otp      = self.otp,
            userFrom = users_db.Data(email=emailFrom, passphrase=passphraseFrom),
            userTo   = users_db.Data(email=email_to)
        )
        
        self.loop = QEventLoop()
        self.otpworker.finished.connect(self.__send)
        self.otpworker.start()
        self.loop.exec()
    
    def __send(self, send_success):
        self.an_wait.close()

        if not send_success:
            logger.security.info('Gửi OTP thất bại')
            gui.announce.otp_failed()
            return
        
        logger.security.info('Gửi OTP thành công')

        try:
            self.mfa_success = False
            while self.otp.check_expired():
                pin_code, ok = self.__input_pincode()
                if not ok: break
                if self.otp.verify(pin_code):
                    self.mfa_success = True
                    return
                gui.announce.MFA_failed()
        finally:
            self.loop.quit()


    def __input_pincode(self) -> tuple:
        return QInputDialog.getText(None, 'pin code', "pin")
    
    def check_success(self) -> bool:
        return self.mfa_success