import time
import json
import traceback
from celery import shared_task

from app.service.gpt_chars import GPTProductCharacteristics, RequestData
from app.models import GPTRequest


def delay_get_product_characteristics(gpt_request, code, name, brand, model, article):
	rd = RequestData(
		code, name, brand, model, article
	)

	request_data = rd.get_data()
	if not request_data:
		gpt_request.status = GPTRequest.STATUSES[0][0]
		gpt_request.help_message = 'Переданы неверные данные или не удалось найти поставщика. \
									Попробуйте еще раз.'
		gpt_request.save()
		return

	gpt_c = GPTProductCharacteristics(
		request_data[0],
		request_data[1],
		request_data[2],
		request_data[3],
	)
	gpt_c.get_characteristics()
	if not gpt_c.result:
		gpt_request.status = GPTRequest.STATUSES[0][0]
		gpt_request.help_message = 'Переданы неверные данные или не удалось найти поставщика. \
									Попробуйте еще раз.'
		gpt_request.save()
		return
	
	if gpt_c.result:
		gpt_request.response = json.dumps(gpt_c.result)
		gpt_request.status = GPTRequest.STATUSES[2][0]
	else:
		gpt_request.status = GPTRequest.STATUSES[0][0]
	gpt_request.save()

@shared_task
def get_product_characteristics(gpt_request_id, code, name, brand, model, article):
	gpt_request = GPTRequest.objects.filter(id=gpt_request_id).first()
	if not gpt_request:
		return
	
	try:
		delay_get_product_characteristics(gpt_request, code, name, brand, model, article)
	except Exception:
		return