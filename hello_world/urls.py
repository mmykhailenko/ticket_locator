from django.urls import path

from . import views


urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>", views.UserView.as_view()),
    path("history/", views.SearchHistoryView.as_view()),
    path("history/<int:user>", views.SearchHistoryView.as_view()),
    path("search/", views.SearchView.as_view()),
]
