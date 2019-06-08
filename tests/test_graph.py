import pytest
from status_map.graph import Vertex


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 1),
    ('lost', 2),
    ('stolen', 2),
    ('seized_for_inspection', 2),
    ('awaiting_pickup_by_receiver', 2),
    ('delivered', 2),
    ('returning_to_sender', 2),
    ('returned_to_sender', 2),
])
def test_distances_from_pending(status, distance, graph):
    pending = graph.get_node('pending')

    assert pending.distance == 0
    assert pending.status == Vertex.UNEXPLORED

    graph.breath_first_search('pending')

    assert pending.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 1),
    ('stolen', 1),
    ('seized_for_inspection', 1),
    ('awaiting_pickup_by_receiver', 1),
    ('delivered', 1),
    ('returning_to_sender', 1),
    ('returned_to_sender', 1),
])
def test_distances_from_shipped(status, distance, graph):
    shipped = graph.get_node('shipped')
    assert shipped.distance == 0
    assert shipped.status == Vertex.UNEXPLORED

    graph.breath_first_search('shipped')

    assert shipped.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 0),
    ('stolen', 1),
    ('seized_for_inspection', 1),
    ('awaiting_pickup_by_receiver', 1),
    ('delivered', 1),
    ('returning_to_sender', 1),
    ('returned_to_sender', 1),
])
def test_distances_from_lost(status, distance, graph):
    lost = graph.get_node('lost')
    assert lost.distance == 0
    assert lost.status == Vertex.UNEXPLORED

    graph.breath_first_search('lost')

    assert lost.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 1),
    ('stolen', 0),
    ('seized_for_inspection', 1),
    ('awaiting_pickup_by_receiver', 1),
    ('delivered', 1),
    ('returning_to_sender', 1),
    ('returned_to_sender', 1),
])
def test_distances_from_stolen(status, distance, graph):
    stolen = graph.get_node('stolen')
    assert stolen.distance == 0
    assert stolen.status == Vertex.UNEXPLORED

    graph.breath_first_search('stolen')

    assert stolen.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 1),
    ('stolen', 1),
    ('seized_for_inspection', 0),
    ('awaiting_pickup_by_receiver', 1),
    ('delivered', 1),
    ('returning_to_sender', 1),
    ('returned_to_sender', 1),
])
def test_distances_from_seized_for_inspection(status, distance, graph):
    seized_for_inspection = graph.get_node('seized_for_inspection')
    assert seized_for_inspection.distance == 0
    assert seized_for_inspection.status == Vertex.UNEXPLORED

    graph.breath_first_search('seized_for_inspection')

    assert seized_for_inspection.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 1),
    ('stolen', 1),
    ('seized_for_inspection', 1),
    ('awaiting_pickup_by_receiver', 0),
    ('delivered', 1),
    ('returning_to_sender', 1),
    ('returned_to_sender', 1),
])
def test_distances_from_awaiting_pickup_by_receiver(status, distance, graph):
    awaiting_pickup_by_receiver = graph.get_node('awaiting_pickup_by_receiver')
    assert awaiting_pickup_by_receiver.distance == 0
    assert awaiting_pickup_by_receiver.status == Vertex.UNEXPLORED

    graph.breath_first_search('awaiting_pickup_by_receiver')

    assert awaiting_pickup_by_receiver.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 0),
    ('stolen', 0),
    ('seized_for_inspection', 0),
    ('awaiting_pickup_by_receiver', 0),
    ('delivered', 0),
    ('returning_to_sender', 0),
    ('returned_to_sender', 0),
])
def test_distances_from_delivered(status, distance, graph):
    delivered = graph.get_node('delivered')
    assert delivered.distance == 0
    assert delivered.status == Vertex.UNEXPLORED

    graph.breath_first_search('delivered')

    assert delivered.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 1),
    ('stolen', 1),
    ('seized_for_inspection', 1),
    ('awaiting_pickup_by_receiver', 2),
    ('delivered', 1),
    ('returning_to_sender', 0),
    ('returned_to_sender', 1),
])
def test_distances_from_returning_to_sender(status, distance, graph):
    returning_to_sender = graph.get_node('returning_to_sender')
    assert returning_to_sender.distance == 0
    assert returning_to_sender.status == Vertex.UNEXPLORED

    graph.breath_first_search('returning_to_sender')

    assert returning_to_sender.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance


@pytest.mark.parametrize('status,distance', [
    ('pending', 0),
    ('shipped', 0),
    ('lost', 0),
    ('stolen', 0),
    ('seized_for_inspection', 0),
    ('awaiting_pickup_by_receiver', 0),
    ('delivered', 0),
    ('returning_to_sender', 0),
    ('returned_to_sender', 0),
])
def test_distances_from_returned_to_sender(status, distance, graph):
    returned_to_sender = graph.get_node('returned_to_sender')
    assert returned_to_sender.distance == 0
    assert returned_to_sender.status == Vertex.UNEXPLORED

    graph.breath_first_search('returned_to_sender')

    assert returned_to_sender.status == Vertex.EXPLORED
    node = graph.get_node(status)
    assert node.distance == distance
