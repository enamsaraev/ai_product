from django.views import View
from django.shortcuts import render, HttpResponse

from app.forms import GettingCharacteristicsForm


class MainPage(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/main.html')
	

class GettingCharacteristicsView(View):
	def get(self, request, *args, **kwargs):
		context = dict()
		context['form'] = GettingCharacteristicsForm()

		return render(request, 'app/getting_characteristics.html', context=context)
	
	def post(self, request, *args, **kwargs):
		print(request.POST)
		return HttpResponse(status=200)
