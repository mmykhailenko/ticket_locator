from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users_accounts.models import CustomUser


class CustomUserAdminForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "password1", "password2",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password",)
