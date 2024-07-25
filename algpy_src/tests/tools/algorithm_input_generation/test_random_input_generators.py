import pytest

from algpy_src.algorithms.graph_algorithms.traversal.bfs import BreadthFirstSearch
from algpy_src.algorithms.sorting.bubble_sort import BubbleSort
from algpy_src.algorithms.sorting.insertion_sort import InsertionSort
from algpy_src.base.constants import TEST_SEED, GraphSize
from algpy_src.tests.test_utils.example_base_objects import ExampleAlgorithm, ExampleSortingAlgorithm
from algpy_src.tools.algorithm_input_generation.random_input_generators import get_generator, RandomInputGeneratorSortingAlgorithm, RandomInputGeneratorGraphTraversalAlgorithm


def test_get_generators() -> None:
    assert get_generator(InsertionSort()) == RandomInputGeneratorSortingAlgorithm
    assert get_generator(BubbleSort()) == RandomInputGeneratorSortingAlgorithm
    assert get_generator(ExampleSortingAlgorithm()) == RandomInputGeneratorSortingAlgorithm
    assert get_generator(BreadthFirstSearch()) == RandomInputGeneratorGraphTraversalAlgorithm
    with pytest.raises(ValueError):
        get_generator(ExampleAlgorithm())


def test_random_input_generators():
    assert list(get_generator(ExampleSortingAlgorithm())(TEST_SEED).generate_random_input(input_size=10)) == [2, 1, 5, 4, 4, 3, 2, 9, 2, 10]
    assert get_generator(BreadthFirstSearch())(TEST_SEED).generate_random_input(input_size=GraphSize(*(5, 5))).adjacency_list == {
        0: {1: None, 4: None, 2: None}, 1: {0: None, 2: None, 4: None}, 2: {1: None, 0: None}, 3: {}, 4: {0: None, 1: None}
    }
