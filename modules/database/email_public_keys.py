from modules.database.db_manager import *
from dataclasses import dataclass 
from typing import overload 

@dataclass
class Data:
    email_manager: str      = ''
    email: str              = ''
    public_key: str         = ''
    ngay_tao: str           = ''
    thoi_han: int           = 0

@overload
def find(email_manager: str) -> list[tuple]: ...
@overload 
def find(email_manager: str, email: str) -> list[tuple]: ...

def find(email_manager: str, email: str = None):
    conn = get_connection()
    cursor = conn.cursor()

    if email is None:
        sql = 'SELECT * FROM EMAIL_PUBLIC_KEYS WHERE EMAIL_MANAGER = ?'
        cursor.execute(sql, (email_manager, ))
    else:
        sql = 'SELECT * FROM EMAIL_PUBLIC_KEYS WHERE EMAIL_MANAGER = ? AND EMAIL = ?'
        cursor.execute(sql, (email_manager, email))

    conn.commit()
    results = cursor.fetchall()
    conn.close()
    
    return results


def insert(infor: Data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = 'INSERT INTO EMAIL_PUBLIC_KEYS VALUES (?, ?, ?, ?, ?)'
        cursor.execute(sql, (infor.email_manager, infor.email, infor.public_key, 
                             infor.ngay_tao, infor.thoi_han))
        conn.commit()
    except:
        raise Exception('khong the insert vao trong table EMAIL_PUBLIC_KEYS')
    finally:
        conn.close()

def delete(infor: Data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = 'DELETE FROM EMAIL_PUBLIC_KEYS WHERE EMAIL_MANAGER = ? AND EMAIL = ?'
        cursor.execute(sql, (infor.email_manager, infor.email))
        conn.commit()
    except:
        raise Exception('khong the delete item trong table EMAIL_PUBLIC_KEYS')
    finally:
        conn.close()


    