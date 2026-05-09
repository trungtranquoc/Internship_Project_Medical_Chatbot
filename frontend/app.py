import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer

from chainlit.input_widget import Select

from services import get_chat_response, get_chat_response_streaming
from config import HTTPClient
import dotenv
import os
import logging
from httpx import HTTPStatusError

from utils import answer_format

logger = logging.getLogger(__name__)

cl.on_settings_update

# Load environment variables from .env file
env = os.getenv("ENV", "development")
dotenv.load_dotenv(f".env.{env}", override=True)

BACKEND_HOST = os.environ.get("BACKEND_HOST", "localhost")
PORT = os.environ.get("BACKEND_PORT", "8001")
HTTP_TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", 20))
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "CHAINLIT_DB")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "CHAINLIT_DB")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "MEDICAL_CHAT_HISTORY")

print(f"Connecting to backend at http://{BACKEND_HOST}:{PORT} with timeout {HTTP_TIMEOUT} seconds")

http_client = HTTPClient(
    base_url=f"http://{BACKEND_HOST}:{PORT}/" ,
    headers={"Content-Type": "application/json", "user": "trungtran"} ,
    timeout=HTTP_TIMEOUT
)

@cl.password_auth_callback
async def auto_callback(username: str, password: str):
    """
    Callback function for password authentication.
    Returns True if the username and password match the environment variables.
    """
    try:
        login_response = await http_client.login(username, password)

        user_id = login_response.get("user_id")
        name = login_response.get("name", username)
        metadata = login_response.get("metadata", {})
        role = metadata.get("role", "user")
        display_name = metadata.get("name", name)

        return cl.User(identifier=username, display_name=display_name, metadata={"role": role, "user_id": user_id, "login": True})
    except HTTPStatusError as e:
        logger.error(f"HTTP error during authentication: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Error in login: {e}")
        return None

@cl.on_chat_resume
async def on_chat_resume():
    # Use for resumt a chat session
    pass

@cl.on_chat_start
async def on_chat_start():
    """
    Called when a new chat session starts.
    Adds the conversation to sidebar.
    """

    try:
        await http_client.ping()  # Check connection to the backend server
        user = cl.user_session.get("user")
        isLogin = user and user.metadata.get("login", False)

        if isLogin:
            user_id = user.metadata.get("user_id")
            if user_id:
                http_client.set_user_header(user_id)
        else:
            logger.error("No user session found. User ID header will not be set.")
            return
        
        settings = await cl.ChatSettings(
            [
                Select(
                    id="role",
                    label="Your Role",
                    values=["patient", "medical student"],
                    initial_index=0,
                )
            ]
        ).send()
        value = settings["role"]

    except Exception as e:
        # Handle connection errors and set the error message
        logger.error(
            f"❌ Không thể kết nối tới máy chủ backend tại {http_client.client.base_url}. Vui lòng kiểm tra lại kết nối mạng hoặc thông tin cấu hình. Lỗi: {str(e)}"
        )
        return
    
@cl.on_chat_end
async def on_chat_end():
    """
    Called when a chat session ends.
    Can be used to clean up resources or save state.
    """
    thread_id = cl.context.session.thread_id
    logger.info(f"Chat session ended with thread_id: {thread_id}")
    
@cl.data_layer
def data_layer():
    """
    Initialize the data layer for the application.
    """
    return SQLAlchemyDataLayer(
        conninfo=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?ssl=require"
    )

@cl.on_message
async def message_receive(message):
    """
    Main function to handle incoming messages.
    """
    msg = cl.Message(content="")
    thread_id = cl.context.session.thread_id
    role = cl.context.session.chat_settings.get("role", "patient")
    print("Role selected:", role)
    
    # Process the message and generate a response
    try:
        async for token in get_chat_response_streaming(
            question=message.content,
            thread_id=thread_id,
            http=http_client
        ):
            await msg.stream_token(token)
        
        await msg.update()
    except Exception as e:
        # Handle exceptions and set the error message
        msg.is_error = True
        msg.content = f"❌ An error occurred: \n{str(e)}. \nPlease try again later."
    
    await msg.send()
