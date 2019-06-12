__version__ = "0.4.0"
from collections.abc import Mapping

from networkx import DiGraph, ancestors, descendants

from .exceptions import (
    AmbiguousTransitionError,
    FutureTransitionError,
    PastTransitionError,
    StatusNotFoundError,
    TransitionNotFoundError,
)


class StatusMap(Mapping):
    def __init__(self, transitions):
        graph = DiGraph()
        graph.add_nodes_from(transitions.keys())
        for node in graph.nodes:
            edges = transitions[node]
            edges = ((node, edge) for edge in edges)
            graph.add_edges_from(edges)

        self._graph = graph

    def __repr__(self):
        return f"StatusMap(statuses={self.statuses})"

    def __str__(self):
        return f"{self.statuses}"

    def __getitem__(self, node):
        return self._graph[node]

    def __len__(self):
        return self._graph.number_of_nodes()

    def __iter__(self):
        return iter(self._graph.nodes)

    @property
    def statuses(self):
        return tuple(self._graph.nodes)

    def validate_transition(self, from_status, to_status):
        if not self._graph.has_node(from_status):
            raise StatusNotFoundError(f"from_status {from_status} not found")

        if not self._graph.has_node(to_status):
            raise StatusNotFoundError(f"to_status {to_status} not found")

        if from_status == to_status or self._graph.has_successor(from_status, to_status):
            return

        is_ancestor = to_status in ancestors(self._graph, from_status)
        is_descendant = to_status in descendants(self._graph, from_status)

        if is_ancestor and is_descendant:
            raise AmbiguousTransitionError(f"from {from_status} to {to_status} is both past and future")

        if is_descendant:
            raise FutureTransitionError(f"from {from_status} to {to_status} should happen in the future")

        if is_ancestor:
            raise PastTransitionError(f"from {from_status} to {to_status} should have happened in the past")

        raise TransitionNotFoundError(f"from {from_status} to {to_status} not found")
