from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Review

# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'followings')