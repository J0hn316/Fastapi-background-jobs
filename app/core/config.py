from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Background Jobs"
    database_url: str = "sqlite:///./app.db"
    worker_poll_interval_seconds: int = 2

    model_config = ConfigDict(env_file=".env")


settings = Settings()
