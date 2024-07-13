from typing import Iterable, TypeVar

import numpy as np

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.constants import InputSize

A = TypeVar('A', bound=Algorithm)


def generate_increasing_input_size_sequence(algorithm: A, max_input_size: InputSize, sequence_length: int = 10) -> Iterable[InputSize]:
    """
    Generate increasing input size sequence for the given algorithm.

    Parameters
    ----------
    algorithm : Algorithm
        The algorithm to generate input sizes for.
    max_input_size : InputSize
        Maximal input size to use. Specific datetype and form depends on the algorithm.
    sequence_length : Optional[int] (default 10)
        Number of input size elements in the returned sequence.

    Returns
    -------
    increasing_input_size_sequence : Iterable[InputSize]
        Input size sequence with increasing difficulty.
    """
    if isinstance(algorithm, SortingAlgorithm):
        if isinstance(max_input_size, int):
            return list(np.linspace(1, max_input_size, num=sequence_length, dtype=int))
        raise ValueError("max_input_size must be an integer for SortingAlgorithm's increasing input size sequence generation")

    raise ValueError('No increasing input size sequence generator assigned for this algorithm class.')
