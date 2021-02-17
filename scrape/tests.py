from django.test import TestCase, Client

# Create your tests here.

def test_gpx_data(self):
    c = Client()
    response = c.get('/gpx_data/')
    self.assertEqual(response.status_code, 200)