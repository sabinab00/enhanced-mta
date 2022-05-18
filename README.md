
<h2 align="center">CSC 74011 Artficial Intelligence: Enhanced MTA</h2>

---


<p align="center"> An Enhanced MTA Trip planner that is designed to account for safety and accessibility in route planning using <b>A* Search</b> algorithm.
    <br> 
</p>


## About

The goal of this project is to create an Enhanced MTA trip planner that can take in both safety and accessibility when planning a transit route. This project takes into account bus and subway routes in Manhattan. The safety measure is developed by using NYPD crime statistics data based on number of complaints filed based on precinct and geocode. The MTA trips are developed from static data of the MTA bus and subway lines based on a weekday evening route.

Read more about our project in our [paper](https://docs.google.com/document/d/1hdGBwT2sm_XIu9Vw7hmSs0OPkikCepEzhM6jq3rnzEs/edit). 


##  Getting Started 

### Prerequisites

To use the GoogleAPI, an API key (`key.txt`) is required in the main directory - this will be directly submitted as a part of the project's deliverables.

Required packages to run this file: `googlemaps`, `sklearn`, `scipy`, `kneed`, `pandas`


## Search Space and Algorithm Design 

### Search Space
The search space is initialized in `NYCT.Graph()` it works by creating nodes from `NYCT.Node()`. Each node represents a stop in the transit system and has attributes such as stop_id, stop_name, geo_code,transit_type to distinguish them from one another, nodes are connected to one another by their route_id, transfers, child, and parent. Other additional attributes such as express, accessibility, line, crime_heuristics are used in [heurstics](#heuristics) calculation.

### A* Search

The search for path between two nodes is performed in `search.py`. The two nodes are obtained by using the `googlemap` API and the output is generated and sorted in `findendpoints.py` details are listed [here](#find-end-points).

We modify small parts of A* search. Instead of making the first in the Priority Queue the next Node in the path, we ensure that it is a node that is reachable from the previous node. The heuristics for our search is listed in the [heuristics](#heuristics) section.

### Heuristics
Our algorithm uses A*-algorithm to find paths between two points using the following heuristics  in `heuristics.py `:
- `distance`: takes geocode of origin and destination and calls the gmap API for the distance between two points
- `transit_mode_check`: checks if the current and destination stop are for the same transit type
- `euclidean_distance`: checks euclidean distance of the two stops given two geocodees
- `route_check`: checks the following between the current stop and destination stop: same route_id, if the neighboring stops that are reachable from current stop has the same route_id as well
- `express_check`: checks if the route taken at the current stop is express or not
- `transfer_check`: penalizes transfers route and modal transfers
- `crime_check`: checks if location is safe given geocode of stop
- `crime_distance`: looks to see if the current stop is in a given radius from the center of a crime cluster. If it is in a danger zone it returns the distance to safety, if it is safe, it returns 0


## Running the program 

You can run the program with the script  `$ py main.py`. Then the program will ask you for the starting and ending destinations for the path as well as if you wish to have an accessible path and if you have a preferred method of transportation (bus, subway, or both). Here is an example of a user going from Hunter College to CUNY Graduate Center requesting an accessible route with no preference for transit mode.
```
What is your starting address?
>>>695 Park Ave New York, NY, 10065

What is your ending address? 
>>>365 5th Ave New York, NY 10016

Would you like to request an accessible route (Y/N)? 
>>>Y
Do you have a preferred mode of transportion? 

Enter "bus", "subway", or "both".
>>>both
```
Our search will return the top result:
```
StopID: B281-MADISON AV/E 69 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 67 ST-B282    Next: MADISON AV/E 72 ST-B283
Transfers: ['B258', 'B296', 'B311', 'B366']
Other: 1, 19.0

StopID: B282-MADISON AV/E 67 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 66 ST-B289    Next: MADISON AV/E 69 ST-B281
Transfers: ['B297', 'B312', 'B367']
Other: 1, 19.0

StopID: B289-MADISON AV/E 66 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 63 ST-B288    Next: MADISON AV/E 67 ST-B282
Transfers: ['B303', 'B319', 'B374']
Other: 1, 19.0

StopID: B288-MADISON AV/E 63 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 60  ST-B287   Next: MADISON AV/E 66 ST-B289
Transfers: ['B318', 'B373']
Other: 1, 19.0

StopID: B287-MADISON AV/E 60  ST M2-M2-bus LOCAL
Prev: MADISON AV/E 57 ST-B115    Next: MADISON AV/E 63 ST-B288
Transfers: ['B302', 'B317', 'B372']
Other: 1, 19.0

StopID: B115-MADISON AV/E 57 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 55  ST-B118   Next: MADISON AV/E 60  ST-B287
Transfers: ['B120', 'B125', 'B147']
Other: 1, 18.0

StopID: B118-MADISON AV/E 55  ST M2-M2-bus LOCAL
Prev: MADISON AV/E 52 ST-B117    Next: MADISON AV/E 57 ST-B115
Transfers: ['B123', 'B128', 'B150']
Other: 1, 18.0

StopID: B117-MADISON AV/E 52 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 49 ST-B114    Next: MADISON AV/E 55  ST-B118
Transfers: ['B122', 'B127', 'B149']
Other: 1, 18.0

StopID: B114-MADISON AV/E 49 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 45 ST-B116    Next: MADISON AV/E 52 ST-B117
Transfers: ['B119', 'B124', 'B146']
Other: 1, 18.0

StopID: B116-MADISON AV/E 45 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 42 ST-B518    Next: MADISON AV/E 49 ST-B114
Transfers: ['B121', 'B126', 'B148']
Other: 1, 18.0

StopID: B518-MADISON AV/E 42 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 40  ST-B520   Next: MADISON AV/E 45 ST-B116
Transfers: ['B521', 'B524', 'B546', 'S105']
Other: 1, 14.0

StopID: B520-MADISON AV/E 40  ST M2-M2-bus LOCAL
Prev: MADISON AV/E 37 ST-B188    Next: MADISON AV/E 42 ST-B518
Transfers: ['B523', 'B526', 'B547', 'S105']
Other: 1, 14.0

StopID: B188-MADISON AV/E 37 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 34 ST-B187    Next: MADISON AV/E 40  ST-B520
Transfers: ['B190', 'B192', 'B208']
Other: 1, 17.0

StopID: B187-MADISON AV/E 34 ST M2-M2-bus LOCAL
Prev: MADISON AV/E 30 ST-B519    Next: MADISON AV/E 37 ST-B188
Transfers: ['B189', 'B191', 'B207']
Other: 1, 17.0
```

## Authors <a name = "authors"></a>

- [@Nancy Sea](https://github.com/socheatos) - transit data preprocessing, formulating search space, writing A* search, heuristics design, test and evaluation
- [@Michelle Cherian](https://github.com/michellecherian95) - incorporated Google API, finding optimal starting/ending routes, writing A* search, test and evaluation
- [@Sabina Bhuiyan](https://github.com/sabinab00) - crime statistics preprocessing, designed safety measure by applying k-means cluster, visualizations


