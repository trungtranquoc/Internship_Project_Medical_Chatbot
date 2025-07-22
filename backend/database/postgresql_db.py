from databases import Database
from .schema import ChatHistorySchema
from .postgresql_serialize import serialize_db_row, serialize_db_rows

import os
from datetime import datetime
import uuid
from typing import Any, Dict
import json

class PostgreSQLDatabase:
    """
    Class to handle PostgreSQL database connections.
    """
    def __init__(self, database_url: str):
        self.database = Database(database_url)

    async def connect(self):
        """
        Connect to the PostgreSQL database.
        """
        await self.database.connect()

    async def disconnect(self):
        """
        Disconnect from the PostgreSQL database.
        """
        await self.database.disconnect()

    async def _all_users(self) -> list:
        """
        Retrieve all users from the database.
        """
        users = await self.database.fetch_all("SELECT * FROM users")
        # Convert to list of dicts and serialize UUID objects
        return serialize_db_rows(users)

    async def _create_user(self, username: str, password: str, name: str, role: str = "user") -> Dict[str, Any]:
        """
        Create a new user in the database.
        """
        if not username or not password:
            raise ValueError("Username and password are required")

        existing_user = await self.database.fetch_one("SELECT * FROM users WHERE identifier = :username", {"username": username})
        
        if existing_user:
            raise ValueError("Username already exists")

        user_id = str(uuid.uuid4())

        query = """INSERT INTO users ("id", "identifier", "metadata", "password", "createdAt") VALUES (:id, :identifier, :metadata, :password, :createdAt)"""
        values = {
            "id": user_id,
            "identifier": username,
            "metadata": json.dumps({"name": name, "role": role}),
            "password": password,
            "createdAt": datetime.now().isoformat()
        }
        
        await self.database.execute(query=query, values=values)
        
        return {"message": "User created successfully", "user_id": user_id}

    async def _conversation_retrieve(self, filter_command: str, sorted: str = "ASC", max_length: int = 100, page: int = 1) -> tuple[list, list]:
        """
        Retrieve conversations based on a filter command.
        """
        
        user_query = f"""SELECT * FROM steps WHERE \
            "type" = 'user_message' \
            AND {filter_command} \
            ORDER BY "createdAt" {sorted} LIMIT {max_length} OFFSET {(page - 1) * max_length}
"""
        assistant_answer = f"""SELECT * FROM steps WHERE \
            "type" = 'assistant_message' AND {filter_command} \
            ORDER BY "createdAt" {sorted} LIMIT {max_length} OFFSET {(page - 1) * max_length}
"""

        user_history = await self.database.fetch_all(user_query)
        assistant_history = await self.database.fetch_all(assistant_answer)
        
        return serialize_db_rows(user_history), serialize_db_rows(assistant_history)
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login a user by verifying username and password.
        Returns user details if successful.
        """
        if not username or not password:
            raise ValueError("Username and password are required")

        user = await self.database.fetch_one("SELECT * FROM users WHERE identifier = :username AND password = :password", 
                                              {"username": username, "password": password})
        
        if not user:
            raise ValueError("Wrong username or password")
        
        return serialize_db_row(user)
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve a user by their ID.
        """
        user = await self.database.fetch_one("SELECT * FROM users WHERE id = :id", {"id": user_id})
        if not user:
            raise ValueError("User not found")
        
        return serialize_db_row(user)

    async def retrieve_history(self, thread_id: str = None, user_id: str = None, max_length: int = 10, page: int = 1) -> list[ChatHistorySchema]:
        """
        Retrieve chat history on specific thread or all threads of a user.
        """
        if not thread_id and not user_id:
            raise ValueError("Either thread_id or user_id must be provided.")
        if thread_id:
            filter_command = f""""threadId" = \'{thread_id}\'"""
        else:
            filter_command = f""""threadId" IN (SELECT "id" FROM threads WHERE "userId" = \'{user_id}\')"""
            
        user_history, assistant_history = await self._conversation_retrieve(filter_command, max_length=max_length, page=page)

        history = []
        for user_step, assistant_step in zip(user_history, assistant_history):
            history.append(ChatHistorySchema(
                user_id=user_step["name"],
                query=user_step["output"],
                answer=assistant_step["output"],
                timestamp=user_step["createdAt"]
            ))

        return history
    
    async def retrieve_context(self, thread_id: str, max_length: int = 3) -> list:
        """
        Retrieve list of chat history entries for a specific thread.
        """
        filter_command = f""""threadId" = \'{thread_id}\'"""
        user_history, assistant_history = await self._conversation_retrieve(filter_command, sorted="DESC", max_length=max_length)

        history = []
        for user_step, assistant_step in zip(user_history[::-1], assistant_history[::-1]):
            history.extend([
                {
                    "role": "user",
                    "content": user_step["output"],
                }, 
                {
                    "role": "assistant",
                    "content": assistant_step["output"].split("### 🗂️ Related questions:")[0].strip() if "### 🗂️ Related questions:" in assistant_step["output"] else assistant_step["output"],
                }
            ])
        return history  # Reverse the order to get the earlest first 
    
    async def delete_history(self, thread_id: str = None, user_id: str = None):
        """
        Delete chat history for a specific thread or user.
        """
        if thread_id:
            delete_query = f"""DELETE FROM steps WHERE "threadId" = '{thread_id}'"""
        else:
            delete_query = f"""DELETE FROM threads WHERE "userId" = '{user_id}'"""
        
        await self.database.execute(delete_query)

# Initializing the database connection