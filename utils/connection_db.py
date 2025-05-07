import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
load_dotenv()
Base = declarative_base()
CLEVER_DB=(
    f"postgresql+asyncpg://{os.getenv('CLEVER_USER')}:"
    f"{os.getenv('CLEVER_PASSWORD')}@"
    f"{os.getenv('CLEVER_HOST')}:"
    f"{os.getenv('CLEVER_PORT')}/"
    f"{os.getenv('CLEVER_DATABASE')}"
)
DATABASE_URL= "sqlite+aiosqlite:///petsdb.db"

engine = create_async_engine(CLEVER_DB, echo=True)

async_session =sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session