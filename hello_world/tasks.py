from celery import shared_task

from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService

@shared_task(time_limit = 100)
def get_flight_info_singapore_air_task(departure_airport, arrival_airport, date):
    return SingaporeAirService().get_flight_info_by_date(departure_airport, arrival_airport, date)

@shared_task(time_limit = 100)
def get_flight_info_transavia_task(departure_airport, arrival_airport, date):
    return TransaviaService().get_flight_info_by_date(departure_airport, arrival_airport, date)

@shared_task(time_limit = 100)
def get_flight_info_turkishairlines_task(departure_airport, arrival_airport, date):
    return TurkishAirlinesService().get_flight_info_by_date(departure_airport, arrival_airport, date)
