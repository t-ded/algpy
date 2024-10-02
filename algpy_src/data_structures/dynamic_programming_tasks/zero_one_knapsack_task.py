from collections import namedtuple
from typing import Callable, Iterable

from algpy_src.data_structures.dynamic_programming_tasks.generic_dynamic_programming_task import GenericDynamicProgrammingTask

ZeroOneKnapsackTaskState = namedtuple('ZeroOneKnapsackTaskState', 'taken_capacity value idx', defaults=[0, 0, 0])


class ZeroOneKnapsackTask(GenericDynamicProgrammingTask[ZeroOneKnapsackTaskState]):

    def __init__(self, capacity: int, weights: list[int], values: list[int]) -> None:
        super().__init__()
        self._capacity = capacity
        self._weights = weights
        self._values = values
        self._state = ZeroOneKnapsackTaskState(0, 0, 0)

    def value_computation(self) -> tuple[Iterable[ZeroOneKnapsackTaskState], Callable]:
        return [], lambda: self._state.value

    def get_state_transitions(self) -> list[ZeroOneKnapsackTaskState]:
        admissible_states: list[ZeroOneKnapsackTaskState] = []
        for i in range(self._state.idx, len(self._weights)):
            taken_capacity_with_item = self._state.taken_capacity + self._weights[i]
            if taken_capacity_with_item <= self._capacity:
                admissible_states.append(ZeroOneKnapsackTaskState(taken_capacity_with_item, self._state.value + self._values[i], i + 1))
            admissible_states.append(ZeroOneKnapsackTaskState(self._state.taken_capacity, self._state.value, i + 1))
        return admissible_states

    @property
    def is_optimization(self) -> bool:
        return True

    @property
    def get_input(self) -> tuple[int, list[int], list[int]]:
        return self._capacity, self._weights, self._values
