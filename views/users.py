from fastapi import APIRouter
from fastapi.responses import FileResponse
from service.users_services import UserService
from schemes.user_schemes import Login, CreatingUser

router = APIRouter()

@router.get("/create")
def create_page():
    return FileResponse("static/create.html")

@router.get("/login")
def login_page():
    return FileResponse("static/login.html")

@router.post("/login_account")
def log_in_account(data: Login):
    response = UserService.valid_login(data)
    return response

@router.post("/create_user")
def creating_user(data: CreatingUser):
    UserService.valid_user_creation(data)
    return {"status": "ok"}