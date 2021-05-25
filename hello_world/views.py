from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .models import User, SearchHistory
from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer
from django.shortcuts import render
from django.views import View
from .forms import SearchForm



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
            for air_company in [TransaviaService, TurkishAirlinesService]:
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
            return Response(result)
        return Response({'Error': 'Please fill all fields.'})


class SearchView(View):
    def post(self, request):
        form = SearchForm(request.POST or None)
        if form.is_valid():
            request.data['departure_airport'] = form.cleaned_data.get('departure_airport')
            request.data['arrival_airport'] = form.cleaned_data.get('arrival_airport')
            request.data['departure_date'] = form.cleaned_data.get('departure_date')
            request.data['direct_flight'] = form.cleaned_data.get('direct_flight')
            result = FlightSearchView().post(request)
            return render(request, 'hello_world/search_block.html', {'result': result.data})
        return render(request, 'hello_world/search_block.html', {'form': form})
