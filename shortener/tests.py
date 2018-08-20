from django.test import TestCase
from shortener import shortener
from tests.testapp.models import CustomUser
import time


class UrlMapTestCase(TestCase):
    def setUp(self):
        self.bob = CustomUser.objects.create_user('bob', 'bob@bob.com', 'bobpassword')
        self.alice = CustomUser.objects.create_user('alice', 'alice@alice.com', 'alicepassword')

    def test_url_creation(self):
        url = shortener.create(self.bob, "http://devget.net/")
        self.assertEqual(shortener.expand(url), "http://devget.net/")

    def test_invalid_link(self):
        url = shortener.create(self.bob, "http://devget.net/")
        self.assertEqual(shortener.expand(url), "http://devget.net/")  # good shortlink
        with self.assertRaisesMessage(KeyError, 'invalid shortlink'):
            self.assertEqual(shortener.expand('photosynthesis'), "http://devget.net/")  # bad shortlink

    def test_shortener_enabled_setting(self):
        with self.settings(SHORTENER_ENABLED=False):
            with self.assertRaisesMessage(PermissionError, 'not authorized to create shortlinks'):
                url = shortener.create(self.bob, "http://devget.net/")

    def test_max_urls_setting(self):
        with self.settings(SHORTENER_MAX_URLS=2):
            shortener.create(self.bob, "http://devget.net/")
            shortener.create(self.bob, "http://devget.net/")
            with self.assertRaisesMessage(PermissionError, 'url quota exceeded'):
                shortener.create(self.bob, "http://devget.net/")

    def test_max_concurrent_setting(self):
        with self.settings(SHORTENER_MAX_CONCURRENT=2):
            shortener.create(self.bob, "http://devget.net/")
            shortener.create(self.bob, "http://devget.net/")
            with self.assertRaisesMessage(PermissionError, 'concurrent quota exceeded'):
                shortener.create(self.bob, "http://devget.net/")

    def test_lifespan_setting(self):
        with self.settings(SHORTENER_LIFESPAN=4):   # 4 seconds
            url = shortener.create(self.bob, "http://blog.devget.net/")
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            time.sleep(5)
            with self.assertRaisesMessage(PermissionError, 'shortlink expired'):
                self.assertEqual(shortener.expand(url), "http://blog.devget.net/")

    def test_max_uses_setting(self):
        with self.settings(SHORTENER_MAX_USES=2):
            url = shortener.create(self.bob, "http://blog.devget.net/")
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            with self.assertRaisesMessage(PermissionError, 'max usages for link reached'):
                # Ensure error is raised when we hit limit
                shortener.expand(url)

