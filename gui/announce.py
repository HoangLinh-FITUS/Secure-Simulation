from PySide6.QtWidgets import *
from PySide6.QtCore import * 

def sign_up_success() -> None:
     QMessageBox.information(
        None,
        'Information',
        'Đăng kí thành công'
    )
     
def add_public_key_success() -> None:
    QMessageBox.information(
        None,
        'Public Key',
        'Thêm public key thành công'
    )

def update_infor_success() -> None:
    QMessageBox.information(
        None,
        'update information',
        'Cập nhật thông tin tài khoản thành công'
    )

def update_infor_fail() -> None:
    QMessageBox.information(
        None,
        'update information',
        'Cập nhật thông tin tài khoản thất bại'
    )

def update_password_success() -> None:
    QMessageBox.information(
        None,
        'update password',
        'Thay đổi mật khẩu thành công'
    )

def update_password_fail() -> None:
    QMessageBox.information(
        None,
        'update password',
        'Thay đổi mật khẩu thất bại'
    )

def exists_public_key() -> None:
    QMessageBox.information(
        None,
        'Public Key',
        'public key đã tồn tại'
    )

def dont_find_public_key() -> None:
    QMessageBox.critical(None, 'Found', 'Không tìm thấy public key trong danh sách')
    
def full_infor_password() -> None:
    QMessageBox.critical(
        None,
        'change password',
        'phải nhập đầu đủ thông tin password'
    )

def recovery_not_success() -> None:
    QMessageBox.critical(
        None,
        'Khôi phục',
        'khôi phục không thành công'
    )

def strong_password() -> None:
    QMessageBox.critical(
        None,
        'Strong Password',
        'Passphrase phải có độ mạnh tối thiểu (gợi ý: ít nhất 8 ký tự, có chữ hoa, số, ký hiệu) và ít hơn 16 kí tự'
    )

def password_mathces() -> None:
    QMessageBox.critical(
        None,
        'wrong',
        'Password sau khi nhập lại không khớp với password ban đầu'
    )

def exist_email() -> None:
    QMessageBox.critical(
        None,
        'Tài Khoản',
        'Tài Khoản đã tồn tại'
    )

def not_exist_email() -> None:
    QMessageBox.critical(
        None,
        'Tài Khoản',
        'Tài Khoản không tồn tại'
    )

def wr_password() -> None:
    QMessageBox.critical(
        None,
        'Password',
        'Nhập sai password'
    )

def MFA_failed() -> None:
    QMessageBox.critical(
        None,
        'MFA',
        'Xác thực thật bại'
    )

def otp_failed() -> None:
    QMessageBox.critical(
        None,
        'OTP',
        'Gửi OTP thất bại'
    )

def update_key_failed() -> None:
    QMessageBox.critical(None, 'update key', 'Tạo khóa mới thất bại')

def update_key_success() -> None:
    QMessageBox.information(None, 'update key', 'Tạo khóa mới thành công')

def decrypt_file_failed() -> None:
    QMessageBox.critical(None, 'decrypt file', 'Giải mã file thất bại')

def lack_key() -> None:
    QMessageBox.critical(None, 'key file', 'Thiếu Key để giải mã file')

def signature_failed() -> None:
    QMessageBox.critical(None, 'signature file', 'ký số tập tin thất bại')

def verify_sign_faild() -> None:
    QMessageBox.critical(None, 'verify signature', 'xác minh ký số tập tin thất bại (không có public key nào được lưu mà có thể xác minh được)')


class Waiting(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setWindowFlags(Qt.FramelessWindowHint)

        layout = QVBoxLayout()
        label = QLabel('Đang xử lý .....')
        label.setStyleSheet('font-size: 15px; padding: 20px; border-radius: 10px; background-color: white; ')
        layout.addWidget(label)
        self.setStyleSheet("QWidget { border: 1px solid black;}")
        
        self.setLayout(layout)
