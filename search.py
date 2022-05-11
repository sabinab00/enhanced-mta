from copy import deepcopy
from math import dist
from NYCT import Graph, Node
from queue import PriorityQueue
import API_functions

# takes geocode of origin and destination and
# calls the gmap API for the distance between the two points
def distance(curr_stop: tuple, destination:tuple):
    '''
    curr_stop: geocode (lat, lon)
    destination: geocode (lat,lon)
    '''
    distance = API_functions.get_distance([curr_stop], [destination])
    return distance

def euclidean_distance(curr_stop: tuple,destination):
    from scipy.spatial import distance
    return distance.euclidean(curr_stop,destination)

def route_check(curr_stop:Node, destination:Node):
    heuristic = 1
    if curr_stop.route_id == destination.route_id:
        heuristic -= .2
    if destination.transfers_id:
        if curr_stop.stop_id in destination.transfers_id:
            heuristic -= 0.05

    # checks for its neighboring stop as well 
    nbdh = expand(curr_stop)
    for n in nbdh:
        if n.route_id == destination.route_id:
            heuristic -=0.1

    return heuristic


def heuristic(curr_stop, destination):
    # if two stops have the same line
    line_heuristic  = route_check(curr_stop, destination)
    distance_heuristic = euclidean_distance(curr_stop.geocode, destination.geocode)

    return distance_heuristic*line_heuristic



# class NodePath():
#     def __init__(self, curr:Node=None, prev:Node = None, next: Node = None):
#         self.curr = curr
#         self.prev = prev 
#         self.next = next
    
#     def getPath(self):
#         node = self
#         while node:
#             if node.prev:
#                 print(node.prev)
#             node = node.prev


def expand(stop: Node):
    # returns the next stop in the sequence as well as 
    # the stops that you can transfer fro herem
    children = []
    if stop.child:
        children.append(stop.child)
        # if stop.child.transfers:
        #     for transfer in stop.child.transfers:
        #         children.append(transfer)
    if stop.parent:
        children.append(stop.parent)
        
    if stop.transfers:
        for transfer in stop.transfers:
            children.append(transfer)
            
    return children    

def ast(origin: Node, destination: Node):
    # traverses through curr_stop but path information is stored in NodePath 
    curr_stop = origin
    

    h = heuristic(curr_stop, destination)
    curr_stop.heuristic_score = h
    # path.heuristic_score = h

    frontier = PriorityQueue()
    reached = set()

    frontier.put((curr_stop.heuristic_score, curr_stop))
    reached.add(curr_stop.stop_id)
    count = 0

    prev_stop = curr_stop
    path = []
    neighborhood = {}
    # curr_node_path = NodePath(curr=prev_stop,prev=None)

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
            # curr_node_path = NodePath(curr = curr_stop, prev = prev_stop)
            prev_stop = curr_stop

        
g = Graph()
origin = g.getStop('60')
destination = b = g.getStop('267')
ast(origin, destination)


