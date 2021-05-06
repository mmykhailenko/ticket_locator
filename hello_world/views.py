from hello_world.models import User, SearchHistory
from hello_world.serializers import UserSerializer, SearchHistorySerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'search_histories': reverse('search_history-list', request=request, format=format)
    })
