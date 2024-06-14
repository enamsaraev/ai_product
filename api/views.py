from django.http import JsonResponse
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from api.serializers import UserCharacteristicsSerializer, ResponseSerializer
from app.models import UserProductData, GPTRequest
from app.tasks import delay_get_product_characteristics


class GetCharacteristicsView(APIView):
	@extend_schema(
		tags=['Получение характеристик'],
		summary='Получение характеристик',
		description='Получение характеристик',
		request=UserCharacteristicsSerializer,
		responses=ResponseSerializer
	)
	def post(self, request, *args, **kwargs):
		serializer = UserCharacteristicsSerializer(request.data)
		user_data = UserProductData.objects.create(**serializer.data)
		gpt_request = GPTRequest.objects.create(
			user_product_data=user_data,
			status=GPTRequest.STATUSES[1][1],
		)
		delay_get_product_characteristics(
			gpt_request, 
			serializer.data['product_code'], 
			serializer.data['product_name'], 
			serializer.data['product_brand'], 
			serializer.data['product_model'], 
			serializer.data['product_partnumber'],
		)

		if gpt_request.response:
			response_serializer = ResponseSerializer(gpt_request)
			return JsonResponse(response_serializer.data, status=200)
		
		return JsonResponse(
			{'message': 'Переданы неверные данные или не удалось найти поставщика. Попробуйте еще раз.'},
			status=400
		)