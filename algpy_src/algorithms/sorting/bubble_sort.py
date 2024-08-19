from typing import Iterable, Any

from algpy_src.algorithms.base.algorithm_properties import SortingAlgorithmProperties, AlgorithmFamily
from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.constants import Comparable, VERBOSITY_LEVELS
from algpy_src.base.utils import print_problem_instance


class BubbleSort(SortingAlgorithm):

    def __init__(self):
        super().__init__()

    @property
    def algorithm_properties(self) -> SortingAlgorithmProperties:
        return SortingAlgorithmProperties(
            name='Bubble Sort',
            algorithm_family=AlgorithmFamily.SORTING,
            is_deterministic=True,
            best_case_time_complexity='n',
            best_case_description='a fully sorted array',
            average_case_time_complexity='n^2',
            worst_case_time_complexity='n^2',
            worst_case_description='a fully unsorted array',
            space_complexity='1',
            is_stable=True,
        )

    def get_worst_case_arguments(self, input_size: int) -> dict[str, Any]:
        """
        Generates a sorted range of integers from 1 to input_size and descending keyword argument as True.

        Parameters
        ----------
        input_size : int
            Size of the range to generate.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with keyword arguments for the input_instance and descending parameters of the run_algorithm method.
        """
        return {'input_instance': range(1, input_size + 1), 'descending': True}

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> tuple[bool, list[Comparable]]:
        """
        Run function of the bubble sort algorithm implemented in a stable (relative order of same-valued keys remains) manner.
        Implementation assumes the less naive approach, taking into account that bubbled elements at the end of the array are known to be sorted already.

        Parameters
        ----------
        input_instance : Iterable[Comparable]
            Iterable input instance of comparable objects to run the sorting algorithm on.
            It is copied and then returned as a sorted list.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print of the iterable before and after and 2 meaning print after every swap.
        descending : bool (default True)
            Whether to sort in descending order.
            Note that the algorithm is built in a stable manner, so that the relative order of items with equal value remains intact.
        args : Any
            Additional arguments passed to the running function.
        kwargs : Any
            Additional keyword arguments passed to the running function.

        Returns
        -------
        result : tuple[bool, list[Comparable]]
            Returns boolean value representing whether the algorithm terminated successfully (always True in this case) and List copy of the given input instance iterable sorted in the required order.
        """
        self.reset_all_counters()
        input_list: list[Comparable] = list(input_instance)
        print_problem_instance(input_list, verbosity_level, 1)
        for i in range(len(input_list) - 1):
            swapped = False
            for j in range(len(input_list) - i - 1):
                if (descending is True and input_list[j] < input_list[j + 1]) or (descending is False and input_list[j] > input_list[j + 1]):
                    input_list[j], input_list[j + 1] = input_list[j + 1], input_list[j]
                    self.increment_n_swaps()
                    swapped = True
                self.increment_n_comparisons()
                print_problem_instance(input_list, verbosity_level, 2)
            if swapped is False:
                break
        print_problem_instance(input_list, verbosity_level, 1)
        return True, input_list
