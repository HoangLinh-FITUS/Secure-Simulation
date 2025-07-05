from PySide6.QtWidgets import * 
from PySide6.QtCore import * 
from PySide6.QtGui import * 

from modules.database import email_public_keys, user_keys
from modules.utils.status import *
from modules.utils.qrcode import *
from modules.config import logger

import gui.announce

import json
import os

PIXMAP = (229 + 40, 216 + 40)

class ReadQR(QWidget):
    
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email_manager = email_manager

        self.setWindowTitle(f'Read QR [{email_manager}]')
        self.setFixedWidth(640)

        self.__create_path()
        self.__create_qr()
        self.__create_results()
        self.__create_button()

        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        main_layout.addLayout(self.path_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.qr_pixmap, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(self.group_box)
        main_layout.addStretch()
        main_layout.addWidget(self.btn_add_public_key, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def __create_path(self) -> None:
        self.path_label = QLabel('Path')
        self.path_line = QLineEdit(readOnly=True)
        self.btn_browser = QPushButton('Browse')

        self.path_layout = QHBoxLayout()
        self.path_layout.addWidget(self.path_label)
        self.path_layout.addWidget(self.path_line)
        self.path_layout.addWidget(self.btn_browser)

        self.btn_browser.clicked.connect(self.__open_file)

    def __create_qr(self) -> None:
        self.qr_pixmap = QLabel('None')
        w, h = PIXMAP
        self.qr_pixmap.setFixedSize(w, h)
        self.qr_pixmap.setStyleSheet('border: 1px solid black')

    def __create_results(self) -> None:
        self.group_box  = QGroupBox('Kết Quả Giải Mã')
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

    def __create_button(self) -> None:
        self.btn_add_public_key = QPushButton('Thêm vào danh sách public key ')
        self.btn_add_public_key.clicked.connect(self.__save_public_key)

    def __save_public_key(self) -> None:

        try:
            logger.user.info('{} - {} - {} - {}'
                             .format(self.email_manager, self.email_label.text(), 
                                     self.ngay_tao_label.text(), self.thoihanconlai))

            user = email_public_keys.find(self.email_manager, self.email_label.text())
            if len(user):
                email_public_keys.delete(
                    email_public_keys.Data(*user)
                )

            email_public_keys.insert(
                email_public_keys.Data(
                    email_manager=self.email_manager,
                    public_key=self.public_key_label.text(),
                    email=self.email_label.text(),
                    ngay_tao=self.ngay_tao_label.text(),
                    thoi_han=self.thoihanconlai
                )
            )
            gui.announce.add_public_key_success()
            logger.user.info(f'Lưu Public Key của {self.email_label.text()} - thành công')

        except:
            gui.announce.exists_public_key()
            logger.user.info(f'Lưu Public Key của {self.email_label.text()} - thất bại')
            logger.user.exception('public key da ton tai')
            
        
        
    def update_image(self, filename: str) -> None:
        w, h = PIXMAP
        self.qr_pixmap.setPixmap(QPixmap(filename).scaled(w, h))

    def update_results(self, email: str, ngay_tao: str, thoihanconlai: int, public_key: str) -> None:
        self.email_label.setText(email)
        self.ngay_tao_label.setText(ngay_tao)
        self.thoihanconlai = thoihanconlai
        self.thoihanconlai_label.setText(str(thoihanconlai) + ' Ngày')
        self.public_key_label.setText(public_key)

    def __open_file(self) -> None:
        filename, ok = QFileDialog.getOpenFileName(self, 'open image qr', 'qr.png', 'Image (*.png)')
        if filename and ok:
            self.path_line.setText(filename)
            self.update_image(filename)

            logger.user.info(f'Đọc ảnh qr tại đường dẫn: {filename}')
            
            data = json.loads(read_qr(filename))
            self.update_results(data['email'], data['ngay_tao'], data['thoihanconlai'], data['public_key'])

class GenQR(QWidget):

    filename = 'data/tmp/gen_qr.png'

    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email = email_manager

        self.setWindowTitle(f'Generate QR [{email_manager}]')
        self.setFixedSize(560, 480)

        self.__create_form()
        self.__create_qrcode()
        self.__create_button()

        layout_qr_btn = QVBoxLayout()
        layout_qr_btn.addWidget(self.pixmap, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_qr_btn.addWidget(self.btn_save, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.form)
        main_layout.addSpacing(30)
        main_layout.addLayout(layout_qr_btn)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def __create_form(self) -> None:
        infor_user = user_keys.find_email(self.email)
        self.infor = user_keys.Data(*infor_user[0])

        self.form = QFormLayout()
        self.form.addRow('Email:',               QLabel(self.infor.email))
        self.form.addRow('Ngày tạo:',            QLabel(self.infor.ngay_tao))
        self.form.addRow('Thời hạn còn lại:',    QLabel(str(thoihanconlai(self.infor.ngay_tao, self.infor.thoi_han)) + ' ngày'))
        self.form.addRow('Public key:',          QLineEdit(self.infor.public_key, readOnly=True))

        self.form.setHorizontalSpacing(40)

    def __create_qrcode(self) -> None:
        data = {
            "email": self.infor.email,
            "ngay_tao": self.infor.ngay_tao,
            "thoihanconlai": thoihanconlai(self.infor.ngay_tao, self.infor.thoi_han),
            'public_key': self.infor.public_key
        }
        logger.user.info('Bắt đầu tạo QR ....')
        try:
            create_qr(json.dumps(data), GenQR.filename)
            logger.user.info("Tạo QR - thành công")
        except:
            logger.user.info("Tạo QR - thất bại")

        self.pixmap = QLabel()
        w, h = PIXMAP
        self.pixmap.setPixmap(QPixmap(GenQR.filename).scaled(w, h))

    def __create_button(self) -> None:
        self.btn_save = QPushButton('Save QR')
        self.btn_save.clicked.connect(self.__save_qr)

    def __save_qr(self) -> None:
        filename, ok = QFileDialog.getSaveFileName(self, 'save qr', "qr.png", "Image (*.png);;All Files (*)")
        if filename and ok:
            with open(GenQR.filename, 'rb') as f:
                img = f.read()

            os.remove(GenQR.filename)            
            
            with open(filename, 'wb') as f:
                f.write(img)
            
