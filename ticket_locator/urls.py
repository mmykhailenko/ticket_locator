from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path, include
from .yasg import urlpatterns as swagger
from hello_world import urls, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(urls)),
    path("", views.SearchAirRoute.as_view(), name="index"),
    path("personal_aria/", views.PersonalAria.as_view(), name="personal_aria"),
    path("accounts/login/", auth.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth.LogoutView.as_view(), name="logout"),
    path("accounts/singup/", views.SingUp.as_view(), name="singup"),
    path("accounts/password-change/",auth.PasswordChangeView.as_view(),name="password_change",),
    path("accounts/password-change/done/",auth.PasswordChangeDoneView.as_view(),name="password_change_done",),
]
urlpatterns += swagger

