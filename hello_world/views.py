from django.shortcuts import render
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .forms import SearchAirRouteForm
from .models import User, SearchHistory
from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService
from .serializers import (
    UsersListSerializer,
    UserDetailSerializer,
    SearchHistorySerializer,
    FlightSearchSerializer,
)

from celery import group
from hello_world.tasks import get_air_data

AIRLINES = ("TurkishAirlinesService", "TransaviaService", "SingaporeAirService")


class UserView(GenericAPIView):
    serializer_class = UsersListSerializer

    def get(self, request, pk=None):
        users = self.get_queryset(pk)
        serializer = (
            UsersListSerializer(users, many=True)
            if not pk
            else UserDetailSerializer(users)
        )
        return Response(serializer.data)

    def get_queryset(self, pk=None):
        if not pk:
            return User.objects.all()
        return User.objects.get(id=pk)


class SearchHistoryView(GenericAPIView):
    serializer_class = SearchHistorySerializer

    def get(self, request, user=None):
        search_history = self.get_queryset(user)
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data)

    def get_queryset(self, user=None):
        if not user:
            return SearchHistory.objects.all()
        return SearchHistory.objects.filter(user=user)


class FlightSearchView(GenericAPIView):
    serializer_class = FlightSearchSerializer

    def post(self, request):
        result = []
        if (
            request.data["departure_airport"]
            and request.data["arrival_airport"]
            and request.data["departure_date"]
        ):
            request_data = request.data
            air_tasks = group(
                [get_air_data.s(airline, request_data) for airline in AIRLINES]
            )
            flights = air_tasks.apply_async()
            while not flights.ready():
                pass
            for flight in flights.get():
                result += flight
            return Response(result)
        return Response({"Error": "Please fill all fields."})


class SearchAirRoute(
    View
):  # view for which renders and processes the search form on the main page
    def get(self, request):
        form = SearchAirRouteForm()
        return render(
            request=request,
            template_name="hello_world/index.html",
            context={"form": form},
        )

    def post(self, request):
        form = SearchAirRouteForm(request.POST)
        if form.is_valid():
            form.cleaned_data["departure_date"] = (
                form.cleaned_data["departure_date"]
            ).strftime("%Y-%m-%d")
            request.data = form.cleaned_data
            result = FlightSearchView().post(request)
            return render(
                request,
                "hello_world/search_results.html",
                {"result": result.data, "form": form},
            )
