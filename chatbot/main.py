# import dotenv
import os
import asyncio

from src.logger import CustomLogger

# env_pat = os.getenv()
# dotenv.load_dotenv(f".env.{env_pat}", override=True)
DEVICE = os.getenv("DEVICE", "cpu")

logger = CustomLogger('main')

from src.agentic_chatbot import AgenticChatbot

async def main():
    agentic_chatbot = AgenticChatbot()
    agentic_chatbot.start()
    logger.info("Chatbot is ready to answer questions.")
    print("Ask a medical question: What is diabetes?")

    async for chunk in agentic_chatbot.start_streaming("What is diabetes?"):
        print(chunk, end='', flush=True)

    while True:
        logger.info("Answer streaming completed.")
        user_question = input("Ask a medical question: ")
        if user_question.lower() in ["exit", "quit"]:
            logger.info("Exiting the chatbot. Goodbye!")
            break
        
        async for chunk in agentic_chatbot.start_streaming(user_question):
            print(chunk, end='', flush=True)

if __name__ == "__main__":
    asyncio.run(main())