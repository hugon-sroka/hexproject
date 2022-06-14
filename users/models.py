from datetime import datetime
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFill
from pydantic.schema import timedelta
from rest_framework.fields import ImageField
import uuid
import os
from users.manager import upload_to

def upload_to(instance, filename):
    return 'user_profile_image/{}/{}'.format(instance.full_name, filename)

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def _create_user(self, email, full_name, password=None, **extra_fields):
        """New user profile creation"""

        if not email:
            raise ValueError('User must have an email address!')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, full_name,password, **extra_fields)

    def create_superuser(self, email, full_name, password, **extra_fields):
        """Create and save a new superuser with details"""
        user = self.create_user(email, full_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length = 200)
    email = models.EmailField(unique=True)
    is_active =  models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    is_enterprise = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def get_full_name(self):
        """Get full name of user"""
        return self.full_name
    def __str__(self):
        return self.email

    @property
    def is_premium_plan(self):
        "Is the user a premium user?"
        return self.is_premium

    @property
    def is_enterprise_plan(self):
        "Is the user a premium user?"
        return self.is_enterprise

class Img(models.Model):
    userprofile = models.ForeignKey(UserProfile, related_name='img', on_delete=models.CASCADE,)
    img = models.FileField(upload_to=upload_to)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url

    # class User(AbstractUser):
#   #Boolean fields to select the type of account.
#   is_basic = models.BooleanField(default=False)
#   is_premium = models.BooleanField(default=False)
#   is_enterprise = models.BooleanField(default=False)
#
# class Basic(models.Model):
#     fullname_bs = models.CharField(max_length=250)
#     email = models.EmailField(max_length=100)
#     image = models.ImageField(upload_to='images')
#
# class Premium(models.Model):
#     fullname_pm = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#     email = models.EmailField(max_length=100)
#     image = models.ImageField(upload_to='images')
#
# class Enterprise(models.Model):
#     fullname_en = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#     email = models.EmailField(max_length=100)
#     image = models.ImageField(upload_to='images')



