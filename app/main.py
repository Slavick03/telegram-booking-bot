import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from .bot.handlers import common
from app.scheduler import setup_scheduler


async def main():

    bot = Bot(token=settings.BOT_TOKEN)
    dp  = Dispatcher()

    dp.include_router(common.router)

    setup_scheduler(bot)

    print('Bot started')
    await dp.start_polling(bot)

if __name__ == '__main__':
      asyncio.run(main())