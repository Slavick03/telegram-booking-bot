import re
from datetime import datetime


def validate_phone(phone: str) -> bool:
    phone_str = phone.replace(' ', '').replace('-', '')
    phone = re.match(r'^(\+373)\d{8}$', phone_str)
    return bool(phone)

def validate_name(name: str) -> bool:
    if not 2 <= len(name) <= 50:
        return False
    return bool(re.match(r'^[а-яёА-ЯЁa-zA-Z\s]+$', name))

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False