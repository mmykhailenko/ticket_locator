
from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager,):
    """Define a model manager for CustomUser"""

    use_in_migrations = True

    def create_user(self, email, password = None):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password = None):
        superuser = self.create_user(email,password)
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser

class CustomUser(AbstractBaseUser):
    """Model CustomUser structure
     - id
     - email(email)
     - password(hash)
     - active(bool, True if user available)"""

    id = models.BigAutoField(primary_key=True, verbose_name="user id")
    email = models.EmailField(verbose_name="user email", unique=True, db_index=True)
    password = models.CharField(max_length=256, verbose_name="password")
    is_active = models.BooleanField(verbose_name="active status", default=True)
    is_staff = models.BooleanField(verbose_name="staff", default=False)# This parameter was added because the internal
                                                                        # structure of Django requires this parameter
                                                                        # to separate user access.

    is_admin = models.BooleanField(verbose_name="admin", default=False) # similar to previous

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


