from typing import Iterable, Optional

import pytest

from algpy_src.algorithms.searching.binary_search import BinarySearch
from algpy_src.base.constants import Comparable


@pytest.fixture()
def bs() -> BinarySearch:
    return BinarySearch()


def test_binary_search_base(bs: BinarySearch) -> None:
    assert bs.name == 'Binary Search'
    assert bs.best_case_time_complexity == '1'
    assert bs.best_case_description == 'search for element is in the middle of the array'
    assert bs.average_case_time_complexity == 'log(n)'
    assert bs.worst_case_time_complexity == 'log(n)'
    assert bs.worst_case_description == 'searched for element not present in the array'
    assert bs.space_complexity == '1'
    assert bs.get_worst_case_arguments(10) == {'input_instance': range(1, 11), 'element_to_search': 11}


def test_worst_case(bs: BinarySearch) -> None:
    assert bs.n_ops == 0
    worst_case_args = bs.get_worst_case_arguments(10)
    assert bs.run_algorithm(**worst_case_args) == (False, None)
    assert bs.n_ops == 4


@pytest.mark.parametrize(
    ('input_instance', 'element_to_search', 'expected_result', 'expected_n_ops'),
    [
        pytest.param([], 1, None, 0, id='Empty list'),
        pytest.param([1, 2, 3], None, None, 0, id='Search for None'),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 4, 1, id='Best case'),
        pytest.param((0, 1, 2, 3, 4), 0, 0, 2, id='Accepts tuple'),
        pytest.param((lambda x: (i for i in range(1, x)))(11), 5, 4, 1, id='Accepts generator'),
        pytest.param(['a', 'b', 'c', 'd', 'e'], 'e', 4, 3, id='Accepts comparable strings'),
        pytest.param([(0, 1), (1, 1), (1, 2)], (2, 2), None, 2, id='Accepts comparable tuples'),
        pytest.param([1, 1, 1], 1, 1, 1, id='Finds first encountered instance within duplicates'),
    ]
)
def test_binary_search_run_algorithm(
        bs: BinarySearch, input_instance: Iterable[Comparable], element_to_search: Optional[Comparable], expected_result: Optional[int], expected_n_ops: int
) -> None:
    assert bs.run_algorithm(input_instance, 0, element_to_search) == (element_to_search is None or expected_result is not None, expected_result)
    assert bs.n_ops == expected_n_ops


def test_search_all_indices(bs: BinarySearch) -> None:
    input_instance = list(range(100))
    for i in range(100):
        assert bs.run_algorithm(input_instance, element_to_search=i) == (True, i)
    assert bs.run_algorithm(input_instance, element_to_search=-1) == (False, None)
    assert bs.run_algorithm(input_instance, element_to_search=100) == (False, None)
