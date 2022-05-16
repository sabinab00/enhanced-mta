from copy import deepcopy
from NYCT import Graph, Node
from queue import PriorityQueue
import API_functions
from path import Path


def distance(curr_stop: tuple, destination:tuple):
    '''
    takes geocode of origin and destination and
    calls the gmap API for the distance between the two points
    '''
    distance = API_functions.get_distance([curr_stop], [destination])
    return distance

def transit_mode_check(curr_stop: Node, destination:Node):
    '''checks if the current and destination'stop are for the same transit type'''
    return 0.005 if curr_stop.transit_type == destination.transit_type else 0

def euclidean_distance(curr_stop: tuple,destination:tuple):
    '''
    checks euclidean distance of the two stops 
    given two geocodes
    '''
    from scipy.spatial import distance
    return distance.euclidean(curr_stop,destination)

def route_check(curr_stop:Node, destination:Node):
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
    nbdh = expand(curr_stop)
    for n in nbdh:
        if destination.line:
            if n.route_id in destination.line:
                heuristic += 0.0001
    return heuristic
def express_check(curr_stop:Node):
    '''
    Checks if the route taken at the current stop is express or not
    
    '''
    express = curr_stop.express
    return 0 if express else 0.001

def transfer_check(curr_stop: Node):
    '''penalizes transfers route and modal transfers'''
    h = curr_stop.n_transfer_route*3 + 2*curr_stop.n_transfer_mode
    return h*0.0005
    

def heuristic(curr_stop: Node, destination: Node, accessibility):
    '''
    Calculate heuristics for each stop. Current heuristics include:
    - `route_check`
    - `euclidean_distance`
    - `express_check`
    - `transit_mode_check`
    - `transfer_check`
    '''
    line_heuristic  = route_check(curr_stop, destination)
    distance_heuristic = euclidean_distance(curr_stop.geocode, destination.geocode)
    express_heuristic = express_check(curr_stop)
    transit_type = transit_mode_check(curr_stop, destination)
    access_heuristic = 0
    transfer_heuristic = transfer_check(curr_stop)

    if accessibility == 'Y' or accessibility == 'y':
        if curr_stop.transit_type == 'bus' or (curr_stop.transit_type == 'subway' and curr_stop.accessibility !=0):
            access_heuristic = 0.001

    return distance_heuristic-line_heuristic-express_heuristic-transit_type- access_heuristic + transfer_heuristic


def expand(stop: Node):
    '''
    Returns a list of the neighboring stops of the current stop, 
    i.e. the stop before, after and stops user is able to transfer to.
    '''
    # returns the previous and next stop 
    # as well as the transfers available from the current stop
    children = []
    if stop.child:
        children.append(stop.child)
    if stop.parent:
        children.append(stop.parent)
    if stop.transfers:
        for transfer in stop.transfers:
            children.append(transfer)     
    return children    

def checkModalTransfer(prev: Node, candidate: Node):
    '''
    If the transit type of previous and candidate stop are not the same
    and accessibility is requested, we need to make sure that the stops
    are both accessible
    '''
     
    if prev.transit_type == candidate.transit_type:
        return True 
    else:
        if prev.accessibility != 0 and candidate.accessibility !=0:
            return True
        else:
            return False 



def ast(origin: Node, destination: Node, accessibility='N'):
    '''
    Implements A* search between two stops
    returns the path user should take
    '''
        
    curr_stop = origin
    prev_stop = curr_stop

    prev_stop_path = Path(curr_stop = prev_stop)

    h = heuristic(curr_stop, destination,accessibility)
    curr_stop.heuristic_score = h

    frontier = PriorityQueue()
    reached = set()

    frontier.put((curr_stop.heuristic_score, curr_stop))
    reached.add(curr_stop.stop_id)

    neighborhood = {}


    while not frontier.empty():    
        candidate_stop = frontier.get()[1]
        
        transferrable = True 
        if accessibility == 'y' or accessibility =='Y':
            transferrable = checkModalTransfer(prev_stop, candidate_stop)

        if ((candidate_stop.route_id == prev_stop.route_id) \
             or (candidate_stop.stop_id in neighborhood[prev_stop.stop_id] if prev_stop.stop_id in neighborhood.keys() else False) if prev_stop.stop_id!=origin.stop_id else True)\
             and transferrable:
            # you can only move forward if with this candidate if:
                # it runs on the same line as the previous stop 
                # OR you can transfer from the previous to this station 
                # OR this stop is a transfer or the child of the previous stop           
            curr_stop = candidate_stop
            curr_stop.updateNTransfers(prev_stop)
            
            curr_stop_path = Path(curr_stop=curr_stop, prev_stop=prev_stop_path)
            
            if curr_stop.isSame(destination):
                                # print('REACHED!')
                # for stop in path:
                #     print(stop.stop_name, stop.route_id)
                
                solution = curr_stop_path.getPath()
               
                # print(f'Path has {curr_stop.n_transfer_route} route transfers')
                # print(f'Path has {curr_stop.n_transfer_mode} modal transfers')

                return (solution,curr_stop.n_transfer_route,curr_stop.n_transfer_mode)  
                           

            # expands the current node to its immediate neighbors
            # the next and previous stop on the route, the stations (both subway and bus) transferrable
            # from the current stop
            neighbors = expand(curr_stop)
            

            if neighbors:
                neighborhood[curr_stop.stop_id] = [i.stop_id for i in neighbors]
                for neighbor in neighbors:
                    neigh_id = neighbor.stop_id
                    neighbor.updateNTransfers(prev_stop)
                    
                    # if the stop is not yet in the stack
                    # calculate the heuristic and add it to stack
                    if neigh_id not in reached:
                        h = heuristic(neighbor, destination,accessibility)
                        neighbor.setHeuristicScore(h)
                        reached.add(neigh_id)
                        frontier.put((h, neighbor))
                        
            
            prev_stop = curr_stop
            prev_stop_path = curr_stop_path
    
    return None


