from NYCT import Graph, Node
from queue import PriorityQueue
import API_functions
from search import ast


if __name__=='__main__':
    g = Graph('subway')
    origin = g.getStop('274')
    destination = b = g.getStop('200')
    ast(origin, destination)