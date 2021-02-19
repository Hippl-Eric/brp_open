from datetime import date, datetime

class GPX_Data(object):
    
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        
# nps.gov data structure
class NPS_Data(object):
    
    def __init__(self, update=datetime, next_update=date, data=[]):
        self.update = update
        self.next_update = next_update
        self.data = data
