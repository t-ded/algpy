import numpy as np
import pytest
from numpy.typing import NDArray

from algpy_src.algorithms.backtracking.backtracking import BacktrackingAlgorithm
from algpy_src.data_structures.backtracking_tasks.n_queens_task import NQueensTask
from algpy_src.data_structures.backtracking_tasks.sudoku_task import SudokuTask


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
    solved, solutions = backtracking.run_algorithm(nqueens)
    assert solved is expected_result
    if expected_result is True:
        assert next(iter(solutions)).is_solved()
    else:
        assert len(solutions) == 0


def test_finds_all_solutions(backtracking: BacktrackingAlgorithm) -> None:
    nqueens = NQueensTask(4)
    solved, solutions = backtracking.run_algorithm(nqueens, find_all=True)
    assert solved is True
    assert len(solutions) == 2
    print([solution.state for solution in solutions])

    expected_solution_1 = NQueensTask(4)
    expected_solution_1.apply_option((0, 1), True)
    expected_solution_1.apply_option((1, 3), True)
    expected_solution_1.apply_option((2, 0), True)
    expected_solution_1.apply_option((3, 2), True)
    assert solutions[0] == expected_solution_1

    expected_solution_2 = NQueensTask(4)
    expected_solution_2.apply_option((0, 2), True)
    expected_solution_2.apply_option((1, 0), True)
    expected_solution_2.apply_option((2, 3), True)
    expected_solution_2.apply_option((3, 1), True)
    assert solutions[1] == expected_solution_2


@pytest.mark.parametrize(
    ('input_array', 'expected_result'),
    [
        pytest.param(np.array([
            [4, 3, 5, 2, 6, 9, 7, 8, 1],
            [6, 8, 2, 5, 7, 1, 4, 9, 3],
            [1, 9, 7, 8, 3, 4, 5, 6, 2],
            [8, 2, 6, 1, 9, 5, 3, 4, 7],
            [3, 7, 4, 6, 8, 2, 9, 1, 5],
            [9, 5, 1, 7, 4, 3, 6, 2, 8],
            [5, 1, 9, 3, 2, 6, 8, 7, 4],
            [2, 4, 8, 9, 5, 7, 1, 3, 6],
            [1, 1, None, None, None, None, None, None, None],
        ], dtype=np.object_), False, id='Unsolvable'),
        pytest.param(np.array([
            [4, 3, 5, 2, 6, 9, 7, 8, 1],
            [6, 8, 2, 5, 7, 1, 4, 9, 3],
            [1, 9, 7, 8, 3, 4, 5, 6, 2],
            [8, 2, 6, 1, 9, 5, 3, 4, 7],
            [3, 7, 4, 6, 8, 2, 9, 1, 5],
            [9, 5, 1, 7, 4, 3, 6, 2, 8],
            [5, 1, 9, 3, 2, 6, 8, 7, 4],
            [2, 4, 8, 9, 5, 7, 1, 3, 6],
            [7, 6, 3, 4, 1, 8, 2, 5, 9]
        ], dtype=np.object_), True, id='Pre-solved'),
        pytest.param(np.array([
            [4, 3, 5, 2, 6, 9, 7, 8, 1],
            [6, 8, 2, 5, 7, 1, 4, 9, 3],
            [1, 9, 7, 8, 3, 4, 5, 6, 2],
            [8, 2, 6, 1, 9, 5, 3, 4, 7],
            [3, 7, 4, 6, 8, 2, 9, 1, 5],
            [9, 5, 1, 7, 4, 3, 6, 2, 8],
            [5, 1, 9, 3, 2, 6, 8, 7, 4],
            [2, 4, 8, 9, 5, 7, 1, 3, 6],
            [None, None, None, None, None, None, None, None, None]
        ], dtype=np.object_), True, id='Mostly pre-solved'),
        pytest.param(np.array([
            [None, None, 4, 1, None, None, None, None, 5],
            [None, None, 7, 8, 3, 2, 6, None, None],
            [3, 9, None, 7, None, None, 8, None, None],
            [6, None, None, 9, 8, None, 1, None, None],
            [8, None, 1, 2, None, 7, None, None, 4],
            [None, 4, 9, None, 1, 3, None, None, 2],
            [None, 1, None, 3, None, 8, 2, 9, 6],
            [7, None, 3, None, None, None, None, None, None],
            [None, None, None, None, 6, 1, 4, None, 7]
        ], dtype=np.object_), True, id='Solvable (Easy)'),
        pytest.param(np.array([
            [1, 3, None, None, 7, 9, 6, 8, 5],
            [5, 9, None, None, None, 2, None, None, None],
            [None, None, 4, None, 3, 8, None, None, 9],
            [None, None, None, 8, 9, 1, None, 7, None],
            [None, None, None, None, None, 6, None, None, 1],
            [None, 7, 1, 3, None, None, 9, None, None],
            [None, None, None, None, 8, None, 3, 4, None],
            [None, None, 7, 9, 1, 3, None, None, 8],
            [6, None, 3, 2, 5, 4, None, None, None],
        ], dtype=np.object_), True, id='Solvable (Medium)'),
    ]
)
def test_backtracking_with_sudoku(backtracking: BacktrackingAlgorithm, input_array: NDArray[np.object_], expected_result: bool) -> None:
    sudoku = SudokuTask(input_array)
    solved, solutions = backtracking.run_algorithm(sudoku)
    assert solved is expected_result
    if expected_result is True:
        assert next(iter(solutions)).is_solved()
    else:
        assert len(solutions) == 0
