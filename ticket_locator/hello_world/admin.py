from django.contrib import admin
from .models import User, SearchHistory

from django import forms
from django.forms import ModelForm, PasswordInput


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'active')


class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'departure_date', 'arrival_date')


admin.site.register(User, UserAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)


