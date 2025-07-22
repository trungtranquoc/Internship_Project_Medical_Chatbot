import grpc
from concurrent import futures
from grpc_generated import chat_pb2, chat_pb2_grpc
from src.chatbot import Chatbot

class ChatBotServicer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.chatbot = Chatbot()
        self.chatbot.start()  # Initialize the chatbot

    def Answer(self, request, context):
        """Handle medical question requests"""
        print(f"💬 Received question from client. Question: {request.query}")
        history = [{"role": "user", "content": h.content} for h in request.history]
        reply, related_questions = self.chatbot.answer(request.query, history)

        return chat_pb2.AnswerResponse(answer=reply, related_questions=related_questions)

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