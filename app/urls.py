from django.urls import path, include

from app.views import MainPage, GettingCharacteristicsView, LoginPage, LogoutView, CheckGPTRequestStatus

app_name = 'app'


urlpatterns = [
	path('login/', LoginPage.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
    path('', MainPage.as_view(), name='main_page'),
	path('getting_characteristics/', GettingCharacteristicsView.as_view(), name='getting_characteristics'),
	path('getting_characteristics/gr/status', CheckGPTRequestStatus.as_view(), name='gr_status'),
]