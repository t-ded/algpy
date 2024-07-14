import pytest

from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.tests.test_utils.example_base_graphs import ExampleDirectedSimpleGraph


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

        assert simple_digraph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert simple_digraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1)}
        assert simple_digraph.number_of_edges == 1
        assert simple_digraph.number_of_nodes == 2
        assert simple_digraph.adjacency_list == {'ExampleNodeA': {'ExampleNodeB': 1}, 'ExampleNodeB': {}}
        assert simple_digraph.adjacency_matrix == [[None, 1], [None, None]]

    def test_directed_simple_graph_add_nodes_edges(self, simple_digraph: ExampleDirectedSimpleGraph) -> None:

        assert simple_digraph.nodes == ['ExampleNodeA', 'ExampleNodeB']
        assert simple_digraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1)}
        assert simple_digraph.number_of_edges == 1
        assert simple_digraph.number_of_nodes == 2

        simple_digraph.add_node('ExampleNodeC')
        simple_digraph.add_edge(('ExampleNodeA', 'ExampleNodeC', 2))
        assert simple_digraph.nodes == ['ExampleNodeA', 'ExampleNodeB', 'ExampleNodeC']
        assert simple_digraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1), ('ExampleNodeA', 'ExampleNodeC', 2)}
        assert simple_digraph.number_of_edges == 2
        assert simple_digraph.number_of_nodes == 3

        simple_digraph.add_nodes_from(['ExampleNodeD', 'ExampleNodeE'])
        simple_digraph.add_edges_from({('ExampleNodeA', 'ExampleNodeD', 3), ('ExampleNodeA', 'ExampleNodeE', 4)})
        assert simple_digraph.nodes == ['ExampleNodeA', 'ExampleNodeB', 'ExampleNodeC', 'ExampleNodeD', 'ExampleNodeE']
        assert simple_digraph.edges == {('ExampleNodeA', 'ExampleNodeB', 1), ('ExampleNodeA', 'ExampleNodeC', 2), ('ExampleNodeA', 'ExampleNodeD', 3), ('ExampleNodeA', 'ExampleNodeE', 4)}
