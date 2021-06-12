from django.urls import path

from . import views


urlpatterns = [
    path("users/", views.UserView.as_view(), name="api_users"),
    path("users/<int:pk>", views.UserView.as_view(), name="api_user"),
    path("history/", views.SearchHistoryView.as_view(), name="api_history"),
    path(
        "history/<int:user>",
        views.SearchHistoryView.as_view(),
        name="api_user_history"
    ),
    path("search", views.FlightSearchView.as_view(), name="api_search"),
]
