from functools import cached_property

import numpy as np
from numpy.typing import NDArray

from algpy_src.data_structures.backtracking_tasks.generic_backtracking_task import GenericBacktrackingTask


class NQueensTask(GenericBacktrackingTask[NDArray[np.bool_], tuple[int, int]]):

    def __init__(self, n: int):
        super().__init__()
        self._n = n
        self._state: NDArray[np.bool_] = np.full((n, n), False, dtype=bool)

    @cached_property
    def get_options(self) -> list[tuple[int, int]]:
        return [(i, j) for i in range(self._n) for j in range(self._n)]

    @property
    def state(self) -> NDArray[np.bool_]:
        return self._state

    def is_option_allowed(self, option: tuple[int, int]) -> bool:
        row, col = option
        return bool(np.sum(self._state[row]) == 0 and np.sum(self._state[col]) == 0 and np.trace(self._state, col - row) == 0 and np.trace(np.fliplr(self._state), row + col - self._n + 1) == 0)

    def apply_option(self, option: tuple[int, int]) -> None:
        self._state[*option] = True

    def is_solved(self) -> bool:
        for i in range(self._n):
            if not np.sum(self._state[i]) == 1 or not np.sum(self._state[i]) == 1:
                return False
        for row in range(self._n):
            for col in range(self._n):
                if np.trace(self._state, col - row) > 1 or np.trace(np.fliplr(self._state), row + col - self._n + 1) > 1:
                    return False
        return True




