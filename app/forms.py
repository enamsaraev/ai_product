from django.forms import Form, CharField, TextInput


class GettingCharacteristicsForm(Form):
	product_code = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_code'}), required=True)

	def __init__(self, *args, **kwargs):
		super(GettingCharacteristicsForm, self).__init__(*args, **kwargs)
