from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.config import settings

router = Router()

@router.message(Command('admin'))
async def cdm_admin(message: Message):
    if message.from_user.id == settings.ADMIN_TELEGRAM_ID:
        await message.answer('Добро пожаловать в админ панель!')
    else:
        await message.answer('У вас нет доступа')