from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, SearchHistory
from .serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer, FlightSearchSerializer
from ticket_locator.services.singaporeair_service import SingaporairService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishairlineslService


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


class FlightSearchView(APIView):
	serializer_class = FlightSearchSerializer

	def post(self, request):
		result = []
		departure = request.data['departure_airport']
		destination = request.data['destination_airport']
		depart_date = request.data['departure_date']

		if departure and destination and depart_date:
			for company in [SingaporairService, TransaviaService, TurkishairlineslService]:
				info_fly = company().get_flight_info_by_date(departure, destination, depart_date)
				result.append(info_fly)

			return Response(result)
		return Response({"Fill all fields"})