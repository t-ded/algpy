from typing import Iterable

import pytest

from algpy_src.algorithms.sorting.insertion_sort import InsertionSort
from algpy_src.base.constants import Comparable


@pytest.fixture()
def ins() -> InsertionSort:
    return InsertionSort()


def test_insertion_sort_base(ins: InsertionSort) -> None:
    assert ins.name == 'Insertion Sort'
    assert ins.best_case_time_complexity == 'n'
    assert ins.best_case_description == 'a fully sorted array'
    assert ins.average_case_time_complexity == 'n^2'
    assert ins.worst_case_time_complexity == 'n^2'
    assert ins.worst_case_description == 'a fully unsorted array'
    assert ins.space_complexity == '1'
    assert ins.get_worst_case_arguments(10) == {'input_instance': range(1, 11), 'descending': True}


def test_worst_case(ins: InsertionSort) -> None:
    assert ins.n_comparisons == 0
    assert ins.n_swaps == 0
    worst_case_args = ins.get_worst_case_arguments(10)
    assert ins.run_algorithm(**worst_case_args) == (True, list(range(10, 0, -1)))
    assert ins.n_comparisons == 45
    assert ins.n_swaps == 45
    ins.reset_all_counters()
    assert ins.n_comparisons == 0
    assert ins.n_swaps == 0


@pytest.mark.parametrize(
    ('input_instance', 'descending', 'expected_result', 'expected_n_comparisons', 'expected_n_swaps'),
    [
        pytest.param([], True, [], 0, 0, id='Empty list'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 45, 45, id='Worst case'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9, 0, id='Best case'),
        pytest.param([1, 1, 1, 1, 1], True, [1, 1, 1, 1, 1], 4, 0, id='Stable descending'),
        pytest.param([1, 1, 1, 1, 1], False, [1, 1, 1, 1, 1], 4, 0, id='Stable ascending'),
        pytest.param((4, 2, 0, 1, 3), True, [4, 3, 2, 1, 0], 6, 4, id='Accepts tuple'),
        pytest.param(range(1, 11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9, 0, id='Accepts range'),
        pytest.param((lambda x: (i for i in range(1, x)))(11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9, 0, id='Accepts generator'),
        pytest.param(['a', 'e', 'i', 'o', 'u'], True, ['u', 'o', 'i', 'e', 'a'], 10, 10, id='Accepts comparable strings'),
        pytest.param([(0, 1), (1, 1), (1, 2)], True, [(1, 2), (1, 1), (0, 1)], 3, 3, id='Accepts comparable tuples'),
    ]
)
def test_insertion_sort_run_algorithm(
        ins: InsertionSort, input_instance: Iterable[Comparable], descending: bool, expected_result: list[Comparable],
        expected_n_comparisons: int, expected_n_swaps: int
) -> None:
    assert ins.run_algorithm(input_instance, 0, descending) == (True, expected_result)
    assert ins.n_comparisons == expected_n_comparisons
    assert ins.n_swaps == expected_n_swaps
