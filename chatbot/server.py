import asyncio
import grpc
from concurrent import futures
from grpc_generated import chat_pb2, chat_pb2_grpc
import os
import dotenv
from src.logger import CustomLogger

dotenv.load_dotenv(f".env.{os.getenv('ENV', 'development')}", override=True)
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'
logger = CustomLogger('grpc_server')

from src.agentic_chatbot import AgenticChatbot

class ChatBotServicer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.chatbot = AgenticChatbot()
        self.chatbot.start()  # Initialize the chatbot

    async def Answer(self, request, context):
        """Handle medical question requests"""
        is_streaming = True
        print(f"💬 Received question from client. Question: {request.query}")
        try:
            if is_streaming:
                async for answer in self.chatbot.start_streaming(request.query, request.history):
                    response = chat_pb2.AnswerResponse(answer=answer)
                    yield response

                logger.info("✅ Answer streaming completed.")
                response = chat_pb2.AnswerResponse(answer="")
                yield response
            else:
                answer = self.chatbot.answer(request.query, request.history)
                logger.info(f"✅ Answer generated: {answer}")
                response = chat_pb2.AnswerResponse(answer=answer)
                yield response
        except Exception as e:
            logger.error(f"❌ Error occurred while processing request: {e}")
            response = chat_pb2.AnswerResponse(answer=f"❌ Error occurred while processing request: {e}")
            yield response

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatBotServicer(), server)

    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f"🚀 Starting Medical Chatbot gRPC Server on {listen_addr}")
    
    await server.start()

    try:
        await server.wait_for_termination()
        await server.stop(0)
    except KeyboardInterrupt:
        await server.stop(0)

if __name__ == "__main__":
    asyncio.run(serve())