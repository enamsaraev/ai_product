import json

from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from app.forms import GettingCharacteristicsForm
from app.tasks import get_product_characteristics
from app.models import UserProductData, GPTRequest


class LoginPage(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/login.html')
	
	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		if not username:
			return self.error_message('Введите имя пользователя', 400)
		
		user = authenticate(username=username)
		login(request, user)

		next_page = request.GET.get('next', '')
		return redirect(next_page) if next_page else redirect('app:getting_characteristics')
	

class LogoutView(View):
	def post(self, request, *args, **kwargs):
		logout(request)
		return redirect(reverse('app:login'))
	

@method_decorator(login_required, name='dispatch')
class GettingCharacteristicsView(View):
	def get(self, request, *args, **kwargs):
		context = dict()
		context['form'] = GettingCharacteristicsForm()
		context['gpt_requests'] = GPTRequest.objects.select_related('user_product_data')\
									.filter(user=request.user).order_by('-id')

		return render(request, 'app/getting_characteristics.html', context=context)
	
	def post(self, request, *args, **kwargs):
		form = GettingCharacteristicsForm(request.POST)
		if not form.is_valid():
			return self.form_error_message(form)

		user_data = UserProductData.objects.create(**form.cleaned_data)
		gpt_request = GPTRequest.objects.create(
			user_product_data=user_data,
			user=request.user,
			status=GPTRequest.STATUSES[1][1],
		)
		get_product_characteristics.apply_async(args=(
				gpt_request.id, 
				form.cleaned_data.get('product_code'),
				form.cleaned_data.get('product_name'),
				form.cleaned_data.get('product_brand'),
				form.cleaned_data.get('product_model'),
				form.cleaned_data.get('product_partnumber'),
			)
		)
		
		return JsonResponse({}, status=200)
	
	def form_error_message(self, form):
		error_list = [errors[0] for _, errors in form.errors.items()]
		msg = '\n'.join(error_list)
		return self.error_message(msg, 400)
	
	def error_message(self, msg, status):
		data = {'msg': msg}
		return JsonResponse(data, status=status)


@method_decorator(login_required, name='dispatch')
class CheckGPTRequestStatus(View):
	def post(self, request, *args, **kwargs):
		gr_id = request.POST.get('gr_id')
		gpt_request = GPTRequest.objects.filter(id=gr_id).first()
		if not gpt_request:
			return self.error_message('Во время проверки статуса произошла ошибка, попробуйте позднее', 500)
		
		return JsonResponse({'status': gpt_request.status}, status=200)
	
	def error_message(self, msg, status):
		data = {'msg': msg}
		return JsonResponse(data, status=status)
	

@method_decorator(login_required, name='dispatch')
class DetailCharacteristics(View):
	def get(self, request, *args, **kwargs):
		context = dict()

		chars = GPTRequest.objects.filter(id=kwargs.get('id')).first()
		if chars and chars.response:
			data = json.loads(chars.response)
			context['chars'] = data.items()
			context['obj'] = chars

		return render(request, 'app/characteristics_detail.html', context=context)