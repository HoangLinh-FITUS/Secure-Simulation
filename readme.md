# Hưỡng dẫn chạy chương trình
**Bước 1**: Cài đặt thư viện trên phiên bản `python = 3.11.13`
```
pip install -r requirements.txt 
```

*trường hợp gặp lỗi với thư viện pyzbar `FileNotFoundError: Could not find module 'libzbar-64.dll'` truy cập link để hưỡng dẫn fix lỗi [here](https://github.com/NaturalHistoryMuseum/pyzbar/issues/93)*

**Bước 2**: thêm biến môi trường vào file `.env` giống với `.env.example`
-  `EMAIL_SEND=''` dùng email thật dùng để gửi xác thực OTP.
- `PASSPHRASE=''` sign-in với app password của gmail có thể xem hướng dẫn tại [here](https://support.google.com/mail/answer/185833?hl=en)


**Bước 3**: chạy toàn bộ project bằng lệnh sau:
```
python main.py
```
***tài khoản admin mặc định sẽ là tài khoản đầu tiên đăng ký vào hệ thống.***