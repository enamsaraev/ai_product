from django.urls import path, include

from app.views import MainPage, GettingCharacteristicsView

app_name = 'app'


urlpatterns = [
    path('main/', MainPage.as_view(), name='main_page'),
	path('getting_characteristics/', GettingCharacteristicsView.as_view(), name='getting_characteristics'),
]