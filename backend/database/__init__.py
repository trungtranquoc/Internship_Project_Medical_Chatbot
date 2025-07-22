from .schema.user import UserSchema
from .schema.chat_history import ChatHistorySchema
from .mongo_db import db as mongo_db
from .postgresql_db import PostgreSQLDatabase
import os

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "CHAINLIT_DB")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "CHAINLIT_DB")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "MEDICAL_CHAT_HISTORY")

postgresql_db = PostgreSQLDatabase(f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

__all__ = ["mongo_db", "UserSchema", "ChatHistorySchema", "postgresql_db"]