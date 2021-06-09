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
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Search history'
        verbose_name_plural = 'Search history'

    def __str__(self):
        return f"{self.departure_city} -> {self.arrival_city}"

if __name__ == "__main__":
    print('454545')
    user1 = User.objects.create(id=50,
                                email='test@example.com',
                                is_staff=False,
                                is_active=True)
    user1.save()
    print(user1)

    history1 = SearchHistory.objects.create(id=60,
                                            user=user1,
                                            departure_city='SIN',
                                            arrival_city='AMS',
                                            departure_date="2021-06-06T00:00:00Z",
                                            arrival_date="2021-06-10T00:00:00Z"
                                            )
    history1.save()

    print(history1)