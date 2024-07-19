import pytest

from algpy_src.data_structures.graphs.digraph import DiGraph


@pytest.fixture
def empty_digraph() -> DiGraph:
    return DiGraph()


@pytest.fixture
def filled_digraph() -> DiGraph:
    return DiGraph({1: {2: 'Edge1'}, 2: {3: 'Edge2'}, 3: {}})


class TestDiGraph:

    def test_digraph_base(self, empty_digraph: DiGraph) -> None:

        assert empty_digraph.name == 'DiGraph'
        assert empty_digraph.space_complexity == 'V + E'
        assert empty_digraph.is_directed is True
        assert empty_digraph.is_multigraph is False
        assert empty_digraph.n_ops == 0
        assert empty_digraph.nodes == []
        assert empty_digraph.edges == set()
        assert empty_digraph.number_of_edges == 0
        assert empty_digraph.number_of_nodes == 0

    def test_digraph_from_adjacency_list(self, filled_digraph: DiGraph) -> None:
        # assert filled_digraph.n_ops == 0
        assert filled_digraph.nodes == [1, 2, 3]
        assert filled_digraph.edges == {(1, 2, 'Edge1'), (2, 3, 'Edge2')}
        assert filled_digraph.number_of_edges == 2
        assert filled_digraph.number_of_nodes == 3
        assert filled_digraph.neighbors(1) == {2}
        assert filled_digraph.degree(1) == 1
        assert filled_digraph.neighbors(2) == {3}
        assert filled_digraph.degree(2) == 1
        assert filled_digraph.neighbors(3) == set()
        assert filled_digraph.degree(3) == 0

    def test_digraph_from_adjacency_list_nodes_filled(self) -> None:

        g = DiGraph({1: {2: 'Edge1', 3: 'Edge2', 4: 'Edge3'}})
        assert g._adjacency_list == {1: {2: 'Edge1', 3: 'Edge2', 4: 'Edge3'}, 2: {}, 3: {}, 4: {}}
        assert g.nodes == [1, 2, 3, 4]
        assert g.number_of_nodes == 4
        assert g.edges == {(1, 2, 'Edge1'), (1, 3, 'Edge2'), (1, 4, 'Edge3')}
        assert g.number_of_edges == 3
