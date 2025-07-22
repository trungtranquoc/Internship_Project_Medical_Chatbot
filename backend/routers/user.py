import json
from fastapi import APIRouter, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

import asyncio
from database import postgresql_db
from datetime import datetime
from time import time

from gRPC import ChatbotGRPCClient
from model import ChatbotQuery, ChatbotAnswering
import logging

from functools import reduce

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

router = APIRouter()
chatbot_grpc_client = ChatbotGRPCClient()

router.add_event_handler("startup", chatbot_grpc_client.connect)
router.add_event_handler("shutdown", chatbot_grpc_client.disconnect)

@router.get("/history")
async def get_history(request: Request, thread_id: str = None) -> list:
    """
    Endpoint to retrieve chat history for the user.
    """
    if thread_id:
        # history = await db['chat_history'].find({"thread_id": thread_id}).to_list(length=None)
        history = await postgresql_db.retrieve_history(thread_id)
    else:
        # history = await db['chat_history'].find({"user_token": user_token}).to_list(length=None)
        history = await postgresql_db.retrieve_history(user_id=request.headers.get("user_id"))

    if not history:
        return []
    
    return history
    # return [
    #     {
    #         "thread_id": entry["thread_id"],
    #         "question": entry["question"],
    #         "answer": entry["answer"],
    #         "timestamp": entry["timestamp"],
    #         "inference_time": entry["inference_time"],
    #         "related_questions": entry.get("related_questions", [])
    #     } for entry in history
    # ]

@router.post("/query")
async def query(request: Request, query_body: ChatbotQuery) -> ChatbotAnswering:
    question = query_body.question
    thread_id = query_body.thread_id
    
    logger.info(f"Session: {thread_id} - Received question: {question}")
    
    # Retrieve history if provided
    history = await postgresql_db.retrieve_context(thread_id=thread_id) if thread_id else []

    logger.info(f"Session id: {thread_id} - Found history: {history}")

    start = time()
    answer, related_questions = await asyncio.to_thread(chatbot_grpc_client.send_question, question, history)
    end = time()
    
    # Update the conversation will be performed in Chainlit Frontend
    return ChatbotAnswering(answer=answer, related_questions=related_questions, inference_time=end - start)

@router.delete("/delete_conversation/{thread_id}")
async def delete_conversation(thread_id: str, request: Request):
    """
    Endpoint to delete a specific conversation by its ID.
    """
    await postgresql_db.delete_history(thread_id=thread_id)
    return JSONResponse(content={"message": "Conversation deleted successfully"}, status_code=200)

@router.delete("/delete_all_conversations")
async def delete_all_conversation(request: Request):
    """
    Endpoint to delete the conversation history for the user.
    """
    user_id = request.headers.get("user_id")

    if not user_id:
        raise HTTPException(status_code=403, detail="User not allowed to access this resource")

    await postgresql_db.delete_history(user_id=user_id)
    return JSONResponse(content={"message": "Conversation history deleted successfully"}, status_code=200)