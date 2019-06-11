import pytest

from status_map import StatusMap
from status_map.graph import Graph


@pytest.fixture
def transitions():
    return {
        "pending": ["processing"],
        "processing": ["approved", "rejected"],
        "approved": ["processed"],
        "rejected": [],
        "processed": [],
    }


@pytest.fixture
def cycle_transitions():
    return {
        "pending": {"processing"},
        "processing": {"approved", "rejected"},
        "approved": {"processed"},
        "rejected": {"pending"},
        "processed": set(),
    }


@pytest.fixture
def complex_transitions():
    return {
        "pending": {"shipped"},
        "shipped": {
            "stolen",
            "seized_for_inspection",
            "returned_to_sender",
            "shipped",
            "delivered",
            "awaiting_pickup_by_receiver",
            "returning_to_sender",
            "lost",
        },
        "lost": {
            "stolen",
            "returned_to_sender",
            "seized_for_inspection",
            "delivered",
            "awaiting_pickup_by_receiver",
            "returning_to_sender",
            "lost",
        },
        "stolen": {
            "seized_for_inspection",
            "returned_to_sender",
            "lost",
            "delivered",
            "returning_to_sender",
            "stolen",
            "awaiting_pickup_by_receiver",
        },
        "seized_for_inspection": {
            "stolen",
            "returned_to_sender",
            "seized_for_inspection",
            "delivered",
            "awaiting_pickup_by_receiver",
            "returning_to_sender",
            "lost",
        },
        "awaiting_pickup_by_receiver": {
            "stolen",
            "returned_to_sender",
            "seized_for_inspection",
            "delivered",
            "awaiting_pickup_by_receiver",
            "returning_to_sender",
            "lost",
        },
        "delivered": set(),
        "returning_to_sender": {
            "stolen",
            "returned_to_sender",
            "seized_for_inspection",
            "delivered",
            "returning_to_sender",
            "lost",
        },
        "returned_to_sender": set(),
    }


@pytest.fixture
def complex_transitions_map(complex_transitions):
    return StatusMap(complex_transitions)


@pytest.fixture
def transitions_map(transitions):
    return StatusMap(transitions)


@pytest.fixture
def cycle_transitions_map(cycle_transitions):
    return StatusMap(cycle_transitions)


@pytest.fixture
def graph(cycle_transitions):
    graph = Graph()
    graph.add_nodes(*cycle_transitions.keys())

    for node in graph.get_nodes():
        to_nodes = cycle_transitions[node]
        graph.add_edges_from_node(node, to_nodes)
    return graph
