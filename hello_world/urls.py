from django.urls import path

from . import views


urlpatterns = [
    path("users/", views.UserView.as_view(),name = "users"),
    path("users/<int:pk>", views.UserView.as_view(),name = "user_detail"),
    path("history/", views.SearchHistoryView.as_view(), name = "history_search"),
    path("history/<int:user>", views.SearchHistoryView.as_view(), name = "history_detail"),
    path("search", views.FlightSearchView.as_view(), name = "search"),
]
