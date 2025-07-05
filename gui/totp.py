import os

from PySide6.QtWidgets import * 
from PySide6.QtCore import * 
from PySide6.QtGui import * 

from modules.auth.totp import TOTP as auth_totp
from modules.utils import qrcode
from modules.config import logger

import gui


class TOTP(QWidget):
    
    PIN_RETRY_LIMIT     = 5

    def __init__(self):
        self.mfa_success  = False

        self.__create_timer()
        self.__send()

    def __send(self):
        self.totp = auth_totp()

        try:
            url = self.totp.create_totp_url(name='Secure Simuation', issuer_name='TOTP')
            qrcode.create_qr(data=url, filename='qr.png')
        except:
            logger.security.exception('Tạo QR TOTP thất bại')
            raise Exception('Tạo QR TOTP thất bại')
            

        self.__totp_expired = self.totp.time_remaining()

        self.__show_qr() 
        self.__start_time_expired()       

        try:
            logger.security.info('Tạo QR TOTP thành công')
            self.mfa_success = False
            for _ in range(TOTP.PIN_RETRY_LIMIT):
                pin_code, ok = self.__input_pincode()
                if not ok: break
                if self.totp.verify(pin_code):
                    self.mfa_success = True
                    return
                
                gui.announce.MFA_failed()
        finally:
            os.remove('qr.png')
            self.__close_qr()
            self.timer.stop()
    
    def __create_timer(self) -> None:
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.__update_time_expired)
    
    def __update_label_time(self) -> None:
        self.label_time.setText(f'{self.__totp_expired}s')

    def __show_qr(self) -> None:
        self.qr_window = QWidget()
        self.qr_window.setWindowTitle("Quét mã QR TOTP")
        self.qr_window.setFixedSize(300, 300)

        layout = QVBoxLayout()
        qr_label = QLabel()
        qr_label.setPixmap(QPixmap("qr.png").scaled(280, 280, 
                                                    Qt.AspectRatioMode.KeepAspectRatio, 
                                                    Qt.TransformationMode.SmoothTransformation))
        
        self.label_time = QLabel()
        layout.addWidget(qr_label)
        layout.addWidget(self.label_time, alignment=Qt.AlignmentFlag.AlignCenter)

        self.qr_window.setLayout(layout)
        self.qr_window.show()
    
    def __close_qr(self) -> None:
        self.qr_window.close()

    def __start_time_expired(self) -> None:
        self.timer.start()
        self.__update_time_expired()

    def __update_time_expired(self) -> None:
        self.__update_label_time()
        self.__totp_expired -= 1
        if self.__totp_expired <= -1:
            gui.announce.MFA_failed()
            self.timer.stop()

    def __input_pincode(self) -> tuple:
        return QInputDialog.getText(None, 'pin code', "pin")

    def check_success(self) -> bool:
        return self.mfa_success