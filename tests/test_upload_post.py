import unittest
import sqlite3
import io
import os

from fastapi import UploadFile
from consts import DB_LINK
from service.posts_services import PostService

class TestUploadPost(unittest.TestCase):
    def setUp(self):
        with open('static/images/0.png', 'rb') as f:
            self.file = UploadFile(
                filename="0.png",
                file=io.BytesIO(f.read())
            )

        self.price = "250.75"
        self.username = "test_user"
        self.title = "Test"

        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()

            user_exists = cursor.execute(
                """
                SELECT username FROM users
                WHERE username = ?
                """,
                (self.username,)
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
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        self.username,
                        "123456",
                        "Test",
                        "User",
                        "Test",
                        "8900000001",
                        "test@gmail.com",
                        "123456892",
                        "1234123412341235"
                    )
                )
                con.commit()

    def test_uploading_post_success(self):
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            posts_before = cursor.execute(
                "SELECT COUNT(*) FROM posts WHERE user_id = (SELECT id FROM users WHERE username = ?)",
                (self.username,)
            ).fetchone()[0]

        PostService.uploading_post(
            price=self.price,
            username=self.username,
            file=self.file,
            title=self.title
        )

        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            posts_after = cursor.execute(
                "SELECT COUNT(*) FROM posts WHERE user_id = (SELECT id FROM users WHERE username = ?)",
                (self.username,)
            ).fetchone()[0]
            self.assertEqual(posts_after, posts_before + 1)

            new_post = cursor.execute(
                """
                SELECT posts.price, posts.photo_url, posts.description, users.username
                FROM posts
                JOIN users
                ON posts.user_id = users.id
                WHERE users.username = ?
                ORDER BY posts.id DESC
                LIMIT 1
                """,
                (self.username,)
            ).fetchone()

            self.assertIsNotNone(new_post)
            self.assertEqual(float(new_post[0]), 250.75)
            self.assertTrue(new_post[1].startswith("static/images/"))
            self.assertEqual(new_post[2], "Test")
            self.assertEqual(new_post[3], self.username)

            self.assertTrue(os.path.exists(new_post[1]))

    def test_uploading_post_invalid_file_type(self):
        invalid_file = UploadFile(
            filename="document.pdf",
            file=io.BytesIO(b"fake pdf")
        )

        with self.assertRaises(Exception) as context:
            PostService.uploading_post(
                price=self.price,
                username=self.username,
                file=invalid_file,
                title=self.title
            )
        self.assertIn("You can not take this file", str(context.exception))

    def test_uploading_post_invalid_price(self):
        with self.assertRaises(Exception) as context:
            PostService.uploading_post(
                price="not_a_number",
                username=self.username,
                file=self.file,
                title=self.title
            )
        self.assertIn("Price is a number, not letters", str(context.exception))

    def test_uploading_post_price_out_of_range(self):
        with self.assertRaises(Exception) as context:
            PostService.uploading_post(
                price="1000000.00",
                username=self.username,
                file=self.file,
                title=self.title
            )
        self.assertIn("Bro, you can not ask for this price", str(context.exception))

    def test_uploading_post_long_title(self):
        long_title = "A" * 31

        with self.assertRaises(Exception) as context:
            PostService.uploading_post(
                price=self.price,
                username=self.username,
                file=self.file,
                title=long_title
            )
        self.assertIn("Title is too long", str(context.exception))
