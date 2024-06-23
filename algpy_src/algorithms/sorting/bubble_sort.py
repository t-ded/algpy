import random
from typing import Iterable, Optional, Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.constants import Comparable


class BubbleSort(Algorithm[Iterable[Comparable], int]):

    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return 'Bubble Sort'

    @property
    def time_complexity(self) -> str:
        return 'n^2'

    @property
    def space_complexity(self) -> str:
        return '1'

    def generate_increasing_input_size_sequence(self, n: int = 6, *args: Any, **kwargs: Any) -> list[int]:
        """
        Generates a list of increasing integers corresponding to number of elements in the to-be-sorted sequence.

        Parameters
        ----------
        n : int
            Exponent of the highest number in the list (10^n).
        *args : Any
            Additional arguments passed to the input sizes generating function.
        **kwargs : Any
            Additional keyword arguments passed to the input sizes generating function.

        Returns
        -------
        input_sizes : list[int]
            List of increasing integers specified as exponents of 10 from 10^0 up to 10^n.
        """
        return [10 ** i for i in range(n)]

    def generate_random_input(self, input_size: int, seed: Optional[int] = None, *args: Any, **kwargs: Any) -> list[int]:
        """
        Generates a list of random integers from range 1 to input_size with replacement.

        Parameters
        ----------
        input_size : int
            Length of the generated list.
        seed : Optional[int]
            Seed for the random generation.
        args : Any
            Additional arguments passed to the random instance generating function.
        kwargs : Any
            Additional keyword arguments passed to the random instance generating function.
        Returns
        -------

        """
        rng = random.Random(seed)
        return [rng.randint(1, input_size) for _ in range(input_size)]

    def run_algorithm(self, input_instance: Iterable[Comparable], descending: bool = True, *args: Any, **kwargs: Any) -> tuple[list[Comparable], int]:
        """
        Run function of the bubble sort algorithm implemented in a stable (relative order of same-valued keys remains) manner.
        Implementation assumes the less naive approach, taking into account that bubbled elements at the end of the array are known to be sorted already.

        Parameters
        ----------
        input_instance : Iterable[Comparable]
            Iterable input instance of comparable objects to run the sorting algorithm on.
            It is copied and then returned as a sorted list.
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
        n_ops : int
            Number of operations (element switches) that were required.
        """
        n_ops = 0
        input_list = list(input_instance)
        for i in range(len(input_list)):
            for j in range(len(input_list) - i - 1):
                if (descending is True and input_list[j] < input_list[j + 1]) or (descending is False and input_list[j] > input_list[j + 1]):
                    input_list[j], input_list[j + 1] = input_list[j + 1], input_list[j]
                    n_ops += 1
        return input_list, n_ops
