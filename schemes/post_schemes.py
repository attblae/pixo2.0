from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str


class PostInfoSchema(BaseModel):
    access_token: str
    link: str

class ResponseUsernameSchema(BaseModel):
    username: str