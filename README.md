# CSC 74011 Artficial Intelligence: Enhanced MTA
The goal of this project is to create an Enhanced MTA trip planner that can take in both safety and accessibility when planning a transit route.  This project takes into account bus and subway routes in Manhattan.  The safety measure is developed by using NYPD crime statistics data based on number of complaints filed based on precinct and geocode.  The MTA trips are developed from static data of the MTA bus and subway lines based on a weekday evening route.

This file does require a google API key.  Our algorithm is formatted such that the google API key will be in a file key.txt that will be read from.

Dataset folder contains original data as well as preprocessed data used in the algorithm:
  - google_transit_bus_manhattan: contains unprocessed MTA bus data for Manhattan
  - google_transit_subway: contains unprocessed MTA subway data for Manhattan
  - bus.csv: first iteration of preprocessed bus data
  - bus2sub.txt: accounts for all transfers between buses to subways
  - subways.csv: first iteration of preprocessed subway data
  - bus_oneD.csv: changed bus data to one direction, instead of two
  - bus_transfers_oneD.txt: accounts for all possible bus transfers
  - sub2bus.txt: accounts for all transfers from subways to buses
  - subway-transfers.csv: accounts for transfers between subways (first iteration)
  - subways_idx4.csv: formatted subway data like bus data (iteration 2 of subways.csv)
  - subways_oneD.csv:  formatted subway data to one direction (iteration 3 of subways.csv)
  -transfers_idx4.txt: subway transfers matched to bus data (iteration 2 of subway-transfers.csv)
  - transfers_oneD.txt: subway transfers in one direction (iteration 3 of subway-transfers.csv)
  - NYPD dataset.csv: hold crime statistics dataset by geocode, precinct and number of complaints

The datasets used in the final algorithm are:
 - Bus2sub.txt
 - bus_oneD.csv
 - bus_transfers_oneD.txt
 - Sub2bus.txt
 - subways_oneD.csv
 - Transfers_idx4.txt
 - NYPD dataset.csv

API functions.py (uses googlemaps API to augment our algorithm) :
  - Get_geocode: takes in a string address and returns a list of the latitude and longitude of the location
  - Get_nearby_stops: takes in a list of latitude and longitude and a radius and returns transit stops in that radius.  List of dictionaries:   {“stop_name”: [{str transit_type: [latitude, longitude]}]
  - Get_directions: takes in an origin and destination and returns the Google API directions for that stop,
    separated in a dictionary by sequences as a key for walking directions, and a starting stop and ending stop
  - Get_distance: takes in two locations, and returns the distance between two places in terms of transit distance

Crime Seach Heuristic.py:
  - Uses crime statistics data and performs k-means clustering, returns the center of three clusters and a radius representing a “danger zone” around the clusters
 
NYCT.py:
  - Develops the search space for MTA using two classes:
  - Graph using our data is initialized by g.Graph()
  - Node:
      - Stop_id: Every stop has a unique stop ID code
      - Stop_name: Name of the stop
      - Geocode: Latitude and Longitude of stop
      - Route_id: The line the stop is at
      - Transit_type: Indicates if it is a “bus” or “subway” stop
      - Express: Indicates if the stop is ona local or express line
      - Heuristic_score: based on crime statistics
  - Graph:
  - This class serves as an overall directory for the NYCT system of all the stops, permissible transfers and all routes the users can access.

Findendpoints.py:
  - Takes in accessibility request (“y” or “n”), transportation mode request, origin address, destination address, graph object, radius or search and returns a list of tuples of two nodes (origin stop, destination stop) that are sorted by transfers and distance
  - Relies on user requests (accessibility, transportation mode, radius) in order to limit the list of tuples
  - These are the possible stops from two addresses that the search algorithm traverses

Helper.py (contains some functions to add in search algorithm):
  - addDict: takes in a key, value and empty dictionary and returns the {key:value}
  - getSequence: gets a stop_sequence element of a node
  - sort: sorts routes by sequence
  - findTopPath: finds top three paths of search, sorted by 3 criteria

Heurstics.py (contains heuristics.py for the search):
  - distance: takes geocode of origin and destination and calls the gmap API for the distance between two points
  - transit_mode_check: checks if the current and destination stop are for the same transit type
  - euclidean_distance: checks euclidean distance of the two stops given two geocodees
  - route_check: checks the following between the current stop and destination stop: same route_id, if the neighboring stops that are reachable from current stop has the same route_id as well
  - express_check: checks if the route taken at the current stop is express or not
  - transfer_check: penalizes transfers route and modal transfers
  - crime_check: checks if location is safe given geocode of stop
  - crime_distance: looks to see if the current stop is in a given radius from the center of a crime cluster.  If it is in a danger zone it returns the distance to safety, if it is safe, it returns 0
 
Search.py:
  - A* search of graph described in NYCT.py using Heuristics.py functions as heuristics of the function
 
Path.py:
  - Helps return the path of the optimal route returned by search.py

Google Evaluation Test Sets and Functions:
  - Googletest.txt: holds the google test sets with each line formatted as:
starting_address |ending_address|start_station, end_station, stops_travelled|...|accessibility=[y,n]
  - Googletest.py: a function that reads in googletest.txt and returns the crime heuristics, transfers, transfer_modes and path for each route in googletest.txt to a googletest-output.txt file
  - Googletest-output.txt: results of heuristic 1 being used
  - Googletest-output-newh.txt: results of heuristic 2 being used
  - Googletest-output-newh2.txt: results of heuristic 3 being used

Enhanced MTA Test Sets and Functions:
  - Tests.txt: Contains starting and ending addresses to test main.py
  - Test.py: reads in test.txt and returns the crime heuristics, transfers, transfer_modes and path for each route in tests.txt to a test-output.txt file
  - Test-output.txt: results for heuristic 1 being used
  - Test-output-newh.txt: results for heuristic 2 being used

Main.py (runs the search):
  - Uses terminal input to find starting and ending addresses, accessibility request and mode of transportation request
  - Performs A* search and returns a path of the optimal route based on user request and safety measure




