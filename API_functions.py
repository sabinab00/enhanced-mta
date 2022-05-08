import googlemaps

#takes in API_key (str) and address (str)
#requires Google API key
#address format: 'building number street name, town, state
#returns a list [latitude,longitude]
def get_geocode(API_key, address):
    gmaps=googlemaps.Client(key=API_key)
    response=gmaps.geocode(address)
    geo_code=list(response[0]["geometry"]["location"].values())

    return geo_code


#takes in API_key (str), geocode (list(latitude, longitude)), and radius (int)
#returns a dictionary of nearby stops in a radius of 100 meters
    #key: stop name
    #value: ["type of transit",[latitude,longitude]]
def get_nearby_stops(API_key, loc, rad=100):
    gmap=googlemaps.Client(key=API_key)
    subways=gmap.places_nearby(location=loc,radius=rad,type='subway_station')
    buses=gmap.places_nearby(location=loc,radius=rad,type='bus_station')
    nearby_stops=dict()
    
    for stop in subways['results']:
        nearby_stops[stop["name"]]=["subway",list(stop['geometry']['location'].values())]
    for stop in buses['results']:
        nearby_stops[stop["name"]]=["bus",list(stop['geometry']['location'].values())]

    return nearby_stops
