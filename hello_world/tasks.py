from celery import shared_task


@shared_task(time_limit=300)
def test_task():
	print("okkkkkkkk")