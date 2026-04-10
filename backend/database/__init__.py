from .schema.user import UserSchema
from .schema.chat_history import ChatHistorySchema
# from .mongo_db import db as mongo_db
from .postgresql_db import PostgreSQLDatabase
from urllib.parse import quote_plus
import os

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

postgresql_db = PostgreSQLDatabase(
    f"postgresql+asyncpg://"
    f"{quote_plus(POSTGRES_USER)}:{quote_plus(POSTGRES_PASSWORD)}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?ssl=require"
)

__all__ = [ "UserSchema", "ChatHistorySchema", "postgresql_db"]