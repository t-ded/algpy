from functools import cached_property
from typing import cast

from algpy_src.data_structures.backtracking_tasks.generic_backtracking_task import GenericBacktrackingTask


class SATTask(GenericBacktrackingTask[list[bool], int, bool]):

    _UNFILLED = cast(bool, object())

    def __init__(self, proposition: list[set[int]]) -> None:
        super().__init__()
        self._proposition = proposition
        self._num_variables = max(abs(var) for clause in self._proposition for var in clause)
        self._state: list[bool] = [self._UNFILLED] * self._num_variables

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SATTask) and self._state == other._state and self._proposition == other._proposition

    @cached_property
    def get_candidates(self) -> list[int]:
        return list(range(1, self._num_variables + 1))

    @cached_property
    def get_non_default_options(self) -> list[bool]:
        return [True, False]

    @property
    def default_option(self) -> bool:
        return self._UNFILLED

    def reset_candidate_to_initial_state(self, candidate: int) -> None:
        candidate_idx = candidate - 1
        self._state[candidate_idx] = self._UNFILLED

    def is_option_allowed(self, candidate: int, option: bool) -> bool:
        candidate_idx = candidate - 1
        original_value = self._state[candidate_idx]
        self._state[candidate_idx] = option
        is_allowed = True
        for clause in self._proposition:
            if candidate in clause:
                is_allowed = self._is_clause_solvable(clause)
                if not is_allowed:
                    break
        self._state[candidate_idx] = original_value
        return is_allowed

    def _is_clause_solvable(self, clause: set[int]) -> bool:
        for var in clause:
            var_idx = abs(var) - 1
            if self._state[var_idx] == self._UNFILLED:
                return True
            if self._state[var_idx] and var > 0:
                return True
            if not self._state[var_idx] and var < 0:
                return True
        return False

    def apply_option(self, candidate: int, option: bool) -> None:
        candidate_idx = candidate - 1
        self._state[candidate_idx] = option

    def is_solved(self) -> bool:
        for clause in self._proposition:
            if not self._is_clause_solved(clause):
                return False
        return True

    def _is_clause_solved(self, clause: set[int]) -> bool:
        is_solved = False
        for var in clause:
            var_idx = abs(var) - 1
            if self._state[var_idx] == self._UNFILLED:
                return False
            if self._state[var_idx] and var > 0:
                is_solved = True
            if not self._state[var_idx] and var < 0:
                is_solved = True
        return is_solved



