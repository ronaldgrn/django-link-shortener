from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.
def get_expiry():
    return datetime.now() + timedelta(seconds=120)


class UrlMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_url = models.CharField(max_length=256)
    short_url = models.CharField(max_length=50, unique=True, db_index=True)
    usage_count = models.IntegerField(default=0)
    max_count = models.IntegerField(default=-1)
    lifespan = models.IntegerField(default=-1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_expired = models.DateTimeField(default=get_expiry)

    def __str__(self):
        return self.full_url


class UrlProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    url_count = models.IntegerField(default=0)
    max_urls = models.IntegerField(default=-1)
    max_concurrent_urls = models.IntegerField(default=100)

    # TODO: Lifespan from SETTINGS
    default_lifespan = models.IntegerField(default=120)
