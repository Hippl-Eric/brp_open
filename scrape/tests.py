import json
from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class ScrapeTestCase(TestCase):
    
    def setUp(self):
        self.c = Client()
    
    def test_gpx_data(self):
        url = reverse('scrape:gpx_data')
        response = self.c.get(url)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data['filename'], str)
        self.assertIsInstance(data['data'], list)
        self.assertIsInstance(data['data'][0], list)
        
    def test_scrape(self):
        url = reverse('scrape:scrape')
        response = self.c.get(url)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIsInstance(datetime.fromisoformat(data['update']), datetime)
        self.assertIsInstance(datetime.fromisoformat(data['next_update']), datetime)
        self.assertIsInstance(data['data'], list)
        self.assertIsInstance(data['data'][0], list)
