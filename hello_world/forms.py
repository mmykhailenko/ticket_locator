from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
    ##################### Widgets ############################
    departure_airport_widget = forms.TextInput(
        attrs={
            "placeholder": "IATA format",
            "required": True,
            "class": "form-control",
            "type": "text",
        }
    )
    departure_date_widget = forms.DateInput(
        attrs={"required": True, "class": "form-control", "type": "date"}
    )
    ######################### Form ###############################
    departure_airport = forms.CharField(max_length=3, widget=departure_airport_widget)
    arrival_airport = forms.CharField(max_length=3, widget=departure_airport_widget)
    departure_date = forms.DateField(widget=departure_date_widget)
    direct_flight = forms.BooleanField(required=False)
