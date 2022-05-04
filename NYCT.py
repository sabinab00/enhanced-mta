import googleAPI
import pandas as pd
import helper

#TODO: figure out mmultimodal transport i.e. how to connect bus and subways with existing data

subways = pd.read_csv(r'datasets\subways.csv', index_col=False)
subways_transfers = pd.read_csv(r'datasets\subway-transfers.csv', index_col=False)
bus = pd.read_csv(r'datasets\bus.csv', index_col=False)

class Node:
    def __init__(self, stop_id, stop_name, stop_sequence, route_id, transit_type,stop_lat, stop_lon, accessibility, notes,precinct,parent=None, child=None):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_sequence = stop_sequence
        
        self.route_id = route_id
        self.transit_type = transit_type
        # self.transfers = []

        self.geocode = [stop_lat, stop_lon]
        self.accessibility = accessibility
        self.accessibility_notes = notes
        self.precinct = precinct
        
        
        self.parent = parent
        self.child = child

    def __lt__(self, other):
        return self.stop_sequence < other.stop_sequence
    
    def __eq__(self, other):
        # two nodes might have the same name and stop id with
        # different route_id
        # if two nodes are equal you can also transfer between them

        return (self.stop_id==other.stop_id) & (self.stop_name==other.stop_name)

    def setStopSeq(self, new_sequence):
        self.stop_sequence = new_sequence

#######################################################################################

class Graph:
    def __init__(self):
        self.transfers = {}
        self.all_stopIDs = {}
        self.routes = {}

    def generateStops(self,mode,dir:int):   # generate stop as Node class based on its stopID
        m = bus if mode=='bus' else subways
        for i in range(len(m)):
            line = m.iloc[i]
            _stop_seq = line['stop_sequence']
            _route_id = line['route_id']
            _stop_name = line['stop_name']
            _stop_lat = line['stop_lat']
            _stop_lon = line['stop_lon']
            _stop_id = line['stop_id']
            _precinct = line['precinct']
            if mode=='bus':
                _accessibility = 1
                _notes = ""
            else:
                _accessibility = line['ADA'] 
                _notes = line['ADA Notes']
            if line['direction_id'] == dir: 
                stop =  Node(_stop_id, _stop_name, _stop_seq, _route_id, 
                            mode,_stop_lat, _stop_lon,
                            _accessibility, _notes,_precinct)
                                       
                helper.addDictaddDict(_stop_id,stop, self.all_stopIDs)
                  

    def generateRoutes(self,mode,dir:int):
        # {line: node_stop_1, node_stop_2,...} where stops are ordered by stop_sequences
        m = bus if mode=='bus' else subways
        routes ={}
        for i in range(len(m)):
            line = m.iloc[i]
            route_id = line['route_id']
            stop_id = line['stop_id']
            if line['direction_id'] == dir: 
                for stop in self.all_stopIDs[stop_id]:
                    if stop.route_id == route_id:
                        helper.addDict(route_id,stop, routes)
        self.routes = helper.sort_sequence_id(routes)

    def connectStops(self):
        for route_id, stations in self.routes.items():
            for i in range(len(stations)):
                for i in range(len(stations)):
                    curr_node = stations[i]
                    # print(curr_node.stop_name, sequence)
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
        sub = subways_transfers
        for i in range(len(sub)):
            entry = sub.iloc[i]
            from_stop = entry[0]
            to_stop = entry[1]
            if (from_stop in self.all_stopIDs.keys()) and (to_stop in self.all_stopIDs.keys()):
                helper.addDict(self.all_stopIDs[from_stop][0][0], self.all_stopIDs[to_stop][0][0],self.transfers)
    
    def generateStopNames(self):
        self.all_stopNames = {}
        for i in self.all_stopIDs:
            stop = self.all_stopIDs[i][0][0]
            helper.addDict(stop.stop_name, stop,self.all_stopNames)

    def findStop(self, stop_name):
        return self.all_stopNames[stop_name]