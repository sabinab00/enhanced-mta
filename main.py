from NYCT import Graph, Node
from search import ast
import findendpoints as fep
import helper

def main():
    g = Graph()

    #origin point and destination point

    start = input('What is your starting address? \n>>>')
    end = input('What is your ending address? \n>>>')
    access = input('Would you like to request an accessible route (Y/N)? \n>>>')
    mode = input('Do you have a preferred mode of transportion? \nEnter "bus", "subway", or "both". \n>>>')

    found_stops = False
    found_path = False
    rad = 0.002
    paths_found = []

    print('Finding best routes for you...')
    while not found_stops or not found_path:
        print(rad)
        # finds the starting and ending points within radius = rad of the start/end user inputs 
        f = (fep.findroutes(access,mode=mode,origin=start,destination=end,graph=g,rad=rad))
        if rad >=0.005:
            print('No paths found... sorry :( ')
            break

        if len(f)>=1:
            found_stops = True
        
            for t in f:
                g.restartTransferCount()
                # a* search here
                sol = ast(t[0][0],t[0][1], accessibility=access)
                # sol returns (path, number of transered modes, number of transferred routes)
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
    if rad <0.005:
        sorted_paths  = helper.findTopPath(paths_found)
        print(f'We found {len(sorted_paths)} routes, here are the top 3:')
        for path in sorted_paths[:3]:
            print('------------')
            p = path[0]
            # print(len(p), path[1], path[2])
            # print(p)
            # sum = 0
            # for i in p:
            #     sum+=i.crime_heuristics
            # print('crimeh:',sum)
        # print(len(paths_found))

    print(str(p))
if __name__=='__main__':
    main()