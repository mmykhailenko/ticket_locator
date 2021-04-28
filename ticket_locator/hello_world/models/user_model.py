from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.db import models
from django import forms
from django.utils.html import format_html

from .role_users_model import UserRole


class User(models.Model):
    """Model User structure
     - id
     - email(email)
     - password(hash)
     - role(id of role, related field with Role model)
     - active(bool, True if user available)"""

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    id = models.BigAutoField(primary_key=True, verbose_name="user id")
    email = models.EmailField(verbose_name="user email", unique=True, db_index=True)
    password = models.CharField(max_length=256, verbose_name="password")
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT, related_name="role_id")
    active = models.BooleanField(verbose_name="active status", default=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """Overriding the method of saving data to the database,
        the password from the admin panel form is saved as a password hash"""
        hash_password = make_password(self.password, None, 'md5')
        self.password = hash_password
        super(User, self).save()


class UserAdminForm(forms.ModelForm):
    """Form is needed to add two fields to the standard form that django generates
    based on the User model, and validate the correct password"""

    class Meta:
        model = User
        fields = "__all__"

    password = forms.CharField(max_length=256, label="Password", widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=256, label="Password confirmation",
                                            widget=forms.PasswordInput)

    def clean_password_confirmation(self):
        if self.cleaned_data["password"] != self.cleaned_data["password_confirmation"]:
            raise forms.ValidationError("Password isn't correct")
        return self.cleaned_data["password"]


class UserAdmin(admin.ModelAdmin):
    """Class model views User in the admin panel"""
    form = UserAdminForm
    fieldsets = [
        ("E-mail", {'fields': ["email"]}),
        ("Input password/Change password", {'fields': ["password", "password_confirmation"]}),
        ("Role", {'fields': ["role"]}),
        ("Active status", {'fields': ["active"]})
    ]
    list_editable = ["active"]
    list_display = ["email", "show_role_url", "active"]
    list_filter = ["role"]
    search_fields = ["email__startswith"]

    def show_role_url(self, obj):
        """Creates a link to the change role"""
        role_id = obj.role.id
        return format_html("<a href='/admin/hello_world/userrole/{url}'>{name}</a>",
                           url=role_id, name=obj.role)

    show_role_url.allow_tags = True
    show_role_url.short_description = 'Role'

