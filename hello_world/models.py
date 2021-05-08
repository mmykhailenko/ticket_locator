from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField('email address', unique=True)
	is_active = models.BooleanField('active', default=True)
	is_staff = models.BooleanField('staff', default=True)

	object = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'

	def __str__(self):
		return self.email


class SearchHistory(models.Model):
	depart_city = models.CharField(max_length=128, blank=False)
	arrival_city = models.CharField(max_length=128, blank=False)
	depart_date = models.DateTimeField()
	arrival_date = models.DateTimeField()
	user = models.ForeignKey('User', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.depart_date} -> {self.arrival_city}"
