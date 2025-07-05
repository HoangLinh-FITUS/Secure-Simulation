from PySide6.QtWidgets import * 
from PySide6.QtCore import * 
from PySide6.QtGui import * 

from modules.database import user_keys
from modules.utils.status import *
from modules.account import info
from modules.config import logger 

import gui 

class ManagerKey(QWidget):
    HEIGHT_WINDOW   = 447
    WIDTH_WINDOW    = 640

    EXTEND_DAYS = 90 

    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.email = email_manager
    
        self.setWindowTitle(f'Quản Lý Khóa Cá Nhân [{email_manager}]')
        self.setFixedSize(ManagerKey.WIDTH_WINDOW, ManagerKey.HEIGHT_WINDOW)

        self.__create_information()
        self.__create_key()
        self.__create_button()

        btns = QHBoxLayout()
        btns.addWidget(self.btn_tao_khoa)
        btns.addWidget(self.btn_gia_han)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.form_layout)
        main_layout.addSpacing(50)
        main_layout.addLayout(self.grid_layout)
        main_layout.addStretch()
        main_layout.addLayout(btns)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def __create_information(self) -> None:
        infor_user_keys = user_keys.find_email(self.email)
        
        self.infor = user_keys.Data(*infor_user_keys[0])

        self.ngaytao_label          = QLabel(self.infor.ngay_tao)
        self.ngayhethan_label       = QLabel(hethan(self.infor.ngay_tao, self.infor.thoi_han))
        self.thoihanconlai_label    = QLabel(str(thoihanconlai(self.infor.ngay_tao, self.infor.thoi_han)) + ' ngày')

        t = thoihanconlai(self.infor.ngay_tao, self.infor.thoi_han)
        self.trang_thai_label       = QLabel('hết hạn' if t <= 0 else ('gần hết hạn' if t < 20 else 'còn hạn'))

        self.form_layout = QFormLayout()
        self.form_layout.addRow('Email: ',                  QLabel(self.infor.email))
        self.form_layout.addRow('Ngày tạo (mm/dd/yy): ',    self.ngaytao_label)
        self.form_layout.addRow('Hết hạn (mm/dd/yy): ',     self.ngayhethan_label)
        self.form_layout.addRow('Thời gian còn lại: ',      self.thoihanconlai_label)
        self.form_layout.addRow('Trạng thái: ',             self.trang_thai_label)
        self.form_layout.addRow('Kích thước key: ',         QLabel(str(self.infor.len_key)))

        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setHorizontalSpacing(40)

    def __create_key(self) -> None:
        self.btn_export_public_key      = QPushButton('Download')
        self.btn_export_private_key     = QPushButton('Download')

        self.public_key_label           = QLineEdit(self.infor.public_key,              readOnly=True)
        self.private_key_label          = QLineEdit(self.infor.private_key_password,    readOnly=True)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(QLabel('Public Key:'),            0, 0)
        self.grid_layout.addWidget(QLabel('Private Key:'),           1, 0)
        self.grid_layout.addWidget(self.public_key_label,            0, 1)
        self.grid_layout.addWidget(self.private_key_label,           1, 1)
        self.grid_layout.addWidget(self.btn_export_public_key,       0, 2)
        self.grid_layout.addWidget(self.btn_export_private_key,      1, 2)

        self.btn_export_public_key.clicked.connect(self.__save_public_key)
        self.btn_export_private_key.clicked.connect(self.__save_private_key)

    def __create_button(self) -> None:
        self.btn_gia_han = QPushButton(f'Gia hạn thêm {ManagerKey.EXTEND_DAYS} ngày')
        self.btn_gia_han.clicked.connect(self.__update_thoi_han)

        self.btn_tao_khoa = QPushButton(f'Tạo khóa mới')
        self.btn_tao_khoa.clicked.connect(self.__update_khoa_moi)


    def __save_private_key(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(self, "Lưu khóa riêng", "private_key.txt", "Text Files (*.txt);;All Files (*)")
        
        if filename:
            with open(filename, 'w') as file:
                file.write(self.infor.private_key_password)
    
    def __save_public_key(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(self, "Lưu khóa công khai", "public_key.txt", "Text Files (*.txt);;All Files (*)")
        
        if filename:
            with open(filename, 'w') as file:
                file.write(self.infor.public_key)

    def update_load_data(self):
        infor_user_keys = user_keys.find_email(self.email)
        infor = user_keys.Data(*infor_user_keys[0])
        
        self.ngaytao_label.setText(infor.ngay_tao)
        self.ngayhethan_label.setText(hethan(infor.ngay_tao, infor.thoi_han))
        self.thoihanconlai_label.setText(str(thoihanconlai(infor.ngay_tao, infor.thoi_han)) + ' ngày')

        t = thoihanconlai(infor.ngay_tao, infor.thoi_han)
        self.trang_thai_label.setText('hết hạn' if t <= 0 else ('gần hết hạn' if t < 20 else 'còn hạn'))
        
        self.public_key_label.setText(infor.public_key)
        self.private_key_label.setText(infor.private_key_password)


    def __update_thoi_han(self) -> None:
        infor_user_keys = user_keys.find_email(self.email)
        self.infor = user_keys.Data(*infor_user_keys[0])
        self.infor.thoi_han += ManagerKey.EXTEND_DAYS

        try:
            user_keys.update(self.infor)
            logger.user.info(f'Gia hạn khóa thêm {ManagerKey.EXTEND_DAYS}')
        except:
            logger.user.exception(f'Gia hạn khóa thêm {ManagerKey.EXTEND_DAYS} thất bại')
        
        self.update_load_data()

    def __update_khoa_moi(self) -> None:
        password, ok_pwd = QInputDialog.getText(None, 'password', 'Nhập mật khẩu: ') 
        pin, ok_pin      = QInputDialog.getText(None, 'Pin', 'Nhập mã khôi phục: ')
        if not ok_pwd or not ok_pin: return 
        logger.user.info('Nhập password')
        logger.user.info('Nhập mã khôi phục')

        try:
            info.change_key(self.email, password, pin)
            logger.user.info(f'Tạo khóa mới thành công')
            
            gui.announce.update_key_success()
        except:
            logger.user.warning(f'Tạo khóa mới thất bại')
            gui.announce.update_key_failed()
        
        self.update_load_data()

