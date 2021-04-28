from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TicketLocatorUser, SearchHistory


class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'departure_date', 'arrival_date')


admin.site.register(TicketLocatorUser, UserAdmin)
admin.site.register(SearchHistory)

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'active', 'is_staff')
