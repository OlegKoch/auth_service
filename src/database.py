from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase
import src.config as config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


engine = create_async_engine(
    config.DATABASE_URL,
    poolclass=NullPool, # полезно для docker контейнера
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    pass



async def get_db():
    async with SessionLocal() as session:
        yield session