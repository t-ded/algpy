import random
from abc import ABC, abstractmethod
from typing import Optional, Generic, Iterable, TypeVar

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.constants import InputSize, ProblemInstance, Comparable

A = TypeVar('A', bound=Algorithm)


class RandomInputGenerator(ABC, Generic[ProblemInstance, InputSize]):
    """
    Base class for random input generators.
    """

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed

    @abstractmethod
    def generate_random_input(self, input_size: InputSize) -> ProblemInstance:
        """
        Way to generate single input instance of given size.
        Output of this function has to be accepted by run_algorithm().

        Parameters
        ----------
        input_size : InputSize
            Desired input size (form depends on specific algorithm).

        Returns
        -------
        instance : ProblemInstance
            A problem instance supported in run_algorithm(input_instance=instance).
        """
        raise NotImplementedError()


class RandomInputGeneratorSortingAlgorithm(RandomInputGenerator[Iterable[Comparable], int]):
    """
    Random input generator for sorting algorithms.
    Generates an iterable of random integers with input size being integer specifying number of items.
    """

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)

    def generate_random_input(self, input_size: int) -> Iterable[Comparable]:
        rng = random.Random(self.seed)
        return (rng.randint(1, input_size) for _ in range(input_size))


def get_generator(algorithm: A) -> type[RandomInputGenerator]:
    """
    Assign appropriate random input generator to algorithm.

    Parameters
    ----------
    algorithm : Algorithm subclass
        Algorithm for which the generator is needed.

    Returns
    -------
    random_input_generator : RandomInputGenerator subclass
        Appropriate random input generator.
    """
    if isinstance(algorithm, SortingAlgorithm):
        return RandomInputGeneratorSortingAlgorithm
    raise KeyError('No random input generator assigned for this algorithm class.')
