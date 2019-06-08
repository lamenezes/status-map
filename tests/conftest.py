import pytest
from status_map import StatusMap
from status_map.graph import Graph


@pytest.fixture
def next_status_map():
    return {
        'pending': {
            'shipped'
        },
        'shipped': {
            'stolen',
            'seized_for_inspection',
            'returned_to_sender',
            'shipped',
            'delivered',
            'awaiting_pickup_by_receiver',
            'returning_to_sender',
            'lost'
        },
        'lost': {
            'stolen',
            'returned_to_sender',
            'seized_for_inspection',
            'delivered',
            'awaiting_pickup_by_receiver',
            'returning_to_sender',
            'lost'
        },
        'stolen': {
            'seized_for_inspection',
            'returned_to_sender',
            'lost',
            'delivered',
            'returning_to_sender',
            'stolen',
            'awaiting_pickup_by_receiver'
        },
        'seized_for_inspection': {
            'stolen',
            'returned_to_sender',
            'seized_for_inspection',
            'delivered',
            'awaiting_pickup_by_receiver',
            'returning_to_sender',
            'lost'
        },
        'awaiting_pickup_by_receiver': {
            'stolen',
            'returned_to_sender',
            'seized_for_inspection',
            'delivered',
            'awaiting_pickup_by_receiver',
            'returning_to_sender',
            'lost'
        },
        'delivered': set(),
        'returning_to_sender': {
            'stolen',
            'returned_to_sender',
            'seized_for_inspection',
            'delivered',
            'returning_to_sender',
            'lost'
        },
        'returned_to_sender': set()
    }


@pytest.fixture
def graph(next_status_map):
    graph = Graph()
    graph.add_nodes(*next_status_map.keys())

    for node in graph.get_nodes():
        to_nodes = next_status_map[node]
        graph.add_edges_from_node(node, to_nodes)
    return graph


@pytest.fixture
def status_map_object(next_status_map):
    return StatusMap(next_status_map)
