from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import config

engine = create_async_engine(
    config.DATABASE_URL, 
    echo=False
)

async_session: async_sessionmaker = async_sessionmaker(
    engine,
    class_= AsyncSession, 
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    return async_session()
        
Base = declarative_base()
