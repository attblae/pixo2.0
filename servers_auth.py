from datetime import timedelta
from jose import jwt, exceptions
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import sqlite3
import time
from consts import *
from schemes import *

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

templates = Jinja2Templates(directory="static")

def create_access_token(subject: str, expires_delta=None) -> str:
    expire = time.time() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).total_seconds()
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def get_account_posts(request):
    con = sqlite3.connect(DB_LINK)
    cursor = con.cursor()

    post = cursor.execute(
        """
            SELECT * FROM posts
            JOIN users ON posts.user_id = users.id
            WHERE users.username = "attblae"
        """
    ).fetchall()

    context = {
        "request": request,
        "arts": [
        ]
    }

    if not post:
        return context

    for i in range(3):
        context["arts"].append(
            {
                "price": post[i][2],
                "photo_url": post[i][4]
            }
        )

    return context

def get_catalog_posts(request):
    con = sqlite3.connect(DB_LINK)
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

    return context

def valid_login(data):
    con = sqlite3.connect(DB_LINK)
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

def valid_user_creation(data):
    con = sqlite3.connect(DB_LINK)
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

def add_to_basket(data, username):
    con = sqlite3.connect(DB_LINK)
    cursor = con.cursor()

    price = data.price
    link = data.link

    post_exists = cursor.execute(
        """
            SELECT link FROM basket_posts
            JOIN users
            ON basket_posts.user_id = users.id
            WHERE users.username = ? and basket_posts.link = ?
        """, (username, link,)
    ).fetchall()

    if not post_exists:
        cursor.execute(
            """
                INSERT INTO basket_posts (
                    user_id,
                    price,
                    link
                )
                VALUES (
                    (SELECT id FROM users WHERE username = ?),
                    ?,
                    ?
                )
            """, (username, float(price), link)
        )
        con.commit()
        con.close()


def get_basket_posts(request, username):
    con = sqlite3.connect(DB_LINK)
    cursor = con.cursor()
    posts = cursor.execute(
        """
            SELECT * FROM basket_posts
            INNER JOIN users
            ON basket_posts.user_id = users.id
            WHERE users.username = ?
        """, (username,)
    ).fetchall()
    cursor.close()
    con.close()
    print(posts)
    context = {
        "request": request,
        "arts": [
        ]
    }

    for post in posts:
        # print(post)
        context["arts"].append(
            {
                "price": post[1],
                "photo_url": post[2]
            }
        )

    return context

def check_token_time(data):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(detail="Token expired", status_code=404)

    username = payload["sub"]

    return username