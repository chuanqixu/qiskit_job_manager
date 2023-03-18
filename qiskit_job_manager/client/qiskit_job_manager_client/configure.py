from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # WEB CONFIGURE
    HOST: str
    PORT: int

    # Notifier SMTP information
    EMAIL: str
    PASSWORD: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        # env_file =".env"


settings = Settings()
