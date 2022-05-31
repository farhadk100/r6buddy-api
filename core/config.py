from pydantic import BaseSettings


class Settings(BaseSettings):
    DETA_PROJECT_KEY: str


settings = Settings()
