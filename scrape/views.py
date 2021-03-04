import os
import requests
import re
from pytz import timezone
import pytz
from datetime import date, datetime

from django.http import JsonResponse

from scrape.parse_gpx import create_gpx_data_class
from scrape.classes import NPS_Data

from dateutil.parser import parse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Create your views here.
load_dotenv()

def gpx_data(request):
    filename = os.getenv('ROUTE_JSON')
    gpx_data = create_gpx_data_class(filename=filename)
    return JsonResponse(gpx_data.__dict__, safe=False)

def scrape(request):
    url = 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data_div = soup.find(id='cs_control_6725830')
    
    # Get the update date
    update = data_div.find('h3', string=re.compile('Road Status as of'))
    update = update.text.strip()
    update = update[18:]
    update = parse(update)
    eastern = timezone('US/Eastern')
    update = eastern.localize(update)
    hour = update.hour
    
    # Get the next update
    next_update = data_div.find('em', string=re.compile('This page will be updated on'))
    next_update = next_update.text.strip()
    next_update = next_update[29:]
    next_update = parse(next_update)
    next_update = next_update.replace(hour=hour)
    next_update = eastern.localize(next_update)

    # Get table data   
    tables = data_div.find_all('div', class_='table-wrapper')
    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if cells:
                row_data = [cell.text.strip() for cell in cells]
                # Only Segments, filter out points for now
                if "-" in row_data[0]:
                    # TODO ensure matches format (XX.X - XX.X)
                    data.append(row_data)
    
    # Return json data
    nps_data = NPS_Data(update=update, next_update=next_update, data=data)
    return JsonResponse(nps_data.__dict__, safe=False)
