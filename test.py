from NYCT import Graph, Node
from search import ast
import findendpoints as fep
import helper

g = Graph()
accessibility = ['y','n']
mode = 'all'

def test(access, mode, g, start, end):
    #origin point and destination point
    found_stops = False
    found_path = False
    rad = 0.002
    paths_found = []

    print('Finding best routes for you...')
    while not found_stops or not found_path:
        # finds the starting and ending points within radius = rad of the start/end user inputs 
        f = (fep.findroutes(access,mode=mode,origin=start,destination=end,graph=g,rad=rad))
        if rad >=0.01:
            print('No paths found... sorry :( ')
            break

        if len(f)>=1:
            found_stops = True
            
            for t in f:
                g.restartTransferCount()
                # a* search here
                sol = ast(t[0][0],t[0][1], accessibility=access)
                if sol:
                    paths_found.append(sol)
                    found_path = True
                                
        rad += 0.0005
        # if len(paths_found)<4:
        #     # ensures we have three or more paths to sort and pick from
        #     found_path=False
        #     found_stops=False

    
    sorted_paths  = helper.findTopPath(paths_found)

    print(f'We found {len(sorted_paths)} routes, here are the top 3:')
    for path in sorted_paths[:3]:
        print('------------')
        p = path[0]
        print(len(p), path[1], path[2])
        print(p)
    if len(sorted_paths)>1:
        return [sorted_paths[0]]   
    else:
        return sorted_paths
  
            
f = open('test-output-newh-3-0.txt','a')

with open('tests.txt') as file:
    for line in file:
        f.write('+++++++++++++++++++++++++++++++++++++'+'\n')
        start, end= line.rstrip().split(';')
        print(f'Starting point: {start}')
        print(f'Ending point: {end}')
        count = 0
        for a in accessibility:
            
            f.write('------------------------'+'\n')
            f.write('start:'+start+'\n')
            f.write('end: '+end+'\n')
            f.write('accessibility: '+a+'\n')
            f.write('------------------------'+'\n')
            paths = test(a, mode, g, start, end)
                        
            if paths:
                for p in paths:
                    crime = 0
                    path = p[0]
                    f.write(f'path{count}***********************'+'\n')
                    count+=1
                    # f.write(str(path)+'\n')
                    for stops in path:
                        crime += stops.crime_heuristics
                        f.write(str(stops)+'\n')
                    f.write('>>>>>> crime h = '+str(crime)+'<<<<<<<<'+'\n')
                    f.write('>>>>>> transfers_route '+str(p[1])+'<<<<<<<<'+'\n')
                    f.write('>>>>>> transfers_mode '+str(p[2])+'<<<<<<<<'+'\n')
                    f.write('>>>>>> number of stops '+str(len(path))+'<<<<<<<<'+'\n')
            else:
                f.write('***********************'+'\n')
                f.write('no paths found for: \n'+start+' to '+end+ a+'\n')


        

        