from shortener.models import UrlMap, UrlProfile
from django.conf import settings
from django.db import IntegrityError
from django.db.models import F
from datetime import datetime, timedelta

from django.utils import timezone

import random


def get_random(tries=0):
    length = getattr(settings, 'SHORTENER_LENGTH', 5)
    length += tries

    # Removed l, I, 1
    dictionary = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz234567890"
    return ''.join(random.choice(dictionary) for _ in range(length))

def get_or_create(user, link):
    try:
        m = UrlMap.objects.get(full_url=link);
        return m.short_url;
    except UrlMap.DoesNotExist:
        create(user, link)
    
def create(user, link):
    # check if user allowed to save link
    try:
        # use user settings where set
        p = UrlProfile.objects.get(user=user)
        enabled = p.enabled if p.enabled is not None else getattr(settings, 'SHORTENER_ENABLED', True)
        max_urls = p.max_urls if p.max_urls is not None else getattr(settings, 'SHORTENER_MAX_URLS', -1)
        max_concurrent = p.max_concurrent_urls if p.max_concurrent_urls is not None else getattr(settings, 'SHORTENER_MAX_CONCURRENT', -1)
        lifespan = p.default_lifespan if p.default_lifespan is not None else getattr(settings, 'SHORTENER_LIFESPAN', -1)
        max_uses = p.default_max_uses if p.default_max_uses is not None else getattr(settings, 'SHORTENER_MAX_USES', -1)

    except UrlProfile.DoesNotExist:
        # Use defaults from settings
        enabled = getattr(settings, 'SHORTENER_ENABLED', True)
        max_urls = getattr(settings, 'SHORTENER_MAX_URLS', -1)
        max_concurrent = getattr(settings, 'SHORTENER_MAX_CONCURRENT', -1)
        lifespan = getattr(settings, 'SHORTENER_LIFESPAN', -1)
        max_uses = getattr(settings, 'SHORTENER_MAX_USES', -1)

    # Ensure User is allowed to create
    if not enabled:
        raise PermissionError("not authorized to create shortlinks")

    # Expiry date, -1 to disable
    if lifespan != -1:
        expiry_date = timezone.now() + timedelta(seconds=lifespan)
    else:
        # Avoid using the absolute maximum date to avoid overflow issues
        # when setting negative timezones
        safe_max_date = datetime(datetime.max.year, 1, 1, tzinfo=timezone.get_default_timezone())
        expiry_date = safe_max_date

    # Ensure user has not met max_urls quota
    if max_urls != -1:
        if UrlMap.objects.filter(user=user).count() >= max_urls:
            raise PermissionError("url quota exceeded")

    # Ensure user has not met concurrent urls quota
    if max_concurrent != -1:
        if UrlMap.objects.filter(user=user, date_expired__gt=timezone.now()).count() >= max_concurrent:
            raise PermissionError("concurrent quota exceeded")

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
        raise KeyError("invalid shortlink")

    # ensure we are within usage counts
    if url.max_count != -1:
        if url.max_count <= url.usage_count:
            raise PermissionError("max usages for link reached")

    # ensure we are within allowed datetime
    # print(timezone.now())
    # print(url.date_expired)
    if timezone.now() > url.date_expired:
        raise PermissionError("shortlink expired")

    # Avoid a race condition by not using `+= 1` here, and using F() instead:
    url.usage_count = F("usage_count") + 1
    # Telling `save` to ONLY save changes to the counter. That's all we need
    # to update, and so we'll save a bit of bandwidth by not sending ALL
    # possible values back across the wire, just to update this field:
    # See: https://docs.djangoproject.com/en/5.0/ref/models/instances/#specifying-which-fields-to-save
    url.save(update_fields=["usage_count"])

    return url.full_url

