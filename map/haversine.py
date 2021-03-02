import math

def get_points(route, start, end):
    
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
    
    i = 0
    d = 0
    points = []
    
    # Find the start point
    if start <= 0:
        d += haversine(route[i], route[i+1])
        i += 1

    else:
        while d < start:
            try:
                d += haversine(route[i], route[i+1])
                i += 1
            except IndexError:
                raise Exception("Start value exceeds total route distance")
                break
    
    # Add the start point
    points.append(route[i-1])
    
    # Add all points up to end
    if end:
        while d < end:
            try:
                points.append(route[i])
                d += haversine(route[i], route[i+1])
                i += 1
            except IndexError:
                # End distance exceeds total length of route, return all points up to the end
                break
    
    return points
