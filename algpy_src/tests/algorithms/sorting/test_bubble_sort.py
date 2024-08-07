from typing import Iterable

import pytest

from algpy_src.algorithms.sorting.bubble_sort import BubbleSort
from algpy_src.base.constants import Comparable


@pytest.fixture()
def bs() -> BubbleSort:
    return BubbleSort()


def test_bubble_sort_base(bs: BubbleSort) -> None:
    assert bs.name == 'Bubble Sort'
    assert bs.best_case_time_complexity == 'n'
    assert bs.best_case_description == 'a fully sorted array'
    assert bs.average_case_time_complexity == 'n^2'
    assert bs.worst_case_time_complexity == 'n^2'
    assert bs.worst_case_description == 'a fully unsorted array'
    assert bs.space_complexity == '1'
    assert bs.get_worst_case_arguments(10) == {'input_instance': range(1, 11), 'descending': True}


def test_worst_case(bs: BubbleSort) -> None:
    assert bs.n_comparisons == 0
    assert bs.n_swaps == 0
    worst_case_args = bs.get_worst_case_arguments(10)
    assert bs.run_algorithm(**worst_case_args) == (True, list(range(10, 0, -1)))
    assert bs.n_comparisons == 45
    assert bs.n_swaps == 45
    bs.reset_all_counters()
    assert bs.n_comparisons == 0
    assert bs.n_swaps == 0


@pytest.mark.parametrize(
    ('input_instance', 'descending', 'expected_result', 'expected_n_comparisons', 'expected_n_swaps'),
    [
        pytest.param([], True, [], 0, 0, id='Empty list'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 45, 45, id='Worst case'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9, 0, id='Best case'),
        pytest.param([1, 1, 1, 1, 1], True, [1, 1, 1, 1, 1], 4, 0, id='Stable descending'),
        pytest.param([1, 1, 1, 1, 1], False, [1, 1, 1, 1, 1], 4, 0, id='Stable ascending'),
        pytest.param((4, 2, 0, 1, 3), True, [4, 3, 2, 1, 0], 10, 4, id='Accepts tuple'),
        pytest.param(range(1, 11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9, 0, id='Accepts range'),
        pytest.param((lambda x: (i for i in range(1, x)))(11), False, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9, 0, id='Accepts generator'),
        pytest.param(['a', 'e', 'i', 'o', 'u'], True, ['u', 'o', 'i', 'e', 'a'], 10, 10, id='Accepts comparable strings'),
        pytest.param([(0, 1), (1, 1), (1, 2)], True, [(1, 2), (1, 1), (0, 1)], 3, 3, id='Accepts comparable tuples'),
    ]
)
def test_bubble_sort_run_algorithm(
        bs: BubbleSort, input_instance: Iterable[Comparable], descending: bool, expected_result: list[Comparable],
        expected_n_comparisons: int, expected_n_swaps: int
) -> None:
    assert bs.run_algorithm(input_instance, 0, descending) == (True, expected_result)
    assert bs.n_comparisons == expected_n_comparisons
    assert bs.n_swaps == expected_n_swaps
