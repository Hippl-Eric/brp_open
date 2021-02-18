from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class ScrapeTestCase(TestCase):
    
    def setUp(self):
        self.c = Client()
    
    def test_gpx_data(self):
        url = reverse('scrape:gpx_data')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_scrape(self):
        url = reverse('scrape:scrape')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        