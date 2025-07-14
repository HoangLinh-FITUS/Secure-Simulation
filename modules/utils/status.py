import datetime 
from modules.database import users as users_db, email_public_keys, user_keys

SECOND_OF_A_DAY =24 * 60 * 26 

def hethan(ngaytao: str, 
           thoihan: float # days
) -> str:
    ngaytao      = datetime.datetime.strptime(ngaytao, '%c')
    ngay_hethan  = ngaytao + datetime.timedelta(seconds=thoihan * SECOND_OF_A_DAY)
    return ngay_hethan.strftime("%c")
    
def thoihanconlai(ngaytao: str, thoihan: int) -> int:
    ngay_da_qua =  datetime.datetime.now() - datetime.datetime.strptime(ngaytao, '%c')
    return max(thoihan - ngay_da_qua.days, 0)


def lock_account(
    email: str, 
    is_block: int = 0, 
    time_lock: int = 0 # second 
):
    users = users_db.find_email(email)
    user = users_db.Data(*users[0])
    user.is_block = is_block
    user.thoi_han_block = hethan(datetime.datetime.now().strftime('%c'), time_lock / SECOND_OF_A_DAY)
    users_db.update(user)
    return user

def check_change_public_key(email_manager: str, email: str) -> bool:
    users = user_keys.find_email(email)
    user_current = user_keys.Data(*users[0])

    users = email_public_keys.find(email_manager, email)
    if not len(users):
        raise Exception('khong tom tai email ma email_manager quan ly')
    
    user_save = email_public_keys.Data(*users[0])
    
    return user_save.public_key != user_current.public_key
