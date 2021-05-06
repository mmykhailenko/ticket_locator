from typing import Any
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from hello_world import views
from hello_world.views import SearchHistoryViewSet, UserViewSet, api_root
from rest_framework import renderers


user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
search_history_list = SearchHistoryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
search_history_detail = SearchHistoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', views.api_root),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('search_histories/', search_history_list, name='search_history-list'),
    path('search_histories/<int:pk>/', search_history_detail, name='search_history-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
