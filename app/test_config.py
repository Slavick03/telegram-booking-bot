from app.config import settings

print(f"Bot token: {settings.BOT_TOKEN}")
print(f"Admin ID: {settings.ADMIN_TELEGRAM_ID}")
print(f"Notification ID: {settings.NOTIFICATION_CHANNEL_ID}")
print(f"Chanel ID: {settings.REQUIRED_CHANNEL_ID}")
print(f"PG User: {settings.POSTGRES_USER}")
print(f"PG Password: {settings.POSTGRES_PASSWORD}")
print(f"PG BD: {settings.POSTGRES_DB}")
print(f"PG Host: {settings.POSTGRES_HOST}")
print(f"PG Port: {settings.POSTGRES_PORT}")