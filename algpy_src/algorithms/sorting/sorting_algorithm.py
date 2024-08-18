from abc import abstractmethod
from typing import Iterable, Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import SortingAlgorithmProperties, AlgorithmFamily
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

    @property
    @abstractmethod
    def algorithm_properties(self) -> SortingAlgorithmProperties:
        return SortingAlgorithmProperties(
            name='Base Sorting Algorithm',
            algorithm_family=AlgorithmFamily.SORTING,
            **{field: value for field, value in vars(super().algorithm_properties).items() if field not in ['name', 'algorithm_family']},
            is_stable=True,
        )

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
    def n_ops(self) -> int:
        return self.n_swaps + self.n_comparisons

    @abstractmethod
    def get_worst_case_arguments(self, input_size: int) -> dict[str, Any]:
        """
        Way to generate keyword arguments for this class' run_algorithm method corresponding to algorithm's worst case scenario.
        Output of this function has to be accepted by run_algorithm() and has to contain a pair 'input_instance': ProblemInstance with the value having given InputSize.

        Parameters
        ----------
        input_size : InputSize
            Desired input size (form depends on specific algorithm).

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with keyword arguments for the run_algorithm method.
        """
        raise NotImplementedError()

    @abstractmethod
    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> tuple[bool, list[Comparable]]:
        raise NotImplementedError()
