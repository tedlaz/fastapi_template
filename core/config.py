from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    SECRET_KEY: str = "change_me_to_a_long_random_secret_key"
    TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env")


cfg = _Settings()
