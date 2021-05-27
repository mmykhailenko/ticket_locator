from celery import group
from django.shortcuts import render
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .tasks import get_flight_info_singapore_air_task, get_flight_info_transavia_task, \
    get_flight_info_turkishairlines_task
from .forms import SearchAirRouteForm
from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer


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

    def post(self, request):
        result = []
        departure_airport = request.data['departure_airport']
        arrival_airport = request.data['arrival_airport']
        date = ''.join(request.data['departure_date'].split('-'))
        if departure_airport and arrival_airport and date:
            flight_info = self._do_tasks(departure_airport, arrival_airport, date)
            if request.data.get('direct_flight', None):
                for flight in flight_info:
                    if len(flight) < 2:
                        result += [flight]
            else:
                result += flight_info
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
                return result_list


class SearchAirRoute(View):  # view for which renders and processes the search form on the main page
    def get(self, request):
        form = SearchAirRouteForm()
        return render(request=request, template_name="hello_world/index.html", context={"form": form})

    def post(self, request):
        form = SearchAirRouteForm(request.POST)
        if form.is_valid():
            request.data = form.cleaned_data
            result = FlightSearchView().post(request)
            return render(request, "hello_world/search_results.html", {"result": result.data,
                                                                       "form": form})
