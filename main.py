from fastapi import Request, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
import uvicorn
from servers_auth import *
from create_tables import *
from test import test_posts

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# errors:

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

# pages:

@app.get("/")
def main_page():
    return FileResponse("static/main.html")


@app.get("/create")
def create_page():
    return FileResponse("static/create.html")


@app.get("/login")
def login_page():
    return FileResponse("static/login.html")


@app.get("/account", response_class=HTMLResponse)
async def account_page(request: Request):
    context = get_account_posts(request)
    return templates.TemplateResponse("account.html", context)


@app.get("/post")
def posts_page():
    return FileResponse("static/upload_post.html")

@app.get("/basket/{username}",  response_class=HTMLResponse)
def basket_page(request: Request, username: str):
    context = get_basket_posts(request, username)
    return templates.TemplateResponse("basket.html", context)

@app.get("/catalog", response_class=HTMLResponse)
async def catalog_page(request: Request):
    context = get_catalog_posts(request)
    return templates.TemplateResponse("catalog.html", context)

@app.get("/support")
def support_page():
    return FileResponse("static/support.html")


@app.get("/about_us")
def about_us_page():
    return FileResponse("static/about_us.html")


# posts:

@app.post("/put_in_basket")
def add_posts_to_basket(data: PostInfo):
    username = check_token_time(data.access_token)
    add_to_basket(data, username)
    return {"status": "ok"}

@app.post("/login_account")
def log_in_account(data: Login):
    response = valid_login(data)
    return response


@app.post("/create_user")
def creating_user(data: CreatingUser):
    valid_user_creation(data)
    return {"status": "ok"}


@app.post("/check_token")
def check_token(data: Token):
    username = check_token_time(data.access_token)
    return {"username": username}

@app.post("/delete_from_basket")
def delete_post(data: PostInfo):
    username = check_token_time(data.access_token)
    delete_basket_post(data, username)
    return {"status": "ok"}

@app.post("/uploading")
def upload_post(data: PostInfo):
    username = check_token_time(data.access_token)
    uploading_post(data, username)
    return {"status": "ok"}

if __name__ == "__main__":
    # 127.0.0.1
    # 0.0.0.0
    creating_tables()
    # test_posts()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8657,
        reload=True
    )