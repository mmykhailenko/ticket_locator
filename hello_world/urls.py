from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path("users/", views.UserView.as_view(), name='users'),
    path("users/<int:pk>", views.UserView.as_view(), name='users_id'),
    path("history/", views.SearchHistoryView.as_view()),
    path("history/<int:user>", views.SearchHistoryView.as_view()),
    path("register/", views.Register.as_view(), name='new_user'),
    path('search/', views.FlightSearchView.as_view(), name='new_search')
]
