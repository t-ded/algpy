from functools import cached_property

import numpy as np
from numpy.typing import NDArray

from algpy_src.data_structures.backtracking_tasks.generic_backtracking_task import GenericBacktrackingTask


class SudokuTask(GenericBacktrackingTask[NDArray[np.object_], tuple[int, int], int | None]):

    def __init__(self, initial_state: NDArray[np.object_]) -> None:
        super().__init__()
        self._state = initial_state.copy()
        self._initial_state = initial_state
        self._filled = set(range(1, 10))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SudokuTask) and np.array_equal(self._state, other._state)

    @cached_property
    def get_candidates(self) -> list[tuple[int, int]]:
        return [(i, j) for i in range(9) for j in range(9) if self._initial_state[i][j] is None]

    @cached_property
    def get_non_default_options(self) -> list[int | None]:
        return list(range(1, 10))

    @property
    def default_option(self) -> None:
        return None

    def reset_candidate_to_initial_state(self, candidate: tuple[int, int]) -> None:
        self._state[*candidate] = self._initial_state[*candidate]

    def is_option_allowed(self, candidate: tuple[int, int], option: int | None) -> bool:
        if option is None:
            return False

        row, col = candidate
        block_start_row = (row // 3) * 3
        block_start_col = (col // 3) * 3
        return bool(
            self._state[row][col] is None and
            option not in self._state[row] and
            option not in self._state[:, col] and
            option not in self._state[block_start_row : block_start_row + 1, block_start_col : block_start_col + 3]
        )

    def apply_option(self, candidate: tuple[int, int], option: int | None) -> None:
        self._state[*candidate] = option

    def is_solved(self) -> bool:
        for i in range(9):
            if set(self._state[i]) != self._filled or set(self._state[:, i]) != self._filled:
                return False
        for block_start_row in range(0, 9, 3):
            for block_start_col in range(0, 9, 3):
                if set(self._state[block_start_row : block_start_row + 3, block_start_col : block_start_col + 3].flatten()) != self._filled:
                    return False
        return True




