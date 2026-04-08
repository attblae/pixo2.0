from fastapi import File, Form, APIRouter, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from service.posts_services import PostService
from consts import *
from schemes.post_schemes import ResponseUsernameSchema, TokenSchema, PostInfoSchema
from schemes.user_schemes import ResponseOkSchema


router = APIRouter()

@router.get("/account/{username}", response_class=HTMLResponse)
async def account_page(request: Request, username: str):
    """
    Модель для перехода на аккаунт конкретного пользователя
    :param request: Request
    :param username: username
    :return: context
    """
    context = PostService.get_account_posts(request, username)
    return templates.TemplateResponse("account.html", context)

@router.get("/post")
def posts_page():
    """
    Модель для перехода на страницу создания поста
    :return: FileResponse
    """
    return FileResponse("static/upload_post.html")

@router.get("/basket/{username}",  response_class=HTMLResponse)
def basket_page(request: Request, username: str):
    """
    Модель для перехода к карзине опреденного пользователя
    :param request: Request
    :param username: str
    :return: context
    """
    context = PostService.get_basket_posts(request, username)
    return templates.TemplateResponse("basket.html", context)

@router.get("/catalog", response_class=HTMLResponse)
async def catalog_page(request: Request, search: str | None = None):
    """
    Модель для перехода к каталогу
    :param request: Request
    :param search: str
    :return: context
    """
    context = PostService.get_catalog_posts(request, search)
    return templates.TemplateResponse("catalog.html", context)

@router.post("/put_in_basket")
def add_posts_to_basket(data: PostInfoSchema):
    """
    Модель для добавления поста в кразину нужного пользователя
    :param data: PostInfo
    :return: ResponseOk
    """
    username = PostService.check_token_time(data.access_token)
    PostService.add_to_basket(data, username)
    return ResponseOkSchema()

@router.post("/check_token")
def check_token(data: TokenSchema):
    """
    Модель для проверки токена и получения ника пользователя из него
    :param data: Token
    :return: ResponseUsernameSchema
    """
    username = PostService.check_token_time(data.access_token)
    return ResponseUsernameSchema(username=username).model_dump()

@router.post("/delete_from_basket")
def delete_post(data: PostInfoSchema):
    """
    Модель для удаления поста из карзины определенного пользователя
    :param data: PostInfoSchema
    :return:
    """
    username = PostService.check_token_time(data.access_token)
    PostService.delete_basket_post(data, username)
    return ResponseOkSchema()

@router.post("/delete_from_catalog")
def delete_post(data: PostInfoSchema):
    """
    Модель для удалдения поста из каталога и аккаунта у определенного пользователя
    :param data: PostInfoSchema
    :return: ResponseOkSchema
    """
    username = PostService.check_token_time(data.access_token)
    PostService.delete_catalog_post(data, username)
    return ResponseOkSchema()

@router.post("/uploading")
def upload_post(file: UploadFile = File(...), price: str = Form(...), token: str = Form(...), title: str = Form(...)):
    """
    Модель для создания поста с верными данными
    :param file: UploadFile
    :param price: str
    :param token: str
    :param title: str
    :return: ResponseOkSchema()
    """
    username = PostService.check_token_time(token)
    PostService.uploading_post(price, username, file, title)
    return ResponseOkSchema()