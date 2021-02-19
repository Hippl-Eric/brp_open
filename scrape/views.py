import requests
import math
import re
import json
from pytz import timezone
import pytz
from datetime import date, datetime

from django.http import JsonResponse

from scrape.parse_gpx import gpx_to_points
from scrape.classes import GPX_Data, NPS_Data

from dateutil.parser import parse
from bs4 import BeautifulSoup

# Create your views here.

def gpx_data(request):
    filename = "scrape\Blue_Ridge_Parkway_-_NS.gpx"
    data = gpx_to_points(filename)
    gpx_data = GPX_Data(filename=filename, data=data)
    return JsonResponse(gpx_data.__dict__, safe=False)

def scrape(request):
    url = 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data_div = soup.find(id='cs_control_6725830')
    
    # Get the update date
    update = data_div.find('h3', string=re.compile('Road Status as of'))
    update = update.text.strip()
    update = update.strip('Road Status as of Thursday, ')
    update = parse(update)
    eastern = timezone('US/Eastern')
    update = eastern.localize(update)
    
    # Get the next update
    next_update = data_div.find('em', string=re.compile('This page will be updated on'))
    next_update = next_update.text.strip()
    next_update = next_update.strip('This page will be updated on ')
    next_update = parse(next_update).date()

    # Get table data   
    tables = data_div.find_all('div', class_='table-wrapper')
    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('p')
            if cells:
                row_data = [cell.text.strip() for cell in cells]
                data.append(row_data)
    
    # Return json data
    nps_data = NPS_Data(update=update, next_update=next_update, data=data)
    return JsonResponse(nps_data.__dict__, safe=False)


def get_distance(coordinates):
    ''' Return total distance in miles between a list of coordinates '''
    
    def haversine(coord1, coord2):
        ''' Return distance in miles between two (2) coordinates '''
        
        lat1, long1, ele1 = coord1
        lat2, long2, ele2 = coord2
        r = 3958.8
        rad = math.pi/180
        lat1 = float(lat1)*rad
        long1 = float(long1)*rad
        lat2 = float(lat2)*rad
        long2 = float(long2)*rad
        d = 2*r*math.asin(math.sqrt((math.sin((lat2-lat1)/2))**2 + math.cos(lat1)*math.cos(lat2)*(math.sin((long2-long1)/2))**2))
        return d
    d = 0
    for i in range(len(coordinates)-1):
        d += haversine(coordinates[i], coordinates[i+1])
    return d