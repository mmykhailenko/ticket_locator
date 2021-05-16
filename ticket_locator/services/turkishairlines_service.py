import datetime
import json

import requests
from ticket_locator.settings import API_KEY_TURKISHAIRLINES, API_SECRET_KEY_TURKISHAIRLINES
from ticket_locator.services.base_service import AirCompanyService


class TurkishairlineslService(AirCompanyService):
	_BASE_URL = 'https://api.turkishairlines.com/test/getAvailability'
	_API_KEY = API_KEY_TURKISHAIRLINES
	_API_SECRET_KEY = API_SECRET_KEY_TURKISHAIRLINES

	_HTTP_HEADERS = {
		'Content-Type': 'application/json',
		'clientTransactionId': 'CLIENT_TEST_1',
		'apikey': _API_KEY,
		'apisecret': _API_SECRET_KEY
	}

	_REQUEST_BODY = {
		"requestHeader":
			{
				"clientUsername": "OPENAPI",
				"clientTransactionId": "CLIENT_TEST_1",
				"channel": "WEB"
			},
		"ReducedDataIndicator": True,
		"RoutingType": "M",
		"PassengerTypeQuantity": [{
			"Code": "adult",
			"Quantity": 1
		}],
		"OriginDestinationInformation": [{
			"DepartureDateTime": {
				"WindowAfter": "P0D",
				"WindowBefore": "P0D",
				"Date": "14JAN"
			},
			"OriginLocation": {
				"LocationCode": "",
				"MultiAirportCityInd": False
			},
			"DestinationLocation": {
				"LocationCode": "",
				"MultiAirportCityInd": False
			},
			"CabinPreferences": [{
				"Cabin": "ECONOMY"
			},
			{
				"Cabin": "BUSINESS"
			}]
		}]
	}

	def _fill_fly_details(self, origin_airport_code, destination_airport_code, departure_date):
		part_of_body = self._REQUEST_BODY['OriginDestinationInformation'][0]
		part_of_body['OriginLocation']['LocationCode'] = origin_airport_code
		part_of_body['DestinationLocation']['LocationCode'] = destination_airport_code
		part_of_body['DepartureDateTime']['Date'] = departure_date

	def get_flight_info_by_date(self, origin_airport_code: str, destination_airport_code: str, departure_date: str):
		result_response = []
		departure_date = datetime.datetime.strptime(departure_date, '%Y-%m-%d').__format__('%d%b').upper()
		self._fill_fly_details(origin_airport_code, destination_airport_code, departure_date)
		response = requests.post(url=self._BASE_URL, data=json.dumps(self._REQUEST_BODY), headers=self._HTTP_HEADERS)
		if response.status_code == 200:
			response_json = response.json()
			flight_offer = (response_json['data']
			['availabilityOTAResponse']
			['createOTAAirRoute']
			['OTA_AirAvailRS']
			['OriginDestinationInformation']
			['OriginDestinationOptions']
			['OriginDestinationOption']['FlightSegment'])
			for offer in flight_offer:
				outer_response = {
					'Aircompany': offer["OperatingAirline"]['CompanyShortName'],
					'Departure date': offer["DepartureDateTime"],
					'Departure airport': offer["DepartureAirport"]['LocationCode'],
					'Arrival date': offer["ArrivalDateTime"],
					'Arrival airport': offer["ArrivalAirport"]['LocationCode'],
					'Flight number': offer["FlightNumber"]
				}
				result_response.append(outer_response)
			return result_response
		else:
			return result_response

	def get_flight_info_by_period(self, *args, **kwargs):
		pass
