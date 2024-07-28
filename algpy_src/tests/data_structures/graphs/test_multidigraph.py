import pytest

from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge
from algpy_src.data_structures.graphs.multidigraph import MultiDiGraph


@pytest.fixture
def empty_multidigraph() -> MultiDiGraph:
    return MultiDiGraph()


@pytest.fixture
def filled_multidigraph() -> MultiDiGraph:
    return MultiDiGraph({1: {2: {'MultiEdge1', 'MultiEdge2'}}, 2: {3: {'MultiEdge3'}}, 3: {}})


class TestMultiDiGraph:

    def test_multidigraph_base(self, empty_multidigraph: MultiDiGraph) -> None:

        assert empty_multidigraph.name == 'MultiDiGraph'
        assert empty_multidigraph.space_complexity == 'V + E'
        assert empty_multidigraph.is_directed is True
        assert empty_multidigraph.is_multigraph is True
        assert empty_multidigraph.n_ops == 0
        assert empty_multidigraph.nodes == []
        assert empty_multidigraph.edges == set()
        assert empty_multidigraph.number_of_edges == 0
        assert empty_multidigraph.number_of_nodes == 0

    def test_multidigraph_from_adjacency_list(self, filled_multidigraph: MultiDiGraph) -> None:
        # assert filled_multidigraph.n_ops == 0
        assert filled_multidigraph.nodes == [1, 2, 3]
        assert filled_multidigraph.edges == {(1, 2, 'MultiEdge1'), (1, 2, 'MultiEdge2'), (2, 3, 'MultiEdge3')}
        assert filled_multidigraph.number_of_edges == 3
        assert filled_multidigraph.number_of_nodes == 3
        assert filled_multidigraph.nodes == [1, 2, 3]
        assert filled_multidigraph.neighbors(1) == {2}
        assert filled_multidigraph.indegree(1) == 0
        assert filled_multidigraph.outdegree(1) == 2
        assert filled_multidigraph.degree(1) == 2
        assert filled_multidigraph.neighbors(2) == {3}
        assert filled_multidigraph.indegree(2) == 2
        assert filled_multidigraph.outdegree(2) == 1
        assert filled_multidigraph.degree(2) == 3
        assert filled_multidigraph.neighbors(3) == set()
        assert filled_multidigraph.indegree(3) == 1
        assert filled_multidigraph.outdegree(3) == 0
        assert filled_multidigraph.degree(3) == 1

    def test_multidigraph_from_adjacency_list_nodes_filled(self) -> None:

        g = MultiDiGraph({1: {2: {'MultiEdge1'}, 3: {'MultiEdge2'}, 4: {'MultiEdge3'}}})
        assert g._adjacency_list == {1: {2: {'MultiEdge1'}, 3: {'MultiEdge2'}, 4: {'MultiEdge3'}}, 2: {}, 3: {}, 4: {}}
        assert g.nodes == [1, 2, 3, 4]
        assert g.number_of_nodes == 4
        assert g.edges == {(1, 2, 'MultiEdge1'), (1, 3, 'MultiEdge2'), (1, 4, 'MultiEdge3')}
        assert g.number_of_edges == 3

    def test_multidigraph_adding_edges(self, empty_multidigraph: MultiDiGraph) -> None:

        g = empty_multidigraph

        g.add_edge((1, 2, None))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, None)}
        assert g.adjacency_list == {1: {2: {None}}, 2: {}}
        assert g.adjacency_matrix == [[NoEdge(), {None}], [NoEdge(), NoEdge()]]
        assert g.get_edge_data(1, 2) == {None}

        g.add_edge((1, 2, 'MultiEdge1'))
        g.add_edge((1, 2, 'MultiEdge2'))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, 'MultiEdge1'), (1, 2, 'MultiEdge2'), (1, 2, None)}
        assert g.adjacency_list == {1: {2: {None, 'MultiEdge1', 'MultiEdge2'}}, 2: {}}
        assert g.adjacency_matrix == [[NoEdge(), {None, 'MultiEdge1', 'MultiEdge2'}], [NoEdge(), NoEdge()]]
        assert g.get_edge_data(1, 2) == {None, 'MultiEdge1', 'MultiEdge2'}

        with pytest.raises(KeyError):
            g.get_edge_data(1, 3)
        with pytest.raises(KeyError):
            g.get_edge_data(3, 1)
        assert g.get_edge_data(2, 1) == NoEdge()

    def test_multidigraph_removing_edges(self, filled_multidigraph: MultiDiGraph) -> None:

        g = filled_multidigraph
        g.add_edge((2, 3, 'MultiEdge4'))
        assert g.edges == {(1, 2, 'MultiEdge1'), (1, 2, 'MultiEdge2'), (2, 3, 'MultiEdge3'), (2, 3, 'MultiEdge4')}
        g.remove_edge(1, 2)
        assert g.adjacency_list == {1: {}, 2: {3: {'MultiEdge3', 'MultiEdge4'}}, 3: {}}
        assert g.edges == {(2, 3, 'MultiEdge3'), (2, 3, 'MultiEdge4')}
        g.remove_edge(2, 3, 'MultiEdge5')
        assert g.adjacency_list == {1: {}, 2: {3: {'MultiEdge3', 'MultiEdge4'}}, 3: {}}
        assert g.edges == {(2, 3, 'MultiEdge3'), (2, 3, 'MultiEdge4')}
        g.remove_edge(2, 3, 'MultiEdge3')
        assert g.adjacency_list == {1: {}, 2: {3: {'MultiEdge4'}}, 3: {}}
        assert g.edges == {(2, 3, 'MultiEdge4')}

    def test_multidigraph_remove_edges_from(self, filled_multidigraph: MultiDiGraph) -> None:
        g = filled_multidigraph
        g.remove_edges_from([(1, 2, 'MultiEdge1'), (2, 3, 'MultiEdge3'), (3, 4)])
        assert g.adjacency_list == {1: {2: {'MultiEdge2'}}, 2: {}, 3: {}}
        assert g.edges == {(1, 2, 'MultiEdge2')}

    def test_multidigraph_remove_node(self, filled_multidigraph: MultiDiGraph) -> None:
        g = filled_multidigraph

        g.remove_node(2)
        assert g.adjacency_list == {1: {}, 3: {}}
        assert g.edges == set()

        g.remove_node(2)
        assert g.adjacency_list == {1: {}, 3: {}}
        assert g.edges == set()

        g.remove_node(3)
        assert g.adjacency_list == {1: {}}
        assert g.edges == set()

        g.remove_node(1)
        assert g.adjacency_list == {}
        assert g.edges == set()

    def test_multidigraph_remove_nodes_from(self, filled_multidigraph: MultiDiGraph) -> None:
        g = filled_multidigraph
        g.remove_nodes_from([1, 2, 3])
        assert g.adjacency_list == {}
        assert g.edges == set()
