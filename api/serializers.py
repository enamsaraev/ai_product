import json

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class UserCharacteristicsSerializer(serializers.Serializer):
	product_code = serializers.CharField(label='Код товара')
	product_name = serializers.CharField(label='Полное наименование')
	# product_type = serializers.CharField(label='Тип')
	product_brand = serializers.CharField(label='Бренд')
	# product_series = serializers.CharField(label='Серия')
	product_model = serializers.CharField(label='Модель')
	product_partnumber = serializers.CharField(label='Partnumber')


class ResponseSerializer(serializers.Serializer):
	product_code = serializers.SerializerMethodField('get_product_code', label='Код товара')
	product_name = serializers.SerializerMethodField('get_product_name', label='Код товара')
	product_brand = serializers.SerializerMethodField('get_product_brand', label='Код товара')
	product_model = serializers.SerializerMethodField('get_product_model', label='Код товара')
	product_partnumber = serializers.SerializerMethodField('get_product_partnumber', label='Код товара')
	characteristcs = serializers.SerializerMethodField('get_characteristcs', label='Характеристики товара')

	@extend_schema_field(serializers.CharField)
	def get_product_code(self, obj):
		return obj.user_product_data.product_code
	
	@extend_schema_field(serializers.CharField)
	def get_product_name(self, obj):
		return obj.user_product_data.product_name
	
	@extend_schema_field(serializers.CharField)
	def get_product_brand(self, obj):
		return obj.user_product_data.product_brand
	
	@extend_schema_field(serializers.CharField)
	def get_product_model(self, obj):
		return obj.user_product_data.product_model
	
	@extend_schema_field(serializers.CharField)
	def get_product_partnumber(self, obj):
		return obj.user_product_data.product_partnumber
	
	@extend_schema_field(serializers.DictField)
	def get_characteristcs(self, obj):
		characteristcs = json.loads(obj.response)
		return characteristcs
