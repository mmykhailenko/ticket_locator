from django.contrib import admin
from django.urls import path, include

from hello_world import urls, views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Ticket Locator",
      default_version='v1',
   ),
)

urlpatterns = [
    path('', views.SearchFlight.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
    path('swagger/', schema_view.with_ui('swagger')),
]
