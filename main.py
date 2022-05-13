from NYCT import Graph, Node
from queue import PriorityQueue
from search import ast
import findendpoints as fep


if __name__=='__main__':
    g = Graph()
    # origin = g.getStop('B1')
    # destination = b = g.getStop('S201')
    # print(destination.transfers)
    # ast(origin, destination)

    #origin point and destination point
    access = "y"
    start = "4 South St Space 2, New York, NY 10004"
    end = "1220 5th Ave, New York, NY 10029"
    rad = 0.002
    f = fep.findroutes(access,mode='subway',origin=start,destination=end,graph=g,rad=rad)

    # prints notes
    # for t in f:
    #     print(f"{t[0][0].stop_name} to {t[0][1].stop_name} : {t[0][0].route_id} to {t[0][1].route_id}")
    #     print(f"{t[0][0].stop_name} to {t[0][1].stop_name} and {t[1]}")
    # print(f[0])
    for t in f:
        print(t[0][0],t[0][1])
        ast(t[0][0],t[0][1], accessibility=access)
        print('------------------')
        # print(f[0])
    print(len(f))