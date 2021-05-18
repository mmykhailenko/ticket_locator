from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, SearchSerializer
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
    serializer_class = SearchSerializer

    def post(self, request):
        departure_city = request.data['departure_airport']
        arrival_city = request.data['arrival_airport']
        date = request.data['departure_date']
        result = service_request.get_request(departure_city, arrival_city, date)
        return Response(result)

