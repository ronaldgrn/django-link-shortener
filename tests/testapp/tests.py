from django.test import TestCase
from shortener import shortener
from shortener.models import UrlProfile
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
                shortener.create(self.bob, "http://devget.net/")

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


class UrlProfileTestCase(TestCase):
    """
    Test User overrides
    """
    def setUp(self):
        self.ronald = CustomUser.objects.create_user('ronald', 'ronald@ronald.com', 'ronaldpassword')
        self.urlProfile, created = UrlProfile.objects.update_or_create(
            user=self.ronald,
            defaults={
                'enabled': None,
                'max_urls': None,
                'max_concurrent_urls': None,
                'default_lifespan': None,
                'default_max_uses': None
            },
        )

    # def tearDown(self):
    #     # Reset UrlProfile
    #     UrlProfile.objects.update_or_create(
    #         user=self.ronald,
    #         defaults={
    #             'enabled': None,
    #             'max_urls': None,
    #             'max_concurrent_urls': None,
    #             'default_lifespan': None,
    #             'default_max_uses': None
    #         },
    #     )

    def test_shortener_enabled_setting(self):
        with self.settings(SHORTENER_ENABLED=False):
            with self.assertRaisesMessage(PermissionError, 'not authorized to create shortlinks'):
                shortener.create(self.ronald, "http://devget.net/")

            # Ensure we can override with UrlProfile
            self.urlProfile.enabled = True
            self.urlProfile.save()
            shortener.create(self.ronald, "http://devget.net/")

            # Ensure we can omit with UrlProfile
            self.urlProfile.enabled = None
            self.urlProfile.save()
            with self.assertRaisesMessage(PermissionError, 'not authorized to create shortlinks'):
                shortener.create(self.ronald, "http://devget.net/")

    def test_max_urls_setting(self):
        with self.settings(SHORTENER_MAX_URLS=0):
            with self.assertRaisesMessage(PermissionError, 'url quota exceeded'):
                shortener.create(self.ronald, "http://devget.net/")

            # Ensure we can override with UrlProfile
            self.urlProfile.max_urls = 2
            self.urlProfile.save()

            shortener.create(self.ronald, "http://devget.net/")
            shortener.create(self.ronald, "http://devget.net/")
            with self.assertRaisesMessage(PermissionError, 'url quota exceeded'):
                shortener.create(self.ronald, "http://devget.net/")

    def test_max_concurrent_setting(self):
        with self.settings(SHORTENER_MAX_CONCURRENT=2):
            shortener.create(self.ronald, "http://devget.net/")
            shortener.create(self.ronald, "http://devget.net/")
            with self.assertRaisesMessage(PermissionError, 'concurrent quota exceeded'):
                shortener.create(self.ronald, "http://devget.net/")

            # Ensure we can override with UrlProfile
            self.urlProfile.max_concurrent_urls = 3
            self.urlProfile.save()

            shortener.create(self.ronald, "http://devget.net/")
            with self.assertRaisesMessage(PermissionError, 'concurrent quota exceeded'):
                shortener.create(self.ronald, "http://devget.net/")

    def test_lifespan_setting(self):
        with self.settings(SHORTENER_LIFESPAN=2):   # 4 seconds
            url = shortener.create(self.ronald, "http://blog.devget.net/")
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            time.sleep(3)
            with self.assertRaisesMessage(PermissionError, 'shortlink expired'):
                self.assertEqual(shortener.expand(url), "http://blog.devget.net/")

            # Ensure we can override with UrlProfile
            self.urlProfile.default_lifespan = 6
            self.urlProfile.save()

            url = shortener.create(self.ronald, "http://blog.devget.net/")
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            time.sleep(4)
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            time.sleep(3)
            with self.assertRaisesMessage(PermissionError, 'shortlink expired'):
                self.assertEqual(shortener.expand(url), "http://blog.devget.net/")

    def test_max_uses_setting(self):
        with self.settings(SHORTENER_MAX_USES=0):
            url = shortener.create(self.ronald, "http://blog.devget.net/")
            with self.assertRaisesMessage(PermissionError, 'max usages for link reached'):
                # Ensure error is raised when we hit limit
                shortener.expand(url)

            # Ensure we can override with UrlProfile
            self.urlProfile.default_max_uses = 2
            self.urlProfile.save()

            url = shortener.create(self.ronald, "http://blog.devget.net/")
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            self.assertEqual(shortener.expand(url), "http://blog.devget.net/")
            with self.assertRaisesMessage(PermissionError, 'max usages for link reached'):
                # Ensure error is raised when we hit limit
                shortener.expand(url)