from fastapi import APIRouter
from fastapi.responses import FileResponse
from service.users_services import UserService
from schemes.user_schemes import LoginSchema, CreatingUserSchema, ResponseOkSchema
from schemes.post_schemes import TokenSchema

router = APIRouter()

@router.get("/create")
def create_page():
    """
    Метод для перехода на страницу создания аккаунта(ссылка)
    :return: FileResponse
    """
    return FileResponse("static/create.html")

@router.get("/login")
def login_page():
    """
    Метод для перехода на страницу авторизиции в аккаунт  (ссылка)
    :return: FileResponse
    """
    return FileResponse("static/login.html")

@router.post("/login_account", response_model=TokenSchema)
def log_in_account(data: LoginSchema):
    """
    Модль для проверки данных пользователя при входе в аккаунт
    :param data: Login
    :return: Token
    """
    return UserService.valid_login(data)

@router.post("/create_user", response_model=ResponseOkSchema)
def creating_user(data: CreatingUserSchema):
    """
    Модель для проверки данных пользователя при создании аккаунта
    :param data: CreatingOk
    :return: ResponseOk
    """
    UserService.valid_user_creation(data)
    return ResponseOkSchema()