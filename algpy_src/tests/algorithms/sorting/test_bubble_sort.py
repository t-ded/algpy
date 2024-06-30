from typing import Iterable

import pytest

from algpy_src.algorithms.sorting.bubble_sort import BubbleSort
from algpy_src.base.constants import TEST_SEED, Comparable


@pytest.fixture()
def bs():
    return BubbleSort()


def test_bubble_sort_base(bs):
    assert bs.name == 'Bubble Sort'
    assert bs.best_case_time_complexity == 'n'
    assert bs.best_case_description == 'fully sorted array'
    assert bs.average_case_time_complexity == 'n^2'
    assert bs.worst_case_time_complexity == 'n^2'
    assert bs.worst_case_description == 'fully unsorted array'
    assert bs.space_complexity == '1'
    assert bs.generate_increasing_input_size_sequence(n=5) == [1, 10, 100, 1_000, 10_000]
    assert bs.generate_random_input(input_size=10, seed=TEST_SEED) == [2, 1, 5, 4, 4, 3, 2, 9, 2, 10]
    assert bs.generate_worst_case(10, descending=True) == range(1, 11)
    assert bs.generate_worst_case(10, descending=False) == range(10, 0, -1)


def test_worst_case(bs):
    worst_case_ascending_sort = bs.generate_worst_case(10, descending=False)
    assert bs.n_ops == 0
    assert bs.run_algorithm(worst_case_ascending_sort, descending=False) == list(range(1, 11))
    assert bs.n_ops == 45
    worst_case_descending_sort = bs.generate_worst_case(10, descending=True)
    assert bs.run_algorithm(worst_case_descending_sort, descending=True) == list(range(10, 0, -1))
    assert bs.n_ops == 45


@pytest.mark.parametrize(
    ('input_instance', 'descending', 'expected_result', 'expected_n_ops'),
    [
        pytest.param([], True, [], 0, id='Empty list'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 45, id='Worst case'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, id='Best case'),
        pytest.param([1, 1, 1, 1, 1], True, [1, 1, 1, 1, 1], 0, id='Stable descending'),
        pytest.param([1, 1, 1, 1, 1], False, [1, 1, 1, 1, 1], 0, id='Stable ascending'),
        pytest.param((4, 2, 0, 1, 3), True, [4, 3, 2, 1, 0], 4, id='Accepts tuple'),
        pytest.param(range(1, 11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, id='Accepts range'),
        pytest.param((lambda x: (i for i in range(1, x)))(11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, id='Accepts generator'),
        pytest.param(['a', 'e', 'i', 'o', 'u'], True, ['u', 'o', 'i', 'e', 'a'], 10, id='Accepts comparable strings'),
        pytest.param([(0, 1), (1, 1), (1, 2)], True, [(1, 2), (1, 1), (0, 1)], 3, id='Accepts comparable tuples'),
    ]
)
def test_bubble_sort_run_algorithm(bs, input_instance: Iterable[Comparable], descending: bool, expected_result: list[Comparable], expected_n_ops: int):
    assert bs.run_algorithm(input_instance, descending) == expected_result
    assert bs.n_ops == expected_n_ops
