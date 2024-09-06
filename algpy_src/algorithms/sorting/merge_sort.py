from typing import Iterable, Any

from algpy_src.algorithms.base.algorithm_properties import SortingAlgorithmProperties, AlgorithmFamily
from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.constants import Comparable, VERBOSITY_LEVELS
from algpy_src.base.utils import print_problem_instance


class MergeSort(SortingAlgorithm):

    def __init__(self):
        super().__init__()

    @property
    def algorithm_properties(self) -> SortingAlgorithmProperties:
        return SortingAlgorithmProperties(
            name='Merge Sort',
            algorithm_family=AlgorithmFamily.SORTING,
            is_deterministic=True,
            best_case_time_complexity='n * log(n)',
            best_case_description='a fully sorted array',
            average_case_time_complexity='n * log(n)',
            worst_case_time_complexity='n * log(n)',
            worst_case_description='two sorted subsections',
            space_complexity='n',
            is_stable=True,
        )

    def get_worst_case_arguments(self, input_size: int) -> dict[str, Any]:
        """
        Generates range of integers from 1 to input_size with two sorted subsections and descending keyword argument as True.

        Parameters
        ----------
        input_size : int
            Size of the range to generate.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with keyword arguments for the input_instance and descending parameters of the run_algorithm method.
        """
        input_size_even = input_size % 2 == 0
        return {
            'input_instance': list(range(0, input_size if input_size_even else input_size - 1, 2)) + list(range(1, input_size if not input_size_even else input_size, 2)),
            'descending': True
        }

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> tuple[bool, list[Comparable]]:
        """
        Run function of the merge sort algorithm implemented in the bottom-up fashion.

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
        work_list: list[Comparable] = input_list[:]
        work_list_switch: bool = False
        print_problem_instance(input_list, verbosity_level, 1)

        width: int = 1
        while width < len(input_list):
            work_list_switch = not work_list_switch
            nth_block: int = 0
            while nth_block < len(input_list):
                if work_list_switch:
                    self._bottom_up_merge(input_list, nth_block, min(nth_block + width, len(input_list)), min(nth_block + 2 * width, len(input_list)), work_list, descending)
                else:
                    self._bottom_up_merge(work_list, nth_block, min(nth_block + width, len(input_list)), min(nth_block + 2 * width, len(input_list)), input_list, descending)
                nth_block += 2 * width
            width *= 2
            print_problem_instance(input_list, verbosity_level, 2)

        if work_list_switch:
            return True, work_list
        else:
            return True, input_list

    def _bottom_up_merge(self, list_a: list[Comparable], left_block_start: int, block_separator: int, right_block_end: int, list_b: list[Comparable], descending: bool) -> None:
        """
        The main logic function of the merge algorithm, which takes the input array and working array,
        sorts the two blocks specified by the indices and merges them in the right order.

        Parameters
        ----------
        list_a : list[Comparable]
            Input array to be sorted.
        left_block_start : int
            Start index of the left block.
        block_separator : int
            Start index of the right block, i.e., index between the two blocks.
        right_block_end : int
            End index of the right block.
        list_b : list[Comparable]
            Working array to be sorted.
        descending : bool
            Whether to sort in descending order.
        """
        i = left_block_start
        j = block_separator
        for k in range(left_block_start, right_block_end):
            self.increment_n_comparisons()
            self.increment_n_swaps()
            if i < block_separator and (j >= right_block_end or (list_a[i] <= list_a[j] if not descending else list_a[i] >= list_a[j])):
                list_b[k] = list_a[i]
                i += 1
            else:
                list_b[k] = list_a[j]
                j += 1