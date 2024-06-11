from django.views import View
from django.shortcuts import render, HttpResponse

from app.forms import GettingCharacteristicsForm
from app.tasks import test


class MainPage(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/main.html')
	

class GettingCharacteristicsView(View):
	def get(self, request, *args, **kwargs):
		context = dict()
		context['form'] = GettingCharacteristicsForm()

		return render(request, 'app/getting_characteristics.html', context=context)
	
	def post(self, request, *args, **kwargs):
		x = int(request.POST.get('x'))
		y = int(request.POST.get('y'))
		test.apply_async(args=(x, y), countdown=15)
		return HttpResponse(status=200)
