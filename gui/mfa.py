from PySide6.QtWidgets import * 
from PySide6.QtCore import * 
from PySide6.QtGui import * 

from modules.config import logger
import gui


class MFA_Window(QMessageBox):
    
    PIN_RETRY_LIMIT     = 5

    def __init__(self, email_to: str):
        super().__init__()

        self.email_to     = email_to
        self.mfa_success  = False

        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle('MFA')
        self.setText('Chọn phương thức xác thực')

        self.btn_otp = self.addButton("OPT", QMessageBox.ButtonRole.YesRole)
        self.btn_totp = self.addButton("TOPT", QMessageBox.ButtonRole.NoRole)

        self.exec()
 
        if self.clickedButton() is self.btn_otp  : self.__choose_otp()
        if self.clickedButton() is self.btn_totp : self.__choose_totp()

    def __choose_otp(self) -> None:
        logger.security.info('Bắt đầu gửi OTP đến {}'.format(self.email_to, self.email_to))
        otp = gui.otp.OTP(email_to=self.email_to)
        if otp.check_success():
            logger.security.info('Xác thực OTP - thành công')
            self.mfa_success = True
        else:
            logger.security.warning('Xác thực OTP - thất bại')
        

    def __choose_totp(self) -> None:
        logger.security.info('Bắt đầu tạo TOTP ...')
        self.totp = gui.totp.TOTP()
        
        if self.totp.check_success():
            logger.security.info('Xác thực TOTP - thành công')
            self.mfa_success = True
        else:
            logger.security.warning('Xác thực TOTP - thất bại')
    
    def check_success(self) -> bool:
        return self.mfa_success