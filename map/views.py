from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from dotenv import load_dotenv
import os
import requests
import json

# Create your views here.

load_dotenv()

def index(request):
    return render(request, "map/index.html")

def token(request):
    token = {"key":os.getenv('MAP_TOKEN')}
    return JsonResponse(token)

def get_route_data(request):
    url = f"http://{request.get_host()}{reverse('scrape:gpx_data')}"
    response = requests.get(url)
    data = json.loads(response.content)
    
    # Create 2 lists, list of new segments to be created, list of existing segments to be updated
    
    # Create the new segments one by one (calls save method)
    
    # Bulk update existing segments
    
    return JsonResponse(data, safe=False)