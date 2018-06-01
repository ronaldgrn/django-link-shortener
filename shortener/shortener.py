from shortener.models import UrlMap, UrlProfile
from django.conf import settings
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.utils import timezone

import random
import string


def get_random(tries=0):
    if hasattr(settings, 'SHORTENER_LENGTH'):
        length = settings.SHORTENER_LENGTH
    else:
        length = 5

    length += tries

    # return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    # Removed l, I, 1
    dictionary = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz234567890"
    return ''.join(random.choice(dictionary) for _ in range(length))


def create(user, link):
    # check if user allowed to save link
    try:
        # use user settings
        p = UrlProfile.objects.get(user=user)
        enabled = p.enabled
        max_urls = p.max_urls
        max_concurrent = p.max_concurrent_urls
        lifespan = p.default_lifespan
        max_uses = p.default_max_uses
    except UrlProfile.DoesNotExist:
        # Use defaults from settings
        if hasattr(settings, 'SHORTENER_ENABLED'):
            enabled = settings.SHORTENER_ENABLED
        else:
            enabled = True

        if hasattr(settings, 'SHORTENER_MAX_URLS'):
            max_urls = settings.SHORTENER_MAX_URLS
        else:
            max_urls = -1

        if hasattr(settings, 'SHORTENER_MAX_CONCURRENT'):
            max_concurrent = settings.SHORTENER_MAX_CONCURRENT
        else:
            max_concurrent = -1

        if hasattr(settings, 'SHORTENER_LIFESPAN'):
            lifespan = settings.SHORTENER_LIFESPAN
        else:
            lifespan = -1

        if hasattr(settings, 'SHORTENER_MAX_USES'):
            max_uses = settings.SHORTENER_MAX_USES
        else:
            max_uses = -1

    # Ensure User is allowed to create
    if not enabled:
        raise PermissionError("User not allowed to access create")

    # Expiry date, -1 to disable
    if lifespan != -1:
        expiry_date = datetime.now() + timedelta(seconds=lifespan)
    else:
        expiry_date = datetime.max

    # Ensure user has not met max_urls quota
    if max_urls != -1:
        if UrlMap.objects.filter(user=user).count() >= max_urls:
            raise PermissionError("User has met url quota")

    # Ensure user has not met concurrent urls quota
    if max_concurrent != -1:
        if UrlMap.objects.filter(user=user, date_expired__gt=datetime.now()).count() >= max_concurrent:
            raise PermissionError("User has met concurrent quota")

    # Try up to three times to generate a random number without duplicates.
    # Each time increase the number of allowed characters
    for tries in range(3):
        try:
            short = get_random(tries)
            m = UrlMap(user=user, full_url=link, short_url=short, max_count=max_uses, date_expired=expiry_date)
            m.save()
            return m.short_url
        except IntegrityError:
            continue

    raise KeyError("Could not generate unique shortlink")


def expand(link):
    try:
        url = UrlMap.objects.get(short_url__exact=link)
    except UrlMap.DoesNotExist:
        raise KeyError("ShortLink Not found")

    # ensure we are within usage counts
    if url.max_count != -1:
        if url.max_count > url.usage_count:
            raise PermissionError("Max usages reached")

    # ensure we are within allowed datetime
    print(datetime.now())
    print(url.date_expired)
    if timezone.now() > url.date_expired:
        raise PermissionError("Link Expired")

    url.usage_count += 1
    url.save()
    return url.full_url

