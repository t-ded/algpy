from functools import cached_property

import numpy as np

from algpy_src.data_structures.backtracking_tasks.n_queens_task import NQueensTask


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
            assert task.state is not None
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
