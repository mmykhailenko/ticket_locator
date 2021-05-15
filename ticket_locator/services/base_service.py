class AirCompanyService:
	_BASE_URL = 'API_URL'
	_API_KEY = 'API_KEY'

	def get_flight_info_by_date(self, *args, **kwargs):
		raise NotImplementedError

	def get_flight_info_by_period(self, *args, **kwargs):
		raise NotImplementedError