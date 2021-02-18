from django.urls import path
from . import views

app_name = 'map'
urlpatterns = [
    path('', views.index, name='index'),
    path('token', views.token, name='token'),
    path('route_data', views.get_route_data, name='route_data'),
]