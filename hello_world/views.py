from .models import User, SearchHistory
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, UserDetailSerializer, SearchHistorySerializer


class UserView(viewsets.ModelViewSet):
	queryset = User.object.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]


class UserDetailView(viewsets.ModelViewSet):
	queryset = User.object.all()
	serializer_class = UserDetailSerializer
	permission_classes = [permissions.IsAuthenticated]


class SearchHistoryView(viewsets.ModelViewSet):
	queryset = SearchHistory.objects.all()
	serializer_class = SearchHistorySerializer
	permission_classes = [permissions.IsAuthenticated]