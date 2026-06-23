from aiogram.fsm.state import State, StatesGroup


class BookingStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_confirmation = State()

class AdminStates(StatesGroup):
    waiting_for_new_day = State()
    waiting_for_slots = State()
    waiting_for_close_day = State()