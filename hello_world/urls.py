from django.urls import path
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path("", TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>", views.UserView.as_view()),
    path("history/", views.SearchHistoryView.as_view()),
    path("history/<int:user>", views.SearchHistoryView.as_view()),
    path('search/', views.FlightSearchView.as_view()),
    path('openapi/', get_schema_view(
        title="TicketLocator",
        description="API for searching the flights.",
        version="1.0.0"
    ), name='openapi-schema'),
    path('index/', views.SearchView.as_view(), name='index')
]
