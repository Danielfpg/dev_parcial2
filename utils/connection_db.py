import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables de entorno desde .env
load_dotenv(dotenv_path="variables.env")

Base = declarative_base ()

# Extraer variables de entorno
USER = os.getenv('CLEVER_USER')
PASSWORD = os.getenv('CLEVER_PASSWORD')
HOST = os.getenv('CLEVER_HOST')
PORT = os.getenv('CLEVER_PORT')
DB_NAME = os.getenv('CLEVER_DATABASE')

# Validar si todas las variables para PostgreSQL están presentes
if all([USER, PASSWORD, HOST, PORT, DB_NAME]):
    DB_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
else:
    # Fallback a SQLite si alguna variable falta
    print("⚠️ Variables de entorno incompletas. Usando SQLite por defecto.")
    DB_URL = "sqlite+aiosqlite:///petsdb.db"

# Crear el engine de conexión
engine = create_async_engine(DB_URL, echo=True)

# Crear el sessionmaker para sesiones asincrónicas
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Crear las tablas en la base de datos
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Proveer una sesión de base de datos
async def get_session():
    async with async_session() as session:
        yield session
