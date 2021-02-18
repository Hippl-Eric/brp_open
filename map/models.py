from django.db import models

# Create your models here.

class Route(models.Model):
    name = models.CharField(max_length=50)
    all_points = models.JSONField()
    
class Update(models.Model):
    timestamp = models.DateTimeField()
    
class Segment(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="segments")
    last_update = models.ForeignKey("Update", on_delete=models.CASCADE, related_name="segments")
    post_range = models.CharField(max_length=50)
    post_start = models.DecimalField(max_digits=4, decimal_places=1)
    post_end = models.DecimalField(max_digits=4, decimal_places=1)
    cross_roads = models.TextField()
    status = models.CharField(max_length=50)
    notes = models.TextField()
    points = models.JSONField()