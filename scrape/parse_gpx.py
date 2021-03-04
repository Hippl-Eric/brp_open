import re
import json

from scrape.classes import GPX_Data

def gpx_to_json(filename):
    """
    Parse a GPX file and return all points matching the defined patten.
    Return data saved in a JSON file.
    
    Defined pattern:
    <trkpt lat="38.03124" lon="-78.85784">
        <ele>577.8</ele>
    </trkpt>
    
    JSON file format - List of lists:
    [["38.03124", "-78.85784", "577.8"]...]
    """

    # Find matches using regex
    with open(filename) as f:
        
        # Read entire file, store as string
        data = f.read()
        
        # Create a list of point tuples
        matches = re.findall(pattern='<trkpt lat="([-0-9\.]+)" lon="([-0-9\.]+)">\n\s+<ele>([-0-9\.]+)</ele>\n\s+</trkpt>', string=data)

    # Create JSON file
    with open('scrape/route-data.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)

def json_to_points(filename):
    """
    Open JSON filename and return JSON data
    """
    with open(filename, 'r') as f:
        return json.load(f)

def create_gpx_data_class(filename):
    """
    Convert JSON filename data to a GPX_Data class to be used by scrape.gpx_data view
    """
    data = json_to_points(filename)
    return GPX_Data(filename=filename, data=data)
