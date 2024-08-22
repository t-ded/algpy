import pytest

from algpy_src.base.constants import FlowEdgeData, Edge, Node
from algpy_src.data_structures.graphs.flow_network import FlowNetwork


@pytest.fixture
def line_flow_network_no_flow() -> FlowNetwork[int]:

    nodes: list[int] = [1, 2, 3, 4, 5]
    edges: list[Edge] = [
        (1, 2, FlowEdgeData(0, None, 10)),
        (2, 3, FlowEdgeData(0, None, 10)),
        (3, 4, FlowEdgeData(0, None, 10)),
        (4, 5, FlowEdgeData(0, None, 10))
    ]

    fn: FlowNetwork[int] = FlowNetwork({1: {}, 5: {}}, source=1, sink=5)
    fn.add_nodes_from(nodes)
    fn.add_edges_from(edges)

    return fn


@pytest.fixture
def line_flow_network_valid_flow() -> FlowNetwork[int]:

    nodes: list[int] = [1, 2, 3, 4, 5]
    edges: list[Edge] = [
        (1, 2, FlowEdgeData(0, 5, 10)),
        (2, 3, FlowEdgeData(0, 5, 10)),
        (3, 4, FlowEdgeData(0, 5, 10)),
        (4, 5, FlowEdgeData(0, 5, 10))
    ]

    fn: FlowNetwork[int] = FlowNetwork({1: {}, 5: {}}, source=1, sink=5)
    fn.add_nodes_from(nodes)
    fn.add_edges_from(edges)

    return fn


def expect_valid_flow(flow_network: FlowNetwork[Node]) -> None:
    try:
        flow_network.check_flow_validity()
    except Exception as e:
        pytest.fail(f'Flow within the network was expected to be valid but instead got exception:\n{e}.')


def test_flow_inequality(line_flow_network_no_flow: FlowNetwork, line_flow_network_valid_flow: FlowNetwork) -> None:
    assert line_flow_network_no_flow != line_flow_network_valid_flow


def test_check_flow_validity() -> None:
    assert FlowNetwork.is_flow_within_bounds(FlowEdgeData(0, 5, 10)) is True
    assert FlowNetwork.is_flow_within_bounds(FlowEdgeData(0, 0, 10)) is True
    assert FlowNetwork.is_flow_within_bounds(FlowEdgeData(0, 10, 10)) is True
    assert FlowNetwork.is_flow_within_bounds(FlowEdgeData(0, None, 10)) is True
    assert FlowNetwork.is_flow_within_bounds(FlowEdgeData(0, -1, 10)) is False
    assert FlowNetwork.is_flow_within_bounds(FlowEdgeData(0, 11, 10)) is False


def test_basic_methods(line_flow_network_valid_flow: FlowNetwork) -> None:

    assert line_flow_network_valid_flow.source == 1
    assert line_flow_network_valid_flow.sink == 5
    expect_valid_flow(line_flow_network_valid_flow)

    line_flow_network_valid_flow.change_flow_between_nodes(1, 2, 10)
    line_flow_network_valid_flow.change_flow_between_nodes(2, 3, 10)
    line_flow_network_valid_flow.change_flow_between_nodes(3, 4, 10)
    line_flow_network_valid_flow.change_flow_between_nodes(4, 5, 10)
    expect_valid_flow(line_flow_network_valid_flow)

    assert line_flow_network_valid_flow.get_node_balance(1) == -10
    for i in range(2, 5):
        assert line_flow_network_valid_flow.get_node_balance(i) == 0
    assert line_flow_network_valid_flow.get_node_balance(5) == 10

    line_flow_network_valid_flow.change_flow_between_nodes(1, 2, 11)
    with pytest.raises(ValueError):
        line_flow_network_valid_flow.check_flow_validity()

    line_flow_network_valid_flow.change_flow_between_nodes(1, 2, 5)
    with pytest.raises(ValueError):
        line_flow_network_valid_flow.check_flow_validity()
