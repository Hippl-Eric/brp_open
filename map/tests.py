import json
from pytz import timezone
import pytz
from datetime import date, datetime, timedelta

from django.test import TestCase, Client
from django.urls import reverse

from .models import Route, Update, Segment

# Create your tests here.
class ModelsTestCase(TestCase):
    
    def setUp(self):
        self.c = Client()
        
        # Create Route
        url = reverse('scrape:gpx_data')
        gpx_response = self.c.get(url)
        gpx_data = json.loads(gpx_response.content)
        route = Route.objects.create(name=gpx_data['filename'], all_points=gpx_data['data'])
        
        # Create Update
        url = reverse('scrape:scrape')
        scr_response = self.c.get(url)
        self.scr_data = json.loads(scr_response.content)
        update = Update.objects.create(timestamp=self.scr_data['update'], next_update=self.scr_data['next_update'])
        
        # Create Segments
        segments = []
        for seg in self.scr_data['data']:
            try:
                Seg = Segment(route=route, last_update=update, post_range=seg[0], cross_roads=seg[1], status=seg[2], notes=seg[3])
                segments.append(Seg)
            except IndexError as e:
                print(seg)
        # Segment.objects.bulk_create(segments)
        for segment in segments:
            segment.save()
        
    def test_models(self):
        route = Route.objects.first()
        self.assertIsNotNone(route)
        
        update = Update.objects.first()
        self.assertIsNotNone(update)
    
        segment_count = route.segments.count()
        self.assertEqual(segment_count, len(self.scr_data['data']))
        
        segment = Segment.objects.first()
        pass
    
    def test_get_route_data(self):
        url = reverse('map:route_data')
        route_data_res = self.c.get(url)
        
    def test_get_route_data_olddate(self):
        update = Update.objects.first()
        update.timestamp = update.timestamp - timedelta(1)
        update.save()
        url = reverse('map:route_data')
        route_data_res = self.c.get(url)
