from pydantic import BaseSettings, Field
import os


class Settings(BaseSettings):
    # Web server configure
    HOST: str = None
    PORT: int = None

    # Account information
    EMAIL: str = None
    PASSWORD: str = None

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')


settings = Settings()
