from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from ticket_locator import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(email=settings.DJANGO_ADMIN_EMAIL).exists():
            User.objects.create_superuser(
                email=settings.DJANGO_ADMIN_EMAIL,
                password=settings.DJANGO_ADMIN_PASSWORD,
            )