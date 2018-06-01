from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from shortener.models import UrlMap, UrlProfile
from shortener import shortener


class UrlMapTestCase(TestCase):
    def setUp(self):
        self.bob = User.objects.create_user('bob', 'bob@bob.com', 'bobpassword')
        self.alice = User.objects.create_user('alice', 'alive@alice.com', 'alicepassword')

    def test_url_creation(self):
        url = shortener.create(self.bob, "http://devget.net/")
        self.assertEqual(shortener.expand(url), "http://devget.net/")

        # TODO: write tests to test security features
