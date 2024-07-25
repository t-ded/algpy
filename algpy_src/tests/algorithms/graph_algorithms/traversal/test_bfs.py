import pytest

from algpy_src.algorithms.graph_algorithms.traversal.bfs import BreadthFirstSearch
from algpy_src.base.constants import GraphSize, SingleEdgeData, Node
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.traversal_graph import TraversalGraph


@pytest.fixture
def bfs() -> BreadthFirstSearch:
    return BreadthFirstSearch()


def test_bfs_base(bfs: BreadthFirstSearch) -> None:
    assert bfs.name == 'Breadth First Search'
    assert bfs.best_case_time_complexity == '1'
    assert bfs.best_case_description == 'starting from searched for element'
    assert bfs.average_case_time_complexity == '|V| + |E|'
    assert bfs.worst_case_time_complexity == '|V| + |E|'
    assert bfs.worst_case_description == 'searched for element not present in the graph'
    assert bfs.space_complexity == '|V|'
    assert bfs.get_worst_case_arguments(GraphSize(*(5, 5))) == {
        'input_instance': Graph({0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None, 2: None}, 2: {0: None, 1: None}, 3: {0: None}, 4: {0: None}}),
        'element_to_search': 6
    }


def test_worst_case(bfs: BreadthFirstSearch) -> None:
    assert bfs.n_ops == 0
    worst_case_args = bfs.get_worst_case_arguments(GraphSize(*(5, 5)))
    expected_traversal_order: list[int] = [0, 1, 2, 3, 4]
    expected_traversal_graph = TraversalGraph()
    expected_traversal_graph.add_nodes_from(expected_traversal_order)
    assert bfs.run_algorithm(**worst_case_args) == (
        False,
        expected_traversal_graph
    )
    assert bfs.n_ops == 10
    bfs.reset_n_ops()
    assert bfs.n_ops == 0


@pytest.mark.parametrize(
    ('input_adjacency_list', 'element_to_search', 'expected_traversal_order', 'expected_n_ops'),
    [
        pytest.param({}, 1, [], 0, id='Empty graph with element to search'),
        pytest.param({}, NoNode(), [], 0, id='Empty graph with no element to search'),
        pytest.param({1: {2: None}, 2: {3: None}, 3: {4: None}, 4: {}}, 1, [1], 2, id='Line graph with element to search in root'),
        pytest.param({1: {2: None}, 2: {3: None}, 3: {4: None}, 4: {}}, 4, [1, 2, 3, 4], 8, id='Line graph with element to search as last'),
        pytest.param({1: {2: None, 4: None, 6: None}, 2: {3: None}, 3: {}, 4: {5: None}, 5: {}, 6: {7: None}, 7: {}}, 8, [1, 2, 4, 6, 3, 5, 7], 14, id='Star graph with two layers'),
    ]
)
def test_bfs_run_algorithm(
        bfs: BreadthFirstSearch, input_adjacency_list: dict[Node, dict[Node, SingleEdgeData]], element_to_search: Node,
        expected_traversal_order: list[Node], expected_n_ops: int
) -> None:

    expected_traversal_graph = TraversalGraph()
    expected_traversal_graph.add_nodes_from(expected_traversal_order)
    expected_verdict = True if element_to_search == NoNode() or element_to_search in input_adjacency_list else False

    graph = Graph(input_adjacency_list)
    digraph = DiGraph(input_adjacency_list)
    assert bfs.run_algorithm(graph, element_to_search=element_to_search) == (expected_verdict, expected_traversal_graph)
    assert bfs.n_ops == expected_n_ops
    assert bfs.run_algorithm(digraph, element_to_search=element_to_search) == (expected_verdict, expected_traversal_graph)
    assert bfs.n_ops == expected_n_ops
