from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class SearchAirRouteForm(forms.Form):
    ##################### Widgets ############################
    departure_airport_widget = forms.TextInput(attrs={"placeholder": "IATA format", "required": True,
                                                      "class": "form-control", "type": "text"})
    departure_date_widget = forms.DateInput(attrs={"required": True, "class": "form-control", "type": "date"})
    ######################### Form ###############################
    departure_airport = forms.CharField(max_length=3, widget=departure_airport_widget)
    arrival_airport = forms.CharField(max_length=3, widget=departure_airport_widget)
    departure_date = forms.DateField(widget=departure_date_widget)
    direct_flight = forms.BooleanField(required=False)

    def clean_departure_date(self):
        data = self.cleaned_data['departure_date']
        prepared_date = (data.strftime('%Y-%m-%d'))
        return prepared_date

class SingUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
