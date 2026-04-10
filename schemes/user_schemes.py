from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    username: str
    password: str


class CreatingUserSchema(LoginSchema):
    password_confirm: str
    name: str
    surname: str
    patronymic: str
    phone: str
    email: str
    pasport: str
    card: str


class ResponseOkSchema(BaseModel):
    status: str = Field(default="ok")
