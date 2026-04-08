from pydantic import BaseModel

class Token(BaseModel):
    access_token: str


class PostInfo(BaseModel):
    access_token: str
    link: str