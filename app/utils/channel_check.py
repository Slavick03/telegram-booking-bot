from aiogram import Bot

async def check_subscription(bot: Bot, user_id: int, channel_id: str) -> bool:
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        return member.status in ['creator', 'administrator', 'member']
    except Exception:
        return False