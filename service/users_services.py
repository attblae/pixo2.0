from datetime import timedelta

from jose import jwt
from fastapi import HTTPException
import time

from db.users import UserRepository
from consts import *
from schemes.user_schemes import LoginSchema, CreatingUserSchema
from schemes.post_schemes import TokenSchema


class UserService:
    @classmethod
    def create_access_token(cls, subject: str, expires_delta=None) -> str:
        """
        Метод для создания токена
        :param subject: str
        :param expires_delta: None
        :return: str
        """
        expire = (
            time.time()
            + (
                expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            ).total_seconds()
        )
        to_encode = {"sub": subject, "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Метод для хеширования пароля пользователя
        :param password: str
        :return: str
        """
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed: str) -> bool:
        """
        Метод для сравнения пароля и его хешированной версии, чтобы убедиться, что пароль верный
        :param password: str
        :param hashed: str
        :return: bool
        """
        return pwd_context.verify(password, hashed)

    @classmethod
    def valid_login(cls, data: LoginSchema) -> TokenSchema:
        """
        Метод для проверки данных при попытке полььзователя войти в существующий аккаунт
        :param data: Login
        :return: Token
        """
        hash_pass = UserRepository.get_password_by_username(data.username)
        if not hash_pass:
            raise HTTPException(detail="User does not exists", status_code=404)

        if not UserService.verify_password(data.password, hash_pass):
            raise HTTPException(detail="Invalid password", status_code=404)

        token = UserService.create_access_token(data.username)

        response = TokenSchema(access_token=token)
        return response

    @classmethod
    def valid_user_creation(cls, data: CreatingUserSchema) -> None:
        """
        Метод для проверки валидости данных при создании аккаунта пользователем
        :param data: CreatingUser
        :return: None
        """
        data_information = data.model_dump()
        if any(" " in data_info for data_info in data_information.values()):
            raise HTTPException(
                status_code=400, detail="Information contains blank space"
            )

        if data.phone.startswith("+7"):
            data.phone = "8" + data.phone.removeprefix("+7")

        if not data.phone[1:].isdigit():
            raise HTTPException(detail="Phone number is not a number", status_code=404)

        if not data.email.endswith(email):
            raise HTTPException(detail="Email is not valid", status_code=404)

        if data.email.count("@") != 1:
            raise HTTPException(detail="Email is not valid", status_code=404)

        username = UserRepository.check_existing_of_username(data.username)

        if username:
            raise HTTPException(detail="username is already used", status_code=404)

        if data.username in bad_words:
            raise HTTPException(detail="You can not name yourself like this", status_code=404)

        if data.password in easy_passwords:
            raise HTTPException(detail="Your password is too simple", status_code=404)

        for i in data.password:
            if data.password.count(i) == len(data.password):
                raise HTTPException(detail="Your password is too simple", status_code=404)

        if data.password_confirm != data.password:
            raise HTTPException(detail="password does not confirmed", status_code=404)


        UserRepository.create_user(
            username=data.username,
            password=UserService.hash_password(data.password),
            name=data.name,
            surname=data.surname,
            patronymic=data.patronymic,
            phone=data.phone,
            email=data.email,
            pasport=data.pasport,
            card=data.card,
        )
