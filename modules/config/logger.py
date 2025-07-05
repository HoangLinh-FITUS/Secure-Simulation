import logging 
import os

DIR_LOGS = 'data/logs/'
LOGIN_LOG_FILE = 'login.log'
BEHAVIOR_LOG_FILE = 'behavior.log'
SECURITY_LOG_FILE = 'security.log'

os.makedirs(DIR_LOGS, exist_ok=True)

def create_logger(name: str, filename: str, level: int = logging.INFO, email: str = None):
    if email:
        os.makedirs(os.path.join(DIR_LOGS, email), exist_ok=True)
        filename = os.path.join(email, filename)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(os.path.join(DIR_LOGS, filename), mode='a', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - [%(name)s]: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


login    = create_logger('login', LOGIN_LOG_FILE)
security = create_logger('security', SECURITY_LOG_FILE)
user     = None
