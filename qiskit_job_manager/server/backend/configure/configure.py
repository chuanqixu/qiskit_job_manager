from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # WEB CONFIGURE
    HOST: str
    PORT: int

    # Database
    DATABASE_NAME: str
    MONGO_CONNECTION_URL: str

    # Notifier SMTP information
    NOTIFIER_FROM_ADDR: str
    NOTIFIER_PASSWORD: str
    NOTIFIER_SMTP_HOST: str
    NOTIFIER_SMTP_PORT: int
    BACKGROUND_INTERVAL: int

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        # env_file =".env"


settings = Settings()
