from celery import shared_task
from hello_world import views


@shared_task(time_limit=300)
def get_air_data(air_company, request_data):
    obj = views.FlightSearchView()
    return obj.start_get_air_info(air_company, request_data)
