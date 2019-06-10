from status_map.graph import Graph


status_map = {
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

graph = Graph()
graph.add_nodes(*status_map.keys())

for node in graph.get_nodes():
    to_nodes = status_map[node]
    graph.add_edges_from_node(node, to_nodes)


def get_distances(graph, from_status):
    print('******')
    print(f'DISTANCES FROM: {from_status}')
    distances = {}
    graph._bfs(from_status)
    for node in graph.nodes.values():
        distances[node.name] = node.distance
    graph._reset_nodes()
    return distances


print(get_distances(graph, 'pending'))
print(get_distances(graph, 'shipped'))
print(get_distances(graph, 'lost'))
print(get_distances(graph, 'stolen'))
print(get_distances(graph, 'seized_for_inspection'))
print(get_distances(graph, 'awaiting_pickup_by_receiver'))
print(get_distances(graph, 'delivered'))
print(get_distances(graph, 'returning_to_sender'))
print(get_distances(graph, 'returned_to_sender'))
