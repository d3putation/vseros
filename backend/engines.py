from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, MetaData
from config import *



async_engine = create_async_engine(
    url=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{5432}/{DB_NAME}",
    echo=True,
)


async_session_factory = async_sessionmaker(async_engine)

metadata_obj = MetaData(schema='ai')
class Base(DeclarativeBase):
    metadata = metadata_obj


    
engine = create_engine(
    url= f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{5432}/{DB_NAME}",
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

sync_session = sessionmaker(engine)


