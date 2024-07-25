from algpy_src.data_structures.graphs.traversal_graph import TraversalGraph


def test_traversal_graph_adjacency_list_ordering_sensitive() -> None:
    traversal_graph_1 = TraversalGraph({1: {2: None}, 2: {3: None}, 3: {}})

    traversal_graph_2 = TraversalGraph()
    traversal_graph_2.add_edges_from([(1, 2, None), (2, 3, None)])

    traversal_graph_3 = TraversalGraph()
    traversal_graph_3.add_edges_from([(2, 3, None), (1, 2, None)])

    assert traversal_graph_1 == traversal_graph_2
    assert traversal_graph_1 != traversal_graph_3
