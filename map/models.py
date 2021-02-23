import re

from django.db import models

from .haversine import get_points

# Create your models here.

class Route(models.Model):
    name = models.CharField(max_length=50)
    all_points = models.JSONField()
    
    def return_points(self, start, end=None):
        return get_points(route=self.all_points, start=start, end=end)
    
class Update(models.Model):
    timestamp = models.DateTimeField()
    next_update = models.DateField()
    
class Segment(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="segments")
    last_update = models.ForeignKey("Update", on_delete=models.CASCADE, related_name="segments")
    post_range = models.CharField(max_length=50)
    post_start = models.FloatField(null=True)
    post_end = models.FloatField(null=True)
    cross_roads = models.TextField()
    status = models.CharField(max_length=50)
    notes = models.TextField()
    points = models.JSONField(null=True)
    
    def save(self, *args, **kwargs):
        self.set_start_end_posts()
        self.set_points()
        super(Segment, self).save(*args, **kwargs)
    
    def set_start_end_posts(self):
        start, end = re.findall(pattern='([0-9\.]+)', string=self.post_range)
        self.post_start = round(float(start), 1)
        self.post_end = round(float(end), 1)
        
    def set_points(self):
        self.points = self.route.return_points(start=self.post_start, end=self.post_end)
