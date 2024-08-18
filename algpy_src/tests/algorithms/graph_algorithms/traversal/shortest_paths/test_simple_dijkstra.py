from typing import Optional

import pytest

from algpy_src.algorithms.graph_algorithms.traversal.shortest_paths.simple_dijkstra import DijkstraShortestPathsAlgorithm
from algpy_src.base.constants import GraphSize, SingleEdgeData, Node
from algpy_src.data_structures.graphs.digraph import DiGraph
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
    assert dijkstra.worst_case_time_complexity == '|V| * [|E| + |V| * log(|V|)]'
    assert dijkstra.worst_case_description == 'all-pairs shortest paths'
    assert dijkstra.space_complexity == '|V|^2'
    assert dijkstra.get_worst_case_arguments(GraphSize(*(5, 5))) == {
        'input_instance': Graph({0: {1: 1, 2: 1, 3: 1, 4: 1}, 1: {0: 1, 2: 1}, 2: {0: 1, 1: 1}, 3: {0: 1}, 4: {0: 1}}),
        'source': NoNode(), 'target': NoNode()
    }


def test_worst_case(dijkstra: DijkstraShortestPathsAlgorithm) -> None:

    assert dijkstra.n_ops == 0
    worst_case_args = dijkstra.get_worst_case_arguments(GraphSize(*(5, 5)))

    shortest_path_graph = ShortestPathsGraph(
        adjacency_list=worst_case_args['input_instance'].adjacency_list,
        shortest_path_lengths={0: {0: 0, 1: 1, 2: 1, 3: 1, 4: 1}, 1: {0: 1, 1: 0, 2: 1, 3: 2, 4: 2}, 2: {0: 1, 1: 1, 2: 0, 3: 2, 4: 2},
                               3: {0: 1, 1: 2, 2: 2, 3: 0, 4: 2}, 4: {0: 1, 1: 2, 2: 2, 3: 2, 4: 0}},
        shortest_path_predecessors={0: {0: NoNode(), 1: 0, 2: 0, 3: 0, 4: 0}, 1: {0: 1, 1: NoNode(), 2: 1, 3: 0, 4: 0}, 2: {0: 2, 1: 2, 2: NoNode(), 3: 0, 4: 0},
                                    3: {0: 3, 1: 0, 2: 0, 3: NoNode(), 4: 0}, 4: {0: 4, 1: 0, 2: 0, 3: 0, 4: NoNode()}}
    )
    assert dijkstra.run_algorithm(**worst_case_args) == (
        True,
        shortest_path_graph
    )
    assert dijkstra.n_ops == 25  # TODO: Update when Fib heap n_ops counting is implemented


@pytest.mark.parametrize(
    ('input_adjacency_list', 'source', 'target', 'expected_path_lengths', 'expected_path_predecessors', 'expected_n_ops'),
    [
        pytest.param({}, 1, 1, None, None, 0, id='Empty graph with source and target nodes'),
        pytest.param({}, NoNode(), NoNode(), {}, {}, 0, id='Empty graph with no source or target node'),
        pytest.param({1: {}, 2: {}}, 1, 2, {}, {}, 0, id='Disconnected nodes'),
        pytest.param(
            {1: {2: 1}, 2: {3: 1}, 3: {}}, 1, 1,
            {1: {1: 0}},
            {1: {1: NoNode()}},
            0, id='Line graph with head as both source and target node'
        ),
        pytest.param(
            {1: {2: 1}, 2: {3: 1}, 3: {}}, NoNode(), NoNode(),
            {1: {1: 0, 2: 1, 3: 2}, 2: {2: 0, 3: 1}, 3: {3: 0}},
            {1: {1: NoNode(), 2: 1, 3: 2}, 2: {2: NoNode(), 3: 2}, 3: {3: NoNode()}},
            9, id='Line graph with no source or target node'
        ),
        pytest.param(
            {1: {2: 1}, 2: {3: 1}, 3: {}}, 1, NoNode(),
            {1: {1: 0, 2: 1, 3: 2}},
            {1: {1: NoNode(), 2: 1, 3: 2}},
            3, id='Line graph with head as source but no target node'
        ),
        pytest.param(
            {1: {2: 1}, 2: {3: 1}, 3: {}}, NoNode(), 3,
            {1: {1: 0, 2: 1, 3: 2}, 2: {2: 0, 3: 1}, 3: {3: 0}},
            {1: {1: NoNode(), 2: 1, 3: 2}, 2: {2: NoNode(), 3: 2}, 3: {3: NoNode()}},
            9, id='Line graph with no source but tail as target node'
        ),
        pytest.param(
            {1: {2: 1}, 2: {3: 1}, 3: {}}, 1, 2,
            {1: {1: 0, 2: 1}},
            {1: {1: NoNode(), 2: 1}},
            1, id='Line graph with head source and its child as target node'
        ),
        pytest.param(
            {0: {1: 1, 2: 1, 3: 1, 4: 1}, 1: {}, 2: {}, 3: {}, 4: {}}, 0, NoNode(),
            {0: {0: 0, 1: 1, 2: 1, 3: 1, 4: 1}},
            {0: {0: NoNode(), 1: 0, 2: 0, 3: 0, 4: 0}},
            3, id='Circular graph with center as source and no target node'
        ),
        pytest.param(
            {0: {1: 5, 2: 1}, 1: {}, 2: {1: 1}}, 0, 1,
            {0: {0: 0, 1: 2, 2: 1}},
            {0: {0: NoNode(), 1: 2, 2: 0}},
            3, id='Triangle with shortcut'
        ),
        pytest.param(
            {0: {1: -1}, 1: {0: 0}}, 0, 1,
            None, None, 3, id='Does not support negative weights'
        ),
        pytest.param(
            {0: {1: None}}, 0, 1,
            {0: {0: 0, 1: 1}}, {0: {0: NoNode(), 1: 0}}, 1, id='None weights are filled on demand'
        ),
        pytest.param(
            {0: {1: 'Non-numeric-value'}}, 0, 1,
            None, None, 1, id='Does not support invalid weight values'
        ),
    ]
)
def test_dijkstra_run_algorithm(
        dijkstra: DijkstraShortestPathsAlgorithm, input_adjacency_list: dict[Node, dict[Node, SingleEdgeData]],
        source: Node | NoNode, target: Node | NoNode, expected_path_lengths: Optional[dict[Node, dict[Node, int | float]]],
        expected_path_predecessors: Optional[dict[Node, dict[Node, Node | NoNode]]], expected_n_ops: int
) -> None:

    digraph = DiGraph(input_adjacency_list)

    if expected_path_lengths is None or expected_path_predecessors is None:
        with pytest.raises(ValueError):
            dijkstra.run_algorithm(digraph, source=source, target=target)
    else:
        expected_shortest_path_graph = ShortestPathsGraph(input_adjacency_list, expected_path_lengths, expected_path_predecessors)
        result, sp_graph = dijkstra.run_algorithm(digraph, source=source, target=target, fill_weight_value=1)

        if (source != NoNode() and expected_path_lengths == {}) or (target != NoNode() and expected_path_predecessors == {}):
            assert result is False
        else:
            assert result is True

        assert sp_graph == expected_shortest_path_graph
