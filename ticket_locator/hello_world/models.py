from django.db import models
from django import forms


USER_ROLES = sorted([(role, role) for role in ('admin', 'user', 'support')])


class User(models.Model):
	email = models.EmailField(blank=False)
	password = models.CharField(max_length=128, blank=False)
	role = models.CharField(choices=USER_ROLES, default='user', max_length=100)
	active = models.BooleanField(default=True)


class SearchHistory(models.Model):
	depart_city = models.CharField(max_length=128, blank=False)
	arrival_city = models.CharField(max_length=128, blank=False)
	depart_date = models.DateTimeField()
	arrival_date = models.DateTimeField()
	owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
