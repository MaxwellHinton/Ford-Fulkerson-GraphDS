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

#Node class
#Contains an ID, a list of neighbours, a predecessor, and flags to identify if it has been visited
#or if it is a source/sink node.
class Node:
    def __init__(self, ID):
        self.ID = ID
        self.neighbours = [] #Neighbours store adjacent edges
        self.source = False
        self.sink = False
        self.visited = False
        self.predecessor = None

    def add_neighbour(self, neighbour):

        if self in self.neighbours:
            print("allready have that neighbour")
        else:
            self.neighbours.append(neighbour)

    def get_neighbours(self):
        return self.neighbours
    
    def get_edge(self, destination):
        for edge in self.neighbours:
            if edge.destination == destination:
                return edge

class Edge:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.capacity = 0
        self.flow = 0
        self.residual_capacity = 0

    def set_capacity(self, capacity):
        self.capacity = capacity
        
    def set_flow(edge, flow):
        edge.flow = flow
        
    def get_destination(self):
        return self.destination
    
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
        #Change to a function call to add a neighbour

        source.add_neighbour(edge)

    def get_edge(self, source, destination):
        for edge in self.edges:
            if edge.source.ID == source.ID and edge.destination.ID == destination.ID:
                return edge
        return None

    def get_source(self):
        for node in self.nodes:
            if node.source:
                return node
            
    def reset_nodes(self):
        for node in self.nodes:
            if node.visited:
                node.visited = False

    def get_sink(self):
        for node in self.nodes:
            if node.sink:
                return node
            

#Create functions

def create_nodes(graph, total_nodes):
    i = 0
    while i < total_nodes:
        node = Node(i)

        if i == 0:
            node.source = True
        elif i == total_nodes - 1:
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

def bfs(graph):
    queue = Queue()
    bottleneck_capacity = [0] * len(graph.nodes)

    source_node = graph.get_source()
    sink_node = graph.get_sink()

    queue.enqueue(source_node)
    source_node.visited = True
    bottleneck_capacity[source_node.ID] = float("inf") #Bottleneck is infinity because we can send any amount from the source
    
    while not queue.isEmpty():
        current_node = queue.dequeue()
        print("")
        #For each un-visited neighbour, we enqueue, mark it as visited, and keep track of its predecessor
        for edge in current_node.neighbours:
            destination = edge.get_destination()
            print(f"Current node: {current_node.ID}, is about to visit {destination.ID}, with capacity: {edge.capacity}")
            
            if not destination.visited and edge.capacity > 0:
                queue.enqueue(destination)
                destination.visited = True
                destination.predecessor = current_node
            
                #New bottleneck is either equal to the current node's bottleneck capcity or the edges.
                bottleneck_capacity[destination.ID] = min(bottleneck_capacity[current_node.ID], edge.capacity)

                if destination.sink:
                    #Reset visited nodes
                    graph.reset_nodes()
                    return sink_node, bottleneck_capacity[sink_node.ID]
    
    graph.reset_nodes()

    return None, 0

        

#Build residual network.
def create_residual(graph):
    residual_graph = Graph()

    for node in graph.nodes:
        new_node = Node(node.ID)

        if node.source:
            new_node.source = True
        elif node.sink:
            new_node.sink = True
    
        residual_graph.add_node(new_node)

    for node in graph.nodes:
        for edge in node.neighbours:
            forward_edge_capacity = edge.capacity - edge.flow
            backward_edge_capacity = edge.flow

            source_node = next(n for n in residual_graph.nodes if n.ID == edge.source.ID)
            destination_node = next(n for n in residual_graph.nodes if n.ID == edge.destination.ID)

            residual_graph.add_edge(source_node, destination_node, capacity = forward_edge_capacity)
            residual_graph.add_edge(destination_node, source_node, capacity = backward_edge_capacity)

    return residual_graph

#Ford-Fulkerson Algorithm. 

def fordFulkerson(graph):

    #Create residual graph
    max_flow = 0
    iteration = 0

    #Enter a loop that will continute until no source is returned from BFS, indicating there are no augmenting paths
    while True:
        
        residual_graph = create_residual(graph)
        iteration += 1
        #BFS returns a source and bottleneck value if there is a path.
        sink, bottleneck = bfs(residual_graph)

        if sink is None:
            break
        
        max_flow += bottleneck

        current_node = sink

        #BFS returns the sink node, the sink node has predecessors which allow us to traverse 
        #backwards through the path.
        while current_node.ID != graph.get_source().ID:
            predecessor = current_node.predecessor

            original_edge = graph.get_edge(predecessor, current_node)
            if original_edge is not None:  # If the edge exists in the original graph, update flow
                original_edge.flow += bottleneck

            current_node = predecessor

    return max_flow, iteration

#main body

graph = Graph()
create_nodes(graph, 6)

graph.add_edge(graph.nodes[0], graph.nodes[1], capacity = 8)
graph.add_edge(graph.nodes[0], graph.nodes[4], capacity = 3)

graph.add_edge(graph.nodes[1], graph.nodes[2], capacity = 9)

graph.add_edge(graph.nodes[2], graph.nodes[5], capacity = 2)

graph.add_edge(graph.nodes[3], graph.nodes[5], capacity = 5)

graph.add_edge(graph.nodes[4], graph.nodes[2], capacity = 7)
graph.add_edge(graph.nodes[4], graph.nodes[3], capacity = 4)

max_flow, iterations = fordFulkerson(graph)

print(max_flow)
print(iterations)

#To-Do:

#Implement the Ford-fulkerson Algorithm, ensure it works on at least 3 different graphs.
#Implement proper testing methods.
#Change graph generation to be automated and random.
#Test.
#Create a graphical representation of the graph, and residual graph.
#'Animate' the Ford-fulkerson steps.
#Learn JavaScript with React framework to create a ford-fulkerson explanation website.

#Next commit - create residual function done, Ford-Fulkerson implemented    