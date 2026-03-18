from datetime import timedelta
from jose import jwt, exceptions
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import shutil
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
 with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        post = cursor.execute(
            """
            SELECT posts.price, posts.photo_url, users.username
            FROM posts
            JOIN users
            ON posts.user_id = users.id
            """
        ).fetchall()

        context = {
            "request": request,
            "arts": [
            ]
        }

        for i in range(len(post)):
            context["arts"].append(
                {
                    "price": post[i][0],
                    "photo_url": post[i][1],
                    "username": post[i][2]
                }
            )

        return context

def get_catalog_posts(request):
    with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        post = cursor.execute(
            """
            SELECT posts.price, posts.photo_url, users.username
            FROM posts
            JOIN users
            ON posts.user_id = users.id
            """
        ).fetchall()

        context = {
            "request": request,
            "arts": [
            ]
        }

        for i in range(len(post)):
            context["arts"].append(
                {
                    "price": post[i][0],
                    "photo_url": post[i][1],
                    "username": post[i][2]
                }
            )

        return context

def valid_login(data):
    with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        hash_pass = cursor.execute("SELECT password FROM users WHERE username = ?", (data.username,)).fetchone()

        if not hash_pass:
            raise HTTPException(detail="User does not exists", status_code=404)

        if not verify_password(data.password, hash_pass[0]):
            raise HTTPException(detail="Invalid password", status_code=404)

        token = create_access_token(data.username)

        response = Token(access_token=token)
        return response

def valid_user_creation(data):
    with sqlite3.connect(DB_LINK, timeout=5) as con:
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

def add_to_basket(data, username):
    with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        price = data.price
        link = data.link
        print(link)

        if link.startswith("static/"):
            link = f"../{link}"
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

        pr = cursor.execute(
            """
                SELECT * FROM basket_posts
            """
        )
        print(pr)


def get_basket_posts(request, username):
    with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        posts = cursor.execute(
            """
                SELECT price, link FROM basket_posts
                INNER JOIN users
                ON basket_posts.user_id = users.id
                WHERE users.username = ?
            """, (username,)
        ).fetchall()

        context = {
            "request": request,
            "arts": [
            ]
        }

        for post in posts:
            print(post)
            context["arts"].append(
                {
                    "price": post[0],
                    "photo_url": post[1]
                }
            )

        return context

def delete_basket_post(data, username):
    link = data.link
    with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        post_exists = cursor.execute(
            """
                SELECT link FROM basket_posts
                JOIN users
                ON basket_posts.user_id = users.id
                WHERE users.username = ? and basket_posts.link = ?
            """, (username, link,)
        ).fetchall()

        print(post_exists)

        if post_exists:
            cursor.execute(
                """
                DELETE FROM basket_posts
                WHERE link = ?
                AND user_id = (
                    SELECT id FROM users WHERE username = ?
                )
                """,
                (link, username,)
            )
            con.commit()

        pr = cursor.execute(
            """
                SELECT * FROM basket_posts
            """
        ).fetchall()
        # print(pr)

def uploading_post(price, username, file):
    with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        link = f"static/images/{file.filename}"

        with open(link, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        post_exists = cursor.execute(
            """
                SELECT photo_url FROM posts
                JOIN users
                ON posts.user_id = users.id
                WHERE users.username = ? and posts.photo_url = ?
            """, (username, link,)
        ).fetchall()

        if not post_exists:
            cursor.execute(
                """
                    INSERT INTO posts (
                        user_id,
                        price,
                        photo_url
                    )
                    VALUES (
                        (SELECT id FROM users WHERE username = ?),
                        ?,
                        ?
                    )
                """, (username, float(price), link)
            )
            con.commit()


def check_token_time(data):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(detail="Token expired", status_code=404)
    username = payload["sub"]

    return username