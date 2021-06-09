from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView

from .managers import CustomUserManager
from .models import User, SearchHistory
from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer, \
    RegisterUsersSerializer


class UserView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, pk=None):
        try:
            users = User.objects.all() if not pk else User.objects.get(id=pk)
            serializer = UsersListSerializer(users, many=True) if not pk else UserDetailSerializer(users)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404


class SearchHistoryView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, user=None):
        search_history = SearchHistory.objects.all() if not user else SearchHistory.objects.filter(user=user)
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data)


class FlightSearchView(GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = FlightSearchSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'hello_world/response.html'

    @staticmethod
    def _history_save(request):
        history = SearchHistory.objects.create(user=request.user,
                                               departure_city=request.data['departure_airport'],
                                               arrival_city=request.data['arrival_airport'],
                                               departure_date=request.data['departure_date'],
                                               arrival_date=request.data['departure_date']
                                               )
        history.save()

    def get(self, request):
        serializer = FlightSearchSerializer
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': serializer})
        else:
            return Response({})

    def post(self, request):
        serializer_class = FlightSearchSerializer(data=request.data)
        if serializer_class.is_valid():
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
            if not request.user.is_anonymous:
                self._history_save(request)
            if request.accepted_renderer.format == 'html':
                return Response({'result': result, 'serializer': serializer_class},
                                template_name='hello_world/response.html')
            else:
                return Response(result)
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': serializer_class}, template_name='hello_world/response.html')
        else:
            return Response({'Error': 'Not all fields are filled in'})


class Register(GenericAPIView):
    serializer_class = RegisterUsersSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'hello_world/singup.html'

    def get(self, request):
        serializer = RegisterUsersSerializer
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': serializer})
        else:
            return Response({})

    def post(self, request):
        if request.method == 'POST':
            serializer_class = RegisterUsersSerializer(data=request.data)
            result = {}
            if serializer_class.is_valid():
                user = serializer_class.save()
                result['response'] = 'successfully registered a new user.'
                result['email'] = user.email
            else:
                result = serializer_class.errors
            if request.accepted_renderer.format == 'html':
                return Response({'serializer': serializer_class, 'data': result})
            else:
                return Response(result)
