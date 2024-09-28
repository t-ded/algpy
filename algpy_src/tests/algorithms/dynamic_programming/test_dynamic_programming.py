import numpy as np
import pytest

from algpy_src.algorithms.dynamic_programming.dynamic_programming import DynamicProgrammingAlgorithm
from algpy_src.data_structures.dynamic_programming_tasks.fibonacci_task import NThFibonacciNumber


@pytest.fixture
def dp() -> DynamicProgrammingAlgorithm:
    return DynamicProgrammingAlgorithm()


class TestDynamicProgramming:

    @staticmethod
    def get_fib(n: int) -> NThFibonacciNumber:
        return NThFibonacciNumber(n)

    @pytest.mark.parametrize('n', list(range(2, 31)) + list(range(100, 901, 100)))
    def test_nth_fib_number(self, dp: DynamicProgrammingAlgorithm, n: int) -> None:

        fib_matrix = np.array([[1, 1], [1, 0]], dtype=object)
        expected_result = np.linalg.matrix_power(fib_matrix, n)[0, 1]

        fib_task = self.get_fib(n)
        success, actual_result = dp.run_algorithm(fib_task)
        assert success is True
        assert actual_result == expected_result

