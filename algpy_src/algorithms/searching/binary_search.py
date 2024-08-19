from typing import Iterable, Any, Optional

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmFamily, AlgorithmProperties
from algpy_src.base.constants import Comparable, VERBOSITY_LEVELS
from algpy_src.base.utils import print_problem_instance


class BinarySearch(Algorithm[Iterable[Comparable], int, int]):

    def __init__(self):
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name='Binary Search',
            algorithm_family=AlgorithmFamily.SEARCHING,
            is_deterministic=True,
            best_case_time_complexity='1',
            best_case_description='search for element is in the middle of the array',
            average_case_time_complexity='log(n)',
            worst_case_time_complexity='log(n)',
            worst_case_description='searched for element not present in the array',
            space_complexity='1',
        )

    def get_worst_case_arguments(self, input_size: int) -> dict[str, Any]:
        """
        Generates a sorted range of integers from 1 to input_size and a searched for element (input_size + 1) which is not present in the array.

        Parameters
        ----------
        input_size : int
            Size of the range to generate.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with keyword arguments for the ̈́'input_instance' and 'element_to_search' parameters of the run_algorithm method.
        """
        return {'input_instance': range(1, input_size + 1), 'element_to_search': input_size + 1}

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, element_to_search: Optional[Comparable] = None,
                      *args: Any, **kwargs: Any) -> tuple[bool, Optional[int]]:
        """
        Run function of the binary search algorithm.

        Parameters
        ----------
        input_instance : Iterable[Comparable]
            Iterable input instance of comparable objects to run the search algorithm on.
            Has to be sorted, otherwise the algorithm will not work as expected.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print results after and 2 meaning print bisected element after every step.
        element_to_search : Optional[Comparable] (default None)
            Element to search for in the given input_instance.
            If None, the algorithm immediately successfully terminates.
        args : Any
            Additional arguments passed to the running function.
        kwargs : Any
            Additional keyword arguments passed to the running function.

        Returns
        -------
        result : tuple[bool, Optional[int]]
            Returns boolean value representing whether the algorithm terminated successfully (True if element_to_search is None or the given element was found in the input_instance)
            and an index of the element if it was found, otherwise None.
        """
        self.reset_n_ops()

        if element_to_search is None:
            return True, None

        input_list: list[Comparable] = list(input_instance)
        left = 0
        right = len(input_list) - 1

        while left <= right:
            self.increment_n_ops()
            current_bisect_index = (right + left) // 2
            current_bisect = input_list[current_bisect_index]

            if current_bisect == element_to_search:
                print_problem_instance(current_bisect, verbosity_level, 1)
                return True, current_bisect_index

            print_problem_instance(current_bisect, verbosity_level, 2)
            if current_bisect > element_to_search:
                right = current_bisect_index - 1
            elif current_bisect < element_to_search:
                left = current_bisect_index + 1

        return False, None
