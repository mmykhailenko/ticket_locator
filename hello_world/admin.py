from django.contrib import admin

from .models import User, SearchHistory

admin.site.register(User)
admin.site.register(SearchHistory)
