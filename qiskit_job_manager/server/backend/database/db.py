import motor.motor_asyncio
from fastapi_users.db import BeanieUserDatabase
from backend.schemas.user import User

from backend.configure import settings



DATABASE_URL = settings.MONGO_CONNECTION_URL
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client[settings.DATABASE_NAME]

job_collection = db.job
user_collection = db.User

async def get_user_db():
    yield BeanieUserDatabase(User)
