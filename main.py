from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import sqlite3
import uvicorn
 
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# classes:

class Creating_user(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    patronymic: str
    pasport: str
    email: str
    card: str

class Login(BaseModel):
    username: str
    password: str

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
    if data.username != 'attblae':
        raise HTTPException(detail='user does not exist', status_code=404)
    return {"status": "ok"}
    
    
    

@app.post("/create_user")
def creating_user(data: Creating_user):
    username = cursor.execute("SELECT username FROM users WHERE username = ?", data.username)

    if username:
        raise HTTPException(detail="username is already used", status_code=404)
    
    cursor.execute(
            """
                INSERT users (username, password, name, surname, patronymic, email, pasport, card)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                data.username,
                data.password,
                data.name,
                data.surname,
                data.patronymic,
                data.email,
                data.pasport,
                data.card
        )
    )


# sql part:
con = sqlite3.connect("tables.sql")
cursor = con.cursor()

def create_tables():
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
                passport_number VARCHAR(16) UNIQUE,
                card VARCHAR(19) UNIQUE
            )
    """
    )


if __name__ == "__main__":
    # 127.0.0.1
    # 0.0.0.0
    create_tables()
    con.commit()
    con.close()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8657,
        reload=True
    )