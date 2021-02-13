import re

# Example pattern
"""
    <trkpt lat="38.03124" lon="-78.85784">
        <ele>577.8</ele>
    </trkpt>
"""

''' Solution 1: I think this loads too much memory '''
# Find matches using regex
with open("small.gpx") as f:
    
    # Read entire file, store as string
    data = f.read()
    
    # Create a list of tuple
    matches = re.findall(pattern='<trkpt lat="([-0-9\.]+)" lon="([-0-9\.]+)">\n\s+<ele>([-0-9\.]+)</ele>\n\s+</trkpt>', string=data)
    
    # Create generator object
    point_gen = (pnt for pnt in matches)
    
# Print the entire match list
print(matches)

# Print the first point from generator
print(next(point_gen))

# Print the second point from generator
print(next(point_gen))

''' Solution 2: Not working'''

data = (line for line in open('small.gpx'))
matches = (re.findall(pattern='<trkpt lat="([-0-9\.]+)" lon="([-0-9\.]+)">\n\s+<ele>([-0-9\.]+)</ele>\n\s+</trkpt>', string=data) for char in data) # Problem here - data needs to be a string
point_gen = (pnt for pnt in matches)

print(matches)
print(next(point_gen))
print(next(point_gen))

''' Solution 3: 
Try using mmap: https://stackoverflow.com/questions/11159077/python-load-2gb-of-text-file-to-memory
Read docs, says can be used with re
'''

def gpx_reader(file_name):
    yield re.findall(pattern='<trkpt lat="([-0-9\.]+)" lon="([-0-9\.]+)">', string=open(file_name, 'r')) # Problem here - data needs to be a string

gpx = gpx_reader('small.gpx')
print(gpx)
print(next(gpx))

