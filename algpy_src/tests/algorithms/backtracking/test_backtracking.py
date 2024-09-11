import pytest

from algpy_src.algorithms.backtracking.backtracking import BacktrackingAlgorithm
from algpy_src.data_structures.backtracking_tasks.n_queens_task import NQueensTask


@pytest.fixture
def backtracking() -> BacktrackingAlgorithm:
    return BacktrackingAlgorithm()


@pytest.mark.parametrize(
    ('n', 'expected_result'),
    [
        pytest.param(1, True, id='1x1 Solvable'),
        pytest.param(2, False, id='2x2 Unsolvable'),
        pytest.param(3, False, id='3x3 Unsolvable'),
        pytest.param(4, True, id='4x4 Solvable'),
        pytest.param(5, True, id='5x5 Solvable'),
        pytest.param(6, True, id='6x6 Solvable'),
        pytest.param(7, True, id='7x7 Solvable'),
        pytest.param(8, True, id='8x8 Solvable'),
    ]
)
def test_backtracking_with_n_queens(backtracking: BacktrackingAlgorithm, n: int, expected_result: bool) -> None:
    nqueens = NQueensTask(n)
    assert backtracking.run_algorithm(nqueens)[0] is expected_result
