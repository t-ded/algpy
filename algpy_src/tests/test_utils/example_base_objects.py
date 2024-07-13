from typing import Any, Optional, Iterable

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.complexity_object import ComplexityObject
from algpy_src.base.constants import Comparable, VERBOSITY_LEVELS, InputSize


class ExampleComplexityObject(ComplexityObject):

    @property
    def name(self) -> str:
        return 'Example Complexity Object'

    @property
    def space_complexity(self) -> str:
        return 'N/A'


class ExampleAlgorithm(Algorithm[Iterable[Comparable], int]):

    @property
    def name(self) -> str:
        return 'Example Algorithm'

    @property
    def is_deterministic(self) -> bool:
        return True

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

    def generate_worst_case(self, input_size: InputSize, *args: Any, **kwargs: Any) -> Iterable[Comparable]:
        return [1]

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0,
                      *args: Any, **kwargs: Any) -> Optional[Iterable[Comparable]]:
        return None


class ExampleSortingAlgorithm(SortingAlgorithm):

    @property
    def name(self) -> str:
        return 'Example Sorting Algorithm'

    @property
    def is_deterministic(self) -> bool:
        return True

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

    @property
    def is_stable(self) -> bool:
        return True

    def generate_worst_case(self, input_size: int, *args: Any, **kwargs: Any) -> Iterable[Comparable]:
        return [1, 2, 3]

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> list[Comparable]:
        return list(sorted(input_instance))
