import API_functions as ap
import NYCT
import googlemaps
import heuristics

g= NYCT.Graph()
#test=["7 State St, New York, NY 10004|199 Chambers St, New York, NY 10007|S0,S4,3|n","365 5th Ave, New York, NY 10016|1234 E 6th St, New York, NY 10009|S244,S240,3|B436,B999,10|n"]
f = open('googletest-output-newh2.txt','a')

with open("googletest.txt") as file:
    for t in file:
        #initializing variables
        tt=t.split("|")
        s=tt[0]
        e=tt[1]
        a=tt.pop()
        pp=tt[2:]
        transfers_route=len(pp)
        transfers_mode=set()

        #finding path
        for p in pp:
            p=p.split(",")
            start=g.getStop(p[0])
            end=g.getStop(p[1])
            transfers_mode.add(start.transit_type)
            upordown=end.stop_sequence-start.stop_sequence
            n=start
            path=[n]
            if upordown>=0:
                for i in range(0,int(p[2])):
                    if n.stop_name!=end.stop_name:
                        n=n.child
                        path.append(n)
                    else:
                        break
            else:
                for i in range(0,int(p[2])):
                    if n.stop_name!=end.stop_name:
                        n=n.parent
                        path.append(n)
                    else:
                        break
        crime=0
        for i in path:
            crime+=i.crime_heuristics

        f.write('+++++++++++++++++++++++++++++++++++++'+'\n')
        print(f'Starting point: {start}')
        print(f'Ending point: {end}')
        f.write('------------------------'+'\n')
        f.write('start:'+s+'\n')
        f.write('end: '+e+'\n')
        f.write('accessibility: '+a+'\n')
        f.write('------------------------'+'\n')            
        for p in path:
            f.write(str(p)+"\n")
        f.write('>>>>>> crime h= '+str(crime)+'<<<<<<<<'+'\n')
        f.write('>>>>>> transfers_route '+str(transfers_route-1)+'<<<<<<<<'+'\n')
        f.write('>>>>>> transfers_mode '+str(len(transfers_mode)-1)+'<<<<<<<<'+'\n')
        f.write('>>>>>> number of stops '+str(len(path))+'<<<<<<<<'+'\n')
    
    





