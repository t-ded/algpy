import pytest

from algpy_src.data_structures.graphs.graph import Graph


@pytest.fixture
def empty_graph() -> Graph:
    return Graph()


@pytest.fixture
def filled_graph() -> Graph:
    return Graph({1: {2: 'Edge1'}, 2: {3: 'Edge2'}, 3: {}})


class TestGraph:

    def test_graph_base(self, empty_graph: Graph) -> None:

        assert empty_graph.name == 'Graph'
        assert empty_graph.space_complexity == 'V + E'
        assert empty_graph.is_directed is False
        assert empty_graph.is_multigraph is False
        assert empty_graph.n_ops == 0
        assert empty_graph.nodes == []
        assert empty_graph.edges == set()
        assert empty_graph.number_of_edges == 0
        assert empty_graph.number_of_nodes == 0

    def test_graph_from_adjacency_list(self, filled_graph: Graph) -> None:
        # assert filled_graph.n_ops == 0
        assert filled_graph.nodes == [1, 2, 3]
        assert filled_graph.edges == {(1, 2, 'Edge1'), (2, 3, 'Edge2')}
        assert filled_graph.number_of_edges == 2
        assert filled_graph.number_of_nodes == 3
        assert filled_graph.neighbors(1) == {2}
        assert filled_graph.degree(1) == 1
        assert filled_graph.neighbors(2) == {1, 3}
        assert filled_graph.degree(2) == 2
        assert filled_graph.neighbors(3) == {2}
        assert filled_graph.degree(3) == 1

    def test_graph_from_adjacency_list_nodes_filled(self) -> None:

        g = Graph({1: {2: 'Edge1', 3: 'Edge2', 4: 'Edge3'}})
        assert g._adjacency_list == {1: {2: 'Edge1', 3: 'Edge2', 4: 'Edge3'}, 2: {1: 'Edge1'}, 3: {1: 'Edge2'}, 4: {1: 'Edge3'}}
        assert g.nodes == [1, 2, 3, 4]
        assert g.number_of_nodes == 4
        assert g.edges == {(1, 2, 'Edge1'), (1, 3, 'Edge2'), (1, 4, 'Edge3')}
        assert g.number_of_edges == 3
