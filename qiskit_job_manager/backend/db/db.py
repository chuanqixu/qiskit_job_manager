# from pymongo import MongoClient
import motor.motor_asyncio
from configure import settings

# client = MongoClient(settings.MONGO_CONNECTION_URL)
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION_URL)
print('Connected to MongoDB...')

db = client[settings.DATABASE_NAME]
user_collection = db.user
job_collection = db.job
