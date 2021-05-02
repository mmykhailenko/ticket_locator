from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser"""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Method controls the creation of a user in the project"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Method controls the creation of a superuser in the project"""
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser


class CustomUser(AbstractUser):
    """Model replaces the standard user with a custom one"""

    id = models.BigAutoField(primary_key=True, verbose_name="user id")
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(verbose_name="user email", unique=True, db_index=True)
    password = models.CharField(max_length=256, verbose_name="password")

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
