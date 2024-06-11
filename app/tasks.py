import time

from celery import shared_task

from app.models import TestModel


@shared_task
def test(x, y):
	result = x + y
	TestModel.objects.create(result=result)