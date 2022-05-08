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


#takes API_key (str), origin (list(latitude, longitude)), and destination (list(latitude, longitude))
#returns a dictionary of walking instructions, start transit stop, end transit stop
    #walking_dir - key: step number
        #value: [List of walking directions]
    #starting - {stop name : (geo_code, step number)}
    #ending - {stop name : (geo_code, step number)}
def get_directions(API_key,origin,destination):
    transit_stops=[]
    walking=dict()
    count=0
    transit_mode=str()
    final_directions=dict()
    
    gmap=googlemaps.Client(key=API_key)
    directions=gmap.directions(origin=origin, destination=destination,mode='transit',transit_mode=["subway","bus"])


    for i in directions[0]['legs'][0]['steps']:
        if i['travel_mode']=="TRANSIT":
            count+=1
            transit_stops.append((i["transit_details"]["arrival_stop"]["name"],list(i["transit_details"]["arrival_stop"]["location"].values()),count))
            transit_stops.append((i["transit_details"]["departure_stop"]["name"],list(i["transit_details"]["departure_stop"]["location"].values()),count))
            transit_mode="transit"
        if i["travel_mode"]=="WALKING":
            st=[]
            count+=1
            for ii in i['steps']:
                st.append(ii["html_instructions"])
            walking[f"{count}"]=st
            transit_mode="walking"

    final_directions["walking_dir"]=walking
    final_directions["starting"]={transit_stops[0][0]: (transit_stops[0][1],transit_stops[0][2])}
    final_directions["ending"]={transit_stops[-1][0]: (transit_stops[-1][1],transit_stops[-1][2])}

    return final_directions
