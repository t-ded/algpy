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
        args
        kwargs

        Returns
        -------

        """
        rng = random.Random(seed)
        return [rng.randint(1, input_size) for _ in range(input_size)]

    def run_algorithm(self, input_instance: Iterable[Comparable], *args, **kwargs) -> tuple[list[Comparable], int]:
        # TODO
        return [], 0
