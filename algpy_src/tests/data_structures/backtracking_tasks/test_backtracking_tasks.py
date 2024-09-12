from functools import cached_property

import numpy as np

from algpy_src.data_structures.backtracking_tasks.n_queens_task import NQueensTask
from algpy_src.data_structures.backtracking_tasks.sudoku_task import SudokuTask


class TestNQueensTask:

    @cached_property
    def get_solved_4x4(self) -> NQueensTask:
        task = NQueensTask(4)
        task.apply_option((0, 1), True)
        task.apply_option((1, 3), True)
        task.apply_option((2, 0), True)
        task.apply_option((3, 2), True)
        return task

    def test_n_queens_task_creation_and_option_application(self) -> None:
        for n in range(1, 11):
            task = NQueensTask(n)
            idx = 0
            for i in range(n):
                for j in range(n):
                    assert task.get_candidates[idx] == (i, j)
                    task.apply_option((i, j), True)
                    idx += 1
                    assert np.sum(task.state) == idx

    def test_allowed_options(self) -> None:
        solved = self.get_solved_4x4
        assert solved.is_solved()
        for candidate in solved.get_candidates:
            assert solved.is_option_allowed(candidate, True) is False
            assert solved.is_option_allowed(candidate, False) is True

    def test_recognizes_unsolved(self) -> None:
        task = NQueensTask(2)
        task.apply_option((0, 0), True)
        assert task.is_solved() is False
        task.apply_option((0, 1), True)
        assert task.is_solved() is False
        task.apply_option((0, 0), False)
        assert task.is_solved() is False
        task.apply_option((1, 0), True)
        assert task.is_solved() is False
        task.apply_option((0, 1), False)
        assert task.is_solved() is False
        task.apply_option((1, 1), True)
        assert task.is_solved() is False
        task.apply_option((1, 0), False)
        assert task.is_solved() is False

        task_4x4 = NQueensTask(4)
        task_4x4.apply_option((0, 0), True)
        task_4x4.apply_option((2, 3), True)
        assert task_4x4.is_option_allowed((3, 2), True) is False


class TestSudokuTask:

    @cached_property
    def get_solved_example(self) -> SudokuTask:
        return SudokuTask(initial_state=np.array([
            [4, 3, 5, 2, 6, 9, 7, 8, 1],
            [6, 8, 2, 5, 7, 1, 4, 9, 3],
            [1, 9, 7, 8, 3, 4, 5, 6, 2],
            [8, 2, 6, 1, 9, 5, 3, 4, 7],
            [3, 7, 4, 6, 8, 2, 9, 1, 5],
            [9, 5, 1, 7, 4, 3, 6, 2, 8],
            [5, 1, 9, 3, 2, 6, 8, 7, 4],
            [2, 4, 8, 9, 5, 7, 1, 3, 6],
            [7, 6, 3, 4, 1, 8, 2, 5, 9]
        ], dtype=np.object_))

    @cached_property
    def get_minimal_example(self) -> SudokuTask:
        return SudokuTask(initial_state=np.array([
            [None, None, None, 8, None, 1, None, None, 2],
            [None, None, None, None, None, None, 4, 3, None],
            [5, None, None, None, None, None, None, None, None],
            [None, None, None, None, 7, None, 8, None, None],
            [None, None, None, None, None, None, 1, None, None],
            [None, 2, None, None, 3, None, None, None, None],
            [6, None, None, None, None, None, None, 7, 5],
            [None, None, 3, 4, None, None, None, None, None],
            [None, None, None, 2, None, None, 6, None, None],
        ]))

    def test_sudoku_option_application(self) -> None:

        task = self.get_solved_example
        assert task.is_solved() is True

        task.apply_option((8, 8), None)
        assert task.is_solved() is False
        task.reset_candidate_to_initial_state((8, 8))
        assert task.is_solved() is True

        for i in range(1, 9):
            task.apply_option((8, 8), i)
            assert task.is_solved() is False
        task.reset_candidate_to_initial_state((8, 8))
        assert task.is_solved() is True

    def test_allowed_options(self) -> None:
        solved = self.get_solved_example
        assert solved.is_solved() is True
        for candidate in solved.get_candidates:
            for option in solved.get_options:
                if option is None or option == solved.state[candidate]:
                    assert solved.is_option_allowed(candidate, option) is True
                else:
                    assert solved.is_option_allowed(candidate, False) is True

    def test_recognizes_unsolved(self) -> None:
        task = self.get_minimal_example
        assert task.is_solved() is False
