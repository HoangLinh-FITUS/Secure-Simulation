import sqlite3
from modules.config.settings import DATABASE
from .model import * 

def __create_table(table_query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(table_query)
        conn.commit()
    except:
        print('table trong db da dc tao truoc do')
    finally:
        conn.close()

def init_db():
    __create_table(table_users)
    __create_table(table_user_keys)
    __create_table(table_email_public_keys)

def get_connection():
    return sqlite3.connect(DATABASE['path'])

