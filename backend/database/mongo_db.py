from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_LINK = os.getenv("MONGODB_LINK")
if not MONGO_LINK:
    raise ValueError("MONGODB_LINK environment variable is not set")

print("Connecting to MongoDB successfully !")

myclient = AsyncIOMotorClient(MONGO_LINK)
db = myclient['medical_chatbot']