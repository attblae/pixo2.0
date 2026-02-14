from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta, time
from jose import JWTError, jwt
from pydantic import BaseModel
import sqlite3
import uvicorn
 
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SECRET_KEY = "change-me-in-production-please"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# classes:

class Creating_user(BaseModel):
    username: str
    password: str
    password_confirm: str
    name: str
    surname: str
    patronymic: str
    phone: str
    email: str
    pasport: str
    card: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str

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

def create_access_token(subject: str, expires_delta = None) -> str:
    expire = time.time() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
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

@app.get("/backet")
def backet_page():
    return FileResponse("static/backet.html")

@app.get("/catalog")
def catalog_page():
    return FileResponse("static/catalog.html")

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
        raise HTTPException(detail="User does not exists")

    if not verify_password(data.password, hash_pass[0]):
        raise HTTPException(detail="Invalid password", status_code=404)

    con.close()
    token = create_access_token(data.username)

    response = Token(token)
    return response
    

@app.post("/create_user")
def creating_user(data: Creating_user):
    data_information = data.model_dump()
    if any(" " in data_info for data_info in data_information.values()):
        raise HTTPException(status_code=400, detail="Information contains blank space")
    
    if data.phone.startswith("+7"):
        data.phone = '8' + data.phone.removeprefix('+7')

    con = sqlite3.connect("base/tables.sql")
    cursor = con.cursor()

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
def check_for_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expires_at = payload["exp"]

    return(expires_at)

# sql part
def create_tables(cursor):
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
                )
        """
    )


if __name__ == "__main__":
    # 127.0.0.1
    # 0.0.0.0
    con = sqlite3.connect("base/tables.sql")
    cursor = con.cursor()
    create_tables(cursor)
    con.commit()
    con.close()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8657,
        reload=True
    )