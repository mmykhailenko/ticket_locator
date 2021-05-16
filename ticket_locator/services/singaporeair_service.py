import json

import requests
from ticket_locator.settings import API_KEY_SINGAPOREAIR
from ticket_locator.services.base_service import AirCompanyService


class SingaporairService(AirCompanyService):
	_BASE_URL = 'https://apigw.singaporeair.com/api/v1/commercial/flightavailability/get'
	_API_KEY = API_KEY_SINGAPOREAIR

	_HTTP_HEADERS = {
		'Content-Type': "application/json",
		'apikey': _API_KEY
	}

	_REQUEST_BODY = {
		'clientUUID': "01",
		'request': {
			'itineraryDetails': [
				{
					'originAirportCode': "",
					'destinationAirportCode': "",
					'departureDate': ""
				}
			],
			'cabinClass': "Y",
			'adultCount': 1
		}
	}

	def _fill_fly_details(self, origin_airport_code, destination_airport_code, departure_date):
		part_of_body = self._REQUEST_BODY['request']['itineraryDetails'][0]
		part_of_body['originAirportCode'] = origin_airport_code
		part_of_body['destinationAirportCode'] = destination_airport_code
		part_of_body['departureDate'] = departure_date

	def get_flight_info_by_date(self, origin_airport_code: str, destination_airport_code: str, departure_date: str):
		result_response = []
		self._fill_fly_details(origin_airport_code, destination_airport_code, departure_date)
		response = requests.post(url=self._BASE_URL, data=json.dumps(self._REQUEST_BODY), headers=self._HTTP_HEADERS)
		if response.status_code == 200 and response.json()['status'] == 'SUCCESS':
			response_json = response.json()
			flight_offer = response_json['response']['flights'][0]['segments']
			for offer in flight_offer:
				offer = offer['legs']
				for offer_leg in offer:
					outer_response = {
						'Aircompany': offer_leg["marketingAirline"]['name'],
						'Departure date': offer_leg["departureDateTime"],
						'Departure airport': offer_leg["originAirportCode"],
						'Arrival date': offer_leg["arrivalDateTime"],
						'Arrival airport': offer_leg["destinationAirportCode"],
						'Flight number': offer_leg["flightNumber"]
					}
					result_response.append(outer_response)
			return result_response
		else:
			return result_response

	def get_flight_info_by_period(self, *args, **kwargs):
		pass