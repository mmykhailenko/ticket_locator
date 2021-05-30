import ast

from django.shortcuts import render
from django.views import View
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .forms import SearchAirRouteForm,SingUpForm
from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer

from celery import group
from hello_world.tasks import get_flight_info_turkishairlines_task,get_flight_info_transavia_task,get_flight_info_singapore_air_task

AIRLINES = (
    'TurkishAirlinesService',
    'TransaviaService',
    'SingaporeAirService'
)

class UserView(GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = UsersListSerializer

    def get(self, request, pk=None):
        users = self.get_queryset(pk)
        print(request.user)
        serializer = UsersListSerializer(users, many=True) if not pk else UserDetailSerializer(users)
        return Response(serializer.data)

    def get_queryset(self, pk=None):
        if not pk:
            return User.objects.all()
        return User.objects.get(id=pk)


class SearchHistoryView(GenericAPIView):
    serializer_class = SearchHistorySerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

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
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        result = []
        departure_airport = request.data['departure_airport']
        arrival_airport = request.data['arrival_airport']
        date = ''.join(request.data['departure_date'].split('-'))
        if departure_airport and arrival_airport and date:
            flight_info = self._do_tasks(departure_airport, arrival_airport, date)
            if ast.literal_eval(request.data['direct_flight']):
                for flight in flight_info:
                    if len(flight) < 2:
                        result += [flight]
            else:
                result += flight_info
            print(result,"++++++++++++++++++")
            return Response(result)
        return Response({'Error': 'Please fill all fields.'})

    def _do_tasks(self, departure_airport, arrival_airport, date):
        result_list = []
        tasks_group = []

        tasks_start_func = (get_flight_info_turkishairlines_task,
                            get_flight_info_transavia_task,
                            get_flight_info_singapore_air_task)

        for task_func in tasks_start_func:
            task = task_func.s(departure_airport, arrival_airport, date)
            tasks_group.append(task)
        tasks = group(tasks_group)
        tasks_result = tasks.apply_async()
        while True:
            if not tasks_result.ready():
                continue
            else:
                for index in range(len(tasks_result.get())):
                    if tasks_result.get()[index]:
                        result_list.append(tasks_result.get()[index][0])
                print(result_list)
                return result_list

class SearchAirRoute(View):  # view for which renders and processes the search form on the main page
    def get(self, request):
        form = SearchAirRouteForm()
        return render(request=request, template_name="hello_world/index.html", context={"form_search": form})

    def post(self, request):
        form = SearchAirRouteForm(request.POST)
        if form.is_valid():
            request.data = form.cleaned_data
            result = FlightSearchView().post(request)
            return render(request, "hello_world/search_results.html", {"result": result.data,
                                                                      "form_search": form})
        return Response({'Error': 'Please fill all fields.'})


class SingUp(View):
    def get(self, request):
        form = SingUpForm()
        return render(request=request, template_name="registration/singup.html", context={"form": form})

    def post(self,request):
        form = SingUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/singup_done.html', {'new_user': new_user})
        else:
            form = SingUpForm()
        return render(request, 'registration/singup.html', {'form': form})

class PersonalAria(View):
    def get(self, request):
        return render(request, "hello_world/personal_aria.html")