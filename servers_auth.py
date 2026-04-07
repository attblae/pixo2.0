from datetime import timedelta
from jose import jwt, exceptions
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import shutil
import sqlite3
import time
import math
from db.users import UserRepository
from db.posts import PostRepository
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

def valid_login(data):
    hash_pass = UserRepository.get_password_by_username(data.username)
    if not hash_pass:
        raise HTTPException(detail="User does not exists", status_code=404)

    if not verify_password(data.password, hash_pass):
        raise HTTPException(detail="Invalid password", status_code=404)

    token = create_access_token(data.username)

    response = Token(access_token=token)
    return response

def valid_user_creation(data):
    data_information = data.model_dump()
    if any(" " in data_info for data_info in data_information.values()):
        raise HTTPException(status_code=400, detail="Information contains blank space")

    if data.phone.startswith("+7"):
        data.phone = '8' + data.phone.removeprefix('+7')

    username = UserRepository.check_existing_of_username(data.username)

    if username:
        raise HTTPException(detail="username is already used", status_code=404)

    if data.password_confirm != data.password:
        raise HTTPException(detail="password does not confirmed", status_code=404)

    UserRepository.create_user(
        username=data.username,
        password=hash_password(data.password),
        name=data.name,
        surname = data.surname,
        patronymic = data.patronymic,
        phone = data.phone,
        email = data.email,
        pasport = data.pasport,
        card = data.card
    )

def get_account_posts(request, username):
    post = PostRepository.get_posts_from_account()

    context = {
        "request": request,
        "username": username,
        "arts": [
        ]
    }

    for i in range(len(post)):
        if post[i][2] == username:
            photo_url = post[i][1]
            if photo_url.startswith("static/"):
                photo_url = f"../{photo_url}"

            context["arts"].append(
                {
                    "price": post[i][0],
                    "photo_url": photo_url,
                    "username": post[i][2]
                }
            )

    return context

def get_catalog_posts(request, search):
    search = search.lower() if search else None

    if search is None:
        post = PostRepository.get_all_catalog_posts()
    else:
        post = PostRepository.get_specific_catalog_posts(search)

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
                "username": post[i][2],
                "title": post[i][3]
            }
        )

    return context

def add_to_basket(data, username):
    link = data.link

    post_exists = PostRepository.check_post_in_basket(username, link)

    if not post_exists:
        PostRepository.put_post_in_basket(username, link)


def get_basket_posts(request, username):
    posts = PostRepository.get_posts_from_basket(username)
    context = {
        "request": request,
        "username": username,
        "amount_art": len(posts),
        "arts": [
        ]
    }

    for post in posts:
        path = post[1]
        if path.startswith("static/"):
            path = f"../{path}"
        context["arts"].append(
            {
                "price": post[0],
                "photo_url": path,
                "author": post[2]
            }
        )
    return context

def delete_basket_post(data, username):
    link = data.link
    if link.startswith("../"):
        link = link.removeprefix("../")

    post_exists = PostRepository.check_post_in_basket(username, link)

    if post_exists:
        PostRepository.delete_post_from_basket(username, link)

def delete_catalog_post(data, username):
    link = data.link

    if link.startswith("../"):
        link = link.removeprefix("../")

    post_exists = PostRepository.check_post_exists_in_catalog(username, link)

    if post_exists:
        PostRepository.delete_post_from_catalog(username, link)

def uploading_post(price, username, file, title):
    with sqlite3.connect(DB_LINK, timeout=5) as con:
        cursor = con.cursor()

        allowed_files = ('png', 'jfif', 'jpg', 'jpeg', 'webp', 'svg', 'tiff', 'psd')

        amount_art = PostRepository.count_amount_catalog_posts()
        if file.filename.split(".")[1] not in allowed_files:
            raise HTTPException(detail="You can not take this file:(", status_code=404)
        
        file.filename = str(amount_art) + ".png"

        link = f"static/images/{file.filename}"

        with open(link, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        post_exists = PostRepository.check_post_exists_in_catalog(username, link)

        if not post_exists:
            if price != "".join(price.split(" ")) or title.isspace():
                raise HTTPException(detail="No blank space, please", status_code=404)
            title = title.lstrip(" ")
            title = title.rstrip(" ")
            try: 
                price = float(price)
            except:
                raise HTTPException(detail="Price is a number, not letters", status_code=404)
            if price < 0 or price > 999999.99:
                raise HTTPException(detail="Bro, you can not ask for this price", status_code=404)
            if len(title) > 30:
                raise HTTPException(detail="Title is too long", status_code=404)
            price = round(price, 2)

            PostRepository.create_post(username=username, price=price, link=link, title=title)


def check_token_time(data):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(detail="Token expired", status_code=404)
    username = payload["sub"]

    return username