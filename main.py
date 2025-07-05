import sys

from PySide6.QtWidgets import * 

from modules.database import db_manager, users as users_db
from modules.config import logger 

import gui


class App(QWidget):

    def __init__(self):
        super().__init__()
        db_manager.init_db()
        sign_in = gui.sign_in.SignIn()
        sign_in.exec()

        if sign_in.check_success():
            self.email_manager = sign_in.email
            logger.login.info('{} - Đăng nhập - thành công'.format(self.email_manager))
            self.create_admin()
            
            self.set_login_user()
            self.start_menu()
        else:
            sys.exit(0)

    def start_menu(self):
        user = users_db.find_email(self.email_manager)
        user = users_db.Data(*user[0])
        self.menu = gui.menu.Menu(user.email, user.role)
        self.menu.show()

    def create_admin(self):
        users = users_db.select_all()
        if len(users) != 1:
            return 
        
        user = users_db.Data(*users[0])
        user.role = 'admin'
        users_db.update(user)

    def set_login_user(self):
        logger.user = logger.create_logger('behavior', logger.BEHAVIOR_LOG_FILE, email=self.email_manager) 

if __name__ == '__main__':
    app = QApplication()
    window = App()
    sys.exit(app.exec())