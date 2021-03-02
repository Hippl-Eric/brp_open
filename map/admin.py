from django.contrib import admin
from .models import Route, Update, Segment

class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

class UpdateAdmin(admin.ModelAdmin):
    list_display = ["id", "timestamp", "next_update"]

class SegmentAdmin(admin.ModelAdmin):
    list_display = ["route", "last_update", "post_range"]

# Register your models here.

admin.site.register(Route, RouteAdmin)
admin.site.register(Update, UpdateAdmin)
admin.site.register(Segment, SegmentAdmin)
