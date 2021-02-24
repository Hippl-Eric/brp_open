import os
import requests
import json
import datetime

from dotenv import load_dotenv

from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from .models import Route, Update, Segment

from .classes import Segment_Data
from scrape.views import gpx_data, scrape

# Create your views here.

load_dotenv()

def index(request):
    return render(request, "map/index.html")

def token(request):
    token = {"key":os.getenv('MAP_TOKEN')}
    return JsonResponse(token)

def get_route_data(request):
    
    # Get the Route, setup database if necessary
    route = Route.objects.first()
    if not route:
        setupDB(request)
        route = Route.objects.first()
    
    # Check if database matches NPS data, update data if not
    most_recent_update = Update.objects.latest('timestamp')
    nps_response = scrape(request)
    nps_data = json.loads(nps_response.content)
    if most_recent_update.timestamp != datetime.datetime.fromisoformat(nps_data['update']):
        
        # Create list of all NPS post_range segment values
        nps_data_post_ranges = [post[0] for post in nps_data['data']]
               
        # Create list of all existing DB segment post_range values
        segment_post_ranges = Segment.objects.values_list('post_range', flat=True).filter(last_update=most_recent_update)
        
        # Create list of segments that match NPS data and DB segment values (to be updated)
        update_segments = Segment.objects.filter(last_update=most_recent_update).filter(post_range__in=nps_data_post_ranges)
        
        # Create list of segments that match NPS data, but are not in the DB (to be created)
        new_segment_post_ranges = [nps_data_post_range for nps_data_post_range in nps_data_post_ranges if nps_data_post_range not in segment_post_ranges]
        
        # Create new Update
        most_recent_update = Update.objects.create(timestamp=nps_data['update'], next_update=nps_data['next_update'])
        most_recent_update.refresh_from_db()
        
        # Bulk update existing segments
        for update_segment in update_segments:
            i = None
            for i, seg in enumerate(nps_data['data']):
                if seg[0] == update_segment.post_range:
                    break
            update_segment.last_update = most_recent_update
            update_segment.status = nps_data['data'][i][2]
            update_segment.notes = nps_data['data'][i][3]
        Segment.objects.bulk_update(update_segments, ['last_update', 'status', 'notes'])

        # Create the new segments one by one (calls save method)
        for post_range in new_segment_post_ranges:
            i = None
            for i, seg in enumerate(nps_data['data']):
                if seg[0] == post_range:
                    break
            new_segment = Segment.objects.create(
                route=route,
                last_update=most_recent_update,
                post_range=nps_data['data'][i][0],
                cross_roads=nps_data['data'][i][1],
                status=nps_data['data'][i][2],
                notes=nps_data['data'][i][3])
    
    # Return most up to date segment data  
    segments = Segment.objects.filter(last_update=most_recent_update)
    segments = [segment.serialize() for segment in segments]
    data = Segment_Data(
        update=most_recent_update.timestamp,
        next_update=most_recent_update.next_update,
        segments=segments)
    return JsonResponse(data.__dict__, safe=False)

def setupDB(request):
    '''Database is empty, create Route, Update, and Segments'''
    
    # Create Route
    gpx_response = gpx_data(request)
    route_data = json.loads(gpx_response.content)
    route = Route.objects.create(name=route_data['filename'], all_points=route_data['data'])
    
    # Create Update
    scr_response = scrape(request)
    scr_data = json.loads(scr_response.content)
    update = Update.objects.create(timestamp=scr_data['update'], next_update=scr_data['next_update'])
    
    # Create Segments
    segments = []
    for seg in scr_data['data']:
        try:
            Seg = Segment(route=route, last_update=update, post_range=seg[0], cross_roads=seg[1], status=seg[2], notes=seg[3])
            segments.append(Seg)
        except IndexError as e:
            print(seg)
    for segment in segments:
        segment.save()
