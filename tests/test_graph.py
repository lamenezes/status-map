import pytest

from status_map.graph import Graph, Vertex


def test_create_vertex():
    vertex = Vertex("node1")

    assert vertex.name == "node1"
    assert vertex.distance == 0
    assert vertex.status == Vertex.UNEXPLORED
    assert vertex.connected_to == {}


def test_vertex_add_neighbor():
    vertex = Vertex("node1")
    vertex.add_neighbor("node2")

    assert len(vertex.get_connections()) == 1


def test_vertex_get_connections():
    vertex = Vertex("node1")
    vertex.add_neighbor("node2")

    assert "node2" in vertex.get_connections()


def test_vertex_reset():
    vertex = Vertex("node1")
    vertex.distance = 10
    vertex.status = Vertex.EXPLORING

    vertex._reset()

    assert vertex.distance == 0
    assert vertex.status == Vertex.UNEXPLORED


def test_vertex_magic_methods():
    vertex = Vertex("node1")

    assert str(vertex) == "node1"
    assert repr(vertex) == "Vertex(node1)"


def test_create_graph():
    graph = Graph()

    assert graph.num_nodes == 0


def test_graph_add_node():
    graph = Graph()
    node = graph.add_node("node")

    assert node.name == "node"
    assert graph.num_nodes == 1


def test_graph_add_nodes():
    graph = Graph()
    nodes = graph.add_nodes("node1", "node2")

    assert nodes[0].name == "node1"
    assert nodes[1].name == "node2"
    assert graph.num_nodes == 2


def test_graph_get_node():
    graph = Graph()
    graph.add_node("node")

    assert graph.get_node("node")
    with pytest.raises(KeyError):
        graph.get_node("does_not_exist")


def test_graph_add_edge():
    graph = Graph()
    from_node, to_node = graph.add_nodes("node1", "node2")

    graph.add_edge("node1", "node2")
    assert to_node in from_node.get_connections()


def test_graph_add_edge_same_node_shoudnt_add():
    graph = Graph()
    from_node, to_node = graph.add_nodes("node1", "node2")

    graph.add_edge("node1", "node1")
    assert len(from_node.get_connections()) == 0


def test_graph_add_edges_from_node():
    graph = Graph()
    from_node, *to_nodes = graph.add_nodes("node1", "node2", "node3")
    graph.add_edges_from_node("node1", ["node2", "node3"])

    assert to_nodes[0] in from_node.get_connections()
    assert to_nodes[1] in from_node.get_connections()


def test_graph_get_nodes():
    graph = Graph()
    graph.add_nodes("node1", "node2")
    assert "node1" in graph.get_nodes()
    assert "node2" in graph.get_nodes()


@pytest.mark.parametrize(
    "status,distance", [("pending", 0), ("processing", 1), ("approved", 2), ("rejected", 2), ("processed", 3)]
)
def test_graph_bfs(status, distance, graph):
    assert graph.get_node(status).distance == 0
    assert graph.get_node(status).status == Vertex.UNEXPLORED

    graph._bfs("pending")

    assert graph.get_node(status).distance == distance
    assert graph.get_node(status).status == Vertex.EXPLORED


@pytest.mark.parametrize(
    "status,distance", [("pending", 0), ("processing", 1), ("approved", 2), ("rejected", 2), ("processed", 3)]
)
def test_graph_reset_nodes(status, distance, graph):
    graph._bfs("pending")

    assert graph.get_node(status).distance == distance
    assert graph.get_node(status).status == Vertex.EXPLORED

    graph._reset_nodes()

    assert graph.get_node(status).distance == 0
    assert graph.get_node(status).status == Vertex.UNEXPLORED


@pytest.mark.parametrize(
    "status,distance", [("pending", 0), ("processing", 1), ("approved", 2), ("rejected", 2), ("processed", 3)]
)
def test_graph_get_distance(status, distance, graph):
    distance = graph._get_distance("pending", status)

    assert distance == distance


@pytest.mark.parametrize(
    "status,distance_from,distance_to",
    [("pending", 0, 0), ("processing", 1, 2), ("approved", 2, 0), ("rejected", 2, 1), ("processed", 3, 0)],
)
def test_graph_get_relative_distances(status, distance_from, distance_to, graph):
    distances = graph.get_relative_distances("pending", status)

    assert distances[("pending", status)] == distance_from
    assert distances[(status, "pending")] == distance_to


def test_magic_methods():
    graph = Graph()
    graph.add_nodes("node1", "node2")

    assert str(graph) == "node1, node2"
    assert repr(graph) == "Graph(Vertex(node1), Vertex(node2))"
