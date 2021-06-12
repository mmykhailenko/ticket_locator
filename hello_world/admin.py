from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, SearchHistory


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "email",
        "is_active",
        "is_superuser",
    )
    fieldsets = (
        (None,
         {"fields": ("email", "password", "is_staff", "is_active")}
         ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active"
                ),
            },
        ),
    )
    search_fields = ()
    list_filter = ()
    ordering = ("email",)


class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "departure_date", "arrival_date")


admin.site.register(User, CustomUserAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)
