from copy import deepcopy
from math import dist
from NYCT import Graph, Node
from queue import PriorityQueue
import API_functions


def distance(curr_stop: tuple, destination:tuple):
    '''
    takes geocode of origin and destination and
    calls the gmap API for the distance between the two points
    '''
    distance = API_functions.get_distance([curr_stop], [destination])
    return distance

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
    if curr_stop.route_id in destination.line:
        # checks for same line because routes in the same line
        # mostly shares the same stops
        heuristic += .025

    # checking neighborhood leads to going backwards so don't really want that
    # nbdh = expand(curr_stop)
    # for n in nbdh:
    #     # if n.route_id == destination.route_id:
    #     if n.route_id in destination.line:
    #         heuristic += 0.01
    return heuristic
def express_check(curr_stop:Node):
    '''
    Checks if the route taken at the current stop is express or not
    
    '''
    express = curr_stop.express
    return 0.001 if express else 0


def heuristic(curr_stop: Node, destination: Node):
    '''
    Calculate heuristics for each stop. Current heuristics include:
    - `route_check`
    - `euclidean_distance`
     
    '''
    line_heuristic  = route_check(curr_stop, destination)
    distance_heuristic = euclidean_distance(curr_stop.geocode, destination.geocode)
    express_heuristic = express_check(curr_stop)

    return distance_heuristic-line_heuristic-express_heuristic


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

def ast(origin: Node, destination: Node):
    '''
    Implements A* search between two stops
    returns the path user should take
    '''
    curr_stop = origin

    h = heuristic(curr_stop, destination)
    curr_stop.heuristic_score = h

    frontier = PriorityQueue()
    reached = set()

    frontier.put((curr_stop.heuristic_score, curr_stop))
    reached.add(curr_stop.stop_id)
    # count = 0

    prev_stop = curr_stop
    path = []
    neighborhood = {}


    while not frontier.empty():
        
        candidate_stop = frontier.get()[1]
        print('____________________')
        print(f'prev stop at H={prev_stop.heuristic_score} {prev_stop.stop_name} {prev_stop.route_id}')
        print(f'prev stop neighborhood: {neighborhood[prev_stop.stop_id] if prev_stop.stop_id in neighborhood.keys() else False}')
        print(f'candidate at H={candidate_stop.heuristic_score} {candidate_stop} ')
        

        if (candidate_stop.route_id == prev_stop.route_id) \
             or (candidate_stop.stop_id in neighborhood[prev_stop.stop_id] if prev_stop.stop_id in neighborhood.keys() else False) if prev_stop.stop_id!=origin.stop_id else True:
            # you can only move forward if with this candidate if:
                # it runs on the same line as the previous stop 
                # OR you can transfer from the previous to this station 
                # OR this stop is a transfer or the child of the previous stop


            curr_stop = candidate_stop
            # if len(path) >1:
            #     if curr_stop.isSame(path[-1]):
            #         path.pop(-1)
            path.append(curr_stop)
            print('____________________')
            print(f'curr at {curr_stop}')
            print('____________________')


            if curr_stop.isSame(destination):
                # curr_node_path.getPath()
                print('REACHED!')
                for stop in path:
                    print(stop.stop_name, stop.route_id)
                # print([(node.stop_name, node.route_id) for node in path])
                break            

            neighbors = expand(curr_stop)
            

            if neighbors:
                neighborhood[curr_stop.stop_id] = [i.stop_id for i in neighbors]
                for neighbor in neighbors:
                    neigh_id = neighbor.stop_id
                    if neigh_id not in reached:
                        h = heuristic(neighbor, destination)
                        neighbor.setHeuristicScore(h)
                        reached.add(neigh_id)
                        frontier.put((h, neighbor))
                        
                        print(f'just discovered {h}: {neigh_id} {neighbor.stop_name} {neighbor.route_id} {neighbor.transfers_id}')   
            prev_stop = curr_stop


