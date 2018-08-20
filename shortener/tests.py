from django.test import TestCase
from shortener.models import UrlMap, UrlProfile
from shortener import shortener
from django.db import models
from tests.models import CustomUser


class UrlMapTestCase(TestCase):
    def setUp(self):
        self.bob = CustomUser.objects.create_user('bob', 'bob@bob.com', 'bobpassword')
        self.alice = CustomUser.objects.create_user('alice', 'alice@alice.com', 'alicepassword')

    def test_url_creation(self):
        url = shortener.create(self.bob, "http://devget.net/")
        self.assertEqual(shortener.expand(url), "http://devget.net/")

        # TODO: write tests to test security features
