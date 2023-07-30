import random


class Node:
    def __init__(self, ID):
        self.ID = ID
        self.neighbours = [] #Neighbours store adjacent edges
        self.source = False
        self.sink = False

class Edge:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.capacity = 0
        self.flow = 0

    def set_capacity(edge, capacity):
        edge.capacity = capacity
        
    def set_flow(edge, flow):
        edge.flow = flow
        
class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, source, destination, capacity):
        edge = Edge(source, destination)
        edge.set_capacity(capacity)
        self.edges.append(edge)
        source.neighbours.append(edge)


#Printing graph information
def  print_graph(graph):

    for node in graph.nodes:
        print("Node " + str(node.ID) + 
              (" (source node)" if node.source else " (sink node)" if node.sink else "") + " has neighbours: ")

        for edge in node.neighbours:
            print(f"\t{edge.destination.ID} with capacity {edge.capacity}")

        print("")

def create_nodes(graph, total_nodes):
    i = 1
    while i <= total_nodes:
        node = Node(i)

        if i == 1:
            node.source = True
        elif i == total_nodes:
            node.sink = True

        graph.add_node(node)
        i = i + 1

def create_edges(graph):
    graph.add_edge(graph.nodes[0], graph.nodes[1], capacity = 4)
    graph.add_edge(graph.nodes[0], graph.nodes[2], capacity = 2)

    graph.add_edge(graph.nodes[1], graph.nodes[2], capacity = 2)
    graph.add_edge(graph.nodes[1], graph.nodes[3], capacity = 2)

    graph.add_edge(graph.nodes[2], graph.nodes[3], capacity = 1)
    graph.add_edge(graph.nodes[2], graph.nodes[4], capacity = 3)

    graph.add_edge(graph.nodes[3], graph.nodes[4], capacity = 3)


#main body
graph = Graph()

create_nodes(graph, 5)
create_edges(graph)

print_graph(graph)