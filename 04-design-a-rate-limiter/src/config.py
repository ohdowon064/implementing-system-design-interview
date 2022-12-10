from pydantic import BaseSettings


class Settings(BaseSettings):
    capacity: int = 1000
    number_of_refilled_tokens_per_second: int = 10


settings = Settings()
