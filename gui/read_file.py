from PySide6.QtWidgets import *
from PySide6.QtCore import *
from modules.account import file
from modules.database import user_keys
from modules.types.customer import *
from modules.config import logger 
import json

import gui 

class ReadFile(QWidget):
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email_manager = email_manager
        
        self.setWindowTitle(f'Read File [{email_manager}]')
        
        self.__create_widgets()
        self.__create_results()

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)
        main_layout.addWidget(self.group_box)
        
        self.setLayout(main_layout)

    def __create_widgets(self):
        self.path_enc_input     = QLineEdit(readOnly=True)
        self.btn_browser_enc    = QPushButton('Browser')
        self.path_key_input     = QLineEdit(readOnly=True)
        self.btn_browser_key    = QPushButton('Browser')
        self.btn_read           = QPushButton('Read')
        self.password_label     = QLineEdit(echoMode=QLineEdit.EchoMode.PasswordEchoOnEdit)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setColumnMinimumWidth(1, 500)
        
        self.grid_layout.addWidget(QLabel('file enc:'),   0, 0)
        self.grid_layout.addWidget(self.path_enc_input,   0, 1)
        self.grid_layout.addWidget(self.btn_browser_enc,  0, 2)

        self.grid_layout.addWidget(QLabel('file key:'),   1, 0)
        self.grid_layout.addWidget(self.path_key_input,   1, 1)
        self.grid_layout.addWidget(self.btn_browser_key,  1, 2)
        self.grid_layout.addWidget(QLabel('password'),    2, 0)
        self.grid_layout.addWidget(self.password_label,   2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.addWidget(self.btn_read,         3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.btn_browser_enc.clicked.connect(self.__open_file_enc)
        self.btn_browser_key.clicked.connect(self.__open_file_key)
        self.btn_read.clicked.connect(self.__read_file)

    def __create_results(self):
        self.group_box  = QGroupBox('Kết Quả Giải Mã')
        self.form       = QFormLayout()

        self.file_name_label    = QLabel('None')
        self.nguoi_gui_label    = QLabel('None')
        self.timestamp_label    = QLabel('None')

        self.form.addRow('Tên file:',        self.file_name_label)
        self.form.addRow('Người gửi:',       self.nguoi_gui_label)
        self.form.addRow('timestamp:',       self.timestamp_label)
        
        self.form.setHorizontalSpacing(50)
        self.group_box.setLayout(self.form)

    def __open_file_enc(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'open file', '', 'encrypt (*.enc)')
        if filename and ok:
            logger.user.info(f'Mở file enc: {filename}')
            self.path_enc_input.setText(filename)

    def __open_file_key(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'open file', '', 'encrypt (*.key)')
        if filename and ok:
            logger.user.info(f'Mở file key: {filename}')
            self.path_key_input.setText(filename)

    def __read_file(self):
        file_enc = self.path_enc_input.text()
        file_key  = self.path_key_input.text()
        password = self.password_label.text()

        if not file_enc:
            raise Exception('khong co file enc')
    
        if file_key:
            with open(file_key, 'r') as f:
                key_enc = json.loads(f.read())

        
        with open(file_enc, 'r') as f:
            data_enc = json.loads(f.read())
        
        data_file = map(Base64Str.from_string, data_enc['file_enc'])
        try:
            data_key = key_enc['key_enc'] if file_key else data_enc['key_enc']
            data_key = Base64Str.from_string(data_key)
        except KeyError:
            gui.announce.lack_key()
            return 
        
        user = user_keys.find_email(self.email_manager)
        private_key_password = Base64Str.from_string(user[0][2])
        
        try:
            logger.security.info('Email: {}'.format(self.email_manager))
            self.data_file_original = file.receive(data_file, data_key, private_key_password, password)
            self.file_name_label.setText(data_enc["ten_file"])
            self.nguoi_gui_label.setText(data_enc["nguoi_gui"])
            self.timestamp_label.setText(data_enc["timestamp"])
            
            logger.user.info(f'tên file: {data_enc["ten_file"]}')
            logger.user.info(f'Nguoi gui: {data_enc["nguoi_gui"]}')
            logger.user.info(f'timestamp: {data_enc["timestamp"]}')
            logger.security.info('Giải mã file thành công')
            self.__save_file()
        except:
            logger.user.exception('Giải mã file thất bại')
            gui.announce.decrypt_file_failed()
        

    def __save_file(self):
        filename, ok = QFileDialog.getSaveFileName(self, 'save file', f'{self.file_name_label.text()}', 'All (*)')
        if filename and ok:
            with open(filename, 'wb') as f:
                f.write(self.data_file_original)

