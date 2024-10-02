from typing import Any, Generic

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import VERBOSITY_LEVELS
from algpy_src.data_structures.dynamic_programming_tasks.generic_dynamic_programming_task import GenericDynamicProgrammingTask, StateType
from algpy_src.data_structures.dynamic_programming_tasks.zero_one_knapsack_task import ZeroOneKnapsackTask


class DynamicProgrammingAlgorithm(Algorithm[GenericDynamicProgrammingTask, tuple[int, list[int], list[int]], int | float], Generic[StateType]):

    def __init__(self) -> None:
        super().__init__()
        self._memo: dict[StateType, int | float] = {}
        self._highest_value: int | float = -float('inf')
        self._recursion_level = 0

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name='Dynamic Programming Algorithm',
            algorithm_family=AlgorithmFamily.DYNAMIC_PROGRAMMING,
            is_deterministic=True,
            best_case_time_complexity='O(#subproblems * T_best(subproblem))',
            best_case_description='each subproblem encountering its best case or being already memoized',
            average_case_time_complexity='O(#subproblems * T_avg(subproblem))',
            worst_case_time_complexity='O(#subproblems * T_worst(subproblem))',
            worst_case_description='going through every subproblem once with each having its own worst case',
            space_complexity='O(n)',
        )

    def get_worst_case_arguments(self, input_size: tuple[int, list[int], list[int]]) -> dict[str, Any]:
        """
        Generate an empty 0-1 Knapsack problem instance as an example of the dynamic programming task with non-trivial complexity.

        Parameters
        ----------
        input_size : tuple[int, list[int], list[int]]
            Size of the 0-1 Knapsack problem instance, where the first integer is the capacity
            of the bag and then there are list of item weights and list of item values.

        Returns
        -------
        knapsack: ZeroOneKnapsackTask
            Empty Knapsack problem instance.
        """
        return {'input_instance': ZeroOneKnapsackTask(*input_size)}

    def run_algorithm(
            self, input_instance: GenericDynamicProgrammingTask, verbosity_level: VERBOSITY_LEVELS = 0, *args: Any, **kwargs: Any
    ) -> tuple[bool, int | float]:

        memo_value = self._memo.get(input_instance.state, None)
        if memo_value is not None:
            return True, memo_value

        current_state = input_instance.state
        value_source_states, value_function = input_instance.value_computation()
        source_state_values = []
        for source_state in value_source_states:
            input_instance.set_state(source_state)
            source_state_values.append(self.run_algorithm(input_instance, verbosity_level)[1])
        input_instance.set_state(current_state)

        current_value = value_function(*source_state_values)
        self._memo[input_instance.state] = current_value

        if not input_instance.is_optimization:
            return True, current_value

        possible_states = input_instance.get_state_transitions()
        if possible_states is None:
            return True, current_value
        best_possible_value: int | float = 0
        for possible_state in possible_states:
            input_instance.set_state(possible_state)
            _, possible_value = self.run_algorithm(input_instance, verbosity_level)
            best_possible_value = max(best_possible_value, possible_value)
            input_instance.set_state(current_state)
        return True, max(current_value, best_possible_value)