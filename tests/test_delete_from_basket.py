import unittest
from service.posts_services import PostService

class TestDeleteBasketPost(unittest.TestCase):
    def setUp(self):
        class PostInfoSchema:
            access_token:

    def test_delete_basket_post(self):
        self.assertEqual(PostService.delete_basket_post(""), 'FOO')