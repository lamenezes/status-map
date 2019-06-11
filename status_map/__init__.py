__version__ = "0.4.0"
from collections.abc import Mapping

from .exceptions import FutureTransition, RepeatedTransition, StatusNotFound, TransitionNotFound
from .graph import Graph, Vertex


class StatusMap(Mapping):
    def __init__(self, transitions):
        graph = Graph()
        graph.add_nodes(*transitions.keys())
        for node in graph.get_nodes():
            to_nodes = transitions[node]
            graph.add_edges_from_node(node, to_nodes)

        self.graph = graph

    def __repr__(self):
        return f"StatusMap(statuses={self.statuses})"

    def __str__(self):
        return f"{self.statuses}"

    def __getitem__(self, key):
        if isinstance(key, Vertex):
            key = key.name
        return self.graph.get_node(key)

    def __len__(self):
        return self.graph.num_nodes

    def __iter__(self):
        return iter(self.graph)

    @property
    def statuses(self):
        return tuple(self.graph.get_nodes())

    def validate_transition(self, from_status, to_status):
        if from_status not in self.graph.get_nodes():
            raise StatusNotFound(f"from_status {from_status} not found")

        if to_status not in self.graph.get_nodes():
            raise StatusNotFound(f"to_status {to_status} not found")

        distances = self.graph.get_relative_distances(from_status, to_status)
        if from_status == to_status or distances[(from_status, to_status)] == 1:
            return

        if distances[(from_status, to_status)] > 1:
            msg = f"transition from {from_status} to {to_status} should happen in the future"
            raise FutureTransition(msg)

        if distances[(from_status, to_status)] == 0 and distances[(to_status, from_status)] > 0:
            msg = f"transition from {from_status} to {to_status} should have happened in the past"
            raise RepeatedTransition(msg)

        msg = f"transition from {from_status} to {to_status} not found"
        raise TransitionNotFound(msg)
