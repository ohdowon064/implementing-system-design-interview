from pydantic import BaseSettings


class Settings(BaseSettings):
    api_server_host: str = "0.0.0.0"
    api_server_port: int = 9999
    capacity: int = 1000
    number_of_refilled_tokens_per_second: int = 10


settings = Settings()
