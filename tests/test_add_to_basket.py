import unittest
import sqlite3

from consts import DB_LINK
from schemes.post_schemes import PostInfoSchema
from service.posts_services import PostService
from service.users_services import UserService

class TestAddToBasket(unittest.TestCase):
    def setUp(self):
        self.data = PostInfoSchema(access_token=UserService.create_access_token(
            "example_name",
            expires_delta=None
            ),
            link="static/images/da.png"
        )

        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()

            user_exists = cursor.execute(
                """
                    SELECT username, password FROM users
                    WHERE username = "example_name" AND password = "123456"
                """
            ).fetchone()

            if not user_exists:
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
                        VALUES (
                        "example_name",
                        "123456",
                        "User",
                        "User",
                        "User",
                        "8900000000",
                        "example@gmal.com",
                        "123456890",
                        "1234123412341234"
                        )
                """,
                )
                con.commit()

            post_exists = cursor.execute(
                """
                    SELECT id FROM posts
                    WHERE photo_url = "static/images/da.png"
                """
            ).fetchone()

            if not post_exists:
                cursor.execute(
                    """
                        INSERT INTO posts (
                            user_id,
                            price,
                            photo_url,
                            description
                        )
                        VALUES (
                            (SELECT id FROM users WHERE username = "example_name"),
                            "20",
                            "static/images/da.png",
                            "something"
                        )
                    """
                )
                con.commit()

    def testAddToBasket(self):
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            post_before = cursor.execute(
                """
                     SELECT id FROM basket_posts
                     WHERE art_id = (SELECT id FROM posts WHERE photo_url = "static/images/da.png")
                """
            ).fetchone()
            self.assertIsNone(post_before)
            self.assertEqual(PostService.add_to_basket(self.data, username="example_name"), None)
            post_after = cursor.execute(
                """
                     SELECT id FROM basket_posts
                     WHERE art_id = (SELECT id FROM posts WHERE photo_url = "static/images/da.png")
                """
            ).fetchone()
            self.assertIsNotNone(post_after)
