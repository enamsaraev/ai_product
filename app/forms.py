from django.forms import Form, CharField, TextInput


class GettingCharacteristicsForm(Form):
	product_code = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_code'}), required=False)
	product_name = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_name'}), required=False)
	product_type = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_type'}), required=False)
	product_brand = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_brand'}), required=False)
	product_series = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_series'}), required=False)
	product_model = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_model'}), required=False)
	product_partnumber = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_partnumber'}), required=False)

	def __init__(self, *args, **kwargs):
		super(GettingCharacteristicsForm, self).__init__(*args, **kwargs)

	def clean(self):
		if not self.cleaned_data.get('product_code'):
			self.add_error('product_code', 'Поле "Код товара" обязательно для заполнения')
		if not self.cleaned_data.get('product_name'):
			self.add_error('product_name', 'Поле "Полное наименование" обязательно для заполнения')
		if not self.cleaned_data.get('product_type'):
			self.add_error('product_type', 'Поле "Тип" обязательно для заполнения')
		if not self.cleaned_data.get('product_brand'):
			self.add_error('product_brand', 'Поле "Бренд" обязательно для заполнения')
		if not self.cleaned_data.get('product_series'):
			self.add_error('product_series', 'Поле "Серия" обязательно для заполнения')
		if not self.cleaned_data.get('product_model'):
			self.add_error('product_model', 'Поле "Модель" обязательно для заполнения')
		if not self.cleaned_data.get('product_partnumber'):
			self.add_error('product_partnumber', 'Поле "Partnumber" обязательно для заполнения')

		return self.cleaned_data
