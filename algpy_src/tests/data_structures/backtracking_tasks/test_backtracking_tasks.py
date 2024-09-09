from functools import cached_property

import numpy as np

from algpy_src.data_structures.backtracking_tasks.n_queens_task import NQueensTask


class TestNQueensTask:

    @cached_property
    def get_solved_4x4(self) -> NQueensTask:
        task = NQueensTask(4)
        task.apply_option((0, 1))
        task.apply_option((1, 3))
        task.apply_option((2, 0))
        task.apply_option((3, 2))
        return task

    def test_n_queens_task_creation_and_option_application(self) -> None:
        for n in range(1, 11):
            task = NQueensTask(n)
            idx = 0
            for i in range(n):
                for j in range(n):
                    assert task.get_options[idx] == (i, j)
                    task.apply_option((i, j))
                    idx += 1
                    assert np.sum(task.state) == idx

    def test_allowed_options(self) -> None:
        solved = self.get_solved_4x4
        assert solved.is_solved()
        for option in solved.get_options:
            assert solved.is_option_allowed(option) is False