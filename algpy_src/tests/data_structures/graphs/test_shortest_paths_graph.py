import pytest

from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.shortest_paths_graph import ShortestPathsGraph
from algpy_src.data_structures.graphs.traversal_graph import TraversalGraph


@pytest.fixture
def simple_shortest_paths_graph() -> ShortestPathsGraph:
    sp_graph = ShortestPathsGraph(
        adjacency_list={'1': {'2': 1}, '2': {'3': 1}, '3': {'4': 1}},
        shortest_path_lengths={
            '1': {'1': 0, '2': 1, '3': 2, '4': 3},
            '2': {'1': float('inf'), '2': 0, '3': 1, '4': 2},
            '3': {'1': float('inf'), '2': float('inf'), '3': 0, '4': 1},
            '4': {'1': float('inf'), '2': float('inf'), '3': float('inf'), '4': 0},
        },
        shortest_path_predecessors={
            '1': {'1': NoNode(), '2': '1', '3': '2', '4': '3'},
            '2': {'1': NoNode(), '2': NoNode(), '3': '2', '4': '3'},
            '3': {'1': NoNode(), '2': NoNode(), '3': NoNode(), '4': '3'},
            '4': {'1': NoNode(), '2': NoNode(), '3': NoNode(), '4': NoNode()},
        }
    )
    return sp_graph


def test_simple_shortest_paths_graph_equality(simple_shortest_paths_graph: ShortestPathsGraph) -> None:

    assert simple_shortest_paths_graph == ShortestPathsGraph(
        adjacency_list={'1': {'2': 1}, '2': {'3': 1}, '3': {'4': 1}},
        shortest_path_lengths={
            '1': {'1': 0, '2': 1, '3': 2, '4': 3},
            '2': {'1': float('inf'), '2': 0, '3': 1, '4': 2},
            '3': {'1': float('inf'), '2': float('inf'), '3': 0, '4': 1},
            '4': {'1': float('inf'), '2': float('inf'), '3': float('inf'), '4': 0},
        },
        shortest_path_predecessors={
            '1': {'1': NoNode(), '2': '1', '3': '2', '4': '3'},
            '2': {'1': NoNode(), '2': NoNode(), '3': '2', '4': '3'},
            '3': {'1': NoNode(), '2': NoNode(), '3': NoNode(), '4': '3'},
            '4': {'1': NoNode(), '2': NoNode(), '3': NoNode(), '4': NoNode()},
        }
    )

    assert simple_shortest_paths_graph != ShortestPathsGraph(
        adjacency_list={'1': {'2': 1}, '2': {'3': 1}, '3': {'4': 0}},
        shortest_path_lengths={
            '1': {'1': 0, '2': 1, '3': 2, '4': 2},
            '2': {'1': float('inf'), '2': 0, '3': 1, '4': 1},
            '3': {'1': float('inf'), '2': float('inf'), '3': 0, '4': 0},
            '4': {'1': float('inf'), '2': float('inf'), '3': float('inf'), '4': 0},
        },
        shortest_path_predecessors={
            '1': {'1': NoNode(), '2': '1', '3': '2', '4': '3'},
            '2': {'1': NoNode(), '2': NoNode(), '3': '2', '4': '3'},
            '3': {'1': NoNode(), '2': NoNode(), '3': NoNode(), '4': '3'},
            '4': {'1': NoNode(), '2': NoNode(), '3': NoNode(), '4': NoNode()},
        }
    )


def test_shortest_paths(simple_shortest_paths_graph: ShortestPathsGraph) -> None:

    for node_1 in range(1, 5):
        for node_2 in range(1, 5):
            node_1_str = str(node_1)
            node_2_str = str(node_2)
            assert simple_shortest_paths_graph.shortest_path_length(node_1_str, node_2_str) == (node_2 - node_1 if node_1_str <= node_2_str else float('inf'))
            if node_2_str == node_1_str:
                one_node_traversal_graph = TraversalGraph()
                one_node_traversal_graph.add_node(node_1_str)
                assert simple_shortest_paths_graph.shortest_path(node_1_str, node_2_str) == one_node_traversal_graph
            elif node_2_str < node_1_str:
                assert simple_shortest_paths_graph.shortest_path(node_1_str, node_2_str) is None
            else:
                assert simple_shortest_paths_graph.shortest_path(node_1_str, node_2_str) == TraversalGraph({str(i): {str(i + 1): 1} for i in range(node_1, node_2)})



