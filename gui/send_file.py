import json
from datetime import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from modules.account import file
from modules.database import email_public_keys
from modules.types.customer import *
from modules.config import logger

import gui 


class SendFile(QWidget):
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email_manager = email_manager

        self.setWindowTitle(f'Send File [{email_manager}]')
        
        self.__create_btn()
        self.__create_widgets()

        self.grid_layout.addLayout(self.btn_send, 2, 0, 1, 3,
                                   alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.grid_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def __create_btn(self):
        self.btn_save_enc       = QPushButton('save .enc')
        self.btn_save_key       = QPushButton('save .enc and .key')

        self.btn_send = QHBoxLayout()
        self.btn_send.addWidget(self.btn_save_enc)
        self.btn_send.addWidget(self.btn_save_key)

    def __create_widgets(self):
        self.label          = QLabel('file:')
        self.path_input     = QLineEdit(readOnly=True)
        self.btn_browser    = QPushButton('Browser')
        
        self.email_label    = QLabel('email:')
        self.email_input    = QLineEdit()
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setColumnMinimumWidth(1, 500)
        
        self.grid_layout.addWidget(self.label,        0, 0)
        self.grid_layout.addWidget(self.path_input,   0, 1)
        self.grid_layout.addWidget(self.btn_browser,  0, 2)
        self.grid_layout.addWidget(self.email_label,  1, 0)
        self.grid_layout.addWidget(self.email_input,  1, 1)
        
        self.btn_browser.clicked.connect(self.__open_file)

    def __open_file(self):
        self.filename, ok = QFileDialog.getOpenFileName(self, 'open file', '', 'All (*)')
        if self.filename and ok:
            self.path_input.setText(self.filename)
            logger.user.info(f'Mở file {self.filename}')

            self.btn_save_key.setEnabled(True)
            if file.check_file_large(self.filename):
                self.btn_save_key.setEnabled(False)

            self.btn_save_enc.clicked.connect(self.__save_enc)
            self.btn_save_key.clicked.connect(self.__save_enc_key)
    
    def __data_send(self):
        infor = email_public_keys.find(self.email_manager, self.email_input.text())
        if not infor:
            gui.announce.dont_find_public_key()
            raise Exception('khong tim thay public key')

        try:
            public_key: Base64Str = Base64Str.from_string(infor[0][2])
            logger.security.info(f'email: {self.email_manager}')
            data_file, data_key = file.send(self.filename, public_key)
            logger.security.info(f'mã hóa file - thành công')
            return data_file, data_key
        except:
            logger.security.warning(f'mã hóa file - thất bại')
    
    def __save(self, data: dict, filename: str, filter: str):
        filename, ok = QFileDialog.getSaveFileName(self, 'save enc', filename, filter)
        if filename and ok:
            with open(filename,'w') as f:
                f.write(json.dumps(data, indent=4))
            
            logger.user.info(f'Lưu file {filename} - thành công')
        else:
            logger.user.warning(f'Lưu file {filename} - thất bại')


    def __save_enc(self):
        data_file, data_key = self.__data_send()
        data = {
            "file_enc": data_file,
            "key_enc": data_key,
            "nguoi_gui": self.email_manager,
            "ten_file": self.filename.split('/')[-1],
            "timestamp":  datetime.utcnow().isoformat() + 'Z'
        }
        self.__save(data, 'file.enc', 'encrypt (*.enc)')

    def __save_enc_key(self):
        data_file, data_key = self.__data_send()
        data = {
            "file_enc": data_file,
            "nguoi_gui": self.email_manager,
            "ten_file": self.filename.split('/')[-1],
            "timestamp":  datetime.utcnow().isoformat() + 'Z'
        }
        self.__save(data, 'file.enc', 'encrypt (*.enc)')
        
        data = {
            "key_enc": data_key,
        }
        self.__save(data, 'file.key', 'encrypt (*.key)')
        

