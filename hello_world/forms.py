from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class SearchForm(forms.Form):
    departure_airport = forms.CharField(max_length=100)
    arrival_airport = forms.CharField(max_length=100)
    departure_date = forms.DateField()
    direct_flight = forms.BooleanField()
