from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>", views.UserView.as_view()),
    path("history/", views.SearchHistoryView.as_view()),
    path("history/<int:user>", views.SearchHistoryView.as_view()),
    path("search_day/",views.CreatePostForMakingSearchDay.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)