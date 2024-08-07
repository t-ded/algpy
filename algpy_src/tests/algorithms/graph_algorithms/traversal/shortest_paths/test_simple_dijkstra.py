import pytest

from algpy_src.algorithms.graph_algorithms.traversal.shortest_paths.simple_dijkstra import DijkstraShortestPathsAlgorithm
from algpy_src.base.constants import GraphSize, SingleEdgeData, Node
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.shortest_paths_graph import ShortestPathsGraph


@pytest.fixture
def dijkstra() -> DijkstraShortestPathsAlgorithm:
    return DijkstraShortestPathsAlgorithm()


def test_dijkstra_base(dijkstra: DijkstraShortestPathsAlgorithm) -> None:
    assert dijkstra.name == "Uni-directional Dijsktra's Shortest Path(s) Algorithm"
    assert dijkstra.best_case_time_complexity == '1'
    assert dijkstra.best_case_description == 'starting from searched for element'
    assert dijkstra.average_case_time_complexity == '|E| + |V| * log(|V|)'
    assert dijkstra.worst_case_time_complexity == '|V| * [|E| + |V|* log(|V|)]'
    assert dijkstra.worst_case_description == 'all-pairs shortest paths'
    assert dijkstra.space_complexity == '|V| ^ 2'
    assert dijkstra.get_worst_case_arguments(GraphSize(*(5, 5))) == {
        'input_instance': Graph({0: {1: 1, 2: 1, 3: 1, 4: 1}, 1: {0: 1, 2: 1}, 2: {0: 1, 1: 1}, 3: {0: 1}, 4: {0: 1}}),
        'source': 0, 'target': NoNode()
    }


def test_worst_case(dijkstra: DijkstraShortestPathsAlgorithm) -> None:

    assert dijkstra.n_ops == 0
    worst_case_args = dijkstra.get_worst_case_arguments(GraphSize(*(5, 5)))

    shortest_path_graph = ShortestPathsGraph(
        adjacency_list=worst_case_args['input_instance'].adjacency_list,
        shortest_path_lengths={0: {0: 0, 1: 1, 2: 1, 3: 1, 4: 1}, 1: {0: 1, 1: 0, 2: 1, 3: 2, 4: 2}, 2: {0: 1, 1: 1, 2: 0, 3: 2, 4: 2},
                               3: {0: 1, 1: 2, 2: 2, 3: 0, 4: 2}, 4: {0: 1, 1: 2, 2: 2, 3: 2, 4: 1}},
        shortest_path_predecessors={0: {0: NoNode(), 1: 0, 2: 0, 3: 0, 4: 0}, 1: {0: 0, 1: NoNode(), 2: 2, 3: 0, 4: 0}, 2: {0: 0, 1: 1, 2: NoNode, 3: 0, 4: 0},
                                    3: {0: 0, 1: 0, 2: 0, 3: NoNode(), 4: 0}, 4: {0: 0, 1: 0, 2: 0, 3: 0, 4: NoNode()}}
    )
    print(shortest_path_graph)
    # assert dijkstra.run_algorithm(**worst_case_args) == (
    #     True,
    #     shortest_path_graph
    # )
    # assert dijkstra.n_ops == 10


# TODO
@pytest.mark.parametrize(
    ('input_adjacency_list', 'source', 'target', 'expected_path_lengths', 'shortest_path_predecessors', 'expected_n_ops'),
    [
        # pytest.param({}, 1, [], 0, id='Empty graph with source and target nodes'),
        # pytest.param({}, NoNode(), [], 0, id='Empty graph with no element to search'),
        # pytest.param({1: {2: None}, 2: {3: None}, 3: {4: None}, 4: {}}, 1, [1], 2, id='Line graph with element to search in root'),
        # pytest.param({1: {2: None}, 2: {3: None}, 3: {4: None}, 4: {}}, 4, [1, 2, 3, 4], 8, id='Line graph with element to search as last'),
        # pytest.param({1: {2: None, 4: None, 6: None}, 2: {3: None}, 3: {}, 4: {5: None}, 5: {}, 6: {7: None}, 7: {}}, 8, [1, 2, 4, 6, 3, 5, 7], 14, id='Star graph with two layers'),
    ]
)
def test_dijkstra_run_algorithm(
        dijkstra: DijkstraShortestPathsAlgorithm, input_adjacency_list: dict[Node, dict[Node, SingleEdgeData]],
        source: Node | NoNode, target: Node | NoNode, expected_path_lengths: dict[Node, dict[Node, int]],
        shortest_path_predecessors: dict[Node, dict[Node, Node]], expected_n_ops: int
) -> None:
    pass
