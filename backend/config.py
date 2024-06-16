from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    SERVER_HOST: str
    SERVER_PORT: int

    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr

    @property
    def DB_URL(self) -> SecretStr:
        return SecretStr(f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}")

settings = Settings()

