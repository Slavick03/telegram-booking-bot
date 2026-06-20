from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker)
from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False
)