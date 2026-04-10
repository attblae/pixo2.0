import sqlite3
from consts import DB_LINK


class PostRepository:
    @classmethod
    def get_posts_from_account(cls):
        """
        Метод для получения всех постов пользователей из аккаунта для дальнейшего вывода
        постов отосящихся только к определенному  пользователю
        :return: tuple | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()

            post = cursor.execute("""
                SELECT posts.price, posts.photo_url, users.username
                FROM posts
                JOIN users
                ON posts.user_id = users.id
                """).fetchall()

        return post if post else None

    @classmethod
    def get_all_catalog_posts(cls):
        """
        Метод для получения всех постов
        :return: tuple | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            post = cursor.execute("""
                SELECT posts.price, posts.photo_url, users.username, posts.description
                FROM posts
                JOIN users
                ON posts.user_id = users.id
                """).fetchall()

        return post if post else None

    @classmethod
    def get_specific_catalog_posts(cls, search: str):
        """
        Метод для поиска определеных постов через поле search
        :param search: str
        :return: tuple | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            post = cursor.execute(
                """
                SELECT posts.price, posts.photo_url, users.username, posts.description
                FROM posts
                JOIN users
                ON posts.user_id = users.id
                WHERE lower(users.username) LIKE ? OR lower(posts.description) LIKE ?
                """,
                (f"%{search}%", f"%{search}%"),
            ).fetchall()

        return post if post else None

    @classmethod
    def check_post_in_basket(cls, username: str, link: str):
        """
        Метод для поиска поста в карзине по его ссылке и имени пользоватедя, который кладет этот пост в карзину
        :param username: str
        :param link: str
        :return: tuple | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            post_exists = cursor.execute(
                """
                    SELECT basket_posts.art_id FROM basket_posts
                    JOIN posts ON basket_posts.art_id = posts.id
                    JOIN users ON basket_posts.user_id = users.id
                    WHERE posts.photo_url = ? AND users.username = ?
                """,
                (link, username),
            ).fetchall()

        return post_exists if post_exists else None

    @classmethod
    def put_post_in_basket(cls, username: str, link: str):
        """
        Метод для добавления поста в карзину полььзователя
        :param username: str
        :param link: str
        :return: None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                    INSERT INTO basket_posts (
                        user_id,
                        art_id)
                    VALUES (
                        (SELECT id FROM users WHERE username = ?),
                        (SELECT id FROM posts WHERE photo_url = ?)
                    )
            """,
                (
                    username,
                    link,
                ),
            ).fetchall()
            con.commit()

    @classmethod
    def get_posts_from_basket(cls, username: str):
        """
        Метод для полученния всех постов, которые пользователь добавил в карзину, по его нику
        :param username: str
        :return: tuple | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()

            posts = cursor.execute(
                """
                    SELECT posts.price, posts.photo_url, users.username FROM basket_posts
                    JOIN users ON basket_posts.user_id = users.id
                    JOIN posts ON basket_posts.art_id = posts.id
                    WHERE basket_posts.user_id = (SELECT id FROM users WHERE username = ?)
                """,
                (username,),
            ).fetchall()

        return posts

    @classmethod
    def delete_post_from_basket(cls, username: str, link: str):
        """
        Метод для удаления поста из карзины пользователя по его ссылке и имени самого пользователя
        :param username: str
        :param link: str
        :return: None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                DELETE FROM basket_posts
                WHERE art_id = (
                    SELECT id FROM posts WHERE photo_url = ?
                ) AND user_id = (
                    SELECT id FROM users WHERE username = ?
                )
                """,
                (
                    link,
                    username,
                ),
            )
            con.commit()

    @classmethod
    def check_post_exists_in_catalog(cls, username, link):
        """
        Метод для проверки существования поста в каталоге по его ссылке и нику авора поста
        :param username: str
        :param link: str
        :return: tuple | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()

            post_exists = cursor.execute(
                """
                    SELECT photo_url FROM posts
                    JOIN users
                    ON posts.user_id = users.id
                    WHERE users.username = ? and posts.photo_url = ?
                """,
                (
                    username,
                    link,
                ),
            ).fetchall()

        return post_exists if post_exists else None

    @classmethod
    def delete_post_from_catalog(cls, username: str, link: str):
        """
        Метод для удаления поста из каталога по его ссылке и нику автора поста
        :param username: str
        :param link: str
        :return: None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                DELETE FROM posts
                WHERE photo_url = ?
                AND user_id = (
                    SELECT id FROM users WHERE username = ?
                )
                """,
                (
                    link,
                    username,
                ),
            )
            con.commit()

    @classmethod
    def count_amount_catalog_posts(cls):
        """
        Метод для подсчета количества постов в каталоге
        :return: int
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            amount_art = cursor.execute("""
                    SELECT COUNT(id) FROM posts
                """).fetchone()

        return amount_art[0]

    @classmethod
    def create_post(cls, username: str, price: float, link: str, title: str):
        """
        Метод созданния поста в каталоге
        :param username: str
        :param price: float
        :param link: str
        :param title: str
        :return: None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                    INSERT INTO posts (
                        user_id,
                        price,
                        photo_url,
                        description
                    )
                    VALUES (
                        (SELECT id FROM users WHERE username = ?),
                        ?,
                        ?,
                        ?
                    )
                """,
                (username, float(price), link, title),
            )
            con.commit()
