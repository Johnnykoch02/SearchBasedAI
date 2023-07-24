''' Jonathan Koch U25318998
Program Implements Weighted Directed Graph and Performs Uninformed Search from node start to node end and returns the path.
'''
from heap_queue import HeapQueue
import math
import os

class Node:
    class Edge:
        '''Constructor'''
        def __init__(self, a, b, weight):
            self.start = a
            self.end = b
            self.weight = weight
            
        def match_id(self, other):
           return id(self) == id(other)
            
        def __lt__(self, other):
            return self.weight < other.weight
        def __gt__(self, other):
            return self.weight > other.weight
        def __eq__(self, other):
            return self.weight == other.weight        
        def __repr__(self):
            return self.__str__()
        def __str__(self):
            return f"From: {self.start} To: {self.end} Weight: {self.weight}"
        
    ''' Graph Nodes with Weighted Directed Edges '''
    def __init__(self, id):
        self.id = id
        self.edges = []
        
    def add_edge(self, node_to, weight):
        self.edges.append(Node.Edge(self, node_to, weight))
        
    def remove_edge(self, node_to: 'Node'):
        for edge in self.edges:
            if node_to == edge.end:
                self.edges.remove(edge)
                
    def __eq__(self, other):
       return id(self) == id(other)
    
    def __str__(self):
        return f"Node: {self.id}"
    def __repr__(self):
        return self.__str__()
class Path:
    def __init__(self, starting_edge):
        self.path = [starting_edge]
        self.weight = starting_edge.weight
        
    def visit(self, edge):
        self.path.append(edge)
        self.weight += edge.weight
        
    def current_edges(self):
        return self.path[-1].end.edges
    
    def is_in_path(self, edge):
        for _edge in self.path:
            if _edge.match_id(edge):
                return True
        return False
    
    @staticmethod
    def new_path(previous_path, new_edge):
        previous_path = previous_path.path
        new_path = Path(previous_path[0])
        for i in range(1, len(previous_path)):
            new_path.visit(previous_path[i])
        new_path.visit(new_edge)
        return new_path
    
    def __lt__(self, other):
            return self.weight < other.weight
    def __gt__(self, other):
            return self.weight > other.weight
    def __eq__(self, other):
            return self.weight == other.weight
    def __str__(self):
        return f"Path: {self.path}\nWeight: {self.weight}"    
    
    def found_path(self, node):
        return self.path[-1].end == node

class Graph:
    def __init__(self):
        self.nodes = []
        
    def get_node(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None
        
    def add_edge(self, node1, node2, weight:int):
        node1_ref = self.get_node(node1)
        node2_ref = self.get_node(node2)
        # Create new nodes if we dont have them already
        if node1_ref is None:
            node1_ref = Node(node1)
            self.nodes.append(node1_ref)
        if node2_ref is None:
            node2_ref = Node(node2)
            self.nodes.append(node2_ref)
            
        node1_ref.add_edge(node2_ref, weight)
    
    @staticmethod
    def graph_from_file(file_path: str):
        graph = Graph()
        if not os.path.exists(file_path):
            raise FileNotFoundError("The path specified does not exist, please check your inputed file location and ensure you are in the right directory.")
        with open(file_path, 'r') as f:
            for line in f:
                data = []
                for i in line.split(" "):
                    try:
                        i = int(i)
                        data.append(i)
                    except ValueError:
                        pass
                try:  
                    graph.add_edge(data[0], data[1], data[2])
                except:
                    print("Weird Data Provided:", data)
        return graph

    def find_shortest_path(self, start_node, end_node):
        starting_node = self.get_node(start_node)
        ending_node = self.get_node(end_node) 
        que = HeapQueue()
        
        if starting_node == None or ending_node == None:
            print("")
            return math.inf
        
        elif starting_node == ending_node:
            return "Path: []\nWeight: 0"
        
        for edge in starting_node.edges:
            que.push(Path(edge))
            
        while que.size() > 0:
            current_path = que.pop()
            if not current_path.found_path(ending_node):
                for edge in current_path.current_edges():
                    if not current_path.is_in_path(edge):
                        que.push(Path.new_path(current_path, edge))
            else:
                return current_path
        
        return math.inf

def main():                    
    graph = Graph.graph_from_file('graph_test_file.txt') # This Line Is editable

    while True:
        node_start = int(input("Enter Starting Node ID:\n"))
        node_end = int(input("Enter Ending Node ID:\n"))
        print(graph.find_shortest_path(node_start, node_end))

    
if __name__ == "__main__":
    main()