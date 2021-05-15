import json
import pprint

import requests
from env_vars import env
from ticket_locator.services.base_service import AirCompanyService


class TransaviaService(AirCompanyService):
	_BASE_URL = 'https://api.transavia.com/v1/flightoffers/'
	_API_KEY = env('API_KEY_TRANSAVIA')

	_HTTP_HEADERS = {
		'Host': 'api.transavia.com',
		'apikey': _API_KEY
	}

	_REQUEST_BODY = {
		'origin': '',
		'destination': '',
		'destinationArrivalDate': ''
	}

	def _fill_fly_details(self, origin_airport_code, destination_airport_code, departure_date):
		self._REQUEST_BODY['origin'] = origin_airport_code
		self._REQUEST_BODY['destination'] = destination_airport_code
		self._REQUEST_BODY['destinationArrivalDate'] = departure_date

	def get_flight_info_by_date(self, origin_airport_code: str, destination_airport_code: str, departure_date: str):
		self._fill_fly_details(origin_airport_code, destination_airport_code, departure_date)
		pprint.pprint(self._REQUEST_BODY)
		response = requests.get(url=self._BASE_URL, params=self._REQUEST_BODY, headers=self._HTTP_HEADERS)

		if response.status_code == 200:
			return response.json()
		else:
			raise requests.exceptions.RequestException

	def get_flight_info_by_period(self, *args, **kwargs):
		pass
