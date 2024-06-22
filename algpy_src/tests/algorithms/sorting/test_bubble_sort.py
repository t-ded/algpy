import pytest

from algpy_src.algorithms.sorting.bubble_sort import BubbleSort
from algpy_src.base.constants import TEST_SEED


@pytest.fixture()
def bs():
    return BubbleSort()


def test_bubble_sort_base(bs):
    assert bs.name == 'Bubble Sort'
    assert bs.time_complexity == 'n^2'
    assert bs.space_complexity == '1'
    assert bs.generate_increasing_input_size_sequence(n=5) == [1, 10, 100, 1_000, 10_000]
    assert bs.generate_random_input(input_size=10, seed=TEST_SEED) == [2, 1, 5, 4, 4, 3, 2, 9, 2, 10]


@pytest.mark.parametrize(
    ('input_instance', 'expected_result'),
    [
        pytest.param([], ([], 0), id='Empty list'),
    ]
)
def test_bubble_sort_run_algorithm(bs, input_instance, expected_result):
    assert bs.run_algorithm(input_instance) == expected_result
