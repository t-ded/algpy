import pytest

from algpy_src.algorithms.graph_algorithms.network_flow.edmonds_karp import EdmondsKarpAlgorithm
from algpy_src.algorithms.graph_algorithms.network_flow.ford_fulkerson import FordFulkersonGraphSize
from algpy_src.base.constants import FlowEdgeData
from algpy_src.data_structures.graphs.flow_network import FlowNetwork


@pytest.fixture
def edmonds_karp() -> EdmondsKarpAlgorithm:
    return EdmondsKarpAlgorithm()


def test_edmonds_karp_base(edmonds_karp: EdmondsKarpAlgorithm) -> None:
    assert edmonds_karp.name == "Edmonds-Karp's Max-Flow Algorithm"
    assert edmonds_karp.best_case_time_complexity == '|E|'
    assert edmonds_karp.best_case_description == 'maximum flow found in 1 iteration'
    assert edmonds_karp.average_case_time_complexity == '|V| * |E| ^ 2'
    assert edmonds_karp.worst_case_time_complexity == '|V| * |E| ^ 2'
    assert edmonds_karp.worst_case_description == 'every augmenting path improving current flow by 1'
    assert edmonds_karp.space_complexity == '|V| + |E|'
    assert edmonds_karp.get_worst_case_arguments(FordFulkersonGraphSize(*(5, 1))) == {
        'input_instance': FlowNetwork(
            adjacency_list={
                0: {1: FlowEdgeData(0, None, 1), 2: FlowEdgeData(0, None, 1), 3: FlowEdgeData(0, None, 1)},
                1: {4: FlowEdgeData(0, None, 1)},
                2: {4: FlowEdgeData(0, None, 1)},
                3: {4: FlowEdgeData(0, None, 1)},
                4: {},
            },
            source=0, sink=4
        ),
    }


def test_worst_case(edmonds_karp: EdmondsKarpAlgorithm) -> None:

    assert edmonds_karp.n_ops == 0
    worst_case_args = edmonds_karp.get_worst_case_arguments(FordFulkersonGraphSize(*(5, 1)))
    expected_flow_network: FlowNetwork[int] = FlowNetwork(
        adjacency_list={
            0: {1: FlowEdgeData(0, 1, 1), 2: FlowEdgeData(0, 1, 1), 3: FlowEdgeData(0, 1, 1)},
            1: {4: FlowEdgeData(0, 1, 1)},
            2: {4: FlowEdgeData(0, 1, 1)},
            3: {4: FlowEdgeData(0, 1, 1)},
            4: {},
        },
        source=0, sink=4
    )
    assert edmonds_karp.run_algorithm(**worst_case_args) == (
        True,
        expected_flow_network
    )
    assert edmonds_karp.n_ops == 50
    assert worst_case_args['input_instance'].current_flow == 3

def test_simple_case_zero_initial_flow(edmonds_karp: EdmondsKarpAlgorithm) -> None:
    input_instance: FlowNetwork[str] = FlowNetwork(
        adjacency_list={
            's': {'u': FlowEdgeData(0, 0, 5), 'v': FlowEdgeData(0, 0, 7), 'w': FlowEdgeData(0, 0, 3)},
            'u': {'t': FlowEdgeData(0, 0, 6)},
            'v': {'t': FlowEdgeData(0, 0, 5), 'u': FlowEdgeData(0, 0, 2)},
            'w': {'t': FlowEdgeData(0, 0, 8)},
            't': {}
        },
        source='s', sink='t'
    )
    res, inp = edmonds_karp.run_algorithm(input_instance, find_initial_feasible=False)
    assert res is True
    assert inp.current_flow == 14

def test_can_utilise_backward_edge_and_start_from_arbitrary_flow(edmonds_karp: EdmondsKarpAlgorithm) -> None:
    input_instance: FlowNetwork[int] = FlowNetwork(
        adjacency_list={
            0: {1: FlowEdgeData(0, 4, 4), 2: FlowEdgeData(2, 5, 5), 3: FlowEdgeData(0, 6, 7)},
            1: {4: FlowEdgeData(0, 4, 7)},
            2: {4: FlowEdgeData(0, 3, 6), 5: FlowEdgeData(1, 1, 4), 6: FlowEdgeData(0, 1, 1)},
            3: {5: FlowEdgeData(0, 5, 8), 6: FlowEdgeData(0, 1, 1)},
            4: {7: FlowEdgeData(0, 7, 7)},
            5: {7: FlowEdgeData(0, 6, 6)},
            6: {7: FlowEdgeData(1, 2, 4)},
            7: {}
        },
        source=0, sink=7
    )
    res, inp = edmonds_karp.run_algorithm(input_instance, find_initial_feasible=False)
    assert res is True
    assert inp.current_flow == 15

def test_can_find_initial_feasible(edmonds_karp: EdmondsKarpAlgorithm) -> None:
    input_instance: FlowNetwork[str] = FlowNetwork(
        adjacency_list={
            's': {'u': FlowEdgeData(1, None, 3), 'v': FlowEdgeData(2, None, 3)},
            'u': {'t': FlowEdgeData(2, None, 4)},
            'v': {'t': FlowEdgeData(0, None, 2), 'u': FlowEdgeData(1, None, 3)},
            't': {}
        },
        source='s', sink='t'
    )
    res, inp = edmonds_karp.run_algorithm(input_instance, find_initial_feasible=True)
    assert res is True
    assert inp.current_flow == 6

def test_improves_ford_fulkersons_worst_case(edmonds_karp: EdmondsKarpAlgorithm) -> None:
    input_instance: FlowNetwork[int] = FlowNetwork(
        adjacency_list={
            0: {1: FlowEdgeData(0, None, 100), 2: FlowEdgeData(0, None, 100)},
            1: {2: FlowEdgeData(0, None, 1), 3: FlowEdgeData(0, None, 100)},
            2: {3: FlowEdgeData(0, None, 100)}, 3: {4: FlowEdgeData(0, None, 200)}, 4: {},
        },
        source=0, sink=4
    )
    res, inp = edmonds_karp.run_algorithm(input_instance, find_initial_feasible=True)
    assert res is True
    assert inp.current_flow == 200
    assert edmonds_karp.n_ops == 48