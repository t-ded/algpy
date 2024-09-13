from typing import Iterable

import pytest

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.backtracking.backtracking import BacktrackingAlgorithm
from algpy_src.algorithms.graph_algorithms.message_passing.relational_classification import RelationalClassificationAlgorithm
from algpy_src.algorithms.graph_algorithms.network_flow.edmonds_karp import EdmondsKarpAlgorithm
from algpy_src.algorithms.graph_algorithms.network_flow.ford_fulkerson import FordFulkersonAlgorithm, FordFulkersonGraphSize
from algpy_src.algorithms.graph_algorithms.traversal.bfs import BreadthFirstSearch
from algpy_src.algorithms.graph_algorithms.traversal.dfs import DepthFirstSearch
from algpy_src.algorithms.load_balancing.round_robin import RoundRobinAlgorithm
from algpy_src.algorithms.searching.binary_search import BinarySearch
from algpy_src.algorithms.sorting.bubble_sort import BubbleSort
from algpy_src.algorithms.sorting.insertion_sort import InsertionSort
from algpy_src.algorithms.sorting.merge_sort import MergeSort
from algpy_src.base.constants import InputSize, GraphSize, LoadBalancingTaskSize
from algpy_src.tests.test_utils.example_base_objects import ExampleAlgorithm
from algpy_src.tools.algorithm_input_generation.generate_increasing_input_size_sequence import generate_increasing_input_size_sequence


@pytest.mark.parametrize(
    ('algorithm', 'max_input_size', 'sequence_length', 'expected_sequence'),
    [
        pytest.param(BubbleSort(), 100_000, 2, [1, 100_000], id='Bubble sort generate increasing input size sequence with 2 elements'),
        pytest.param(BubbleSort(), 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Bubble sort generate increasing input size sequence with 10 elements'),
        pytest.param(InsertionSort(), 100_000, 2, [1, 100_000], id='Insertion sort generate increasing input size sequence with 2 elements'),
        pytest.param(InsertionSort(), 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Insertion sort generate increasing input size sequence with 10 elements'),
        pytest.param(MergeSort(), 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Merge sort generate increasing input size sequence with 10 elements'),
        pytest.param(BinarySearch(), 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Binary search generate increasing input size sequence with 10 elements'),
        pytest.param(BreadthFirstSearch(), GraphSize(*(10, 10)), 10, [(i, i) for i in range(1, 11)],
                     id='Breadth First Search generate increasing input size sequence with up to 10 nodes and edges with same counts'),
        pytest.param(BreadthFirstSearch(), GraphSize(*(100, 10)), 10, [(10 * (i - 1) + i, i) for i in range(1, 11)],
                     id='Breadth First Search generate increasing input size sequence with up to 10 nodes and edges with more nodes'),
        pytest.param(BreadthFirstSearch(), GraphSize(*(10, 100)), 10, [(i, 10 * (i - 1) + i) for i in range(1, 11)],
                     id='Breadth First Search generate increasing input size sequence with up to 10 nodes and edges with more edges'),
        pytest.param(DepthFirstSearch(), GraphSize(*(10, 10)), 10, [(i, i) for i in range(1, 11)],
                     id='Depth First Search generate increasing input size sequence with up to 10 nodes and edges with same counts'),
        pytest.param(RelationalClassificationAlgorithm(), GraphSize(*(10, 10)), 10, [(i, i) for i in range(1, 11)],
                     id='Relational classification algorithm generate increasing input size sequence with up to 10 nodes and edges with same counts'),
        pytest.param(FordFulkersonAlgorithm(), FordFulkersonGraphSize(*(10, 100)), 10, [(i, 10 * (i - 1) + i) for i in range(1, 11)],
                     id="Ford-Fulkerson's algorithm generate increasing input size sequence with up to 10 edges with up to 100 upper bound"),
        pytest.param(EdmondsKarpAlgorithm(), FordFulkersonGraphSize(*(10, 100)), 10, [(i, 10 * (i - 1) + i) for i in range(1, 11)],
                     id="Edmonds-Karp's algorithm generate increasing input size sequence with up to 10 edges with up to 100 upper bound"),
        pytest.param(BacktrackingAlgorithm(), 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Backtracking generate increasing input size sequence with 10 elements'),
        pytest.param(RoundRobinAlgorithm(), LoadBalancingTaskSize(*(10, 10)), 10, [(i, i) for i in range(1, 11)],
                     id='Round Robin load balancing algorithm generate increasing input size sequence with up to 10 tasks and servers with same counts'),
    ]
)
def test_generate_valid_increasing_input_size_sequence(algorithm: Algorithm, max_input_size: InputSize, sequence_length: int, expected_sequence: Iterable[InputSize]) -> None:
    assert generate_increasing_input_size_sequence(algorithm, max_input_size, sequence_length) == expected_sequence


def test_fails_on_base_algorithms() -> None:
    with pytest.raises(ValueError):
        generate_increasing_input_size_sequence(ExampleAlgorithm(), 10, 10)
