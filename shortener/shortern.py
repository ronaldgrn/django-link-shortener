from shortener.models import UrlMap, UrlProfile
from django.conf import settings
from django.db import IntegrityError

import random
import string


def get_random(tries=0):
    if hasattr(settings, 'SHORTENER_LENGTH'):
        length = settings.SHORTENER_LENGTH
    else:
        length = 5

    length += tries

    # Removed l, I, 1
    # return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    return ''.join(random.choice("ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz234567890") for _ in range(length))


def convert(user, link):
    # Try up to three times to generate a random number without duplicates.
    # Each time increase the number of allowed characters
    for tries in range(3):
        try:
            short = get_random(tries)
            m = UrlMap(user=user, full_url=link, short_url=short)
            m.save()
            return m.short_url
        except IntegrityError:
            continue

    raise KeyError("Could not generate unique shortlink")


def revert(link):
    try:
        url = UrlMap.objects.get(short_url__exact=link)
        return url
    except UrlMap.DoesNotExist:
        return -1  # TODO: improve this

