from PySide6.QtWidgets import * 
from PySide6.QtCore import * 
from PySide6.QtGui import * 

from modules.database import users as users_db
from modules.auth import controller
from modules.account import info
from modules.config import logger

import gui


class Information(QWidget):
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email_manager = email_manager

        self.setWindowTitle(f'Thông Tin Tài Khoản [{email_manager}]')
        self.setFixedSize(640, 200)

        self.__create_information()
        self.__create_password()
        self.__create_btn_update()

        form = QHBoxLayout()
        form.addLayout(self.layout_left)
        form.addSpacing(25)
        form.addLayout(self.layout_right)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form)
        main_layout.addSpacing(20)
        main_layout.addLayout(self.btn_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    def __create_information(self):
        users = users_db.find_email(self.email_manager)

        self.infor_user = users_db.Data(*users[0])

        self.hoten_label        = QLineEdit(self.infor_user.hoten)
        self.ngaysinh_label     = QDateEdit(QDate.fromString(self.infor_user.ngaysinh, "M/d/yyyy"))
        self.SDT_label          = QLineEdit(self.infor_user.sdt)
        self.diachi_label       = QLineEdit(self.infor_user.diachi)

        self.layout_left = QFormLayout()
        self.layout_left.addRow('Họ Và Tên:',               self.hoten_label)
        self.layout_left.addRow('Ngày Sinh (mm/dd/yy):',    self.ngaysinh_label)
        self.layout_left.addRow('SĐT:',                     self.SDT_label)
        self.layout_left.addRow('Địa chỉ:',                 self.diachi_label)

    def __create_password(self):
        self.old_password_label           = QLineEdit()
        self.new_password_label           = QLineEdit()
        self.new_password_again_label     = QLineEdit()
        
        self.layout_right = QFormLayout()
        self.layout_right.addRow('Mật Khẩu Cũ:',    self.old_password_label)
        self.layout_right.addRow('Mật Khẩu Mới:',   self.new_password_label)
        self.layout_right.addRow('Xác Nhận Lại:',   self.new_password_again_label)

    def __create_btn_update(self):
        self.btn_upd_infor      = QPushButton('Update information')
        self.btn_upd_pwd        = QPushButton('Update password')
        
        self.btn_upd_infor.clicked.connect(self.update_account)
        self.btn_upd_pwd.clicked.connect(self.update_new_password)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.btn_upd_infor, alignment=Qt.AlignmentFlag.AlignRight)
        self.btn_layout.addWidget(self.btn_upd_pwd, alignment=Qt.AlignmentFlag.AlignLeft)

    def update_account(self) -> None:
        logger.user.info('Bắt đầu cập thật thông tin tài khoản')
        
        self.infor_user.hoten       = self.hoten_label.text()
        self.infor_user.ngaysinh    = self.ngaysinh_label.text()
        self.infor_user.sdt         = self.SDT_label.text()
        self.infor_user.diachi      = self.diachi_label.text()
        
        logger.user.info('Đầu vào : {} - {} - {} - {}'
                          .format(self.infor_user.hoten, self.infor_user.ngaysinh, 
                                  self.infor_user.sdt, self.infor_user.diachi))

        try:
            users_db.update(self.infor_user)
            gui.announce.update_infor_success()
            logger.user.info('cập thật thông tin tài khoản thành công')
        except:
            gui.announce.update_infor_fail()
            logger.user.warning('cập thật thông tin tài khoản thất bại')
        

    def update_new_password(self) -> None:
        old_password        = self.old_password_label.text()
        new_password        = self.new_password_label.text()
        new_password_again  = self.new_password_again_label.text()

        if not old_password or not new_password or not new_password_again:
            gui.announce.full_infor_password()
            return
        
        auth_old = controller.AuthController(self.email_manager, old_password)
        if not auth_old.check_account(): 
            gui.announce.wr_password()
            return
        
        auth_new = controller.AuthController(self.email_manager, new_password)

        if not auth_new.check_strong_password(): 
            gui.announce.strong_password()
            return
        
        if not auth_new.check_password_matches(new_password_again): 
            gui.announce.password_mathces()
            return

        try:
            info.update_new_password(self.email_manager, new_password, old_password=old_password)
            gui.announce.update_password_success()
            logger.user.info(f'Thay đổi password mới thành công')
        except:
            gui.announce.update_password_fail()
            logger.user.warning('Thay đổi password mới thất bại')


