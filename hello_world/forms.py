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


class SearchTourForm(forms.Form):
	departure_airport = forms.CharField(max_length=3, min_length=3)
	arrival_airport = forms.CharField(max_length=3, min_length=3)
	departure_date = forms.DateField(widget=forms.SelectDateWidget())
