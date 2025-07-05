from PySide6.QtWidgets import *
from PySide6.QtCore import *

from modules.database import users as users_db
from modules.config import logger 


class ViewAccounts(QWidget):
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f'View Accounts [{email_manager}]')
        self.resize(900, 500)

        self.accounts_all = [users_db.Data(*acc) for acc in users_db.select_all()]
        self.accounts = self.accounts_all.copy()

        self.create_view()

    def create_view(self):
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        self.email_filter = QLineEdit()
        self.email_filter.setPlaceholderText("Lọc theo Email...")
        self.email_filter.textChanged.connect(self.filter_email)
        filter_layout.addWidget(QLabel("Tìm Email:"))
        filter_layout.addWidget(self.email_filter)
        layout.addLayout(filter_layout)

        self.table_account = QTableWidget()
        self.table_account.setColumnCount(8)
        self.table_account.setHorizontalHeaderLabels([
            'Email', 'Họ tên', 'Ngày sinh', 'SĐT', 'Địa chỉ', 'Trạng thái', 'Vai trò', 'thời hạn block tài khoản'
        ])       

        self.table_account.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_account.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_account.setSelectionMode(QAbstractItemView.SingleSelection)
        
        header = self.table_account.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)

        layout.addWidget(self.table_account)

        btn_layout = QHBoxLayout()
        self.btn_toggle_block = QPushButton("Khóa / Mở khóa")
        self.btn_change_role = QPushButton("Phân quyền")

        self.btn_toggle_block.clicked.connect(self.toggle_block)
        self.btn_change_role.clicked.connect(self.change_role)

        btn_layout.addWidget(self.btn_toggle_block)
        btn_layout.addWidget(self.btn_change_role)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table_account.setRowCount(len(self.accounts))
        for row, acc in enumerate(self.accounts):
            email_item = QTableWidgetItem(acc.email)
            email_item.setToolTip(acc.email)  
            self.table_account.setItem(row, 0, email_item)
            self.table_account.setItem(row, 1, QTableWidgetItem(acc.hoten))
            self.table_account.setItem(row, 2, QTableWidgetItem(acc.ngaysinh))
            self.table_account.setItem(row, 3, QTableWidgetItem(acc.sdt))
            self.table_account.setItem(row, 4, QTableWidgetItem(acc.diachi))
            self.table_account.setItem(row, 5, QTableWidgetItem("Bị khóa" if acc.is_block else "Hoạt động"))
            self.table_account.setItem(row, 6, QTableWidgetItem(acc.role))
            self.table_account.setItem(row, 7, QTableWidgetItem(acc.thoi_han_block))

    def get_selected_account_index(self):
        selected = self.table_account.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Chưa chọn dòng", "Vui lòng chọn 1 tài khoản.")
            return None
        return selected

    def toggle_block(self):
        index = self.get_selected_account_index()
        if index is not None:
            acc = self.accounts[index]
            acc.is_block = 0 if acc.is_block else 1
            self.load_data()

            logger.user.info(f'{acc.email}' + '- ' + ('Unblock' if acc.is_block else 'block') +  ' account')

            users_db.update(acc)

    def change_role(self):
        index = self.get_selected_account_index()
        if index is not None:
            acc = self.accounts[index]
            acc.role = 'admin' if acc.role == 'user' else 'user'
            self.load_data()
            logger.user.info(f'{acc.email} thay đổi role thành {acc.role}')
            users_db.update(acc)
            

    def filter_email(self, text):
        keyword = text.strip().lower()
        if keyword == '':
            self.accounts = self.accounts_all.copy()
        else:
            self.accounts = [
                acc for acc in self.accounts_all
                if keyword in acc.email.lower()
            ]
        self.load_data()



