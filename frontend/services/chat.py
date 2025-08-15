import json
from typing import AsyncGenerator
from config import HTTPClient

async def get_chat_response(question: str, thread_id: str, http: HTTPClient) -> str:
    response = await http.post(
        "/chatbot/query",
        body={"question": question, "thread_id": thread_id},
    )

    print(f"Response from server: {response.get('answer', 'No answer found')}")

    return response.get("answer", "No answer found")

async def get_chat_response_streaming(question: str, thread_id: str, http: HTTPClient) -> AsyncGenerator[str, None]:
    async for chunk in http.streaming(
        "/chatbot/streaming",
        body={"question": question, "thread_id": thread_id},
    ):
        yield chunk