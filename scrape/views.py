from django.shortcuts import render
from django.http import JsonResponse
from scrape.parse_gpx import gpx_to_points
from bs4 import BeautifulSoup
import requests
import math

# Create your views here.

def gpx_data(request):
    file = "scrape\Blue_Ridge_Parkway_-_NS.gpx"
    data = gpx_to_points(file)
    print(get_distance(data))
    return JsonResponse(data, safe=False)

def scrape(request):
    url = 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    tables = soup.find_all('div', class_='table-wrapper')
    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('p')
            if cells:
                row_data = [cell.text.strip() for cell in cells]
                data.append(row_data)
    # TODO Validate data: ensure data not empty
    return JsonResponse(data, safe=False)


def get_distance(coordinates):
    def haversine(coord1, coord2):
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