from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_TELEGRAM_ID: int
    NOTIFICATION_CHANNEL_ID: int
    REQUIRED_CHANNEL_ID: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432

    @property
    def database_url(self):
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        db = self.POSTGRES_DB
        return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'

    class Config:
        env_file = ".env"
settings = Settings()