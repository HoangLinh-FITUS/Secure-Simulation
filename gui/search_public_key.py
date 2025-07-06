from PySide6.QtWidgets import * 
from PySide6.QtCore import *
from PySide6.QtGui import *
from modules.database import email_public_keys
from modules.utils.status import *
import gui.announce
from modules.utils import qrcode
from modules.config import logger 

from dataclasses import asdict
import json 

PIXMAP = (229 + 40, 216 + 40)

class Search_PublicKey(QWidget):
    
    filename = 'data/tmp/qr.png'

    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email_manager = email_manager

        self.setWindowTitle(f'Search Public Key [{email_manager}]')
        self.setFixedWidth(640)

        self.__create_path()
        self.__create_qr()
        self.__create_results()

        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        main_layout.addLayout(self.path_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.qr_pixmap, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(self.group_box)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def __create_path(self) -> None:
        self.path_label = QLabel('Email')
        self.path_line = QLineEdit()
        self.btn_search = QPushButton('Search')

        self.path_layout = QHBoxLayout()
        self.path_layout.addWidget(self.path_label)
        self.path_layout.addWidget(self.path_line)
        self.path_layout.addWidget(self.btn_search)

        self.btn_search.clicked.connect(self.search_public_key)
        self.path_line.returnPressed.connect(self.search_public_key)
    
    def search_public_key(self):
        search_email = self.path_line.text()

        results = email_public_keys.find(self.email_manager)
        
        for i, row in enumerate(results):
            search_data = email_public_keys.Data(*row)
            
            if search_email == search_data.email:    
                
                if thoihanconlai(search_data.ngay_tao, search_data.thoi_han) == 0:
                    gui.announce.public_key_hethan()
                    return
                if check_change_public_key(self.email_manager, search_data.email):
                    gui.announce.public_key_change()
                    return
                
                self.update_results(search_data.email, search_data.ngay_tao, 
                                    thoihanconlai(search_data.ngay_tao, search_data.thoi_han), 
                                    search_data.public_key)

                search_data = asdict(search_data)
                qrcode.create_qr(json.dumps(search_data), Search_PublicKey.filename)
                self.update_image(Search_PublicKey.filename)
                
                logger.user.info('Tìm Public key của {}'.format(search_email))
                return
            
        logger.user.info('Không tìm thấy public key của {}'.format(search_email))
        gui.announce.dont_find_public_key()

    def __create_qr(self) -> None:
        self.qr_pixmap = QLabel('None')
        w, h = PIXMAP
        self.qr_pixmap.setFixedSize(w, h)
        self.qr_pixmap.setStyleSheet('border: 1px solid black')

    def __create_results(self) -> None:
        self.group_box  = QGroupBox('Kết Quả')
        self.form       = QFormLayout()

        self.email_label            = QLabel('None')
        self.ngay_tao_label         = QLabel('None')
        self.thoihanconlai_label    = QLabel('None')
        self.public_key_label       = QLineEdit(readOnly=True)

        self.form.addRow('Email:',                  self.email_label)
        self.form.addRow('Ngày tạo:',               self.ngay_tao_label)
        self.form.addRow('Thời hạn còn lại:',       self.thoihanconlai_label)
        self.form.addRow('Public key:',             self.public_key_label)
        
        self.form.setHorizontalSpacing(50)
        self.group_box.setLayout(self.form)
    
        
    def update_image(self, filename: str) -> None:
        w, h = PIXMAP
        self.qr_pixmap.setPixmap(QPixmap(filename).scaled(w, h))

    def update_results(self, email: str, ngay_tao: str, thoihanconlai: int, public_key: str) -> None:
        self.email_label.setText(email)
        self.ngay_tao_label.setText(ngay_tao)
        self.thoihanconlai_label.setText(str(thoihanconlai) + ' Ngày')
        self.public_key_label.setText(public_key)

