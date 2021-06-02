from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as swagger
from hello_world import urls, views

urlpatterns = [
    path("", views.SearchAirRoute.as_view(), name="index"),
    path("history/", views.UserSearchHistoryView.as_view(), name="history"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("api/", include(urls)),
]
urlpatterns += swagger
