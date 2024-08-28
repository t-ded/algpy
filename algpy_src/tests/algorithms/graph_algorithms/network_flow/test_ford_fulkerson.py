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
                2: {3: FlowEdgeData(0, None, 100)}, 3: {4: FlowEdgeData(0, None, 100)}, 4: {},
            },
            source=0, sink=4
        ),
    }


def test_worst_case(ford_fulkerson: FordFulkersonAlgorithm) -> None:

    assert ford_fulkerson.n_ops == 0
    worst_case_args = ford_fulkerson.get_worst_case_arguments(FordFulkersonGraphSize(*(6, 100)))

