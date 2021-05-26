from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, SearchHistory
from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer


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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'hello_world/response.html'

    def get(self, request):
        serializer = FlightSearchSerializer
        return Response({'serializer': serializer})

    def post(self, request):
        serializer_class = FlightSearchSerializer(data=request.data)
        if not serializer_class.is_valid():
            pass
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
                            result += flight
                else:
                    result += flight_info
            print(result)
            return Response({'result': result, 'serializer': serializer_class}, template_name='hello_world/response.html')
        return Response({'serializer': serializer_class}, template_name='hello_world/response.html')