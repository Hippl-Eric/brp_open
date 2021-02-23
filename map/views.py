import os
import requests
import json

from dotenv import load_dotenv

from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from .models import Route, Update, Segment

# Create your views here.

load_dotenv()

def index(request):
    return render(request, "map/index.html")

def token(request):
    token = {"key":os.getenv('MAP_TOKEN')}
    return JsonResponse(token)

def get_route_data(request):
    
    most_recent_update = Update.objects.latest('timestamp')
    segments = Segment.objects.values_list('post_range', flat=True).filter(last_update=most_recent_update)
    
    # Create 2 lists, list of new segments to be created, list of existing segments to be updated
    
    # Create the new segments one by one (calls save method)
    
    # Bulk update existing segments
    
    return JsonResponse(data, safe=False)