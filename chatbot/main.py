from src.chatbot import Chatbot
import dotenv
import os

env_pat = os.getenv("ENV", "development")
dotenv.load_dotenv(f".env.{env_pat}", override=True)
DEVICE = os.getenv("DEVICE", "cpu")

def main():
    chatbot = Chatbot(device="mps")
    chatbot.start()
    print("Chatbot is ready to answer questions.")

    while True:
        user_question = input("Ask a medical question: ")
        if user_question.lower() in ["exit", "quit"]:
            print("Exiting the chatbot. Goodbye!")
            break
        
        try:
            answer = chatbot.answer(user_question)
            print(f"Answer: {answer}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    main()