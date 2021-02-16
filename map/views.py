from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import os

# Create your views here.

load_dotenv()

def index(request):
    return render(request, "map/index.html")

def token(request):
    token = {"key":os.getenv('MAP_TOKEN')}
    return JsonResponse(token)
