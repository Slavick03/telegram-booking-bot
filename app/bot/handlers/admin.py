import asyncio
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.config import settings
from app.bot.keyboards.user_kb import admin_menu
from aiogram import F
from app.database.repository import get_all_active_bookings, add_working_day, add_time_slot, close_working_day
from app.database.engine import async_session_maker
from aiogram.fsm.context import FSMContext
from app.bot.states import AdminStates


router = Router()

@router.message(Command('admin'))
async def cdm_admin(message: Message):
    if message.from_user.id == settings.ADMIN_TELEGRAM_ID:
        await message.answer('Добро пожаловать в админ панель!', reply_markup=admin_menu())
    else:
        await message.answer('У вас нет доступа')

@router.callback_query(F.data == 'admin_bookings')
async def get_all_active_bookings_admin(callback: CallbackQuery):

    if callback.from_user.id != settings.ADMIN_TELEGRAM_ID:
        await callback.answer('У вас нет доступа')
        return

    async with async_session_maker() as session:
        active_bookings = await get_all_active_bookings(session)
        if not active_bookings:
            await callback.message.answer('Нет активных записей')
            await callback.answer()
            return
        await callback.message.answer('Существующие записи:')
        for booking in active_bookings:
            show_booking = f"Дата:{booking.time_slot.working_day.date}\nВремя:{booking.time_slot.time.strftime('%H:%M')}\nИмя:{booking.user.full_name}\nТелефон:{booking.user.phone}"
            await callback.message.answer(show_booking)
        await callback.answer()


@router.callback_query(F.data == 'admin_add_day')
async def admin_add_day(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != settings.ADMIN_TELEGRAM_ID:
        await callback.answer('У вас нет доступа')
        return
    await state.set_state(AdminStates.waiting_for_new_day)
    await callback.message.answer('Введите дату в формате ГГГГ-ММ-ДД:')

@router.message(AdminStates.waiting_for_new_day)
async def add_day(message: Message, state: FSMContext):
    date_str = message.text
    async with async_session_maker() as session:
        working_day = await add_working_day(session, date_str)
        await state.update_data(working_day_id=working_day.id)
        await state.set_state(AdminStates.waiting_for_slots)

        await message.answer(f'Рабочий день {date_str} добавлен! Теперь введите временные слоты через запятую (например: 10:00,11:00,12:00)')
        
@router.message(AdminStates.waiting_for_slots)
async def add_slots(message: Message, state: FSMContext):

    data = await state.get_data()
    working_day_id = data['working_day_id']
    time_slots = message.text.split(',')
    for time_slot in time_slots:
        async with async_session_maker() as session:
            await add_time_slot(session, working_day_id, time_slot.strip())
    await message.answer('Слоты добавлены!')
    await state.clear()

@router.callback_query(F.data == 'admin_close_day')
async def close_working_days(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != settings.ADMIN_TELEGRAM_ID:
        await callback.answer('У вас нет доступа')
        return
    
    await state.set_state(AdminStates.waiting_for_close_day)
    await callback.message.answer('Введите дату для закрытия в формате ГГГГ-ММ-ДД:')

@router.message(AdminStates.waiting_for_close_day)
async def close_day(message: Message, state: FSMContext):
    date_str = message.text
    async with async_session_maker() as session:
        close_date = await close_working_day(session, date_str)
        if close_date is None:
            await message.answer('День не найден')
            await state.clear()
            return
        await message.answer(f'День {date_str} закрыт')
        await state.clear()


    