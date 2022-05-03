from turtle import down
import googleAPI
import pandas as pd
import helper

subways = pd.read_csv(r'datasets\subways.csv', index_col=False)
subways_transfers = pd.read_csv(r'datasets\subway-transfers.csv', index_col=False)
bus = pd.read_csv(r'datasets\bus.csv', index_col=False)

class Node:
    def __init__(self, stop_name, route_id,stop_lat, stop_lon, stop_id, accessibility, notes,precinct,transit_type,parent=None, child=None):
        self.stop_name = stop_name
        self.stop_id = stop_id
        self.route_id = route_id
        self.geocode = [stop_lat, stop_lon]
        self.accessibility = accessibility
        self.accessibility_notes = notes
        self.precinct = precinct
        self.transit_type = transit_type
        
        self.parent = parent
        self.child = child
        self.transfers = []

#######################################################################################

class Graph:
    def __init__(self):
        self.transfers = {}
        self.all_stops = {}
        self.uptown = {}
        self.downtown = {}
        self.routes={}

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
                stop =  Node(_route_id,_stop_name,
                            _stop_lat, _stop_lon,_stop_id,
                            _accessibility, _notes,
                            _precinct, mode)            
                helper.addDict(_stop_id,(stop,_stop_seq), self.all_stops)   
        return self.all_stops

    def generateRoutes(self,mode,dir:int):
        # {line: node_stop_1, node_stop_2,...} where stops are ordered by stop_sequences
        m = bus if mode=='bus' else subways
        routes ={}
        for i in range(len(m)):
            line = m.iloc[i]
            route_id = line['route_id']
            stop_id = line['stop_id']
            if line['direction_id'] == dir: 
                helper.addDict(route_id,self.all_stops[stop_id][0], routes)
        self.routes = helper.sort(routes)

    def connectStops(self):
        for route_id, stations in self.routes.items():
            for i in range(len(stations)):
                curr_node, sequence = stations[i]
                if sequence == 0:
                    curr_node.parent = None
                    curr_node.child = stations[i+1][0]
                elif sequence == len(stations)-1:
                    curr_node.parent = stations[i-1][0]
                    curr_node.child = None
                else:
                    curr_node.parent = stations[i-1][0]
                    curr_node.child = stations[i+1][0]
                # addDict(route_id, curr_node, route)       

    def generateTransfers(self):
        sub = subways_transfers
        for i in range(len(sub)):
            entry = sub.iloc[i]
            from_stop = entry[0]
            to_stop = entry[1]
            if (from_stop in self.all_stops.keys()) and (to_stop in self.all_stops.keys()):
                helper.addDict(self.all_stops[from_stop][0][0], self.all_stops[to_stop][0][0],self.transfers)



            