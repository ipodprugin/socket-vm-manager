from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int

settings = Settings()

