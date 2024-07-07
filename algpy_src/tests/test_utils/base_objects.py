from typing import Any, Optional, Iterable

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.complexity_object import ComplexityObject
from algpy_src.base.constants import Comparable, VERBOSITY_LEVELS


class ExampleComplexityObject(ComplexityObject):

    @property
    def name(self) -> str:
        return 'Example Complexity Object'

    @property
    def space_complexity(self) -> str:
        return 'N/A'


class ExampleSortingAlgorithm(SortingAlgorithm, Algorithm[Iterable[Comparable], int]):

    @property
    def name(self) -> str:
        return 'Example Sorting Algorithm'

    @property
    def best_case_time_complexity(self) -> str:
        return 'N/A'

    @property
    def best_case_description(self) -> str:
        return 'N/A'

    @property
    def average_case_time_complexity(self) -> str:
        return 'N/A'

    @property
    def worst_case_time_complexity(self) -> str:
        return 'N/A'

    @property
    def worst_case_description(self) -> str:
        return 'N/A'

    @property
    def space_complexity(self) -> str:
        return 'N/A'

    def generate_increasing_input_size_sequence(self, *args: Any, **kwargs: Any) -> Iterable[int]:
        return [1, 2, 3]

    def generate_random_input(self, input_size: int, seed: Optional[int] = None, *args: Any, **kwargs: Any) -> Iterable[Comparable]:
        return [1, 2, 3]

    def generate_worst_case(self, input_size: int, *args: Any, **kwargs: Any) -> Iterable[Comparable]:
        return [1, 2, 3]

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> list[Comparable]:
        return list(sorted(input_instance))
