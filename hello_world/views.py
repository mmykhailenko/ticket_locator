from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ticket_locator.services.constants import logos
from .forms import SearchAirRouteForm, RegistrationForm, LoginForm
from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer

from celery import group
from hello_world.tasks import get_air_data

AIRLINES = ("TurkishAirlinesService", "TransaviaService", "SingaporeAirService")


class UserView(GenericAPIView):
    serializer_class = UsersListSerializer

    def get(self, request, pk=None):
        users = self.get_queryset(pk)
        serializer = UsersListSerializer(users, many=True) if not pk else UserDetailSerializer(users)
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

    @staticmethod
    def get_air_info(request_data):
        result = []
        air_tasks = group([get_air_data.s(airline, request_data) for airline in AIRLINES])
        flights = air_tasks.apply_async()
        while not flights.ready():
            pass
        for flight in flights.get():
            result += flight
        return result

    def post(self, request):
        if request.data["departure_airport"] and request.data["arrival_airport"] and request.data["departure_date"]:
            result = self.get_air_info(request.data)
            return Response(result)
        return Response({"Error": "Please fill all fields."})


class SearchAirRoute(View):  # view for which renders and processes the search form on the main page
    def get(self, request):
        form = SearchAirRouteForm()
        return render(
            request=request,
            template_name="hello_world/index.html",
            context={"result": "init", "form": form},
        )

    def post(self, request):
        form = SearchAirRouteForm(request.POST)
        if form.is_valid():
            form.cleaned_data["departure_date"] = form.cleaned_data["departure_date"].strftime("%Y-%m-%d")
            if request.user.is_authenticated:
                user = User.objects.filter(email=request.user)[0]
                data = form.cleaned_data
                SearchHistory.objects.get_or_create(user=user,
                                                    departure_city=data["departure_airport"],
                                                    arrival_city=data["arrival_airport"],
                                                    departure_date=data["departure_date"],
                                                    arrival_date=f'2022-12-12 00:00')
            request.data = form.cleaned_data
            result = FlightSearchView().post(request).data
            for flight in result:
                for flight_item in flight:
                    flight_item['AirlineLogo'] = logos.get(flight_item.get('Airline'))
            return render(request, "hello_world/index.html", {"result": result, "form": form})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {"result": "init", 'form': form}
        return render(request=request, template_name="hello_world/registration.html", context=context)

    @csrf_exempt
    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            context = {"result": "Wrong", 'form': form}
            return render(request=request, template_name="hello_world/registration.html", context=context)
        form.save()
        return redirect('/login')


class Login(View):
    def get(self, request):
        form = LoginForm()
        context = {"result": "init", 'form': form}
        return render(request=request, template_name="hello_world/login.html", context=context)

    @csrf_exempt
    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            form = LoginForm()
            context = {"result": "Wrong", 'form': form}
            return render(request=request, template_name="hello_world/login.html", context=context)
        return redirect('/')


class UserSearchHistoryView(View):

    def get(self, request):
        search_form = SearchAirRouteForm()
        context = []
        if request.user.is_authenticated:
            context = SearchHistory.objects.filter(user=request.user).values()
        return render(request=request, template_name="hello_world/history.html", context={"history": context,
                                                                                          "form": search_form})
