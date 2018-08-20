from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, error_messages={
        'unique': "A user with that email already exists."
    })
