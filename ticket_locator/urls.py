from django.contrib import admin
from django.urls import path, include

from hello_world import urls
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
    path('openapi/', get_schema_view(
            title="Ticket locator",
            description="API for all things …",
            version="1.0.0"
        ), name='openapi-schema'),
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
