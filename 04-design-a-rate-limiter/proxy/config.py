from pydantic import BaseSettings


class Settings(BaseSettings):
    api_server_host: str = "0.0.0.0"
    api_server_port: int = 9999
    capacity: int = 1000
    refill_period: int = 1
    number_of_refilled_tokens_per_period: int = 10


settings = Settings()
