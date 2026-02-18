from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from datetime import timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
import sqlite3
import uvicorn
import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

templates = Jinja2Templates(directory="static")

SECRET_KEY = "change-me-in-production-please"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Login(BaseModel):
    username: str
    password: str


# classes:
class CreatingUser(Login):
    password_confirm: str
    name: str
    surname: str
    patronymic: str
    phone: str
    email: str
    pasport: str
    card: str


class Token(BaseModel):
    access_token: str


class PostsInfo(BaseModel):
    link: str
    price: str


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


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


def create_access_token(subject: str, expires_delta=None) -> str:
    expire = time.time() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).total_seconds()
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


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


@app.get("/account")
def account_page():
    return FileResponse("static/account.html")


@app.get("/post")
def posts_upload():
    return FileResponse("static/upload_post.html")


@app.get("/backet")
def backet_page():
    return FileResponse("static/backet.html")


@app.get("/catalog", response_class=HTMLResponse)
async def catalog_page(request: Request):
    con = sqlite3.connect("base/tables.sql")
    cursor = con.cursor()

    post = cursor.execute(
        "SELECT * FROM posts"
    ).fetchall()

    context = {
        "request": request,
        "arts": [
        ]
    }

    for i in range(3):
        context["arts"].append(
            {
                "price": post[i][2],
                "photo_url": post[i][4]
            }
        )

    return templates.TemplateResponse("catalog.html", context)
    # return FileResponse("static/catalog.html")


@app.get("/support")
def support_page():
    return FileResponse("static/support.html")


@app.get("/about_us")
def about_us_page():
    return FileResponse("static/about_us.html")


# posts:

@app.post("/login_account")
def login_account(data: Login):
    con = sqlite3.connect("base/tables.sql")
    cursor = con.cursor()

    hash_pass = cursor.execute("SELECT password FROM users WHERE username = ?", (data.username,)).fetchone()

    if not hash_pass:
        raise HTTPException(detail="User does not exists", status_code=404)

    if not verify_password(data.password, hash_pass[0]):
        raise HTTPException(detail="Invalid password", status_code=404)

    con.close()
    token = create_access_token(data.username)

    response = Token(access_token=token)
    return response


@app.post("/create_user")
def creating_user(data: CreatingUser):
    con = sqlite3.connect("base/tables.sql")
    cursor = con.cursor()
    data_information = data.model_dump()
    if any(" " in data_info for data_info in data_information.values()):
        raise HTTPException(status_code=400, detail="Information contains blank space")

    if data.phone.startswith("+7"):
        data.phone = '8' + data.phone.removeprefix('+7')

    username = cursor.execute("SELECT username FROM users WHERE username = ?", (data.username,)).fetchone()

    if username:
        raise HTTPException(detail="username is already used", status_code=404)

    if data.password_confirm != data.password:
        raise HTTPException(detail="password does not confirmed", status_code=404)

    cursor.execute(
        """
            INSERT INTO users (
            username, 
            password, 
            name, 
            surname, 
            patronymic,
            phone, 
            email, 
            pasport,
            card
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data.username,
            hash_password(data.password),
            data.name,
            data.surname,
            data.patronymic,
            data.phone,
            data.email,
            data.pasport,
            data.card
        )
    )
    con.commit()
    con.close()
    return {"status": "ok"}


@app.post("/check_token")
def check_token(data: Token):
    payload = jwt.decode(data.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    expires_at = payload["exp"]
    username = payload["sub"]

    if time.time() >= expires_at:
        raise HTTPException(detail="Token expired", status_code=404)

    return {"status": "ok"}, username


# sql part
def create_tables():
    con = sqlite3.connect("base/tables.sql")
    cursor = con.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(30) UNIQUE,
                password VARCHAR(255),
                name VARCHAR(35),
                surname VARCHAR(35),
                patronymic VARCHAR(35),
                phone VARCHAR(11) UNIQUE,
                email VARCHAR(50) UNIQUE,
                pasport VARCHAR(16) UNIQUE,
                card VARCHAR(19) UNIQUE
            );
    """
    )
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    price DECIMAL(11, 2) not NULL,
                    description VARCHAR(256) NULL,
                    photo_url VARCHAR(40) not NULL UNIQUE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
        """
    )


if __name__ == "__main__":
    # 127.0.0.1
    # 0.0.0.0
    create_tables()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8657,
        reload=True
    )