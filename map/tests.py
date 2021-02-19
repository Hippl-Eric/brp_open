import json
from pytz import timezone
import pytz
from datetime import date, datetime

from django.test import TestCase, Client
from django.urls import reverse

from .models import Route, Update, Segment
from scrape.parse_gpx import gpx_to_points

# Create your tests here.
class ModelsTestCase(TestCase):
    
    def setUp(self):
        self.c = Client()
        
        # Create Route
        url = reverse('scrape:gpx_data')
        gpx_response = self.c.get(url)
        gpx_data = json.loads(gpx_response.content)
        Route.objects.create(name=gpx_data['filename'], all_points=gpx_data['data'])
        
        # Create an Update
        url = reverse('scrape:scrape')
        scr_response = self.c.get(url)
        scr_data = json.loads(scr_response.content)
        Update.objects.create(timestamp=scr_data['update'], next_update=scr_data['next_update'])
        
    def test_route(self):
        route = Route.objects.first()
        self.assertIsNotNone(route)
        
    def test_update(self):
        update = Update.objects.first()
        self.assertIsNotNone(update)
    
    # def test_segment(self):
    #     pass