from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from .role_actions_set_model import ActionsSet


class UserRole(models.Model):
    """Model defines a list of possible user roles in the project """
    id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=90)
    actions_set = models.OneToOneField(ActionsSet, on_delete=models.CASCADE, related_name="actions_set")

    def __str__(self):
        upper_name = str(self.role_name).upper()
        return f"Role name: {upper_name}"


class UserRoleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Role name", {'fields': ["role_name"]}),
        ("Actions set", {'fields': ["actions_set"]})
    ]
    list_display = ["role_name", "show_action_set_url"]
    list_filter = ["actions_set"]
    search_fields = ["role_name"]
    save_on_top = True
    save_as = True

    def show_action_set_url(self, obj):
        """Creates a link to the change action_set"""
        actions_set_id= obj.actions_set.id
        return format_html("<a href='/admin/hello_world/actionsset/{url}'>{name}</a>",
                           url=actions_set_id, name=obj.actions_set)

    show_action_set_url.allow_tags = True
    show_action_set_url.short_description = 'Actions set'