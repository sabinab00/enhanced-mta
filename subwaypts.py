import API_functions as ap
import NYCT
from scipy.spatial import distance
import numpy as np

#adjust google api stop names to our graph stop names
def findpts(t,allstops):
    stps=dict()
    pts=[]
    for tt in t.keys():
        i=tt
        if " - " in tt:
            tt=tt.replace(" - ","-")
        if 'Station' in tt:
            tt=tt.replace("Station","")
        if "Street" in tt:
            tt=tt.replace("Street","St")
        tt=tt.rstrip() 
        stps[tt]=t[i]
    for a in allstops:
        for tt in stps.keys():
            if tt in a:
                pts.append(g.getStop(a))
    return list(np.concatenate(pts).flat)

#finds the euclidean distance between two points
def euclidean(origin,destination):
    return distance.euclidean(tuple(origin),tuple(destination))

#checks the accessibility of a station
def accessible(points):
    available=[]
    for p in points:
        if p.accessibility!=0:
            available.append(p)
    return available


#returns list of paths to try starting with the best to the worst
#input(string API_key, graph object, string Y or N for accessibility, string starting address, string ending address)
def findsubwaypaths(API_key,g,access,start,end):
    #list of all stop names in database
    allstops=set()
    for x in g.stopIDs:
        allstops.add(g.getStop(x).stop_name)
    
    #colors key and access
    colors={"GS":"shuttle","FX":"orange",'A':'blue','C':'blue','E':'blue','B':'orange', 'D':'orange',"F":'orange',"M":'orange','G':'lime',"L":'gray',"J":'brown',"Z":'brown',"N":'yellow',"Q":"yellow","R":"yellow","W":"yellow","1":"red","2":"red","3":"red","4":"green","5":"green","6":"green","7":"purple"}

    #starting point
    origin=ap.get_geocode(API_key,start)
    r=100
    t=ap.get_nearby_stops(API_key,origin,r)
    while len(t)==0 and r<=5000:
        r=r+100
        t=ap.get_nearby_stops(API_key,origin,r)


    #ending point
    destination=ap.get_geocode(API_key,end)
    r=100
    t2=ap.get_nearby_stops(API_key,destination,r)
    while len(t2)==0 and r<=5000:
        r=r+100
        t2=ap.get_nearby_stops(API_key,destination,r)

    #finds all nearby stops and finds the nodes in the database
    originpts=findpts(t,allstops)
    destpts=findpts(t2,allstops)

    #takes out stops that are not accessible if requested
    if access=="Y" or access=="y":
        originpts=accessible(originpts)
        destpts=accessible(destpts)
    if len(originpts)==0 or len(destpts)==0:
        print("No Nearby Stops")
    else:
    
        #orders origin points by stops closest to origin
        #(node,distance from origin)
        closest2origin=[]
        for o in originpts:
            closest2origin.append((o,euclidean(origin,o.geocode)))
        closest2origin.sort(key=lambda x:(x[1]))

        #orders destination points by stops closest to destination
        #(node,distance from destination)
        closest2dest=[]
        for d in destpts:
            closest2dest.append((d,euclidean(d.geocode,destination)))
        closest2dest.sort(key=lambda x:(x[1]))

        #separates stops from same route and different route
        #(node-pair,sum of both distances,if the routes are in the same color group F if yes, T if no,express: if none are express 2, if one is express 1, if both are express 0)
        sameroutes=[]
        diffroutes=[]
        visited=set()
        for o in closest2origin:
            for d in closest2dest:
                new=((o[0],d[0]),o[1]+d[1],colors[o[0].route_id]!=colors[d[0].route_id],2-o[0].express-d[0].express)
                if o[0].route_id==d[0].route_id:
                    if new not in sameroutes:
                        sameroutes.append(new)
                        visited.add((o[0].stop_name,d[0].stop_name))
                else:
                    if new not in diffroutes and (o[0].stop_name,d[0].stop_name) not in visited:
                        diffroutes.append(new)
                        visited.add((o[0].stop_name,d[0].stop_name))
        sameroutes.sort(key=lambda x:(x[1],x[3]))
        diffroutes.sort(key=lambda x:(x[2],x[1],x[3]))


        #final routes in correct order
        #(starting node, destination node)
        finalroutes=[]
        for s in sameroutes:
            finalroutes.append(s)
        for d in diffroutes:
            finalroutes.append(d)

        return finalroutes


##generating graph object        
#g = NYCT.Graph()
#g.generateTransfers()
#g.generateStops('subway',0)
#g.generateStopNames()
#g.generateRoutes('subway',0)
#g.mapStopTransfers()
#g.connectStops() 

##uploading key
#f=open("key.txt")
#API_key=f.read()
#f.close()


    
##Is the route accessible? Y or N
#access=input("Do you need an accessible route? Y or N ")


##starting point: string
#start=input("Where is your origin address? ")
#start="4 South St Space 2, New York, NY 10004"


##ending point:string
#end=input("Where is your destination address? ")
#end="85 Greenwich St, New York, NY 10006"

#finds routes
#finalroutes=findsubwaypaths(API_key,g,access,start,end)

#prints out stopnames
#for d in finalroutes:
    #print(f"{d[0][0].stop_name} to {d[0][1].stop_name} on line {d[0][0].route_id} and {d[0][1].route_id} at {d[1]} colors: {d[2]}")


    




