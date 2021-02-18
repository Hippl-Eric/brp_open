from django.urls import path
from . import views

app_name = 'scrape'
urlpatterns = [
    path("gpx_data", views.gpx_data, name="gpx_data"),
    path("scrape", views.scrape, name="scrape"),
]