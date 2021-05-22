from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, SearchHistory
from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer

from django.views import View
from django.shortcuts import render

from ticket_locator.services.constants import logos


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


class FlightSearchView(GenericAPIView):
    serializer_class = FlightSearchSerializer

    def post(self, request):
        result = []
        if request.data['departure_airport'] and request.data['arrival_airport'] and request.data['departure_date']:
            for air_company in [SingaporeAirService, TransaviaService, TurkishAirlinesService]:
                flight_info = air_company().get_flight_info_by_date(
                    request.data['departure_airport'],
                    request.data['arrival_airport'],
                    ''.join(request.data['departure_date'].split('-')))
                if request.data.get('direct_flight', None):
                    for flight in flight_info:
                        if len(flight) < 2:
                            result += [flight]
                else:
                    result += flight_info
            return Response(result)
        return Response({'Error': 'Please fill all fields.'})


class SearchFlight(View):

    def get(self, request):
        return render(request, template_name='hello_world/index.html')

    def post(self, request):
        request.data = {
            'departure_airport': request._post.get('departure_airport'),
            'arrival_airport': request._post.get('arrival_airport'),
            'departure_date': request._post.get('departure_date'),
            'direct_flight': request._post.get('direct_flight')
        }
        flights = FlightSearchView().post(request).data
        if not isinstance(flights, dict):
            for flight in flights:
                for flight_item in flight:
                    flight_item['AirlineLogo'] = logos.get(flight_item.get('Airline'))
            return render(request,
                          template_name='hello_world/index.html',
                          context={'flights': flights})
        else:
            return render(request, template_name='hello_world/index.html')
