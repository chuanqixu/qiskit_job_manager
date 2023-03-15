from backend.configure import settings
import motor.motor_asyncio



client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION_URL, uuidRepresentation="standard")
