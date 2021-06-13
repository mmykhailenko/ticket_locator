from celery import shared_task

from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService
from hello_world import views


@shared_task(time_limit=300)
def get_air_data(air_company, request_data):
    obj = views.FlightSearchView()
    return obj.start_get_air_info(air_company, request_data)
