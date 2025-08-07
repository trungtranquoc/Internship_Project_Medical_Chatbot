import dotenv
import os

env_pat = os.getenv("ENV", "development")
dotenv.load_dotenv(f".env.{env_pat}", override=True)
DEVICE = os.getenv("DEVICE", "cpu")

from src.agentic_chatbot import AgenticChatbot

def main():
    agentic_chatbot = AgenticChatbot()
    agentic_chatbot.start()
    print("Chatbot is ready to answer questions.")

    answer, keywords, related_questions, isSuccess = agentic_chatbot.answer("What is diabetes?")

    while True:
        user_question = input("Ask a medical question: ")
        if user_question.lower() in ["exit", "quit"]:
            print("Exiting the chatbot. Goodbye!")
            break
        
        answer, keywords, related_questions = agentic_chatbot.answer(user_question)
        print(f"Related questions: {related_questions}")
    
if __name__ == "__main__":
    main()