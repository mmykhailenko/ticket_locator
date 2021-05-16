from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from ticket_locator.services import service_request


class UserView(APIView):

    def get(self, request, pk=None):
        users = User.objects.all() if not pk else User.objects.get(id=pk)
        serializer = UsersListSerializer(users, many=True) if not pk else UserDetailSerializer(users)
        return Response(serializer.data)


class SearchHistoryView(APIView):

    def get(self, request, user=None):
        search_history = SearchHistory.objects.all() if not user else SearchHistory.objects.filter(user=user)
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data)


class SearchView(APIView):

    def get(self, request, format=None):
        departure_city = input('departure_city: ')
        arrival_city = input('arrival_city: ')
        date = input('date(YYYY-MM-DD): ')
        return Response(service_request.get_request(departure_city, arrival_city, date))
