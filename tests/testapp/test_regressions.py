from django.test import TestCase
from shortener import shortener
from shortener.models import UrlProfile
from tests.testapp.models import CustomUser
import time


class RegressionsTestCase(TestCase):
    def setUp(self):
        self.bob = CustomUser.objects.create_user('bob', 'bob@bob.com', 'bobpassword')
        self.alice = CustomUser.objects.create_user('alice', 'alice@alice.com', 'alicepassword')

    def test_negative_timezone(self):
        with self.settings(TIME_ZONE="America/New_York"):  # negative timezone UTC-5
            shortener.create(self.bob, "https://devget.net/")
