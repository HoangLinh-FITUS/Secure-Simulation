from PySide6.QtWidgets import *
from PySide6.QtCore import *

from modules.auth import controller
from modules.account import info
from modules.database.db_manager import *
from modules.config import logger
from modules.utils import status

import gui


class SignIn(QDialog):
    
    __LIMIT_TIME_LOCK = 300 # second
    __LIMIT_CNT_WR_PWD = 5

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_success = False
        
        self.setWindowTitle('Sign In')
        self.setFixedWidth(312)
    
        self.__reset()

        self.__create_form_input()
        self.__create_buttons()
        self.__create_label_lock()
        self.__create_timer()

        layout = QVBoxLayout()
        layout.addLayout(self.form_input)
        layout.addLayout(self.layout_btns)
        layout.addWidget(self.label_lock)

        self.setLayout(layout)

        self.show()

    def __create_form_input(self) -> None:
        self.email_input        = QLineEdit()
        self.password_input     = QLineEdit(echoMode=QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.form_input         = QFormLayout()
        self.form_input.addRow('Email:', self.email_input)
        self.form_input.addRow('Password:', self.password_input)

    def __create_buttons(self) -> None:
        self.btn_sign_in        = QPushButton('Sign In')
        self.btn_sign_up        = QPushButton('Sign Up')
        self.btn_forgot_pwd     = QPushButton('Forgot Password ?')

        self.layout_btns        = QGridLayout()
        self.layout_btns.addWidget(self.btn_sign_in, 0, 0, 
                                   alignment=Qt.AlignmentFlag.AlignRight)
        self.layout_btns.addWidget(self.btn_sign_up, 0, 1,
                                   alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_btns.addWidget(self.btn_forgot_pwd, 1, 1,
                                   alignment=Qt.AlignmentFlag.AlignRight)
        
        self.btn_sign_in.clicked.connect(self.__verify_account)
        self.btn_sign_up.clicked.connect(self.__open_sign_up)
        self.btn_forgot_pwd.clicked.connect(self.__recover_account)

    def __open_sign_up(self) -> None:
        self.sign_up_window = gui.sign_up.SignUp()
        self.sign_up_window.show()

    def __create_label_lock(self) -> None:
        self.label_lock = QLabel()
        
    def __create_timer(self) -> None:
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.__update_time_lock)

    def __update_label_lock(self) -> None:
        self.label_lock.setText(f'Tài khoản đã bị khóa trong {self.__time_lock}s')
        self.label_lock.setHidden(not bool(self.__time_lock))

    def __verify_account(self) -> None:
        self.email             = self.email_input.text()
        password               = self.password_input.text()
        auth_controller        = controller.AuthController(self.email, password)

        if not auth_controller.check_email():
            gui.announce.not_exist_email()
            return

        if auth_controller.check_account():
            if auth_controller.is_block():
                self.__time_lock = auth_controller.time_block()
                if self.__time_lock == -1:
                    status.lock_account(self.email, 0)
                else:
                    self.__lock_account()
                    return 
            
            self.mfa_window = gui.mfa.MFA_Window(email_to=self.email)
            
            if self.mfa_window.check_success():
                self.close()
                self.is_success = True

            return
        
        
        gui.announce.wr_password()

        self.__cnt_wr_pwd += 1

        logger.login.warning('{} - Số lần nhập sai mật khẩu: {}'.format(self.email, self.__cnt_wr_pwd))
        
        if self.__cnt_wr_pwd == self.__LIMIT_CNT_WR_PWD:
            status.lock_account(self.email, 1, SignIn.__LIMIT_TIME_LOCK)
            self.__lock_account()
            

    def __lock_account(self) -> bool:
        logger.login.info('{} - Lock tài khoản trong {} giây'.format(self.email, self.__time_lock))
        
        self.timer.start()
        self.__update_label_lock()
        self.btn_sign_in.setEnabled(False)

    def __reset(self) -> None:
        self.__time_lock    = self.__LIMIT_TIME_LOCK
        self.__cnt_wr_pwd   = 0

    def __update_time_lock(self) -> None:
        self.__time_lock -= 1
        self.__update_label_lock()
        
        if self.__time_lock <= 0:
            self.timer.stop()
            self.__reset()
            self.btn_sign_in.setEnabled(True)
            status.lock_account(self.email, 0)

    def __recover_account(self) -> None:
        email                  = self.email_input.text()
        self.pin, ok           = QInputDialog.getText(self, 'recover', 'Nhập mã khôi phục')
        auth_controller        = controller.AuthController(email, '')

        if self.pin and ok:
            if auth_controller.check_recover_account(self.pin):
                self.__update_new_password(email, self.pin)
            else:
                gui.announce.recovery_not_success()
                logger.login.warning(f'{self.email} - khôi phục tài khoản thất bại')

    def __update_new_password(self, email, pin):
        new_password, ok = QInputDialog.getText(self, 'new password', 'mật khẩu mới')
        if new_password and ok:
            auth_controller = controller.AuthController(email, new_password)
            if auth_controller.check_strong_password():
                try:
                    info.update_new_password(email, new_password, pin=pin)
                    logger.login.info(f'{email} - Thay đổi password mới thành công')
                except:
                    logger.login.warning(f'{email} - Thay đổi password mới thất bại')
            else:
                gui.announce.strong_password()
                self.__update_new_password(email, pin)

    def check_success(self):
        return self.is_success
    