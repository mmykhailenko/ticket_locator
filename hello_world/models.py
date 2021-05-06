from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField('staff', default=False)
    is_active = models.BooleanField('active', default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class SearchHistory(models.Model):
    departure_city = models.CharField('Departure city', max_length=128)
    arrival_city = models.CharField('Arrival city', max_length=128)
    departure_date = models.DateTimeField('Departure date')
    arrival_date = models.DateTimeField('Arrival date')
    user = models.ForeignKey('User', to_field='email', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Search history'
        verbose_name_plural = 'Search history'

    def __str__(self):
        return f"{self.departure_city} -> {self.arrival_city}"
