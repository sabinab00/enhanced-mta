import API_functions
# from NYCT import Node
import pandas as pd

crimesearch = __import__('Crime Search Heuristic')
crime = pd.read_csv(r'datasets\NYPD dataset.csv')
# center_1, center_2, center_3 = crimesearch.cluster(crime)
centers,radii = crimesearch.cluster(crime)

def distance(curr_stop: tuple, destination:tuple):
    '''
    takes geocode of origin and destination and
    calls the gmap API for the distance between the two points
    '''
    distance = API_functions.get_distance([curr_stop], [destination])
    return distance

def transit_mode_check(curr_stop, destination):
    '''checks if the current and destination'stop are for the same transit type'''
    return 0.005 if curr_stop.transit_type == destination.transit_type else 0

def euclidean_distance(curr_stop: tuple,destination:tuple):
    '''
    checks euclidean distance of the two stops 
    given two geocodes
    '''
    from scipy.spatial import distance
    return distance.euclidean(curr_stop,destination)

def route_check(curr_stop, destination):
    ''' 
    Checks the following between the current stop and desination stop:
      - the same route_id 
      - if the neigboring stops that are reachable from curr stop has the same route_id as well
    '''
    heuristic = 0
    if curr_stop.route_id == destination.route_id:
        # checks for the same route id
        heuristic +=0.001
    if destination.line:
        if curr_stop.route_id in destination.line:
            # checks for same line because routes in the same line
            # mostly shares the same stops
            heuristic += .0025

    # checking neighborhood leads to going backwards so don't really want that
    # nbdh = expand(curr_stop)
    # for n in nbdh:
    #     if destination.line:
    #         if n.route_id in destination.line:
    #             heuristic += 0.0001
    return heuristic
def express_check(curr_stop):
    '''
    Checks if the route taken at the current stop is express or not
    
    '''
    express = curr_stop.express
    return 0 if express else 0.001

def transfer_check(curr_stop):
    '''penalizes transfers route and modal transfers'''
    h = curr_stop.n_transfer_route*3 + 2*curr_stop.n_transfer_mode
    return h*0.0005
    
def crime_check(curr_stop):
    ''' 
    Checks if location is safe given geocode of stop
    '''
    heuristic = 0
    for code in crime.Geocode:
        if str(curr_stop.geocode) == code:
            heuristic += .0001
    return heuristic

def crime_distance(curr_stop):

    # distance_1 = euclidean_distance(curr_stop.geocode, (center_1[0],center_1[1]))
    # distance_2 = euclidean_distance(curr_stop.geocode, (center_2[0],center_2[1]))
    # distance_3 = euclidean_distance(curr_stop.geocode, (center_3[0],center_3[1]))

    # return min(distance_1, distance_2,distance_3)*0.1
    # return kmeansfitted.predict(curr_stop)

    h = 0 
    for i in range(3):
        center = centers[i]
        radius = radii[i]

        distance = euclidean_distance(curr_stop.geocode, (center[0],center[1]))
        if distance>=radius:
            h+=0
        else:
            h+=radius-distance
    return h*0.1
        