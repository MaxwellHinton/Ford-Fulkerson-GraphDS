import random


class Queue:
    def __init__(self):
        self.elements = []

    #Adds an element to the rear of the queue
    def enqueue(self, element):
        self.elements.append(element)

    #Removes element at the front of the queue
    def dequeue(self):
        if not self.isEmpty():
            return self.elements.pop(0)
        else:
            print("Your queue is empty.") #Raise an exception
    
    #Returns element at the front of the queue
    def first(self):
        if not self.isEmpty():
            return self.elements[0]
        else:
            print("Your queue is empty.") #Raise an exception

    #Returns if the queue is empty or not
    def isEmpty(self):
        return len(self.elements) == 0

    def size(self):
        return len(self.elements)

class Node:
    def __init__(self, ID):
        self.ID = ID
        self.neighbours = [] #Neighbours store adjacent edges
        self.source = False
        self.sink = False
        self.visited = False

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

    def get_source(self):
        for node in self.nodes:
            if node.source:
                return node

#Create functions
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

#Printing functions
def  print_graph(graph):
    for node in graph.nodes:
        print("Node " + str(node.ID) + 
              (" (source node)" if node.source else " (sink node)" if node.sink else "") + " has neighbours: ")

        for edge in node.neighbours:
            print(f"\t{edge.destination.ID} with capacity {edge.capacity} and flow {edge.flow}")

        print("")

def print_queue(queue):
    if not queue.isEmpty():
        for i in range(0, queue.size()):
            node_id = queue.elements[i].ID
            print("Node ", node_id)
    else:
        print("Queue empty")

#Breadth-first-search

def bfs(graph, source):
    empty_queue = Queue()
    source_node = source

    empty_queue.enqueue(source_node)
    source_node.visited = True
    
    while not empty_queue.isEmpty():
        current_node = empty_queue.dequeue()
        print("Visited Node: ", current_node.ID)

        for edge in current_node.neighbours:
            #Get the neighbours (edges) of the current node. Each edge has a destination which
            #is the next node to be traversed to.
            next_node = edge.destination

            if not next_node.visited:
                empty_queue.enqueue(next_node)
                next_node.visited = True

        

#main body
graph = Graph()

create_nodes(graph, 5)
create_edges(graph)

bfs(graph, graph.get_source())

for node in graph.nodes:
    if node.visited:
        print(f"Node {node.ID} has been visited.")
    else:
        print(f"Node {node.ID} has not been visited.")
