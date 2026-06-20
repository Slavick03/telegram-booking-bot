from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Записаться', callback_data='book')],
        [InlineKeyboardButton(text='Отменить запись', callback_data='cancel')],
        [InlineKeyboardButton(text='Прайсы', callback_data='prices')],
        [InlineKeyboardButton(text='Портфолио', callback_data='portfolio')],])
    return keyboard

def subscription_keyboard(channel_url: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подписаться', url=channel_url)],
        [InlineKeyboardButton(text='Проверить подписку', callback_data='check_subscription')]
    ])
    return keyboard

def time_slots_keyboard(slots: list):
    keyboard = []

    for slot in slots:
        callback_data = f'time_{slot}'
        button = InlineKeyboardButton(text=slot, callback_data=callback_data)
        keyboard.append([button])



    return InlineKeyboardMarkup(inline_keyboard=keyboard)