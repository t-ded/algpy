import numpy as np
import pytest

from algpy_src.algorithms.dynamic_programming.dynamic_programming import DynamicProgrammingAlgorithm
from algpy_src.data_structures.dynamic_programming_tasks.fibonacci_task import NThFibonacciNumberTask
from algpy_src.data_structures.dynamic_programming_tasks.zero_one_knapsack_task import ZeroOneKnapsackTask


@pytest.fixture
def dp() -> DynamicProgrammingAlgorithm:
    return DynamicProgrammingAlgorithm()


class TestDynamicProgramming:

    @pytest.mark.parametrize('n', list(range(2, 31)) + list(range(100, 901, 100)))
    def test_nth_fib_number(self, dp: DynamicProgrammingAlgorithm, n: int) -> None:

        fib_matrix = np.array([[1, 1], [1, 0]], dtype=object)
        expected_result = np.linalg.matrix_power(fib_matrix, n)[0, 1]

        fib_task = NThFibonacciNumberTask(n)
        success, actual_result = dp.run_algorithm(fib_task)

        assert success is True
        assert actual_result == expected_result

    @pytest.mark.parametrize(
        ('capacity', 'values', 'weights', 'expected_result'),
        [
            pytest.param(10, [10, 20, 25], [5, 5, 10], 30),
            pytest.param(10, [10, 20, 35], [5, 5, 10], 35),
            pytest.param(10, [10, 20, 25], [2, 5, 10], 30),
            pytest.param(67, [505, 352, 458, 220, 354, 414, 498, 545, 473, 543], [23, 26, 20, 18, 32, 27, 29, 26, 30, 27], 1_270),
        ]
    )
    def test_zero_one_knapsack(self, capacity: int, values: list[int], weights: list[int], expected_result: int, dp: DynamicProgrammingAlgorithm) -> None:

        zero_one_knapsack_task = ZeroOneKnapsackTask(capacity, weights, values)
        success, actual_result = dp.run_algorithm(zero_one_knapsack_task)
        assert success is True
        assert actual_result == expected_result
