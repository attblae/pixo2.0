from jose import jwt, exceptions
from fastapi import HTTPException, UploadFile, Request
from fastapi.responses import RedirectResponse
import shutil
import os
from db.posts import PostRepository
from consts import *
from schemes.post_schemes import PostInfoSchema


class PostService:
    @classmethod
    def get_account_posts(
        cls, request: Request, username: str, token: str
    ) -> dict | RedirectResponse:
        """
        Метод для отображения данных поста в аккаунте пользователя
        :param request: Request
        :param username: str
        :return: dict | RedirectResponse
        """
        try:
            username_from_token = PostService.check_token_time(token)
        except Exception:
            return RedirectResponse("/login")

        if username_from_token != username:
            return RedirectResponse(f"/account/{username_from_token}/{token}")

        post = PostRepository.get_posts_from_account()

        context = {"request": request, "username": username, "arts": []}
        if post:
            for i in range(len(post)):
                if post[i][2] == username:
                    photo_url = post[i][1]
                    if photo_url.startswith("static/"):
                        photo_url = f"../../{photo_url}"

                    context["arts"].append(
                        {
                            "price": post[i][0],
                            "photo_url": photo_url,
                            "username": post[i][2],
                        }
                    )

        return context

    @classmethod
    def get_catalog_posts(cls, request: Request, search: str) -> dict:
        """
        Метод для отображения всех данных поста в каталоге
        :param request: Request
        :param search: str
        :return: dict
        """
        search = search.lower() if search else None

        if search is None:
            post = PostRepository.get_all_catalog_posts()
        else:
            post = PostRepository.get_specific_catalog_posts(search)

        context = {"request": request, "arts": []}

        if post:
            for i in range(len(post)):
                context["arts"].append(
                    {
                        "price": post[i][0],
                        "photo_url": post[i][1],
                        "username": post[i][2],
                        "title": post[i][3],
                    }
                )

        return context

    @classmethod
    def delete_catalog_post(cls, data: PostInfoSchema, username: str) -> None:
        """
        Метод для приведения к правильному виду ссфлок файлов перед их удалением из каталога
        :param data: PosInfo
        :param username: str
        :return: None
        """
        link = data.link

        if link.startswith("../../"):
            link = link.removeprefix("../../")

        post_exists = PostRepository.check_post_exists_in_catalog(username, link)

        if post_exists:
            PostRepository.delete_post_from_catalog(username, link)
            os.remove(link)

    @classmethod
    def add_to_basket(cls, data: PostInfoSchema, username: str) -> None:
        """
        Метод для корректного добавления файлов в кразину
        :param data: PostInfo
        :param username: str
        :return: None
        """
        link = data.link

        post_exists = PostRepository.check_post_in_basket(username, link)

        if not post_exists:
            PostRepository.put_post_in_basket(username, link)

    @classmethod
    def get_basket_posts(
        cls, request: Request, username: str, token: str
    ) -> dict | RedirectResponse:
        """
        Метод для вывода всех данных поста в карзие пользователя
        :param request: Request
        :param username: str
        :param token: str
        :return: dict | RedirectResponse
        """
        try:
            username_from_token = PostService.check_token_time(token)
        except Exception:
            return RedirectResponse("/login")

        if username_from_token != username:
            return RedirectResponse(f"/basket/{username_from_token}/{token}")

        posts = PostRepository.get_posts_from_basket(username)
        context = {
            "request": request,
            "username": username,
            "amount_art": len(posts),
            "arts": [],
        }

        for post in posts:
            path = post[1]
            if path.startswith("static/"):
                path = f"../../{path}"
            context["arts"].append(
                {"price": post[0], "photo_url": path, "author": post[2]}
            )
        return context

    @classmethod
    def delete_basket_post(cls, data: PostInfoSchema, username: str) -> None:
        """
        Метод для приведения к правильному виду ссфлок файлов перед их удалением из карзины
        :param data: PostInfo
        :param username: str
        :return: None
        """
        link = data.link
        if link.startswith("../../"):
            link = link.removeprefix("../../")

        post_exists = PostRepository.check_post_in_basket(username, link)

        if post_exists:
            PostRepository.delete_post_from_basket(username, link)

    @classmethod
    def uploading_post(
        cls, price: str, username: str, file: UploadFile, title: str
    ) -> None:
        """
        Метод для обработки данных, которые пользователь хочет выложить в качестве поста
        :param price: str
        :param username: str
        :param file: UploadFile
        :param title: str
        :return: None
        """
        allowed_files = ("png", "jfif", "jpg", "jpeg", "webp", "svg", "tiff", "psd")

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
                raise HTTPException(
                    detail="Price is a number, not letters", status_code=404
                )
            if price < 0 or price > 999999.99:
                raise HTTPException(
                    detail="Bro, you can not ask for this price", status_code=404
                )
            if len(title) > 30:
                raise HTTPException(detail="Title is too long", status_code=404)
            price = round(price, 2)

            PostRepository.create_post(
                username=username, price=price, link=link, title=title
            )

    @classmethod
    def check_token_time(cls, data: str) -> str:
        """
        Метод для проверки валидности токен, истек ли он. Если он не истек, возвращает username
        :param data: str
        :return: str
        """
        try:
            payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        except exceptions.ExpiredSignatureError:
            raise HTTPException(detail="Token expired", status_code=403)
        username = payload["sub"]

        return username
