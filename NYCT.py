import pandas as pd
from copy import deepcopy
import helper 

class Node:
    def __init__(self, stop_id, stop_name, stop_sequence, route_id, transit_type,express,transfers,stop_lat, stop_lon, accessibility, notes=None,precinct=None,parent=None, child=None):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_sequence = stop_sequence
        
        self.route_id = route_id
        self.transit_type = transit_type
        self.express = express
        self.transfers =transfers
        self.transfers_id = deepcopy(transfers)

        self.geocode = (stop_lat, stop_lon)
        self.accessibility = accessibility
        self.accessibility_notes = notes
        self.precinct = precinct
        
        self.parent = parent
        self.child = child

        self.heuristic_score = None

    def setHeuristicScore(self, value):
        self.heuristic_score = value

    def isSame(self, other):      
        # two stops are the same if they have the same transfers or you can transfer bewteen them
        same_trans = False
        
        if self.stop_id == other.stop_id:
            same_trans = True
        if self.transfers and other.transfers:
            if (self.stop_id in other.transfers_id) and (other.stop_id in self.transfers_id):
                this_transfers = deepcopy(self.transfers_id)
                other_transfers = deepcopy(other.transfers_id)
                
                if (this_transfers == other_transfers) or (this_transfers.remove(other.stop_id) == other_transfers.remove(self.stop_id)):
                    same_trans = True
                    
            
        return same_trans

    def getPath(self,origin):
        # need to consider different routes
        node, hist = self, []
        same = False
        while node:
            if same:
                break
            same = node.isSame(origin)
            # print(node.stop_id, origin.stop_id)
            hist.append(node)
            node = node.parent
            
        hist.reverse()
        solution = [node.stop_name for node in hist]
        return solution

    def __lt__(self, other):
        # priority queue comparison
        # compares the heuristic between the two stops
        return self.heuristic_score < other.heuristic_score

    def __repr__(self):
        if not self.child:
            child = 'NA'
            child_id = 'NA'
        else: 
            child = self.child.stop_name
            child_id = self.child.stop_id
        if not self.parent:
            par = 'NA'
            par_id = 'NA'
        else:
            par = self.parent.stop_name
            par_id = self.parent.stop_id
        exp = 'LOCAL'
        if self.express==1:
            exp= 'EXPRESS'
        # return f'StopID: {self.stop_id}-{self.stop_name} \nRoute: {self.route_id} Seq:{self.stop_sequence} Transfers: {transfers} \nPrev: {par} \t Next: {child} \nOther: {self.accessibility}, {self.precinct}  \n\n'
        return f'StopID: {self.stop_id}-{self.stop_name} \nRoute: {self.route_id} {exp} Seq:{self.stop_sequence} Transfers: {self.transfers_id} \nPrev: {par}-{par_id} \t Next: {child}-{child_id} \nOther: {self.accessibility}, {self.precinct}  \n\n'

    

    def setStopSeq(self, new_sequence):
        self.stop_sequence = new_sequence


   
####################################################
subways = pd.read_csv(r'datasets\subways_oneD.csv', index_col=False)
bus = pd.read_csv(r'datasets\bus.csv', index_col=False)
subways_transfers = r'datasets\transfers_oneD.txt'

class Graph:
    def __init__(self):
        self.transfers = {}
        self.stopIDs = {}
        self.uptown = {}
        self.downtown = {}
        self.routes = {}

        self.generateTransfers()
        self.generateStops('subway',0)
        self.generateStopNames()
        self.generateRoutes('subway',0)
        self.mapStopTransfers()
        self.connectStops() 



    def generateStops(self,mode,dir:int):   # generate stop as Node class based on its stopID
        m = bus if mode=='bus' else subways
        for i in range(len(m)):
            line = m.iloc[i]
            _stop_seq = line['stop_sequence']
            _route_id = line['route_id']
            _stop_name = line['stop_name']
            _stop_lat = line['stop_lat']
            _stop_lon = line['stop_lon']
            _stop_id = str(line['stop_id'])
            _precinct = line['precinct']
            _express = line['express']
            if mode=='bus':
                _accessibility = 1
                _notes = ""
            else:
                _accessibility = line['ADA'] 
                _notes = line['ADA Notes']
            if line['direction_id'] == dir: 
                if str(_stop_id) in self.transfers.keys():
                    transfers = self.transfers[str(_stop_id)]
                else: 
                    transfers=None
                stop =  Node(_stop_id, _stop_name, _stop_seq, _route_id, 
                            mode,_express,transfers,
                            _stop_lat, _stop_lon,
                            _accessibility, _notes,_precinct)

                self.stopIDs[_stop_id] = stop                     
                  

    def generateRoutes(self,mode,dir:int):
        m = bus if mode=='bus' else subways
        routes ={}
        for i in range(len(m)):
            line = m.iloc[i]
            route_id = line['route_id']
            stop_id = str(line['stop_id'])
            if line['direction_id'] == dir: 
                if self.stopIDs[stop_id].route_id == route_id:
                    helper.addDict(route_id, self.stopIDs[stop_id], routes)     
        self.routes = helper.sort(routes)

    def connectStops(self):
        for route_id, stations in self.routes.items():
            for i in range(len(stations)):
                curr_node = stations[i]
                if curr_node.stop_sequence == 0:
                    curr_node.parent = None
                    curr_node.child = stations[i+1]
                elif curr_node.stop_sequence == len(stations)-1:
                    curr_node.parent = stations[i-1]
                    curr_node.child = None
                else:
                    curr_node.parent = stations[i-1]
                    curr_node.child = stations[i+1]
    
    def generateTransfers(self):
        # for subways only... right now
        with open(subways_transfers) as file:
            for line in file:
                key= line.rstrip().split(',')
                if len(key) != 1:
                    self.transfers[key[0]] = key[1:]
        

    def mapStopTransfers(self):
        for id, node in self.stopIDs.items():
            if id in self.transfers.keys():
                transfers = self.transfers[id]
                for i in range(len(transfers)):
                    if transfers[i] in self.stopIDs.keys():
                        t = self.stopIDs[transfers[i]]
                        node.transfers[i] = t

    def generateStopNames(self):
        self.stopNames = {}
        for id, stop in self.stopIDs.items():
            helper.addDict(stop.stop_name, stop,self.stopNames)

    def getStop(self, stop):
        try:
            return self.stopNames[stop]
        except:
            return self.stopIDs[stop]

