from django.contrib import admin
from django.db import models
from ticket_locator import settings


class SearchHistory(models.Model):
    """Model search history structure- id
    - Depart City
    - Araivl City
    - depart date
    - araivl date
    - user_id(related field with User model)"""
    class Meta:
        unique_together = (("depart_city", "arrival_city","depart_date","arrival_date","user_id"),)

    id  = models.BigAutoField(primary_key=True)
    depart_city = models.CharField(max_length= 250, null=False)
    arrival_city = models.CharField(max_length=250, null=False)
    depart_date = models.DateField(null=False)
    arrival_date = models.DateField(null=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return str(self.user_id).upper()


class SearchHistoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("User", {"fields": ["user_id"]}),
        ("City", {"fields": ["depart_city","arrival_city"]}),
        ("Date", {"fields": ["depart_date", "arrival_date"]})
    ]
    list_display = ["user_id", "depart_city", "arrival_city", "depart_date", "arrival_date"]
    list_filter = ["user_id"]
    search_fields = ["user_id"]
    save_on_top = True
