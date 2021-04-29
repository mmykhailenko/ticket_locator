from django.contrib import admin

from .models.role_actions_set_model import ActionsSet, ActionsSetAdmin
from .models.role_users_model import UserRole, UserRoleAdmin
from .models.search_history_model import SearchHistory, SearchHistoryAdmin
from .models.user_model import User, UserAdmin

admin.site.register(SearchHistory, SearchHistoryAdmin) # register model SearchHistory
admin.site.register(ActionsSet, ActionsSetAdmin) # register model ActionsSet
admin.site.register(UserRole, UserRoleAdmin) # register model UserRole
admin.site.register(User, UserAdmin) # register model User