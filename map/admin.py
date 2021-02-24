from django.contrib import admin
from .models import Route, Update, Segment

# Register your models here.

admin.site.register(Route)
admin.site.register(Update)
admin.site.register(Segment)
