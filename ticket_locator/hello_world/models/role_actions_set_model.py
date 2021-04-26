from django.contrib import admin
from django.db import models


class ActionsSet(models.Model):
    """Model describes the possible actions of the
    user according to his role in the database"""
    id = models.BigAutoField(primary_key=True)
    actions_set_name = models.CharField(max_length=250)
    on_read = models.BooleanField(null=False)
    on_write = models.BooleanField(null=False)
    on_update = models.BooleanField(null=False)
    on_create = models.BooleanField(null=False)
    on_delete = models.BooleanField(null=False)


    def __str__(self):
        upper_name = str(self.actions_set_name).upper()
        return f"Actions set: {upper_name}"


class ActionsSetAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Actions set name", {'fields': ["actions_set_name"]}),
        ('Permissions', {'fields': ["on_read", "on_write", "on_update", "on_create", "on_delete"]})
    ]
    list_display = ["actions_set_name", "on_read", "on_write", "on_update", "on_create", "on_delete"]
    list_filter = ["actions_set_name"]
    search_fields = ["actions_set_name__startswith"]
    save_on_top = True
    save_as = True
    list_editable = ["on_read", "on_write", "on_update", "on_create", "on_delete"]

