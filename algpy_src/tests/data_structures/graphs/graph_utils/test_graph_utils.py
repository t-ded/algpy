import pytest

from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge
from algpy_src.data_structures.graphs.graph_utils.no_feature_object import NoFeature
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode


def test_no_edge() -> None:
    no_edge: NoEdge = NoEdge()
    assert no_edge == NoEdge()
    assert no_edge is not None
    assert NoEdge() != object()


def test_no_node() -> None:
    no_node: NoNode = NoNode()
    assert no_node == NoNode()
    assert no_node is not None
    assert NoNode() != object()


def test_no_feature() -> None:
    no_feature: NoFeature = NoFeature()
    assert no_feature == NoFeature()
    assert no_feature is not None
    assert NoFeature() != object()


@pytest.fixture
def empty_digraph() -> DiGraph:
    return DiGraph()


def test_affects_adjacency_matrix(empty_digraph: DiGraph) -> None:

    def unaffecting_subfunction(g: DiGraph) -> None:
        g.adjacency_list[1] = {2: None}
        g.adjacency_list[2] = {}

    @affects_adjacency_matrix
    def affecting_subfunction(g: DiGraph) -> None:
        g.adjacency_list[1] = {2: None}
        g.adjacency_list[2] = {}

    unaffecting_subfunction(empty_digraph)
    assert empty_digraph.adjacency_matrix == []
    assert empty_digraph.n_ops == 0

    empty_digraph.remove_edge(1, 2)
    empty_digraph.remove_nodes_from([1, 2])
    affecting_subfunction(empty_digraph)
    assert empty_digraph.adjacency_matrix == [[NoEdge(), None], [NoEdge(), NoEdge()]]
    assert empty_digraph.n_ops == 4
