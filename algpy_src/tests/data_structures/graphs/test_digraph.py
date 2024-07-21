import pytest

from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge


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

    def test_digraph_adding_edges(self, empty_digraph: DiGraph) -> None:

        g = empty_digraph

        g.add_edge((1, 2, None))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, None)}
        assert g.adjacency_list == {1: {2: None}, 2: {}}
        assert g.adjacency_matrix == [[NoEdge(), None], [NoEdge(), NoEdge()]]
        assert g.get_edge_data(1, 2) is None

        g.add_edge((1, 2, 'Edge1'))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, 'Edge1')}
        assert g.adjacency_list == {1: {2: 'Edge1'}, 2: {}}
        assert g.adjacency_matrix == [[NoEdge(), 'Edge1'], [NoEdge(), NoEdge()]]
        assert g.get_edge_data(1, 2) == 'Edge1'

    def test_digraph_removing_edges(self, filled_digraph: DiGraph) -> None:

        g = filled_digraph
        with pytest.raises(ValueError):
            g.remove_edge(1, 2, 'MultiEdge1', 'MultiEdge2')
        g.remove_edge(1, 2)
        assert g.adjacency_list == {1: {}, 2: {3: 'Edge2'}, 3: {}}
        g.remove_edge(2, 3, 'Edge1')
        assert g.adjacency_list == {1: {}, 2: {3: 'Edge2'}, 3: {}}
        g.remove_edge(2, 3, 'Edge2')
        assert g.adjacency_list == {1: {}, 2: {}, 3: {}}
