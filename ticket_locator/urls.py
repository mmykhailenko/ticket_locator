from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as swagger
from hello_world import urls, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(urls)),
    path("", views.SearchAirRoute.as_view(), name="index"),
]
urlpatterns += swagger
