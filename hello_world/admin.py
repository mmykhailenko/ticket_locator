from django.contrib import admin
from .models.search_history_model import SearchHistory, SearchHistoryAdmin

admin.site.register(SearchHistory, SearchHistoryAdmin) # register model SearchHistory
