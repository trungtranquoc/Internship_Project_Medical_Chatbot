import grpc
from concurrent import futures
from grpc_generated import chat_pb2, chat_pb2_grpc
import os
import dotenv

dotenv.load_dotenv(f".env.{os.getenv('ENV', 'development')}", override=True)
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'

from src.agentic_chatbot import AgenticChatbot

class ChatBotServicer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.chatbot = AgenticChatbot()
        self.chatbot.start()  # Initialize the chatbot

    def Answer(self, request, context):
        """Handle medical question requests"""
        print(f"💬 Received question from client. Question: {request.query}")
        try:
            reply, keywords, related_questions = self.chatbot.answer(request.query, request.history)
            return chat_pb2.AnswerResponse(answer=reply, keywords=keywords, related_questions=related_questions, isSuccess=True)
        except Exception as e:
            return chat_pb2.AnswerResponse(answer=f"❌ Error occurred while processing request: {e}", keywords=[], related_questions=[], isSuccess=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatBotServicer(), server)

    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f"🚀 Starting Medical Chatbot gRPC Server on {listen_addr}")
    
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()