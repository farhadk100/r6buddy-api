from pydantic import BaseSettings


class Settings(BaseSettings):
    DETA_PROJECT_KEY: str
    R6BUDDY_API_KEY: str


settings = Settings()
