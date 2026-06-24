from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, WorkingDay, TimeSlot, Booking, BookingStatus
from datetime import datetime, time, date, timedelta
from sqlalchemy.orm import selectinload


async def create_booking(session, telegram_id, username, full_name, phone, date_str, time_str):

    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(telegram_id=telegram_id, username=username, full_name=full_name, phone=phone)
        session.add(user)
        await session.flush()


    date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
    result_work_day = await session.execute(select(WorkingDay).where(WorkingDay.date == date_obj))
    working_day = result_work_day.scalar_one_or_none()


    time_obj = datetime.strptime(time_str, "%H:%M").time()
    result_time_slot = await session.execute(select(TimeSlot).where(TimeSlot.working_day_id == working_day.id, TimeSlot.time == time_obj))
    time_slot = result_time_slot.scalar_one_or_none()

    booking = Booking(user_id=user.id, time_slot_id=time_slot.id)
    time_slot.is_booked = True
    session.add(booking)
    await session.commit()

async def get_available_slots(session, date_str):
    date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
    result_work_day = await session.execute(select(WorkingDay).where(WorkingDay.date == date_obj))
    working_day = result_work_day.scalar_one_or_none()

    if working_day is None or working_day.is_closed:
        return []
    
    result_time_slot = await session.execute(select(TimeSlot).where(TimeSlot.working_day_id == working_day.id, TimeSlot.is_booked == False))
    time_slot = result_time_slot.scalars().all()
    return [slot.time.strftime("%H:%M") for slot in time_slot]

async def get_user_bookings(session, telegram_id):
    result_user = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result_user.scalar_one_or_none()

    if user is None:
        return []
    
    user_bookings = await session.execute(select(Booking).where(Booking.user_id == user.id, Booking.status == BookingStatus.active).options(selectinload(Booking.time_slot).selectinload(TimeSlot.working_day)))
    result_booking = user_bookings.scalars().all()
    return result_booking

async def cancel_booking(session, booking_id):
    result = await session.execute(select(Booking).where(Booking.id == booking_id).options(selectinload(Booking.time_slot)))
    booking = result.scalar_one_or_none()

    booking.status = BookingStatus.cancelled
    booking.time_slot.is_booked = False
    await session.commit()

async def get_upcoming_bookings(session):
    tomorrow = date.today() + timedelta(days=1)

    result = await session.execute(select(Booking).join(Booking.time_slot).join(TimeSlot.working_day).where(Booking.status == BookingStatus.active, WorkingDay.date == tomorrow).options(selectinload(Booking.time_slot).selectinload(TimeSlot.working_day), selectinload(Booking.user)))
    bookings = result.scalars().all()
    return bookings

async def get_all_active_bookings(session):
    result  = await session.execute(select(Booking).join(Booking.time_slot).join(TimeSlot.working_day).where(Booking.status == BookingStatus.active).order_by(WorkingDay.date, TimeSlot.time).options(selectinload(Booking.time_slot).selectinload(TimeSlot.working_day), selectinload(Booking.user)))
    bookings = result.scalars().all()
    return bookings

async def add_working_day(session, date_str):
    date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
    working_day = WorkingDay(date=date_obj, is_closed=False)

    session.add(working_day)
    await session.commit()
    return working_day

async def add_time_slot(session, working_day_id, time_str):
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    time_slot = TimeSlot(working_day_id=working_day_id, time=time_obj, is_booked=False)

    session.add(time_slot)
    await session.commit()
    return time_slot

async def close_working_day(session, date_str):
    date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()

    result = await session.execute(select(WorkingDay).where(WorkingDay.date == date_obj))
    working_day = result.scalar_one_or_none()
    if working_day is None:
        return None
    
    working_day.is_closed = True
    await session.commit()
    return working_day       
