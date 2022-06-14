import uuid
import os
from django.contrib.auth.models import BaseUserManager

def upload_to(instance, filename):
    return 'user_profile_image/{}/{}'.format(instance.user_id, filename)


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, full_name, password, **extra_fields):
        """New user profile creation"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_basic", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError('User must have an email address!')
        if not password:
            raise ValueError("User must have password")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)


        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser with details"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user