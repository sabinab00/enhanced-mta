from NYCT import Graph, Node
from queue import PriorityQueue
from path import Path
import heuristics as he

def heuristic(curr_stop: Node, destination: Node, accessibility):
    '''
    Calculate heuristics for each stop. Current heuristics include:
    - `route_check`
    - `euclidean_distance`
    - `express_check`
    - `transit_mode_check`
    - `transfer_check`
    '''
    line_heuristic  = he.route_check(curr_stop, destination)
    distance_heuristic = he.euclidean_distance(curr_stop.geocode, destination.geocode)
    express_heuristic = he.express_check(curr_stop)
    transit_type = he.transit_mode_check(curr_stop, destination)
    access_heuristic = 0
    transfer_heuristic = he.transfer_check(curr_stop)

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
                # OR you can transfer from the previous stop to this station 
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


