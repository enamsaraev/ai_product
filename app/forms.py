from django.forms import Form, CharField, TextInput


class GettingCharacteristicsForm(Form):
	x = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_code'}), required=True)
	y = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_product_code'}), required=True)

	def __init__(self, *args, **kwargs):
		super(GettingCharacteristicsForm, self).__init__(*args, **kwargs)
