from django.db import models

# Create your models here.
# User:
# - id
# - email(email)
# - password(hash)
# - role(id of role, related field with Role model)
# - active(bool, True if user available)
#
# SearchHistory:
# - id
# - Depart City
# - Araivl City
# - depart date
# - araivl date
# - user_id(related field with User model)


class User(models.Model):
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)
    active = models.BooleanField(default=False)


class SearchHistory(models.Model):
    depart_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)
    depart_date = models.DateField()
    arrival_date = models.DateField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
