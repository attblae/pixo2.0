from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class CreatingUser(Login):
    password_confirm: str
    name: str
    surname: str
    patronymic: str
    phone: str
    email: str
    pasport: str
    card: str