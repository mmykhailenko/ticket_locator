from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=120)
    role = models.IntegerField()
    active = models.BooleanField()

class SearchHistory(models.Model):
    depart_city = models.CharField(max_length=30)
    araivl_city = models.CharField(max_length=30)
    depart_date = models.DateTimeField(auto_now_add=True)
    araivl_date = models.DateTimeField(auto_now_add=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
