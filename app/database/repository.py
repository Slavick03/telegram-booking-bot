from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, WorkingDay, TimeSlot, Booking
from datetime import datetime, time


async def create_booking(session, telegram_id, username, full_name, phone, date_str, time_str):

    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(telegram_id=telegram_id, username=username, full_name=full_name, phone=phone)
        session.add(user)
        await session.flush()


    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    result_work_day = await session.execute(select(WorkingDay).where(WorkingDay.date == date_obj))
    working_day = result_work_day.scalar_one_or_none()


    time_obj = datetime.strptime(time_str, "%H:%M").time()
    result_time_slot = await session.execute(select(TimeSlot).where(TimeSlot.working_day_id == working_day.id, TimeSlot.time == time_obj))
    time_slot = result_time_slot.scalar_one_or_none()

    booking = Booking(user_id=user.id, time_slot_id=time_slot.id)
    time_slot.is_booked = True
    session.add(booking)
    await session.commit()
