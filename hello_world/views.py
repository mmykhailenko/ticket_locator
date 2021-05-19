from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, SearchSerializer
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.singapore_air_service import SingaporeAirService


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


class SearchView(GenericAPIView):
    serializer_class = SearchSerializer
    queryset = SearchHistory.objects.all()

    def post(self, request: object):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            result = []
            flight_info_SingaporeAir = SingaporeAirService().get_flight_info_by_date(
                request.data['departure_city'],
                request.data['arrival_city'],
                request.data['departure_date'])
            result.append(flight_info_SingaporeAir)
            flight_info_Transavia = TransaviaService().get_flight_info_by_date(
                request.data['departure_city'],
                request.data['arrival_city'],
                ''.join(request.data['departure_date'].split('-')))
            result.append(flight_info_Transavia)
            return Response(result)
        return Response({'Error': 'Please fill all the fields in the form.'})
