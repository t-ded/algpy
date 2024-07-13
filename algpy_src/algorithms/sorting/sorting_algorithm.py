from abc import abstractmethod
from typing import Iterable, Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.constants import Comparable, VERBOSITY_LEVELS


class SortingAlgorithm(Algorithm[Iterable[Comparable], int]):
    """
    Base class for sorting algorithms.
    Implements attributes n_comparisons and n_swaps
    """

    def __init__(self) -> None:
        super().__init__()
        self.n_comparisons = 0
        self.n_swaps = 0

    def increment_n_comparisons(self, increment: int = 1) -> None:
        self.n_comparisons += increment

    def reset_n_comparisons(self) -> None:
        self.n_comparisons = 0

    def increment_n_swaps(self, increment: int = 1) -> None:
        self.n_swaps += increment

    def reset_n_swaps(self) -> None:
        self.n_swaps = 0

    def reset_all_counters(self) -> None:
        self.n_swaps = 0
        self.n_comparisons = 0

    @property
    def name(self) -> str:
        return 'Base Sorting Algorithm'

    @property
    def is_deterministic(self) -> bool:
        raise NotImplementedError()

    @property
    def n_ops(self) -> int:
        return self.n_swaps + self.n_comparisons

    @property
    @abstractmethod
    def is_stable(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def generate_worst_case(self, input_size: int, *args: Any, **kwargs: Any) -> Iterable[Comparable]:
        """
        Way to generate single input instance of given size corresponding to algorithm's worst case scenario.
        Output of this function has to be accepted by run_algorithm().

        Parameters
        ----------
        input_size : InputSize
            Desired input size (form depends on specific algorithm).
        *args : Any
            Additional arguments passed to the generating function.
        **kwargs : Any
            Additional keyword arguments passed to the generating function.

        Returns
        -------
        instance : ProblemInstance
            A problem instance supported in run_algorithm(input_instance=instance).
        """
        raise NotImplementedError()

    @abstractmethod
    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> list[Comparable]:
        raise NotImplementedError()
