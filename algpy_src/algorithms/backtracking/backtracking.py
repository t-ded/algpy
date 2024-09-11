from typing import Any, Optional

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import VERBOSITY_LEVELS
from algpy_src.base.utils import print_problem_instance
from algpy_src.data_structures.backtracking_tasks.generic_backtracking_task import GenericBacktrackingTask
from algpy_src.data_structures.backtracking_tasks.n_queens_task import NQueensTask


class BacktrackingAlgorithm(Algorithm[GenericBacktrackingTask, int, GenericBacktrackingTask]):

    def __init__(self) -> None:
        super().__init__()
        self._last_candidate_idx: int = 0

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name='Backtracking Algorithm',
            algorithm_family=AlgorithmFamily.BACKTRACKING,
            is_deterministic=True,
            best_case_time_complexity='O(n^k)',
            best_case_description='already solved task, where k is a constant related to the task itself',
            average_case_time_complexity='O(n!)',
            worst_case_time_complexity='O(n!)',
            worst_case_description='having to try all possible options at all possible positions',
            space_complexity='O(n^k)',
        )

    def get_worst_case_arguments(self, input_size: int) -> dict[str, Any]:
        """
        Generate an empty N Queens problem instance as an example of the backtracking task with non-trivial complexity.

        Parameters
        ----------
        input_size : int
            Size of the N Queens problem instance.

        Returns
        -------
        nqueens: NQueensTask
            Empty N Queens problem instance.
        """
        return {'input_instance': NQueensTask(input_size)}

    def run_algorithm(self, input_instance: GenericBacktrackingTask, verbosity_level: VERBOSITY_LEVELS = 0, *args: Any, **kwargs: Any) -> tuple[bool, Optional[GenericBacktrackingTask]]:
        """
        Main run function of the backtracking algorithm, serves as a wrapper around the recursive method.
        Assuming GenericBacktrackingTask interface, this algorithm should be task-agnostic.

        Parameters
        ----------
        input_instance : GenericBacktrackingTask
            Backtracking task to solve.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print the state in the beginning and in the end and
            2 meaning also print the state following every candidate expansion and backtracking.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, GenericBacktrackingTask]
            Returns True along with the solved input instance if a solution was found, otherwise False and the given input instance.
        """
        print_problem_instance(input_instance.state, verbosity_level, 1)
        self._backtrack(input_instance, verbosity_level)
        print_problem_instance(input_instance.state, verbosity_level, 1)
        return input_instance.is_solved(), input_instance

    def _backtrack(self, input_instance: GenericBacktrackingTask, verbosity_level: VERBOSITY_LEVELS = 0, *args: Any, **kwargs: Any) -> tuple[bool, Optional[GenericBacktrackingTask]]:
        """
        Main run function of the backtracking algorithm, serves as a wrapper around the recursive method.
        Assuming GenericBacktrackingTask interface, this algorithm should be task-agnostic.

        Parameters
        ----------
        input_instance : GenericBacktrackingTask
            Backtracking task to solve.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print the state in the beginning and in the end and
            2 meaning also print the state following every candidate expansion and backtracking.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, GenericBacktrackingTask]
            Returns True along with the solved input instance if a solution was found, otherwise False and the given input instance.
        """
        print_problem_instance(input_instance.state, verbosity_level, 2)
        if input_instance.is_solved():
            return True, input_instance

        for i, candidate in enumerate(input_instance.get_candidates[self._last_candidate_idx:]):
            for option in input_instance.get_options:
                if option != input_instance.default_option and input_instance.is_option_allowed(candidate, option):
                    self.increment_n_ops()
                    input_instance.apply_option(candidate, option)
                    self._last_candidate_idx += i + 1
                    if self._backtrack(input_instance, verbosity_level, *args, **kwargs)[0]:
                        return True, input_instance
                    input_instance.apply_option(candidate, input_instance.default_option)
                    self._last_candidate_idx -= i + 1

        return False, input_instance
