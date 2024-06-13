import time

from celery import shared_task

from app.models import UserProductData, GPTRequest


@shared_task
def get_product_characteristics(gpt_request):
	pass