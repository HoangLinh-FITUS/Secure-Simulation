from datetime import datetime 
import json

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from modules.types.customer import *
from modules.crypto import signature
from modules.database import user_keys
from modules.crypto import AES
from modules.config import logger 

import gui 


class SignatureFile(QWidget):
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email_manager = email_manager

        self.setWindowTitle(f'Signature File [{email_manager}]')
        
        self.__create_widgets()

    def __create_widgets(self):
        self.path_file_input     = QLineEdit(readOnly=True)
        self.btn_browser_file    = QPushButton('Browser')
        self.path_sig_input     = QLineEdit(readOnly=True)
        self.btn_browser_sig    = QPushButton('Browser')
        self.btn_sign          = QPushButton('Signature')
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setColumnMinimumWidth(1, 500)
        
        self.grid_layout.addWidget(QLabel('file:'),        0, 0)
        self.grid_layout.addWidget(self.path_file_input,   0, 1)
        self.grid_layout.addWidget(self.btn_browser_file,  0, 2)
        self.grid_layout.addWidget(self.btn_sign,          1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid_layout)

        self.btn_browser_file.clicked.connect(self.open_file)
        self.btn_sign.clicked.connect(self.sign)

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'file', '', 'All (*)')
        if filename and ok:
            logger.user.info(f'đọc file: {filename}')
            
            self.path_file_input.setText(filename)
            with open(filename, 'rb') as f:
                self.data_file = f.read()

    def sign(self):
        password, ok = QInputDialog.getText(self, 'input password', 'password')
        if not ok:
            return
        
        user = user_keys.find_email(self.email_manager)
        private_key_password_enc = Base64Str.from_string(user[0][2])
        try:
            private_key = AES.decrypt(password.encode(), private_key_password_enc)
            logger.security.info('{} - AES giải mã private key bằng password - thành công'.format(self.email_manager))
        except:
            logger.security.info('{} - AES giải mã private key bằng password - thất bại'.format(self.email_manager))
            gui.announce.signature_failed()
            return 

        private_key = Base64Str.from_string(private_key)

        filename, ok = QFileDialog.getSaveFileName(self, 'save signature', 'file', 'sig (*.sig)')
        if filename and ok:
            with open(filename, 'w') as f:
                data = {
                    "timestamp": datetime.utcnow().isoformat() + 'Z',
                    "data_sign": Base64Str(signature.generate_key(private_key, self.data_file))
                }
                f.write(json.dumps(data, indent=4))
            
            logger.user.info('ký số tập tin - thành công')
            logger.user.info('Lưu file {} - thành công'.format(filename))

        
            

