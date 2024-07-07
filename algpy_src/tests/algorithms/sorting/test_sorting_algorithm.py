import pytest

from algpy_src.tests.test_utils.base_objects import ExampleSortingAlgorithm


@pytest.fixture()
def sa() -> ExampleSortingAlgorithm:
    return ExampleSortingAlgorithm()


def test_base_sorting_algorithm(sa: ExampleSortingAlgorithm) -> None:
    assert sa.name == 'Example Sorting Algorithm'

    assert sa.n_comparisons == 0
    sa.increment_n_comparisons(5)
    assert sa.n_comparisons == 5
    sa.reset_n_comparisons()
    assert sa.n_comparisons == 0
    sa.increment_n_comparisons(2)

    assert sa.n_swaps == 0
    sa.increment_n_swaps(3)
    assert sa.n_swaps == 3
    sa.reset_n_swaps()
    assert sa.n_swaps == 0
    sa.increment_n_swaps(1)

    assert sa.n_ops == 3
    sa.reset_all_counters()
    assert sa.n_comparisons == 0
    assert sa.n_swaps == 0
