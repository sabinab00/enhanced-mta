import googlemaps

try:
    file = open('key.txt')
    api_key = file.readline()
    file.close()
    
except:
    print('No API Key detected')
gmaps = googlemaps.Client(key=api_key)


#takes address (str)
#address format: 'building number street name, town, state
#returns a list [latitude,longitude]
def get_geocode(address):
    response=gmaps.geocode(address)
    geo_code=list(response[0]["geometry"]["location"].values())

    return geo_code


#takes in  geocode (list(latitude, longitude)), and radius (int)
#returns a dictionary of nearby stops in a radius of 100 meters
    #key: stop name
    #value: ["type of transit",[latitude,longitude]]
def get_nearby_stops(loc, rad=100):
    subways= gmaps.places_nearby(location=loc,radius=rad,type='subway_station')
    buses= gmaps.places_nearby(location=loc,radius=rad,type='bus_station')
    nearby_stops=dict()
    
    for stop in subways['results']:
        nearby_stops[stop["name"]]=["subway",list(stop['geometry']['location'].values())]
    for stop in buses['results']:
        nearby_stops[stop["name"]]=["bus",list(stop['geometry']['location'].values())]

    return nearby_stops


#takes origin (list(latitude, longitude)), and destination (list(latitude, longitude))
#returns a dictionary of walking instructions, start transit stop, end transit stop
    #walking_dir - key: step number
        #value: [List of walking directions]
    #starting - {stop name : (geo_code, step number)}
    #ending - {stop name : (geo_code, step number)}
#takes API_key (str), origin (list(latitude, longitude)), and destination (list(latitude, longitude))
#returns a dictionary of walking instructions, start transit stop, end transit stop
    #walking_dir - key: step number
        #value: [List of walking directions]
    #starting - {stop name : (geo_code, step number)}
    #ending - {stop name : (geo_code, step number)}
def get_directions(origin,destination):
    transit_stops=[]
    walking=dict()
    count=0
    final_directions=dict()
    
    directions=gmaps.directions(origin=origin, destination=destination,mode='transit',transit_mode=["subway","bus"])


    for i in directions[0]['legs'][0]['steps']:
        if i['travel_mode']=="TRANSIT":
            count+=1
            transit_stops.append((i["transit_details"]["arrival_stop"]["name"],list(i["transit_details"]["arrival_stop"]["location"].values()),count))
            transit_stops.append((i["transit_details"]["departure_stop"]["name"],list(i["transit_details"]["departure_stop"]["location"].values()),count))
        if i["travel_mode"]=="WALKING":
            st=[]
            count+=1
            for ii in i['steps']:
                if 'html_instructions' in ii.keys():
                    st.append(ii["html_instructions"])
                    walking[f"{count}"]=st
                else:
                    st.append(f"Walk for {ii['distance']['text']}")
            walking[f"{count}"]=st

    final_directions["walking_dir"]=walking
    final_directions["starting"]={transit_stops[0][0]: (transit_stops[0][1],transit_stops[0][2])}
    final_directions["ending"]={transit_stops[-1][0]: (transit_stops[-1][1],transit_stops[-1][2])}

    return final_directions

# returns the distance between two places in terms of transit distance
# each location inputs are list of either string(s) or tuple(s) of geocode
def get_distance(location1, location2):
    mode = 'transit'
    transit_mode = ['train']
    distance = 0
    if location1 != location2:
        distance_matrix = gmaps.distance_matrix(origins=location1, destinations = location2, mode= mode, transit_mode=transit_mode)
        rows = distance_matrix['rows'][0]
        elements = rows['elements']
        distance = int(elements[0]['distance']['value'])
        
    return distance
