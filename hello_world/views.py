from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ticket_locator.services.singapor_air_service import SingaporeService
from ticket_locator.services.transavia_service import TransaviaService
from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, \
    CreatePostForMakingSearchDaySerializer


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


class CreatePostForMakingSearchDay(GenericAPIView):
    serializer_class = CreatePostForMakingSearchDaySerializer

    def post(self,request):
        serializer = CreatePostForMakingSearchDaySerializer(data = request.data)
        if serializer.is_valid():
            result_data = {}
            departure_date_format = {"singapor_air": serializer.data["departure_date"],
                                     "transavia": "".join((serializer.data["departure_date"]).split("-"))}
            if serializer.data["cabin_class"] == "Economy":
                cabin_class_format = {"singapor_air": "Y",
                                      "transavia": "Basic"}
            else:
                cabin_class_format = {"singapor_air": "J",
                                      "transavia": "Max"}
            result_transavia = TransaviaService().get_flight_info_by_date(serializer.data["departure_airport"],
                                                                          serializer.data["arrival_airport"],
                                                                          departure_date_format["transavia"],
                                                                          cabin_class_format["transavia"],
                                                                          serializer.data["adult_count"],
                                                                          serializer.data["child_count"])
            result_singapor_air = SingaporeService().get_flight_info_by_date(serializer.data["departure_airport"],
                                                                             serializer.data["arrival_airport"],
                                                                             departure_date_format["singapor_air"],
                                                                             cabin_class_format["singapor_air"],
                                                                             serializer.data["adult_count"],
                                                                             serializer.data["child_count"],
                                                                             serializer.data["infant_count"])

            if not result_transavia:
                result_data["transavia"] = {}
            else:
                result_data["transavia"] = result_transavia
            if not result_singapor_air:
                result_data["singapor_air"] = {}
            else:
                result_data["singapor_air"] = result_singapor_air
            return Response(result_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

