import re

from scrape.classes import GPX_Data

def gpx_to_points(file_name):
    """
    Parse a gpx file and return all points matching the defined patten.
    Return a tuple of tuples for each point (lat, long, elev).
    
    Defined pattern:
    <trkpt lat="38.03124" lon="-78.85784">
        <ele>577.8</ele>
    </trkpt>
    
    Return:
    ((38.03124, -78.85784, 577.8))
    """

    # Find matches using regex
    with open(file_name) as f:
        
        # Read entire file, store as string
        data = f.read()
        
        # Create a list of point tuples
        matches = re.findall(pattern='<trkpt lat="([-0-9\.]+)" lon="([-0-9\.]+)">\n\s+<ele>([-0-9\.]+)</ele>\n\s+</trkpt>', string=data)

    def tuple_to_list(tup):
        return list(tup)
    
    return list(map(tuple_to_list, matches))

def create_gpx_data_class(file_name):
    data = gpx_to_points(file_name)
    return GPX_Data(filename=file_name, data=data)
