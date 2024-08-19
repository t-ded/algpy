from dataclasses import dataclass
from enum import StrEnum


class AlgorithmFamily(StrEnum):

    # Base algorithms, Test algorithms, Example algorithms
    BASE_CLASS = 'Base Generic Algorithms'
    EXAMPLE = 'Example Algorithms'

    # Container-based
    SORTING = 'Sorting Algorithms',
    SEARCHING = 'Searching Algorithms',

    # Graph-based
    GRAPH_TRAVERSAL = 'Graph Traversal Algorithms',
    MESSAGE_PASSING = 'Relational Classification Algorithms',

    # System design
    LOAD_BALANCING = 'Load Balancing Algorithms',


@dataclass
class AlgorithmProperties:
    name: str
    algorithm_family: AlgorithmFamily
    is_deterministic: bool
    best_case_time_complexity: str
    best_case_description: str
    average_case_time_complexity: str
    worst_case_time_complexity: str
    worst_case_description: str
    space_complexity: str


@dataclass
class SortingAlgorithmProperties(AlgorithmProperties):
    is_stable: bool

