from typing import Any, Optional

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.constants import GraphSize, VERBOSITY_LEVELS, Node
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph import Graph


class BFS(Algorithm[Graph | DiGraph, GraphSize]):
    """
    Breadth First Search algorithm.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return 'Breadth First Search'

    @property
    def is_deterministic(self) -> bool:
        return True

    @property
    def best_case_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_description(self) -> str:
        return 'starting from searched for element'

    @property
    def average_case_time_complexity(self) -> str:
        return '|V| + |E|'

    @property
    def worst_case_time_complexity(self) -> str:
        return '|V| + |E|'

    @property
    def worst_case_description(self) -> str:
        return 'searched for element not present in the graph'

    @property
    def space_complexity(self) -> str:
        return '|V|'

    def generate_worst_case(self, input_size: GraphSize, *args: Any, **kwargs: Any) -> DiGraph:
        raise NotImplementedError()

    def run_algorithm(self, input_instance: Graph | DiGraph, verbosity_level: VERBOSITY_LEVELS = 0, element_to_search: Optional[Node] = None, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()