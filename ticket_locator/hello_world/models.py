from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class TicketLocatorUser(AbstractUser):
    pass


class SearchHistory(models.Model):
    depart_city = models.CharField(max_length=50)
    arrival_city = models.CharField(max_length=50)
    depart_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Search history'
        verbose_name_plural = 'Search history'

    def __str__(self):
        return f"{self.departure_city} => {self.arrival_city}"
