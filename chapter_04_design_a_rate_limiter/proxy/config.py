from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    api_server_host: str
    api_server_port: int

    capacity: int
    refill_period: int
    number_of_refilled_tokens_per_period: int


settings = Settings()
