from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from hello_world import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'search_history', views.SearchHistoryViewSet)

# The API URLs are now determined automatically by the router.
app_name = "hello_world"

urlpatterns = [
    path('', include(router.urls)),
]