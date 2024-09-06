from typing import Iterable

import pytest

from algpy_src.algorithms.sorting.merge_sort import MergeSort
from algpy_src.base.constants import Comparable


@pytest.fixture()
def ms() -> MergeSort:
    return MergeSort()


def test_merge_sort_base(ms: MergeSort) -> None:
    assert ms.name == 'Merge Sort'
    assert ms.best_case_time_complexity == 'n * log(n)'
    assert ms.best_case_description == 'a fully sorted array'
    assert ms.average_case_time_complexity == 'n * log(n)'
    assert ms.worst_case_time_complexity == 'n * log(n)'
    assert ms.worst_case_description == 'two sorted subsections'
    assert ms.space_complexity == 'n'
    assert ms.get_worst_case_arguments(10) == {'input_instance': [0, 2, 4, 6, 8, 1, 3, 5, 7, 9], 'descending': True}


def test_worst_case(ms: MergeSort) -> None:
    assert ms.n_comparisons == 0
    assert ms.n_swaps == 0
    worst_case_args = ms.get_worst_case_arguments(10)
    assert ms.run_algorithm(**worst_case_args) == (True, list(range(9, -1, -1)))
    assert ms.n_comparisons == 40
    assert ms.n_swaps == 40
    ms.reset_all_counters()
    assert ms.n_comparisons == 0
    assert ms.n_swaps == 0


@pytest.mark.parametrize(
    ('input_instance', 'descending', 'expected_result', 'expected_n_comparisons', 'expected_n_swaps'),
    [
        pytest.param([], True, [], 0, 0, id='Empty list'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 40, 40, id='Worst case'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 40, 40, id='Best case'),
        pytest.param([1, 1, 1, 1, 1], True, [1, 1, 1, 1, 1], 15, 15, id='Stable descending'),
        pytest.param([1, 1, 1, 1, 1], False, [1, 1, 1, 1, 1], 15, 15, id='Stable ascending'),
        pytest.param((4, 2, 0, 1, 3), True, [4, 3, 2, 1, 0], 15, 15, id='Accepts tuple'),
        pytest.param(range(1, 11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 40, 40, id='Accepts range'),
        pytest.param((lambda x: (i for i in range(1, x)))(11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 40, 40, id='Accepts generator'),
        pytest.param(['a', 'e', 'i', 'o', 'u'], True, ['u', 'o', 'i', 'e', 'a'], 15, 15, id='Accepts comparable strings'),
        pytest.param([(0, 1), (1, 1), (1, 2)], True, [(1, 2), (1, 1), (0, 1)], 6, 6, id='Accepts comparable tuples'),
    ]
)
def test_merge_sort_run_algorithm(
        ms: MergeSort, input_instance: Iterable[Comparable], descending: bool, expected_result: list[Comparable],
        expected_n_comparisons: int, expected_n_swaps: int
) -> None:
    assert ms.run_algorithm(input_instance, 0, descending) == (True, expected_result)
    assert ms.n_comparisons == expected_n_comparisons
    assert ms.n_swaps == expected_n_swaps
