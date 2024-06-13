from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class UserProductData(models.Model):
	product_code = models.CharField(
		max_length=255,
		blank=True,
		verbose_name='Код товара'
	)
	product_name = models.CharField(
		max_length=255,
		blank=True,
		verbose_name='Полное наименование'
	)
	product_type = models.CharField(
		max_length=255,
		blank=True,
		verbose_name='Тип'
	)
	product_brand = models.CharField(
		max_length=255,
		blank=True,
		verbose_name='Тип'
	)
	product_series = models.CharField(
		max_length=255,
		blank=True,
		verbose_name='Серия'
	)
	product_model = models.CharField(
		max_length=255,
		blank=True,
		verbose_name='Модель'
	)
	product_partnumber = models.CharField(
		max_length=255,
		blank=True,
		verbose_name='Partnumber'
	)


class GPTRequest(models.Model):
	STATUSES = (
		('Ошибка', 'Ошибка'),
		('Обрабатывается', 'Обрабатывается'),
		('Успешно', 'Успешно'),
	)
	user_product_data = models.ForeignKey(
		UserProductData,
		related_name='gpt_requests',
		on_delete=models.SET_NULL,
		null=True
	)
	user = models.ForeignKey(
		User,
		related_name='gpt_requests',
		on_delete=models.SET_NULL,
		null=True
	)
	status = models.CharField(
		choices=STATUSES,
		verbose_name='Статус',
	)
	response = models.JSONField(
		verbose_name='Ответ GPT',
		null=True,
		blank=True
	)