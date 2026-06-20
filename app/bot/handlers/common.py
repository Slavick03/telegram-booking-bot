import asyncio
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import Command
from app.bot.keyboards.user_kb import main_menu, subscription_keyboard, time_slots_keyboard
from app.bot.keyboards.calendar_kb import generate_calendar
from app.utils.channel_check import check_subscription
from app.config import settings
from aiogram.fsm.context import FSMContext
from app.bot.states import BookingStates
from app.database.repository import create_booking, get_available_slots, get_user_bookings, cancel_booking
from app.database.engine import async_session_maker


router = Router()
@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Привет! Я бот для записи к мастеру.', reply_markup=main_menu())

@router.callback_query(F.data == 'prices')
async def show_prices(callback: CallbackQuery):
    await callback.message.answer('💰 Прайс-лист:\n\nФренч — 1000₽\nКвадрат — 500₽')
    await callback.answer()

@router.callback_query(F.data == 'portfolio')
async def show_portfolio(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Смотреть портфолио', url='https://ru.pinterest.com/crystalwithluv/_created/')],])
    await callback.message.answer('Вот тут можете посмотреть наши работы', reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == 'book')
async def book_handler(callback: CallbackQuery, state: FSMContext):
    
    bot = callback.bot
    is_subscribed = await check_subscription(
        bot, callback.from_user.id,
        settings.REQUIRED_CHANNEL_ID)

    if is_subscribed:
        await state.set_state(BookingStates.waiting_for_date)
        await callback.message.answer('Отлично! Выберите дату для записи:', reply_markup=generate_calendar())
        await callback.answer()
        return
    else:
        channel_url = f"https://t.me/{settings.REQUIRED_CHANNEL_ID.replace('@', '')}"
        await callback.message.answer('Чтобы записаться к мастеру надо быть подписанным на канал', reply_markup=subscription_keyboard(channel_url))
        await callback.answer()

@router.callback_query(F.data.startswith('date_'))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    date_str = callback.data.replace('date_', '')
    await state.update_data(selected_date=date_str)
    await state.set_state(BookingStates.waiting_for_time)
    async with async_session_maker() as session:
        slots = await get_available_slots(session, date_str)
    if not slots:
        await callback.message.answer('На эту дату нет доступных слотов')
        await callback.answer()
        return
    await callback.message.answer(f'Вы выбрали дату:{date_str}\n\nТеперь выберите время:', reply_markup=time_slots_keyboard(slots))
    await callback.answer()

@router.callback_query(F.data.startswith('time_'), BookingStates.waiting_for_time)
async def choose_time(callback: CallbackQuery, state: FSMContext):
    time_str = callback.data.replace('time_', '')
    await state.update_data(selected_time=time_str)
    await state.set_state(BookingStates.waiting_for_name)
    await callback.message.answer(f'Вы выбрали время:{time_str}\n\nТеперь введите имя:')
    await callback.answer()

@router.message(BookingStates.waiting_for_name)
async def enter_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(BookingStates.waiting_for_phone)
    await message.answer(f'Введите ваш номер телефона:')

@router.message(BookingStates.waiting_for_phone)
async def enter_phone(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    await state.set_state(BookingStates.waiting_for_confirmation)
    data = await state.get_data()
    await message.answer(f"Дата: {data['selected_date']}\nВремя: {data['selected_time']}\nИмя: {data['name']}\nТелефон: {phone}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подтвердить', callback_data='confirm_booking')],
        [InlineKeyboardButton(text='Отменить', callback_data='cancel_booking')],
    ])
    await message.answer(f"Подтвердите запись:", reply_markup=keyboard)

@router.callback_query(F.data == 'confirm_booking', BookingStates.waiting_for_confirmation)
async def confirm_booking(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    async with async_session_maker() as session:
        await create_booking(session, callback.from_user.id, callback.from_user.username, callback.from_user.full_name, data['phone'], data['selected_date'], data['selected_time'])
        await state.clear()
        await callback.message.answer('Запись подтверждена!')
        await callback.answer()

@router.callback_query(F.data == 'cancel')
async def cancel_booking_command(callback: CallbackQuery):
    async with async_session_maker() as session:
        bookings = await get_user_bookings(session, callback.from_user.id)
        if not bookings:
            await callback.message.answer('У вас нет активных записей')
            await callback.answer()
            return
        rows = []
        for booking in bookings:
            text = f"{booking.time_slot.working_day.date} {booking.time_slot.time.strftime('%H:%M')}"
            button = InlineKeyboardButton(text=text, callback_data=f"cancel_booking_{booking.id}")
            rows.append([button])
        keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
        await callback.message.answer('Выберите запись для отмены:', reply_markup=keyboard)
        await callback.answer()
        
@router.callback_query(F.data.startswith('cancel_booking_'))
async def cancel_booking_button(callback: CallbackQuery):
    booking_id = int(callback.data.replace('cancel_booking_', ''))

    async with async_session_maker() as session:
        await cancel_booking(session, booking_id)
        await callback.message.answer('Запись отменена')
        await callback.answer()



    

