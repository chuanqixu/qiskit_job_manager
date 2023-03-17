import motor.motor_asyncio
from fastapi_users.db import BeanieUserDatabase
from ..configure import settings
from ..schemas.user import User



client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION_URL, uuidRepresentation="standard")
db = client[settings.DATABASE_NAME]

job_collection = db.job
user_collection = db.User

async def get_user_db():
    yield BeanieUserDatabase(User)
