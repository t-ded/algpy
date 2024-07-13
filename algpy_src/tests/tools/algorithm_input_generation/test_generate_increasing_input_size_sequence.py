from typing import Iterable

import pytest

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.sorting.bubble_sort import BubbleSort
from algpy_src.algorithms.sorting.insertion_sort import InsertionSort
from algpy_src.base.constants import InputSize
from algpy_src.tests.test_utils.example_base_objects import ExampleAlgorithm
from algpy_src.tools.algorithm_input_generation.generate_increasing_input_size_sequence import generate_increasing_input_size_sequence


@pytest.mark.parametrize(
    ('algorithm', 'max_input_size', 'sequence_length', 'expected_sequence'),
    [
        pytest.param(BubbleSort(), 100_000, 2, [1, 100_000], id='Bubble sort generate increasing input size sequence with 2 elements'),
        pytest.param(BubbleSort(), 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Bubble sort generate increasing input size sequence with 10 elements'),
        pytest.param(InsertionSort(), 100_000, 2, [1, 100_000], id='Insertion sort generate increasing input size sequence with 10 elements'),
        pytest.param(InsertionSort(), 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Bubble sort generate increasing input size sequence with 10 elements'),
    ]
)
def test_generate_valid_increasing_input_size_sequence(algorithm: Algorithm, max_input_size: InputSize, sequence_length: int, expected_sequence: Iterable[InputSize]) -> None:
    assert generate_increasing_input_size_sequence(algorithm, max_input_size, sequence_length) == expected_sequence


def test_fails_on_base_algorithms() -> None:
    with pytest.raises(ValueError):
        generate_increasing_input_size_sequence(ExampleAlgorithm(), 10, 10)
