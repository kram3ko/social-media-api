from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from config import settings


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(max_length=500, blank=True)
    photo = models.ImageField(upload_to="profile/", blank=True)
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
