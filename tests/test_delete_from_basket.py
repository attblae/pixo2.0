import unittest

from service.posts_services import PostService
from service.users_services import UserService

class TestDeleteBasketPost(unittest.TestCase):
    def setUp(self):
        class PostInfoSchema:
            access_token: dict = UserService.create_access_token("example_name", expires_delta=None)
            link: str = "static/images/0.png"

    def test_delete_basket_post(self):
        self.assertEqual(PostService.delete_basket_post(), 'FOO')