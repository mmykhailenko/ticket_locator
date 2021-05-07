from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hello_world import views


router = DefaultRouter()
router.register(r'search_histories', views.SearchHistoryViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
