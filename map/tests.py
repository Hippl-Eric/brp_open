import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Route
from scrape.parse_gpx import gpx_to_points

# Create your tests here.
class ModelsTestCase(TestCase):
    
    def setUp(self):
        self.c = Client()
        
        # Create Route
        url = reverse('scrape:gpx_data')
        response = self.c.get(url)
        data = json.loads(response.content)
        Route.objects.create(name=data['filename'], all_points=data['data'])
        
    def test_route(self):
        route = Route.objects.first()
        self.assertIsNotNone(route)
        
    # def test_update(self):
    #     pass
    
    # def test_segment(self):
    #     pass