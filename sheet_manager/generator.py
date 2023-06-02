import hashlib
import pytz
from datetime import datetime

def generate_reg_id(str_input):
    return hashlib.md5(str_input.encode()).hexdigest()

def generate_current_time():
    return datetime.strftime(
        datetime.now(pytz.timezone('Asia/Singapore')),
        '%Y-%m-%dT%H:%M:%S.%f'
    )

