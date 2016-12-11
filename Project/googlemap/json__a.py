
import json

with open('geo.json') as data_file:    
    data = json.load(data_file)
    print data["ListingID"]
