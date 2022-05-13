import NYCT
import API_functions as ap
from scipy.spatial import distance

#takes in two lists: [float latitude, float longitude]
#returns the distance between the two points
def euclidean(origin,destination):
    return distance.euclidean(tuple(origin),tuple(destination))

#takes in (graph node,str origin address,str destination address,float radius of search)
#returns a list of tuples (origin stop, destination stop)
    #ordered by (transfers, distance)
def busroutes(API_key,g,origin,destination,rad=0.0001):

    #get geo_code of origin and destination
    loc=ap.get_geocode(API_key,origin)
    loc2=ap.get_geocode(API_key,destination)
    
    #finds nearby origin stops
    originpts=[]
    for x in g.stopIDs:
        node=g.getStop(x)
        new=(node,euclidean(loc,node.geocode))
        if new not in originpts and node.transit_type=="bus":
            originpts.append(new)

    #finds nearby destination stops
    destpts=[]
    for x in g.stopIDs:
        node=g.getStop(x)
        new=(node,euclidean(loc2,node.geocode))
        if new not in destpts and node.transit_type=="bus":
            destpts.append(new)

    #shortens origin and destination list based on radius
    originpts=[x for x in originpts if x[1]<=rad]
    destpts=[x for x in destpts if x[1]<=rad]
    
    #separates stops into same and different group combinations
    #((origin stop, destination stop), sum of distances)
    sameroutes=[]
    diffroutes=[]
    visited=set()
    for o in originpts:
        for d in destpts:
            new=((o[0],d[0]),o[1]+d[1])
            if o[0].route_id==d[0].route_id:
                if new not in sameroutes:
                    sameroutes.append(new)
                    visited.add((o[0].stop_name,d[0].stop_name))
            else:
                if new not in diffroutes and (o[0].stop_name,d[0].stop_name) not in visited:
                    diffroutes.append(new)
                    visited.add((o[0].stop_name,d[0].stop_name))

    #sorts lists based on distance            
    sameroutes.sort(key=lambda x:(x[1]))
    diffroutes.sort(key=lambda x:(x[1]))

    #same routes come first, then different routes
    #returns a list of tuples (origin stop, destination stop)
    finalroutes=[]
    for s in sameroutes:
        finalroutes.append(s[0])
    for d in diffroutes:
        finalroutes.append(d[0])

    if finalroutes==[]:
        print("No results found.  Please try a larger radius or take a car.")
    return finalroutes


##initializing graph
#g = NYCT.Graph()
#g.generateTransfers()
#g.generateStops('bus',0)
#g.generateStopNames()
#g.generateRoutes('bus',0)
#g.mapStopTransfers()
#g.connectStops()

##uploading key
#f=open("key.txt")
#API_key=f.read()
#f.close()

##origin point and destination point
#start="4 South St Space 2, New York, NY 10004"
#end="85 Greenwich St, New York, NY 10006"

##calls function
#finalroutes=busroutes(API_key,g,start,end,0.002)

##prints notes
#for d in finalroutes:
    #print(f"{d[0].stop_name} to {d[1].stop_name}")

