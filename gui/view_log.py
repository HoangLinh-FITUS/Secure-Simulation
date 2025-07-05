from PySide6.QtWidgets import *
from PySide6.QtCore import * 
import os 
from modules.config import logger

class ViewLog(QWidget):
    def __init__(self, email_manager: str, parent=None):
        super().__init__(parent)
        
        self.email_manager = email_manager

        self.setWindowTitle(f'View log [{email_manager}]')        
        self.setFixedSize(1000, 500)
        self.create_view_log()

    def create_view_log(self):
        
        self.list_log = QListWidget()
        self.log_view = QTextEdit(readOnly=True)

        for root, dirs, files in os.walk(logger.DIR_LOGS):
            for filename in files:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, logger.DIR_LOGS)
                self.list_log.addItem(relative_path)

        
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.list_log, 2)
        main_layout.addWidget(self.log_view, 5)

        self.setLayout(main_layout)

        self.list_log.itemClicked.connect(self.open_log)

    def open_log(self, item):
        logger.user.info(f'Xem log: {item.text()}')
        filename = os.path.join(logger.DIR_LOGS, item.text())
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.log_view.setPlainText(f.read())
        except Exception as e:
            self.log_view.setPlainText(f"Failed to open file:\n{str(e)}")


