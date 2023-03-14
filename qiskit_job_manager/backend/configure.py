from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_NAME: str
    MONGO_CONNECTION_URL: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        # env_file =".env"


settings = Settings()
