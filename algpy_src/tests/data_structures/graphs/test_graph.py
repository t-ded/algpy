import pytest

from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge


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

    def test_graph_adding_edges(self, empty_graph: Graph) -> None:

        g = empty_graph

        g.add_edge((1, 2, None))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, None)}
        assert g.adjacency_list == {1: {2: None}, 2: {1: None}}
        assert g.adjacency_matrix == [[NoEdge(), None], [None, NoEdge()]]
        assert g.get_edge_data(1, 2) is None
        assert g.get_edge_data(2, 1) is None

        g.add_edge((1, 2, 'Edge1'))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, 'Edge1')}
        assert g.adjacency_list == {1: {2: 'Edge1'}, 2: {1: 'Edge1'}}
        assert g.adjacency_matrix == [[NoEdge(), 'Edge1'], ['Edge1', NoEdge()]]
        assert g.get_edge_data(1, 2) == 'Edge1'
        assert g.get_edge_data(2, 1) == 'Edge1'

        with pytest.raises(KeyError):
            g.get_edge_data(1, 3)
        with pytest.raises(KeyError):
            g.get_edge_data(3, 1)

    def test_graph_removing_edges(self, filled_graph: Graph) -> None:

        g = filled_graph
        with pytest.raises(ValueError):
            g.remove_edge(1, 2, 'MultiEdge1', 'MultiEdge2')
        assert g.edges == {(1, 2, 'Edge1'), (2, 3, 'Edge2')}
        g.remove_edge(1, 2)
        assert g.adjacency_list == {1: {}, 2: {3: 'Edge2'}, 3: {2: 'Edge2'}}
        assert g.edges == {(2, 3, 'Edge2')}
        g.remove_edge(2, 3, 'Edge1')
        assert g.adjacency_list == {1: {}, 2: {3: 'Edge2'}, 3: {2: 'Edge2'}}
        assert g.edges == {(2, 3, 'Edge2')}
        g.remove_edge(2, 3, 'Edge2')
        assert g.adjacency_list == {1: {}, 2: {}, 3: {}}
        assert g.edges == set()

    def test_graph_remove_edges_from(self, filled_graph: Graph) -> None:
        g = filled_graph
        g.remove_edges_from([(1, 2), (2, 3, 'Edge2'), (3, 4)])
        assert g.adjacency_list == {1: {}, 2: {}, 3: {}}
        assert g.edges == set()

    def test_graph_remove_node(self, filled_graph: Graph) -> None:
        g = filled_graph

        g.remove_node(1)
        assert g.adjacency_list == {2: {3: 'Edge2'}, 3: {2: 'Edge2'}}
        assert g.edges == {(2, 3, 'Edge2')}

        g.remove_node(1)
        assert g.adjacency_list == {2: {3: 'Edge2'}, 3: {2: 'Edge2'}}
        assert g.edges == {(2, 3, 'Edge2')}

        g.remove_node(2)
        assert g.adjacency_list == {3: {}}
        assert g.edges == set()

        g.remove_node(3)
        assert g.adjacency_list == {}
        assert g.edges == set()

    def test_graph_remove_nodes_from(self, filled_graph: Graph) -> None:
        g = filled_graph
        g.remove_nodes_from([1, 2, 3])
        assert g.adjacency_list == {}
        assert g.edges == set()
