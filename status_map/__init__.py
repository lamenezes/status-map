__version__ = "0.4.0"
from collections.abc import Mapping

from networkx import DiGraph, ancestors, descendants

from .exceptions import FutureTransition, RepeatedTransition, StatusNotFound, TransitionNotFound


class StatusMap(Mapping):
    def __init__(self, transitions):
        graph = DiGraph()
        graph.add_nodes_from(transitions.keys())
        for node in graph.nodes:
            edges = transitions[node]
            edges = [(node, edge) for edge in edges]
            graph.add_edges_from(edges)

        self.graph = graph

    def __repr__(self):
        return f"StatusMap(statuses={self.statuses})"

    def __str__(self):
        return f"{self.statuses}"

    def __getitem__(self, node):
        return self.graph[node]

    def __len__(self):
        return self.graph.number_of_nodes()

    def __iter__(self):
        return iter(self.graph.nodes)

    @property
    def statuses(self):
        return tuple(self.graph.nodes)

    def validate_transition(self, from_status, to_status):
        if not self.graph.has_node(from_status):
            raise StatusNotFound(f"from_status {from_status} not found")

        if not self.graph.has_node(to_status):
            raise StatusNotFound(f"to_status {to_status} not found")

        if from_status == to_status:
            return

        if self.graph.has_successor(from_status, to_status):
            return

        # future needs to be the first validation to treat cyclic status map correct
        if to_status in descendants(self.graph, from_status):
            msg = f"transition from {from_status} to {to_status} should happen in the future"
            raise FutureTransition(msg)

        if to_status in ancestors(self.graph, from_status):
            msg = f"transition from {from_status} to {to_status} should have happened in the past"
            raise RepeatedTransition(msg)

        msg = f"transition from {from_status} to {to_status} not found"
        raise TransitionNotFound(msg)
