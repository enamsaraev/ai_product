from django.urls import path, include

from app.views import LoginPage, LogoutView, GettingCharacteristicsView, CheckGPTRequestStatus, DetailCharacteristics

app_name = 'app'


urlpatterns = [
	path('login/', LoginPage.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('', GettingCharacteristicsView.as_view(), name='getting_characteristics'),
	path('getting_characteristics/gr/status', CheckGPTRequestStatus.as_view(), name='gr_status'),
	path('detail_characteristics/<str:id>/', DetailCharacteristics.as_view(), name='detail_characteristics'),
]