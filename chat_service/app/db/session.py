import os
from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


# in case of scripts then main.py won't activate and the env variables won't load
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

DATABASE_URL = os.environ.get("CHAT_DB_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class BaseRead(DeclarativeBase):
    """for models reading from existing django models"""

    pass


class BaseWrite(DeclarativeBase):
    """for db tables that chat_service microservice might own"""

    pass
