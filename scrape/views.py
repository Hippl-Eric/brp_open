from django.shortcuts import render
from django.http import JsonResponse
from scrape.parse_gpx import gpx_to_points

# Create your views here.

def gpx_data(request):
    file = "scrape/parkway_n_to_s.gpx"
    data = gpx_to_points(file)
    return JsonResponse(data, safe=False)