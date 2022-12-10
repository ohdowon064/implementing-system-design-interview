from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

    class Config:
        env_prefix = "redis_"


class Settings(BaseSettings):
    redis = RedisSettings()

    class Config:
        env_file = ".env"


settings = Settings()
