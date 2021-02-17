from django.urls import path
from . import views

urlpatterns = [
    path("gpx_data", views.gpx_data, name="gpx_data"),
]