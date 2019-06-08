from collections import deque


class Vertex:
    UNEXPLORED = 'unexplored'
    EXPLORING = 'exploring'
    EXPLORED = 'explored'

    def __init__(self, key):
        self.name = key
        self.connected_to = {}

        self.distance = 0
        self.predecessor = None
        self.status = self.UNEXPLORED

    def add_neighbor(self, neighbor, weight=0):
        self.connected_to[neighbor] = weight

    def get_connections(self):
        return self.connected_to.keys()

    def get_weight(self, neighbor):
        return self.connected_to[neighbor]

    def __str__(self):
        return f'{self.name} connected to: {[node.name for node in self.connected_to]}'


class Graph:

    def __init__(self):
        self.nodes = {}
        self.num_nodes = 0

    def add_nodes(self, *keys):
        for key in keys:
            self.add_node(key)

    def add_node(self, key):
        self.num_nodes += 1
        node = Vertex(key)
        self.nodes[key] = node
        return node

    def get_node(self, key):
        return self.nodes[key]

    def add_edges_from_node(self, from_node, to_nodes, weight=0):
        for to_node in to_nodes:
            self.add_edge(from_node, to_node, weight)

    def add_edge(self, from_node, to_node, weight=0):
        if from_node == to_node:
            return

        from_node = self.get_node(from_node)
        to_node = self.get_node(to_node)
        from_node.add_neighbor(to_node, weight)

    def get_nodes(self):
        return self.nodes.keys()

    def breath_first_search(self, node):
        node = self.get_node(node)
        vertex_queue = deque()
        vertex_queue.append(node)

        while len(vertex_queue):
            current_vertex = vertex_queue.pop()
            for neighbor in current_vertex.get_connections():
                if neighbor.status == Vertex.UNEXPLORED:
                    neighbor.status = Vertex.EXPLORING
                    neighbor.distance = current_vertex.distance + 1
                    neighbor.predecessor = current_vertex
                    vertex_queue.append(neighbor)

            current_vertex.status = Vertex.EXPLORED

    def __iter__(self):
        return iter(self.nodes.values())

    def __contains__(self, key):
        return key in self.nodes

    def __str__(self):
        return ', '.join([str(node) for node in self.nodes.values()])
