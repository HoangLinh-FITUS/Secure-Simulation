from PySide6.QtWidgets import * 
from PySide6.QtCore import *

from modules.config import logger 

import gui

class Menu(QWidget):
    def __init__(self, email_manager: str, role: str, parent=None):
        super().__init__(parent)
        
        self.email_manager = email_manager
        self.role = role

        self.setWindowTitle(f'Menu [{email_manager}]')
        
        self.__create_btn()

    def __create_btn(self):
        btn_update_infor        = QPushButton('Cập Nhật Thông Tin')
        btn_manager_key         = QPushButton('Quản Lý Khóa Cá Nhân')
        btn_qrcode_read         = QPushButton('Đọc QR')
        btn_qrcode_write        = QPushButton('Tạo QR')
        btn_read_file           = QPushButton('Đọc File')
        btn_search_pubkey       = QPushButton('Tìm Kiếm Public Key')
        btn_send_file           = QPushButton('Gửi File')
        btn_signature_file      = QPushButton('Ký Số Tập Tin')
        btn_verify_signature    = QPushButton('Xác Thực Chữ Ký')
        btn_view_account        = QPushButton('Xem Tài Khoản')
        btn_view_log            = QPushButton('Xem Log')

        grid_btn = QGridLayout()
        btns = [btn_update_infor, btn_manager_key, btn_qrcode_read, 
                btn_qrcode_write, btn_read_file, btn_search_pubkey,
                btn_send_file, btn_signature_file, btn_verify_signature]

        btns_admin = [btn_view_account, btn_view_log]

        num_col = 6
        for id, btn in enumerate(btns):
            row, col = id // num_col , id % num_col
            grid_btn.addWidget(btn, row, col)

        if self.role == 'admin':
            for id, btn in enumerate(btns_admin):
                row, col = (len(btns) + id) // num_col, (len(btns) + id) % num_col
                grid_btn.addWidget(btn, row, col)

        self.setLayout(grid_btn)

        btn_update_infor.clicked.connect(self.open_update_infor)
        btn_manager_key.clicked.connect(self.open_manager_key)
        btn_qrcode_read.clicked.connect(self.open_qrcode_read)
        btn_qrcode_write.clicked.connect(self.open_qrcode_write)
        btn_read_file.clicked.connect(self.open_read_file)
        btn_search_pubkey.clicked.connect(self.open_search_pubkey)
        btn_send_file.clicked.connect(self.open_send_file)
        btn_signature_file.clicked.connect(self.open_signature_file)
        btn_verify_signature.clicked.connect(self.open_verify_signature)
        btn_view_account.clicked.connect(self.open_view_account)
        btn_view_log.clicked.connect(self.open_view_log)


    def open_update_infor(self):
        logger.user.info('cập nhật thông tin')
        self.window_infor = gui.information.Information(self.email_manager)
        self.window_infor.show()

    def open_manager_key(self):
        logger.user.info('xem quản lý khóa')
        self.window_manager_key = gui.manager_key.ManagerKey(self.email_manager)
        self.window_manager_key.show()

    def open_qrcode_read(self):
        logger.user.info('Đọc QR')
        self.window_qrcode_read = gui.qrcode.ReadQR(self.email_manager)
        self.window_qrcode_read.show()

    def open_qrcode_write(self):
        logger.user.info('Tạo QR')
        self.window_qrcode_gen = gui.qrcode.GenQR(self.email_manager)
        self.window_qrcode_gen.show()

    def open_read_file(self):
        logger.user.info('Đọc file được gửi')
        self.window_read_file = gui.read_file.ReadFile(self.email_manager)
        self.window_read_file.show()

    def open_search_pubkey(self):
        logger.user.info('Tìm kiếm Public Key')
        self.window_search_pubkey = gui.search_public_key.Search_PublicKey(self.email_manager)
        self.window_search_pubkey.show()

    def open_send_file(self):
        logger.user.info('Gửi File')
        self.window_send_file = gui.send_file.SendFile(self.email_manager)
        self.window_send_file.show()

    def open_signature_file(self):
        logger.user.info('Ký File')
        self.window_signature_file = gui.signature_file.SignatureFile(self.email_manager)
        self.window_signature_file.show()

    def open_verify_signature(self):
        logger.user.info('xác thực chữ ký')
        self.window_verify_signature = gui.verify_signature.VerifySignature(self.email_manager)
        self.window_verify_signature.show()

    def open_view_account(self):
        logger.user.info('Xem các tài khoản trong hệ thông')
        self.window_view_account = gui.view_account.ViewAccounts(self.email_manager)
        self.window_view_account.show()

    def open_view_log(self):
        logger.user.info('Xem log hệ thống')
        self.window_view_log = gui.view_log.ViewLog(self.email_manager)
        self.window_view_log.show()
