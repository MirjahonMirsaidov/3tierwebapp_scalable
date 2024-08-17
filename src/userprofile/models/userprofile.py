import random
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from userprofile.manager import ProfileManager


class UserProfile(AbstractUser):
    """ Profile (custom User ) model """
    role = models.ForeignKey('userprofile.Role', null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=256, default=uuid.uuid4, unique=True)
    email = models.EmailField(null=True, unique=True)
    phone_number = models.CharField(max_length=12, null=True, unique=True)
    middle_name = models.CharField(max_length=150, blank=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    # model manager
    objects = ProfileManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        db_table = "profile"




