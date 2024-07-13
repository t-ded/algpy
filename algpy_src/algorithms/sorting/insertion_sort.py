from typing import Iterable, Any

from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.constants import Comparable, VERBOSITY_LEVELS
from algpy_src.base.utils import print_problem_instance


class InsertionSort(SortingAlgorithm):

    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return 'Insertion Sort'

    @property
    def is_deterministic(self) -> bool:
        return True

    @property
    def best_case_time_complexity(self) -> str:
        return 'n'

    @property
    def best_case_description(self) -> str:
        return 'a fully sorted array'

    @property
    def average_case_time_complexity(self) -> str:
        return 'n^2'

    @property
    def worst_case_time_complexity(self) -> str:
        return 'n^2'

    @property
    def worst_case_description(self) -> str:
        return 'a fully unsorted array'

    @property
    def space_complexity(self) -> str:
        return '1'

    @property
    def is_stable(self) -> bool:
        return True

    def generate_worst_case(self, input_size: int, *args: Any, **kwargs: Any) -> Iterable[int]:
        """
        Generates a sorted range of integers from 1 to input_size.
        If 'descending' is passed as a keyword argument with value False, the order of the range is descending, otherwise ascending
        (i.e., contrary to expected result of the sort).

        Parameters
        ----------
        input_size : int
            Size of the range to generate.
        *args : Any
            Additional arguments that are expected to be passed to the run_algorithm function.
        **kwargs : Any
            Additional keyword arguments that are expected to be passed to the run_algorithm function.

        Returns
        -------
        instance : range
            Range of sorted integers in order opposite to expected order of the run_algorithm function output.
        """
        if kwargs.get('descending', True) is False:
            return range(input_size, 0, -1)
        return range(1, input_size + 1)

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> list[Comparable]:
        """
        Run function of the insertion sort algorithm implemented in a stable (relative order of same-valued keys remains) manner.

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
        input_list : list[Comparable]
            List copy of the given input instance iterable sorted in the required order.
        """
        self.reset_all_counters()
        input_list: list[Comparable] = list(input_instance)
        print_problem_instance(input_list, verbosity_level, 1)
        for i in range(1, len(input_list)):
            value = input_list[i]
            j = i - 1
            pair_sorted = True
            while j >= 0 and ((input_list[j] < value and descending is True) or (input_list[j] > value and descending is False)):
                pair_sorted = False
                input_list[j + 1] = input_list[j]
                j -= 1
                self.increment_n_swaps()
                self.increment_n_comparisons()
            if pair_sorted is True:
                self.increment_n_comparisons()
            input_list[j + 1] = value
            print_problem_instance(input_list, verbosity_level, 2)
        print_problem_instance(input_list, verbosity_level, 1)
        return input_list
