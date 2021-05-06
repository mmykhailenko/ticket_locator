from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from hello_world import views

urlpatterns = [
    path('history/', views.SearchHistoryList.as_view()),
    path('history/<int:pk>/', views.SearchHistoryDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
