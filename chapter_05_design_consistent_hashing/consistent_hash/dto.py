from pydantic import BaseModel


class ReadRequest(BaseModel):
    key: str


class WriteRequest(BaseModel):
    key: str
    value: str
