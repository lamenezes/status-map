from collections import deque


class Vertex:
    UNEXPLORED = 'unexplored'
    EXPLORING = 'exploring'
    EXPLORED = 'explored'

    def __init__(self, key):
        self.name = key
        self.connected_to = {}

        self.distance = 0
        self.status = self.UNEXPLORED

    def add_neighbor(self, neighbor, weight=0):
        self.connected_to[neighbor] = weight

    def get_connections(self):
        return self.connected_to.keys()

    def _reset(self):
        self.distance = 0
        self.status = self.UNEXPLORED

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Vertex({self.name})'


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

    def _bfs(self, node):
        node = self.get_node(node)
        vertex_queue = deque()
        vertex_queue.append(node)

        while len(vertex_queue):
            current_vertex = vertex_queue.pop()
            for neighbor in current_vertex.get_connections():
                if neighbor.status == Vertex.UNEXPLORED:
                    neighbor.status = Vertex.EXPLORING
                    neighbor.distance = current_vertex.distance + 1
                    vertex_queue.append(neighbor)

            current_vertex.status = Vertex.EXPLORED

    def _reset_nodes(self):
        for node in self.nodes.values():
            node._reset()

    def _get_distance(self, from_status, to_status):
        distance = None
        self._bfs(from_status)

        for node in self.nodes.values():
            if node.name == to_status:
                distance = node.distance
                break

        self._reset_nodes()
        return distance

    def get_relative_distances(self, from_status, to_status):
        distances = {}
        distances[(from_status, to_status)] = self._get_distance(from_status, to_status)
        distances[(to_status, from_status)] = self._get_distance(to_status, from_status)
        return distances

    def __str__(self):
        return ', '.join([str(node) for node in self.nodes.values()])

    def __repr__(self):
        _repr = ', '.join([repr(node) for node in self.nodes.values()])
        return f'Graph({_repr})'
