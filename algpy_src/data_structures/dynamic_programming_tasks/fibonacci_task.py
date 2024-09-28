from typing import Callable, Iterable

from algpy_src.data_structures.dynamic_programming_tasks.generic_dynamic_programming_task import GenericDynamicProgrammingTask


class NThFibonacciNumber(GenericDynamicProgrammingTask[int]):

    def __init__(self, n: int) -> None:
        super().__init__()
        self._state: int = n

    def value_computation(self) -> tuple[Iterable[int], Callable]:
        if self._state <= 2:
            return [], lambda: 1
        return [self._state - 1, self._state - 2], lambda a, b: a + b

    def compute_value(self, value_1: int, value_2: int) -> int:
        return value_1 + value_2

    def get_state_transitions(self) -> None:
        return None

    @property
    def is_optimization(self) -> bool:
        return False
