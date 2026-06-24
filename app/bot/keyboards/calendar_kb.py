from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_calendar():

    today = datetime.now().date()

    keyboard = []
    row = []
    for i in range(1, 31):
        date = today + timedelta(days=i)
        date_str_display = date.strftime("%d.%m")
        date_str_full = date.strftime("%d.%m.%Y")
        callback_data = f'date_{date_str_full}'

        button = InlineKeyboardButton(text=date_str_display, callback_data=callback_data)
        row.append(button)

        if len(row) == 5:
            keyboard.append(row)
            row = []
        
    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)