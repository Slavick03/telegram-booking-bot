from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_calendar():

    today = datetime.now().date()

    keyboard = []
    row = []
    for i in range(14):
        date = today + timedelta(days=i)
        date_str = date.strftime("%d.%m")
        callback_data = f'date_{date.isoformat()}'

        button = InlineKeyboardButton(text=date_str, callback_data=callback_data)
        row.append(button)

        if len(row) == 7:
            keyboard.append(row)
            row = []
        
    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)