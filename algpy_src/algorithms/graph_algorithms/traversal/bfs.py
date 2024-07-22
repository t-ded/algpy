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

    def get_worst_case_arguments(self, input_size: GraphSize) -> dict[str, Any]:
        """
        Generate a graph with input_size.nodes nodes and input_size.edges edges and search for element that is not present in the graph.
        The graph instance starts as a star graph, sequentially adding new star roots until desired number of edges is reached or until the graph is fully connected.

        Parameters
        ----------
        input_size : GraphSize
            Tuple of n_nodes, n_edges with desired graph size.

        Returns
        -------
        run_algorithm_kwargs: dict[str, Any]
            A dictionary with the created graph as 'input_instance' value and 'element_to_search' which is not present in the graph.
        """
        g: Graph = Graph()
        g.add_nodes_from(range(0, input_size.nodes))
        num_edges = 0
        root = 0
        while num_edges < input_size.edges and root < input_size.nodes:
            for new_neighbour in range(root, input_size.nodes):
                g.add_edge((root, new_neighbour, None))
                num_edges += 1
                if num_edges == input_size.edges:
                    break
            root += 1
        return {'input_instance': g, 'element_to_search': input_size.nodes + 1}

    def run_algorithm(self, input_instance: Graph | DiGraph, verbosity_level: VERBOSITY_LEVELS = 0, element_to_search: Optional[Node] = None, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()
