import unittest
import sqlite3

from fastapi import UploadFile

from consts import DB_LINK
from schemes.post_schemes import PostInfoSchema
from service.posts_services import PostService
from service.users_services import UserService

class TestUploadPost(unittest.TestCase):
    def setUp(self):
        import io
        with open('static/images/0.png', 'rb') as f:
            self.file = UploadFile(
                filename="0.png",
                file=io.BytesIO(f.read())
            )

    def test_some(self):
        print(self.file)
        self.assertIs(1, 1)