from datetime import datetime
from sqlalchemy import Integer, String, BigInteger, Boolean, DateTime, Date, Time, ForeignKey, Enum, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    bookings: Mapped[list['Booking']] = relationship(back_populates='user')

class WorkingDay(Base):
    __tablename__ = 'working_days'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(Date, unique=True)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    time_slots: Mapped[list['TimeSlot']] = relationship(back_populates='working_day')


class TimeSlot(Base):
    __tablename__ = 'time_slots'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    working_day_id: Mapped[int] = mapped_column(ForeignKey('working_days.id', ondelete='CASCADE'))
    time: Mapped[datetime] = mapped_column(Time)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    working_day: Mapped['WorkingDay'] = relationship(back_populates='time_slots')
    booking: Mapped['Booking'] = relationship(back_populates='time_slot')

    __table_args__ = (
        UniqueConstraint('working_day_id', 'time', name='uq_working_day_time'),
        )  

class BookingStatus(enum.Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    time_slot_id: Mapped[int] = mapped_column(ForeignKey('time_slots.id', ondelete='CASCADE'))
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.active)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    user: Mapped['User'] = relationship(back_populates='bookings')
    time_slot: Mapped['TimeSlot'] = relationship(back_populates='booking')
    reminder: Mapped['Reminder'] = relationship(back_populates='booking')

class ReminderStatus(enum.Enum):
    pending = 'pending'
    sent = 'sent'
    cancelled = "cancelled"

class Reminder(Base):
    __tablename__ = 'reminders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey('bookings.id', ondelete='CASCADE'))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[ReminderStatus] = mapped_column(Enum(ReminderStatus), default=ReminderStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    booking: Mapped['Booking'] = relationship(back_populates='reminder')
     