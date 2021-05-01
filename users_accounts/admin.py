from django.contrib import admin
from users_accounts.models import CustomUser
from users_accounts.forms import CustomUserAdminForm



class CustomUserAdmin(admin.ModelAdmin):
    """Class model views User in the admin panel"""
    form = CustomUserAdminForm
    fieldsets = [
        ("E-mail", {'fields': ["email"]}),
        ("Input password/Change password", {'fields': ["password1", "password2"]}),
        ("Active status", {'fields': ["is_active", "is_staff","is_admin"]})
    ]
    list_editable = ["is_active","is_staff","is_admin"]
    list_display = ["email", "is_active","is_staff","is_admin"]
    list_filter = ["email"]
    search_fields = ["email__startswith"]

admin.site.register(CustomUser, CustomUserAdmin)
