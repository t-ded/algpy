import pytest

from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.tests.test_utils.example_base_graphs import ExampleDirectedMultigraph, ExampleMultigraph


@pytest.fixture
def multidigraph() -> Graph:
    return ExampleDirectedMultigraph()


class TestDirectedMultigraph:

    def test_directed_multigraph_base(self, multidigraph: ExampleDirectedMultigraph) -> None:

        assert multidigraph.name == 'Example Directed Multigraph'
        assert multidigraph.space_complexity == 'V + E'
        assert multidigraph.is_directed is True
        assert multidigraph.is_multigraph is True
        assert multidigraph.n_ops == 0
        assert multidigraph.nodes == []
        assert multidigraph.edges == set()
        assert multidigraph.number_of_edges == 0
        assert multidigraph.number_of_nodes == 0

    def test_directed_multigraph_add_nodes_edges(self, multidigraph: ExampleDirectedMultigraph) -> None:

        multidigraph.add_nodes_from(['ExampleNodeA', 'ExampleNodeB'])
        multidigraph.add_edges_from({('ExampleNodeA', 'ExampleNodeB', 1)})
        assert multidigraph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert multidigraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1)}
        assert multidigraph.number_of_edges == 1
        assert multidigraph.number_of_nodes == 2
        assert multidigraph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': [1]}, 'ExampleNodeB': {}}
        assert multidigraph.adjacency_matrix == [[None, [1]], [None, None]]
        assert multidigraph.neighbors('ExampleNodeA') == {'ExampleNodeB'}
        assert multidigraph.degree('ExampleNodeA') == 1
        assert multidigraph.neighbors('ExampleNodeB') == set()
        assert multidigraph.degree('ExampleNodeB') == 0

        multidigraph.add_edge(('ExampleNodeA', 'ExampleNodeB', 2))
        assert multidigraph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert multidigraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1), ('ExampleNodeA', 'ExampleNodeB', 2)}
        assert multidigraph.number_of_edges == 2
        assert multidigraph.number_of_nodes == 2
        assert multidigraph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': [1, 2]}, 'ExampleNodeB': {}}
        assert multidigraph.adjacency_matrix == [[None, [1, 2]], [None, None]]
        assert multidigraph.neighbors('ExampleNodeA') == {'ExampleNodeB'}
        assert multidigraph.degree('ExampleNodeA') == 2
        assert multidigraph.neighbors('ExampleNodeB') == set()
        assert multidigraph.degree('ExampleNodeB') == 0


@pytest.fixture
def multigraph() -> Graph:
    return ExampleMultigraph()


class TestSimpleGraph:

    def test_multigraph_base(self, multigraph: ExampleMultigraph) -> None:

        assert multigraph.name == 'Example Multigraph'
        assert multigraph.space_complexity == 'V + E'
        assert multigraph.is_directed is False
        assert multigraph.is_multigraph is True
        assert multigraph.n_ops == 0
        assert multigraph.nodes == []
        assert multigraph.edges == set()
        assert multigraph.number_of_edges == 0
        assert multigraph.number_of_nodes == 0

    def test_multigraph_add_nodes_edges(self, multigraph: ExampleMultigraph) -> None:

        multigraph.add_nodes_from(['ExampleNodeA', 'ExampleNodeB'])
        multigraph.add_edges_from({('ExampleNodeA', 'ExampleNodeB', 1)})
        assert multigraph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert multigraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1)}
        assert multigraph.number_of_edges == 1
        assert multigraph.number_of_nodes == 2
        assert multigraph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': [1]}, 'ExampleNodeB': {'ExampleNodeA': [1]}}
        assert multigraph.adjacency_matrix == [[None, [1]], [[1], None]]
        assert multigraph.neighbors('ExampleNodeA') == {'ExampleNodeB'}
        assert multigraph.degree('ExampleNodeA') == 1
        assert multigraph.neighbors('ExampleNodeB') == {'ExampleNodeA'}
        assert multigraph.degree('ExampleNodeB') == 1

        multigraph.add_edge(('ExampleNodeA', 'ExampleNodeB', 2))
        assert multigraph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert multigraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1), ('ExampleNodeA', 'ExampleNodeB', 2)}
        assert multigraph.number_of_edges == 2
        assert multigraph.number_of_nodes == 2
        assert multigraph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': [1, 2]}, 'ExampleNodeB': {'ExampleNodeA': [1, 2]}}
        assert multigraph.adjacency_matrix == [[None, [1, 2]], [[1, 2], None]]
        assert multigraph.neighbors('ExampleNodeA') == {'ExampleNodeB'}
        assert multigraph.degree('ExampleNodeA') == 2
        assert multigraph.neighbors('ExampleNodeB') == {'ExampleNodeA'}
        assert multigraph.degree('ExampleNodeB') == 2
