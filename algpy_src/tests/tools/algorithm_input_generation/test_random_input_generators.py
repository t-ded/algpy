import pytest

from algpy_src.algorithms.graph_algorithms.message_passing.relational_classification import RelationalClassificationAlgorithm
from algpy_src.algorithms.graph_algorithms.traversal.bfs import BreadthFirstSearch
from algpy_src.algorithms.graph_algorithms.traversal.dfs import DepthFirstSearch
from algpy_src.algorithms.graph_algorithms.traversal.shortest_paths.simple_dijkstra import DijkstraShortestPathsAlgorithm
from algpy_src.algorithms.load_balancing.round_robin import RoundRobinAlgorithm
from algpy_src.algorithms.sorting.bubble_sort import BubbleSort
from algpy_src.algorithms.sorting.insertion_sort import InsertionSort
from algpy_src.base.constants import TEST_SEED, GraphSize, LoadBalancingTaskSize
from algpy_src.data_structures.graphs.base_graph import BaseGraph
from algpy_src.data_structures.graphs.feature_graph import FeatureGraph
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.system_design.load_task import LoadTask
from algpy_src.data_structures.system_design.server import Server
from algpy_src.tests.test_utils.example_base_objects import ExampleAlgorithm, ExampleSortingAlgorithm
from algpy_src.tools.algorithm_input_generation.random_input_generators import get_generator, RandomInputGeneratorSortingAlgorithm, RandomInputGeneratorGraphTraversalAlgorithm, \
    RandomInputGeneratorGraphRelationalClassificationAlgorithm, RandomInputGeneratorLoadBalancingAlgorithms


@pytest.fixture
def graph_traversal_random_input() -> BaseGraph:
    return Graph(adjacency_list={0: {1: None, 4: None, 2: None}, 1: {0: None, 2: None, 4: None}, 2: {1: None, 0: None}, 3: {}, 4: {0: None, 1: None}})


def test_get_generators() -> None:

    # Base or Example Algorithms
    with pytest.raises(ValueError):
        get_generator(ExampleAlgorithm())

    # Sorting Algorithms
    assert get_generator(InsertionSort()) == RandomInputGeneratorSortingAlgorithm
    assert get_generator(BubbleSort()) == RandomInputGeneratorSortingAlgorithm
    assert get_generator(ExampleSortingAlgorithm()) == RandomInputGeneratorSortingAlgorithm

    # Graph Traversal Algorithms
    assert get_generator(BreadthFirstSearch()) == RandomInputGeneratorGraphTraversalAlgorithm
    assert get_generator(DepthFirstSearch()) == RandomInputGeneratorGraphTraversalAlgorithm
    assert get_generator(DijkstraShortestPathsAlgorithm()) == RandomInputGeneratorGraphTraversalAlgorithm

    # Message Passing Algorithms
    assert get_generator(RelationalClassificationAlgorithm()) == RandomInputGeneratorGraphRelationalClassificationAlgorithm

    # Load Balancing Algorithms
    assert get_generator(RoundRobinAlgorithm()) == RandomInputGeneratorLoadBalancingAlgorithms


def test_random_input_generators(graph_traversal_random_input: BaseGraph) -> None:

    # Base or Example Algorithms

    # Sorting Algorithms
    assert list(get_generator(ExampleSortingAlgorithm())(TEST_SEED).generate_random_input(input_size=10)) == [2, 1, 5, 4, 4, 3, 2, 9, 2, 10]

    # Graph Traversal Algorithms
    assert get_generator(BreadthFirstSearch())(TEST_SEED).generate_random_input(input_size=GraphSize(*(5, 5))) == graph_traversal_random_input
    assert get_generator(DepthFirstSearch())(TEST_SEED).generate_random_input(input_size=GraphSize(*(5, 5))) == graph_traversal_random_input
    assert get_generator(DijkstraShortestPathsAlgorithm())(TEST_SEED).generate_random_input(input_size=GraphSize(*(5, 5))) == graph_traversal_random_input

    # Message Passing Algorithms
    assert get_generator(RelationalClassificationAlgorithm())(TEST_SEED).generate_random_input(input_size=GraphSize(*(20, 20))) == FeatureGraph(
        adjacency_list={
            0: {18: None, 12: None}, 1: {14: None, 3: None, 8: None}, 2: {15: None}, 3: {1: None, 8: None, 9: None},
            4: {10: None, 9: None}, 5: {17: None, 13: None, 18: None}, 6: {}, 7: {}, 8: {3: None, 1: None},
            9: {12: None, 16: None, 4: None, 3: None}, 10: {4: None, 13: None}, 11: {18: None, 16: None},
            12: {9: None, 0: None}, 13: {5: None, 10: None, 14: None}, 14: {1: None, 13: None}, 15: {2: None, 16: None},
            16: {9: None, 11: None, 15: None}, 17: {5: None}, 18: {11: None, 0: None, 5: None}, 19: {}
        },
        node_features={
            0: 0, 1: 0, 3: 0, 4: 0, 7: 0, 8: 1, 10: 0,
            11: 0, 12: 1, 15: 0, 18: 1, 19: 1
        }
    )

    # Load Balancing Algorithms
    assert get_generator(RoundRobinAlgorithm())(TEST_SEED).generate_random_input(input_size=LoadBalancingTaskSize(*(5, 1))) == (
        [
            LoadTask(identifier='random_0', size=0.0), LoadTask(identifier='random_1', size=0.0), LoadTask(identifier='random_2', size=0.0),
            LoadTask(identifier='random_3', size=0.0), LoadTask(identifier='random_4', size=0.0)
        ],
        [Server(identifier='random_0')]
    )
