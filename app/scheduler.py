from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.engine import async_session_maker
from app.database.repository import get_upcoming_bookings


async def send_reminders(bot):
    async with async_session_maker() as session:
        bookings = await get_upcoming_bookings(session)
        for booking in bookings:
            await bot.send_message(chat_id=booking.user.telegram_id, text=f"⏰ Напоминание! Завтра у вас запись.\nДата: {booking.time_slot.working_day.date}\nВремя: {booking.time_slot.time.strftime('%H:%M')}")
    
def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=send_reminders,
                      trigger='cron',
                      hour=10,
                      minute=0,
                      args=[bot])
    scheduler.start()
    return scheduler
    