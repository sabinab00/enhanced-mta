from copy import deepcopy
from NYCT import Graph, Node
from queue import PriorityQueue
import API_functions

# takes geocode of origin and destination and
# calls the gmap API for the distance between the two points

def heuristic(origin, destination):
    '''
    origin: geocode (lat, lon)
    destination: geocode (lat,lon)
    '''
    return API_functions.get_distance([origin], [destination])

class NodePath():
    def __init__(self,origin:Node, curr:Node=None, prev:Node = None, next: Node = None):
        self.origin = origin
        self.curr = curr
        self.prev = prev 
        self.next = next
    
    def getPath(self):
        node = self
        while node.prev:
            print(node.prev)
            if node.curr.stop_id == self.origin.stop_id:
                break
            node = node.prev


def expand(stop: Node):
    children = []
    if stop.child:
        children.append(stop.child)
        if stop.child.transfers:
            for transfer in stop.child.transfers:
                children.append(transfer)
    if stop.transfers:
        for transfer in stop.transfers:
            # child_path = NodePath(origin, curr = transfer, prev=path)
            # print(child_path.curr, child_path.prev.curr.stop_id, path.curr.stop_id)
            children.append(transfer)
            
    return children    

def ast(origin: Node, destination: Node):
    # traverses through curr_stop but path information is stored in NodePath 
    curr_stop = origin

    h = heuristic(curr_stop.geocode, destination.geocode)
    curr_stop.heuristic_score = h
    # path.heuristic_score = h

    frontier = PriorityQueue()
    reached = set()

    frontier.put((curr_stop.heuristic_score, curr_stop))
    reached.add(curr_stop.stop_id)
    count = 0

    while not frontier.empty():
        # TODO make sure that currstop has either 
        # 1 same line as prev stop
        # or is in a transferrable station
        curr_stop = frontier.get()[1]
        print(f'now at {curr_stop}')
        print('____________________')
        
        if curr_stop.isSame(destination):
            print('REACHED!')
            break            

        neighbors = expand(curr_stop)

        if neighbors:
            for neighbor in neighbors:
                neigh_id = neighbor.stop_id
                if neigh_id not in reached:
                    h = heuristic(neighbor.geocode, destination.geocode)
                    neighbor.setHeuristicScore(h)
                    reached.add(neigh_id)
                    frontier.put((h, neighbor))
                    
                    # print(f'just discovered {h}: {neigh_id} {neighbor.stop_name}')       
        
g = Graph()
origin = g.getStop('Canal St')[-1]
destination = b = g.getStop('168 St-Washington Hts')[0]
ast(origin, destination)


