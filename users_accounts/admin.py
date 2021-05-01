from django.contrib import admin
from users_accounts.models import CustomUser
from users_accounts.forms import CustomUserAdminForm


class CustomUserAdmin(admin.ModelAdmin):
    """Class model views User in the admin panel"""
    form = CustomUserAdminForm
    fieldsets = [
        ("E-mail", {'fields': ["email"]}),
        ("Input password/Change password", {'fields': ["password1", "password2"]}),
        ("Active status", {'fields': ["is_active", "is_staff", "is_superuser"]})
    ]
    list_editable = ["is_active", "is_staff", "is_superuser"]
    list_display = ["email", "is_active", "is_staff", "is_superuser", "last_login", "date_joined"]
    list_filter = ["email", "is_active", "is_staff", "is_superuser"]
    ordering = ["email"]
    search_fields = ["email__startswith"]


admin.site.register(CustomUser, CustomUserAdmin)
