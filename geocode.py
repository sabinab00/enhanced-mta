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

