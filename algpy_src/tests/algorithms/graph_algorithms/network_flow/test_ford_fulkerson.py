import pytest

from algpy_src.algorithms.graph_algorithms.network_flow.ford_fulkerson import FordFulkersonAlgorithm, FordFulkersonGraphSize
from algpy_src.base.constants import FlowEdgeData
from algpy_src.data_structures.graphs.flow_network import FlowNetwork


@pytest.fixture
def ford_fulkerson() -> FordFulkersonAlgorithm:
    return FordFulkersonAlgorithm()


def test_ford_fulkerson_base(ford_fulkerson: FordFulkersonAlgorithm) -> None:
    assert ford_fulkerson.name == "Ford-Fulkerson's Max-Flow Algorithm"
    assert ford_fulkerson.best_case_time_complexity == '|E|'
    assert ford_fulkerson.best_case_description == 'maximum flow found in 1 iteration'
    assert ford_fulkerson.average_case_time_complexity == '|E| * f_max'
    assert ford_fulkerson.worst_case_time_complexity == '|E| * f_max'
    assert ford_fulkerson.worst_case_description == 'every augmenting path improving current flow by 1'
    assert ford_fulkerson.space_complexity == '|V| + |E|'
    assert ford_fulkerson.get_worst_case_arguments(FordFulkersonGraphSize(*(6, 100))) == {
        'input_instance': FlowNetwork(
            adjacency_list={
                0: {1: FlowEdgeData(0, None, 100), 2: FlowEdgeData(0, None, 100)},
                1: {2: FlowEdgeData(0, None, 1), 3: FlowEdgeData(0, None, 100)},
                2: {3: FlowEdgeData(0, None, 100)}, 3: {4: FlowEdgeData(0, None, 200)}, 4: {},
            },
            source=0, sink=4
        ),
    }


def test_worst_case(ford_fulkerson: FordFulkersonAlgorithm) -> None:

    assert ford_fulkerson.n_ops == 0
    worst_case_args = ford_fulkerson.get_worst_case_arguments(FordFulkersonGraphSize(*(6, 100)))
    expected_flow_network: FlowNetwork[int] = FlowNetwork(
        adjacency_list={
            0: {1: FlowEdgeData(0, 100, 100), 2: FlowEdgeData(0, 100, 100)},
            1: {2: FlowEdgeData(0, 0, 1), 3: FlowEdgeData(0, 100, 100)},
            2: {3: FlowEdgeData(0, 100, 100)}, 3: {4: FlowEdgeData(0, 200, 200)}, 4: {},
        },
        source=0, sink=4
    )
    assert ford_fulkerson.run_algorithm(**worst_case_args) == (
        True,
        expected_flow_network
    )
    assert ford_fulkerson.n_ops == 800
    assert worst_case_args['input_instance'].current_flow == 200

def test_simple_case_zero_initial_flow(ford_fulkerson: FordFulkersonAlgorithm) -> None:
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
    res, inp = ford_fulkerson.run_algorithm(input_instance)
    assert res is True
    assert inp.current_flow == 14

