from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    email = models.EmailField('E-Mail')
    password = models.CharField(max_length=32)
    # role = models.ForeignKey('role') ?
    active = models.BooleanField('Activity', default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def save(self, **kwargs):
        some_salt = 'some_salt'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)


class SearchHistory(models.Model):
    departure_city = models.CharField('Departure city', max_length=128)
    arrival_city = models.CharField('Arrival city', max_length=128)
    departure_date = models.DateTimeField('Departure date')
    arrival_date = models.DateTimeField('Arrival date')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Search history'
        verbose_name_plural = 'Search history'

    def __str__(self):
        return f"{self.departure_city} -> {self.arrival_city}"
