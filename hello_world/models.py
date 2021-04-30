from django.conf import settings
from django.db import models


class SearchHistoryPost(models.Model):

    departure_city = models.CharField(max_length=40, )
    arrival_city = models.CharField(max_length=40)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
