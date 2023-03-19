from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # Web server configure
    HOST: str
    PORT: int

    # Account information
    EMAIL: str
    PASSWORD: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        # env_file =".env"


settings = Settings()
