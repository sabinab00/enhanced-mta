from NYCT import Graph, Node
from queue import PriorityQueue
from search import ast
import findendpoints as fep
import helper


if __name__=='__main__':
    g = Graph()

    #origin point and destination point
    access = "n"
    start = "65 Bayard St, New York, NY 10013"
    end = "253 W 125th St, New York, NY 10027"

    found_stops = False
    found_path = False
    rad = 0.002
    paths_found = []

    while not found_stops or not found_path:
        # finds the starting and ending points within radius = rad of the start/end user inputs 
        f = (fep.findroutes(access,mode='all',origin=start,destination=end,graph=g,rad=rad))
        
        if len(f)>=1:
            found_stops = True
            print('Finding best routes for you...')
            for t in f:
                g.restartTransferCount()
                # a* search here
                sol = ast(t[0][0],t[0][1], accessibility=access)
                if sol:
                    
                    paths_found.append(sol)
                    found_path = True
                                
        rad += 0.0005
        if len(paths_found)<4:
            # ensures we have three or more paths to sort and pick from
            found_path=False
            found_stops=False

    # sorts the paths found by
    #   (1) number of modal transfers
    #   (2) number of stops passed through
    #   (3) number of route transfers
    
    sorted_paths  = helper.findTopPath(paths_found)
    for path in sorted_paths[:3]:
        print('------------')
        p = path[0]
        print(len(p), path[1], path[2])
        print(p)
    # print(len(paths_found))

