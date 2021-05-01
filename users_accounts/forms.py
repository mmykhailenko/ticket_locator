from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from users_accounts.models import CustomUser


class CustomUserAdminForm(UserCreationForm):
    """Form is needed to add two fields to the standard form that django generates
    based on the User model, and validate the correct password"""

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email","password1","password2",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email","password",)