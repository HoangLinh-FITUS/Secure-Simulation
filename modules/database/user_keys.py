from dataclasses import dataclass 
from .db_manager import get_connection 
from .db_manager import *

@dataclass
class Data:
    email: str                              = ''
    public_key: str                         = ''
    private_key_password: str               = ''
    private_key_recovery: str               = ''
    ngay_tao: str                           = ''
    thoi_han: int                           = 90
    len_key: int                            = 2048

def insert(infor: Data) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = 'INSERT INTO USER_KEYS VALUES (?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, (infor.email, infor.public_key, infor.private_key_password, 
                      infor.private_key_recovery, 
                      infor.ngay_tao, infor.thoi_han, infor.len_key))
        conn.commit()
    except:
        raise Exception('then user_keys bi trung')
    finally:
        conn.close() 

def find_email(email: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'SELECT * FROM USER_KEYS WHERE EMAIL = ?'
    cursor.execute(sql, (email, ))
    conn.commit()

    users = cursor.fetchall()
    conn.close()

    return users

def update(infor: Data) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = 'UPDATE USER_KEYS SET PUBLIC_KEY = ?, PRIVATE_KEY_PASSWORD = ?, PRIVATE_KEY_RECOVERY = ?, NGAY_TAO = ?, THOI_HAN = ?, LEN_KEY = ?  WHERE EMAIL= ?'
        cursor.execute(sql, (infor.public_key, infor.private_key_password, 
                      infor.private_key_recovery, 
                      infor.ngay_tao, infor.thoi_han, infor.len_key, infor.email))
        conn.commit()
    except:
        raise Exception('update USER_KEYS that bai')
    finally:
        conn.close()

def delete(email: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = 'DELETE FROM USER_KEYS WHERE EMAIL= ?'
        cursor.execute(sql, (email, ))
        conn.commit()
    except:
        raise Exception(f'delete {email} from USER_KEYS that bai')
    finally:
        conn.close()
   
