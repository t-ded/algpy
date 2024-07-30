import pytest

from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge
from algpy_src.data_structures.graphs.multigraph import MultiGraph


@pytest.fixture
def empty_multigraph() -> MultiGraph:
    return MultiGraph()


@pytest.fixture
def filled_multigraph() -> MultiGraph:
    return MultiGraph({1: {2: {'MultiEdge1', 'MultiEdge2'}}, 2: {3: {'MultiEdge3'}}, 3: {}})


class TestMultiGraph:

    def test_multigraph_base(self, empty_multigraph: MultiGraph) -> None:

        assert empty_multigraph.name == 'MultiGraph'
        assert empty_multigraph.space_complexity == 'V + E'
        assert empty_multigraph.is_directed is False
        assert empty_multigraph.is_multigraph is True
        assert empty_multigraph.n_ops == 0
        assert empty_multigraph.nodes == []
        assert empty_multigraph.edges == set()
        assert empty_multigraph.number_of_edges == 0
        assert empty_multigraph.number_of_nodes == 0

    def test_multigraph_from_adjacency_list(self, filled_multigraph: MultiGraph) -> None:
        # assert filled_multigraph.n_ops == 0
        assert filled_multigraph.nodes == [1, 2, 3]
        assert filled_multigraph.edges == {(1, 2, 'MultiEdge1'), (1, 2, 'MultiEdge2'), (2, 3, 'MultiEdge3')}
        assert filled_multigraph.number_of_edges == 3
        assert filled_multigraph.number_of_nodes == 3
        assert filled_multigraph.nodes == [1, 2, 3]
        assert filled_multigraph.neighbors(1) == {2}
        assert filled_multigraph.indegree(1) == 2
        assert filled_multigraph.outdegree(1) == 2
        assert filled_multigraph.degree(1) == 2
        assert filled_multigraph.neighbors(2) == {1, 3}
        assert filled_multigraph.indegree(2) == 3
        assert filled_multigraph.outdegree(2) == 3
        assert filled_multigraph.degree(2) == 3
        assert filled_multigraph.neighbors(3) == {2}
        assert filled_multigraph.indegree(3) == 1
        assert filled_multigraph.outdegree(3) == 1
        assert filled_multigraph.degree(3) == 1

    def test_multigraph_from_adjacency_list_nodes_filled(self) -> None:

        g = MultiGraph({1: {2: {'MultiEdge1'}, 3: {'MultiEdge2'}, 4: {'MultiEdge3'}}})
        assert g._adjacency_list == {1: {2: {'MultiEdge1'}, 3: {'MultiEdge2'}, 4: {'MultiEdge3'}}, 2: {1: {'MultiEdge1'}}, 3: {1: {'MultiEdge2'}}, 4: {1: {'MultiEdge3'}}}
        assert g.nodes == [1, 2, 3, 4]
        assert g.number_of_nodes == 4
        assert g.edges == {(1, 2, 'MultiEdge1'), (1, 3, 'MultiEdge2'), (1, 4, 'MultiEdge3')}
        assert g.number_of_edges == 3

    def test_multigraph_adjacency_list_transposed(self, filled_multigraph: MultiGraph) -> None:
        assert filled_multigraph.adjacency_list_transposed == filled_multigraph.adjacency_list

    def test_multigraph_adding_edges(self, empty_multigraph: MultiGraph) -> None:

        g = empty_multigraph

        g.add_edge((1, 2, None))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, None)}
        assert g.adjacency_list == {1: {2: {None}}, 2: {1: {None}}}
        assert g.adjacency_matrix == [[NoEdge(), {None}], [{None}, NoEdge()]]
        assert g.get_edge_data(1, 2) == {None}

        g.add_edge((1, 2, 'MultiEdge1'))
        g.add_edge((1, 2, 'MultiEdge2'))
        assert g.nodes == [1, 2]
        assert g.edges == {(1, 2, 'MultiEdge1'), (1, 2, 'MultiEdge2'), (1, 2, None)}
        assert g.adjacency_list == {1: {2: {None, 'MultiEdge1', 'MultiEdge2'}}, 2: {1: {None, 'MultiEdge1', 'MultiEdge2'}}}
        assert g.adjacency_matrix == [[NoEdge(), {None, 'MultiEdge1', 'MultiEdge2'}], [{None, 'MultiEdge1', 'MultiEdge2'}, NoEdge()]]
        assert g.get_edge_data(1, 2) == {None, 'MultiEdge1', 'MultiEdge2'}

        with pytest.raises(KeyError):
            g.get_edge_data(1, 3)
        with pytest.raises(KeyError):
            g.get_edge_data(3, 1)

    def test_multigraph_removing_edges(self, filled_multigraph: MultiGraph) -> None:

        g = filled_multigraph
        g.add_edge((2, 3, 'MultiEdge4'))
        assert g.adjacency_list == {1: {2: {'MultiEdge1', 'MultiEdge2'}}, 2: {1: {'MultiEdge1', 'MultiEdge2'}, 3: {'MultiEdge3', 'MultiEdge4'}}, 3: {2: {'MultiEdge3', 'MultiEdge4'}}}
        assert g.edges == {(1, 2, 'MultiEdge1'), (1, 2, 'MultiEdge2'), (2, 3, 'MultiEdge3'), (2, 3, 'MultiEdge4')}
        g.remove_edge(1, 2)
        assert g.adjacency_list == {1: {}, 2: {3: {'MultiEdge3', 'MultiEdge4'}}, 3: {2: {'MultiEdge3', 'MultiEdge4'}}}
        assert g.edges == {(2, 3, 'MultiEdge3'), (2, 3, 'MultiEdge4')}
        g.remove_edge(2, 3, 'MultiEdge5')
        assert g.adjacency_list == {1: {}, 2: {3: {'MultiEdge3', 'MultiEdge4'}}, 3: {2: {'MultiEdge3', 'MultiEdge4'}}}
        assert g.edges == {(2, 3, 'MultiEdge3'), (2, 3, 'MultiEdge4')}
        g.remove_edge(2, 3, 'MultiEdge3')
        assert g.adjacency_list == {1: {}, 2: {3: {'MultiEdge4'}}, 3: {2: {'MultiEdge4'}}}
        assert g.edges == {(2, 3, 'MultiEdge4')}

    def test_multidigraph_remove_edges_from(self, filled_multigraph: MultiGraph) -> None:
        g = filled_multigraph
        g.remove_edges_from([(1, 2, 'MultiEdge1'), (2, 3, 'MultiEdge3'), (3, 4)])
        assert g.adjacency_list == {1: {2: {'MultiEdge2'}}, 2: {1: {'MultiEdge2'}}, 3: {}}
        assert g.edges == {(1, 2, 'MultiEdge2')}

    def test_multidigraph_remove_node(self, filled_multigraph: MultiGraph) -> None:
        g = filled_multigraph

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

    def test_multidigraph_remove_nodes_from(self, filled_multigraph: MultiGraph) -> None:
        g = filled_multigraph
        g.remove_nodes_from([1, 2, 3])
        assert g.adjacency_list == {}
        assert g.edges == set()
