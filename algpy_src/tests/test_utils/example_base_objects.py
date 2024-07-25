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

    def get_worst_case_arguments(self, input_size: InputSize) -> dict[str, Any]:
        return {'input_instance': [1]}

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0,
                      *args: Any, **kwargs: Any) -> tuple[bool, Optional[Iterable[Comparable]]]:
        return True, None


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

    def get_worst_case_arguments(self, input_size: int) -> dict[str, Any]:
        return {'input_instance': [1, 2, 3]}

    def run_algorithm(self, input_instance: Iterable[Comparable], verbosity_level: VERBOSITY_LEVELS = 0, descending: bool = True,
                      *args: Any, **kwargs: Any) -> tuple[bool, list[Comparable]]:
        return True, list(sorted(input_instance))
