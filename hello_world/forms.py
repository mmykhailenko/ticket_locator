from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django import forms

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class SearchAirRouteForm(forms.Form):
    departure_airport_widget = forms.TextInput(
        attrs={
            "placeholder": "Откуда:",
            "required": True,
            "class": "form-control mt-4",
            "type": "text",
            "pattern": "[A-Z]{3}",
            "title": 'IATA код аэропорта. Пример: "BCN", "AMS" ...',
        }
    )
    arrival_airport_widget = forms.DateInput(
        attrs={
            "placeholder": "Куда:",
            "required": True,
            "class": "form-control mt-4",
            "type": "text",
            "pattern": "[A-Z]{3}",
            "title": 'IATA код аэропорта. Пример: "BCN", "AMS" ...',
        }
    )
    departure_date_widget = forms.DateInput(
        attrs={"required": True, "class": "form-control mt-4", "type": "date"}
    )
    departure_airport = forms.CharField(
        max_length=3,
        widget=departure_airport_widget
    )
    arrival_airport = forms.CharField(
        max_length=3,
        widget=arrival_airport_widget
    )
    departure_date = forms.DateField(widget=departure_date_widget)
    direct_flight = forms.BooleanField(required=False)


class RegistrationForm(UserCreationForm):
    email = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("email", "password")
