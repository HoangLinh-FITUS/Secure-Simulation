from dataclasses import dataclass 
from .db_manager import *

@dataclass 
class Data:
    email: str              = ''
    hoten: str              = ''
    ngaysinh: str           = ''
    sdt: str                = ''
    diachi: str             = ''
    passphrase: str         = ''
    ma_khoi_phuc: str       = ''
    is_block: int           = 0         #  or 1
    role: str               = 'user'    #  or admin
    thoi_han_block: str     = 'None'


def insert(infor: Data):
    conn = get_connection()
    cursor = conn.cursor() 

    try:
        sql = "INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, (infor.email, infor.hoten, infor.ngaysinh, infor.sdt, infor.diachi, 
                             infor.passphrase, infor.ma_khoi_phuc, infor.is_block, infor.role, infor.thoi_han_block))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception('insert users bi trung')
    finally:
        conn.close()

def update(infor: Data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = 'UPDATE USERS SET HOTEN = ?, NGAYSINH = ?, SDT = ?, DIACHI = ?, PASSPHRASE = ?, MA_KHOI_PHUC = ?, IS_BLOCK = ?, ROLE = ?, THOI_HAN_BLOCK = ? WHERE EMAIL = ?'
        cursor.execute(sql, (infor.hoten, infor.ngaysinh, infor.sdt, infor.diachi, 
                             infor.passphrase, infor.ma_khoi_phuc, infor.is_block, 
                             infor.role, infor.thoi_han_block, infor.email))
        conn.commit()
    except:
        raise Exception('update users that bai')
    finally:
        conn.close()

def find_email(email: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'SELECT * FROM USERS WHERE EMAIL = ?'
    cursor.execute(sql, (email,))
    
    results = cursor.fetchall()
    conn.close()

    return results

def select_all() -> list:
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'SELECT * FROM USERS'
    cursor.execute(sql)
    
    results = cursor.fetchall()
    conn.close()

    return results
