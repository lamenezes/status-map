__version__ = "0.4.0"
from .graph import Graph
from .exceptions import RepeatedTransition, StatusNotFound, TransitionNotFound


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

    def __getitem__(self, key):
        if isinstance(key, Status):
            key = key.name
        return self._statuses[key]

    def __len__(self):
        return len(self._statuses)

    def __iter__(self):
        return iter(self._statuses)

    @property
    def statuses(self):
        return tuple(self.graph.get_nodes())

    def validate_status_exists(self, from_status, to_status):
        if from_status not in self.graph.get_nodes():
            raise StatusNotFound(f"from_status {from_status} not found")

        if to_status not in self.graph.get_nodes():
            raise StatusNotFound(f"to_status {to_status} not found")

    def validate_is_previous(self, from_status, to_status):
        self.graph.breath_first_search(from_status)

        from_status = self.graph.get_node(from_status)
        to_status = self.graph.get_node(to_status)

        if from_status.distance in from_status.previous:
            msg = f"transition from {from_status.name} to {to_status.name} should have happened in the past"
            raise RepeatedTransition(msg)

    def validate_is_future(self, from_status, to_status):
        self.graph.breath_first_search(to_status)
        from_status = self.graph.get_node(from_status)
        to_status = self.graph.get_node(to_status)

    def validate_transition(self, from_status, to_status):
        self.validate_status_exists(from_status, to_status)
        self.validate_is_previous(from_status, to_status)
        self.validate_is_future(from_status, to_status)

        

        raise TransitionNotFound(f"transition from {from_status.name} to {to_status.name} not found")
