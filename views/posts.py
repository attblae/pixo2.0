from fastapi import File, Form, APIRouter, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from service.posts_services import PostService
from consts import *
from schemes import *


router = APIRouter()

@router.get("/account/{username}", response_class=HTMLResponse)
async def account_page(request: Request, username: str):
    context = PostService.get_account_posts(request, username)
    return templates.TemplateResponse("account.html", context)

@router.get("/post")
def posts_page():
    return FileResponse("static/upload_post.html")

@router.get("/basket/{username}",  response_class=HTMLResponse)
def basket_page(request: Request, username: str):
    context = PostService.get_basket_posts(request, username)
    print(context)
    return templates.TemplateResponse("basket.html", context)

@router.get("/catalog", response_class=HTMLResponse)
async def catalog_page(request: Request, search: str | None = None):
    context = PostService.get_catalog_posts(request, search)
    return templates.TemplateResponse("catalog.html", context)

@router.post("/put_in_basket")
def add_posts_to_basket(data: PostInfo):
    username = PostService.check_token_time(data.access_token)
    PostService.add_to_basket(data, username)
    return {"status": "ok"}

@router.post("/check_token")
def check_token(data: Token):
    username = PostService.check_token_time(data.access_token)
    return {"username": username}

@router.post("/delete_from_basket")
def delete_post(data: PostInfo):
    username = PostService.check_token_time(data.access_token)
    PostService.delete_basket_post(data, username)
    return {"status": "ok"}

@router.post("/delete_from_catalog")
def delete_post(data: PostInfo):
    username = PostService.check_token_time(data.access_token)
    PostService.delete_catalog_post(data, username)
    return {"status": "ok"}

@router.post("/uploading")
def upload_post(file: UploadFile = File(...), price: str = Form(...), token: str = Form(...), title: str = Form(...)):
    username = PostService.check_token_time(token)
    PostService.uploading_post(price, username, file, title)
    return {"status": "ok"}