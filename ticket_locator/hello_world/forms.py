from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import TicketLocatorUser


class TicketLocatorUserCreationForm(UserCreationForm):
    class Meta:
        model = TicketLocatorUser
        fields = ('username', 'email', 'password1', 'password2')


class TicketLocatorUserChangeForm(UserChangeForm):
    class Meta:
        model = TicketLocatorUser
        fields = ('username', 'email', 'password1', 'password2')
