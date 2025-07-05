from PySide6.QtWidgets import * 
from PySide6.QtCore import * 
from modules.database import users as users_db
from modules.crypto import SHA_256

from modules.auth.controller import AuthController
from modules.account import info
from modules.config import logger 

import gui


class SignUp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Sign Up')
        self.setFixedWidth(380)
        self.setFixedHeight(337)

        self.__create_group()

        self.setLayout(self.main_layout)

    def __create_form_input(self) -> None:
        
        self.email_input                     = QLineEdit()
        self.ho_va_ten_input                 = QLineEdit()
        self.ngay_sinh_input                 = QDateEdit()
        self.sdt_input                       = QLineEdit()
        self.dia_chi_input                   = QLineEdit()
        self.passphrase_input                = QLineEdit(echoMode=QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.nhaplai_passphrase_input        = QLineEdit(echoMode=QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.ma_khoi_phuc_input              = QLineEdit()
        
        self.form_input                      = QFormLayout()

        self.form_input.addRow('Email:',                    self.email_input)
        self.form_input.addRow('Họ Và Tên:',                self.ho_va_ten_input)
        self.form_input.addRow('Ngày Sinh (mm/dd/yy):',     self.ngay_sinh_input)
        self.form_input.addRow('Số Điền Thoại:',            self.sdt_input)
        self.form_input.addRow('Địa Chỉ:',                  self.dia_chi_input)
        self.form_input.addRow('Password:',                 self.passphrase_input)
        self.form_input.addRow('Nhập Lại Password:',        self.nhaplai_passphrase_input)
        self.form_input.addRow('Mã Khôi Phục:',             self.ma_khoi_phuc_input)

    def __create_button(self) -> None:
        self.btn_sign_up = QPushButton('Sign Up')
        self.btn_sign_up.clicked.connect(self.__sign_up_account)

    def __create_group(self) -> None:
        self.__create_form_input()
        self.__create_button()

        self.layout_input = QVBoxLayout()
        self.layout_input.addLayout(self.form_input)
        self.layout_input.addWidget(self.btn_sign_up)

        self.group_Box = QGroupBox('Điền Thông Tin Cá Nhân')
        self.group_Box.setLayout(self.layout_input)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.group_Box)

    def __sign_up_account(self) -> None:

        autho_controller = AuthController(self.email_input.text(), self.passphrase_input.text())

        if not autho_controller.check_strong_password(): 
            gui.announce.strong_password()
            return
        
        if not autho_controller.check_password_matches(self.nhaplai_passphrase_input.text()):
            gui.announce.password_mathces()
            return
        
        logger.login.info('{} - Bắt đầu đăng ký tài khoản .... '.format(self.email_input.text()))
        logger.login.info('{} - {} - {} - {} - {}'.format(
            self.email_input.text(), 
            self.ho_va_ten_input.text(),
            self.ngay_sinh_input.text(),
            self.sdt_input.text(),
            self.dia_chi_input.text()
        ))

        self.__insert_account()
        self.__generate_keys()

        self.close()

    def __insert_account(self) -> None:
        logger.security.info('{} - Mã hóa mật khẩu bằng SHA_256 '.format(self.email_input.text()))
        passphrase_enc = SHA_256.hash_text(self.passphrase_input.text())
        
        logger.security.info('{} - Mã hóa mã khôi phục bằng SHA_256 '.format(self.email_input.text()))
        ma_khoi_phuc_enc = SHA_256.hash_text(self.ma_khoi_phuc_input.text())                     
        
        try:
            users_db.insert(
                users_db.Data(
                    self.email_input.text(),
                    self.ho_va_ten_input.text(),
                    self.ngay_sinh_input.text(),
                    self.sdt_input.text(),
                    self.dia_chi_input.text(),
                    passphrase_enc,
                    ma_khoi_phuc_enc
                )
            )
        except:
            gui.announce.exist_email()
            logger.login.info('{} - Tài khoản đã tồn tại '.format(self.email_input.text()))

    def __generate_keys(self) -> None:
        info.insert_key( 
            email       = self.email_input.text(), 
            password    = self.passphrase_input.text(),
            pin         = self.ma_khoi_phuc_input.text()
        )     

        gui.announce.sign_up_success()
        logger.login.info('{} - Đăng ký tài khoản thành công '.format(self.email_input.text()))


