import datetime
import json

import requests
from ticket_locator.settings import API_KEY_TRANSAVIA
from ticket_locator.services.base_service import AirCompanyService


class TransaviaService(AirCompanyService):
	_BASE_URL = 'https://api.transavia.com/v1/flightoffers/'
	_API_KEY = API_KEY_TRANSAVIA

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
		result_response = []
		departure_date = datetime.datetime.strptime(departure_date, '%Y-%m-%d').__format__('%Y%m%d')
		self._fill_fly_details(origin_airport_code, destination_airport_code, departure_date)
		response = requests.get(url=self._BASE_URL, params=self._REQUEST_BODY, headers=self._HTTP_HEADERS)
		if response.status_code == 200:
			response_json = response.json()
			flight_offer = response_json['flightOffer']
			for offer in flight_offer:
				fly = offer['outboundFlight']
				outer_response = {
					'Aircompany': fly["marketingAirline"]['companyShortName'],
					'Departure date': fly["departureDateTime"],
					'Departure airport': fly["departureAirport"]['locationCode'],
					'Arrival date': fly["arrivalDateTime"],
					'Arrival airport': fly["arrivalAirport"]['locationCode'],
					'Flight number': fly["flightNumber"]
				}
				result_response.append(outer_response)
			return result_response
		else:
			return result_response

	def get_flight_info_by_period(self, *args, **kwargs):
		pass
