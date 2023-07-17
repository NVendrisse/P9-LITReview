from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_followed = models.BooleanField
    is_following = models.BooleanField
    