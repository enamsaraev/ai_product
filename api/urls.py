from django.urls import path, include

from api.views import GetCharacteristicsView
app_name = 'api'


urlpatterns = [
	path('get_characteristics/', GetCharacteristicsView.as_view(), name='api_get_characteristics'),
]