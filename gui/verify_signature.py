import json

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from modules.types.customer import *
from modules.crypto import signature
from modules.database import email_public_keys
from modules.config import logger

import gui 

class VerifySignature(QWidget):
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email_manager = email_manager

        self.setWindowTitle(f'Signature File [{email_manager}]')
        
        self.__create_widgets()

    def __create_widgets(self):
        self.path_file_input     = QLineEdit(readOnly=True)
        self.btn_browser_file    = QPushButton('Browser')
        self.path_sig_input      = QLineEdit(readOnly=True)
        self.btn_browser_sig     = QPushButton('Browser')
        self.btn_sign            = QPushButton('Check')
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setColumnMinimumWidth(1, 500)
        
        self.grid_layout.addWidget(QLabel('file:'),        0, 0)
        self.grid_layout.addWidget(self.path_file_input,   0, 1)
        self.grid_layout.addWidget(self.btn_browser_file,  0, 2)

        self.grid_layout.addWidget(QLabel('file sig:'),   1, 0)
        self.grid_layout.addWidget(self.path_sig_input,   1, 1)
        self.grid_layout.addWidget(self.btn_browser_sig,  1, 2)
        self.grid_layout.addWidget(self.btn_sign,         2, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.grid_layout)

        self.btn_browser_file.clicked.connect(self.open_file)
        self.btn_browser_sig.clicked.connect(self.open_file_sig)
        self.btn_sign.clicked.connect(self.check_sign)

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'file', '', 'All (*)')
        if filename and ok:
            logger.user.info(f'Mở file {filename}')
            self.path_file_input.setText(filename)
            with open(filename, 'rb') as f:
                self.data_file = f.read()

    def open_file_sig(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'sig', '', 'sig (*.sig)')
        if filename and ok:
            logger.user.info(f'Mở file {filename}')
            self.path_sig_input.setText(filename)
            with open(filename, 'r') as f:
                data = json.loads(f.read())
                self.timestamp = data['timestamp']
                self.data_file_sig = Base64Str.from_string(data['data_sign']).decode()

    def check_sign(self):
        users = email_public_keys.find(self.email_manager)
        
        for user in users:
            public_key = Base64Str.from_string(users[0][2])
            self.nguoi_ky = user[1]

            ok = signature.verify(public_key, self.data_file, self.data_file_sig)
            if ok:
                logger.user.info('Nguoi ky: {} - Thoi gian: {} - Xác minh chữ ký thành công'.format(self.nguoi_ky, self.timestamp))
                QMessageBox.information(None, 'Content', f'Người ký: {self.nguoi_ky}\nTimestamp: {self.timestamp}')
                return
        
        gui.announce.verify_sign_faild()
        logger.user.info('Xác minh chữ ký thất bại')
        