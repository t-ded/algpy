import pytest

from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.tests.test_utils.example_base_graphs import ExampleDirectedSimpleGraph, ExampleSimpleGraph


@pytest.fixture
def simple_digraph() -> Graph:
    return ExampleDirectedSimpleGraph()


class TestDirectedSimpleGraph:

    def test_directed_simple_graph_base(self, simple_digraph: ExampleDirectedSimpleGraph) -> None:

        assert simple_digraph.name == 'Example Directed Simple Graph'
        assert simple_digraph.space_complexity == 'V + E'
        assert simple_digraph.is_directed is True
        assert simple_digraph.is_multigraph is False
        assert simple_digraph.n_ops == 0
        assert simple_digraph.nodes == []
        assert simple_digraph.edges == set()
        assert simple_digraph.number_of_edges == 0
        assert simple_digraph.number_of_nodes == 0

    def test_directed_simple_graph_add_nodes_edges(self, simple_digraph: ExampleDirectedSimpleGraph) -> None:

        simple_digraph.add_nodes_from(['ExampleNodeA', 'ExampleNodeB'])
        simple_digraph.add_edges_from({('ExampleNodeA', 'ExampleNodeB', 1)})
        assert simple_digraph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert simple_digraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1)}
        assert simple_digraph.number_of_edges == 1
        assert simple_digraph.number_of_nodes == 2
        assert simple_digraph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': 1}, 'ExampleNodeB': {}}
        assert simple_digraph.adjacency_matrix == [[None, 1], [None, None]]
        assert simple_digraph.neighbors('ExampleNodeA') == {'ExampleNodeB'}
        assert simple_digraph.degree('ExampleNodeA') == 1
        assert simple_digraph.neighbors('ExampleNodeB') == set()
        assert simple_digraph.degree('ExampleNodeB') == 0

        simple_digraph.add_node('ExampleNodeC')
        simple_digraph.add_edge(('ExampleNodeA', 'ExampleNodeC', 2))
        assert simple_digraph.nodes == ['ExampleNodeA', 'ExampleNodeB', 'ExampleNodeC']
        assert simple_digraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1), ('ExampleNodeA', 'ExampleNodeC', 2)}
        assert simple_digraph.number_of_edges == 2
        assert simple_digraph.number_of_nodes == 3
        assert simple_digraph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': 1, 'ExampleNodeC': 2}, 'ExampleNodeB': {}, 'ExampleNodeC': {}}
        assert simple_digraph.adjacency_matrix == [[None, 1, 2], [None, None, None], [None, None, None]]
        assert simple_digraph.neighbors('ExampleNodeA') == {'ExampleNodeB', 'ExampleNodeC'}
        assert simple_digraph.degree('ExampleNodeA') == 2
        assert simple_digraph.neighbors('ExampleNodeB') == set()
        assert simple_digraph.degree('ExampleNodeB') == 0
        assert simple_digraph.neighbors('ExampleNodeC') == set()
        assert simple_digraph.degree('ExampleNodeC') == 0


@pytest.fixture
def simple_graph() -> Graph:
    return ExampleSimpleGraph()


class TestSimpleGraph:

    def test_simple_graph_base(self, simple_graph: ExampleSimpleGraph) -> None:

        assert simple_graph.name == 'Example Simple Graph'
        assert simple_graph.space_complexity == 'V + E'
        assert simple_graph.is_directed is False
        assert simple_graph.is_multigraph is False
        assert simple_graph.n_ops == 0
        assert simple_graph.nodes == []
        assert simple_graph.edges == set()
        assert simple_graph.number_of_edges == 0
        assert simple_graph.number_of_nodes == 0

    def test_simple_graph_add_nodes_edges(self, simple_graph: ExampleSimpleGraph) -> None:

        simple_graph.add_nodes_from(['ExampleNodeA', 'ExampleNodeB'])
        simple_graph.add_edges_from({('ExampleNodeA', 'ExampleNodeB', 1)})
        assert simple_graph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert simple_graph.edges == {('ExampleNodeA', 'ExampleNodeB', 1)}
        assert simple_graph.number_of_edges == 1
        assert simple_graph.number_of_nodes == 2
        assert simple_graph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': 1}, 'ExampleNodeB': {'ExampleNodeA': 1}}
        assert simple_graph.adjacency_matrix == [[None, 1], [1, None]]
        assert simple_graph.neighbors('ExampleNodeA') == {'ExampleNodeB'}
        assert simple_graph.degree('ExampleNodeA') == 1
        assert simple_graph.neighbors('ExampleNodeB') == {'ExampleNodeA'}
        assert simple_graph.degree('ExampleNodeB') == 1

        simple_graph.add_node('ExampleNodeC')
        simple_graph.add_edge(('ExampleNodeA', 'ExampleNodeC', 2))
        assert simple_graph.nodes == ['ExampleNodeA', 'ExampleNodeB', 'ExampleNodeC']
        assert simple_graph.edges == {('ExampleNodeA', 'ExampleNodeB', 1), ('ExampleNodeA', 'ExampleNodeC', 2)}
        assert simple_graph.number_of_edges == 2
        assert simple_graph.number_of_nodes == 3
        assert simple_graph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': 1, 'ExampleNodeC': 2}, 'ExampleNodeB': {'ExampleNodeA': 1}, 'ExampleNodeC': {'ExampleNodeA': 2}}
        assert simple_graph.adjacency_matrix == [[None, 1, 2], [1, None, None], [2, None, None]]
        assert simple_graph.neighbors('ExampleNodeA') == {'ExampleNodeB', 'ExampleNodeC'}
        assert simple_graph.degree('ExampleNodeA') == 2
        assert simple_graph.neighbors('ExampleNodeB') == {'ExampleNodeA'}
        assert simple_graph.degree('ExampleNodeB') == 1
        assert simple_graph.neighbors('ExampleNodeC') == {'ExampleNodeA'}
        assert simple_graph.degree('ExampleNodeC') == 1
