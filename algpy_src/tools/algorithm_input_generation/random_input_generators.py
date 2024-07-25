import random
from abc import ABC, abstractmethod
from itertools import combinations
from typing import Optional, Generic, Iterable, TypeVar

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.graph_algorithms.traversal.bfs import BreadthFirstSearch
from algpy_src.algorithms.sorting.sorting_algorithm import SortingAlgorithm
from algpy_src.base.constants import InputSize, ProblemInstance, Comparable, GraphSize
from algpy_src.data_structures.graphs.base_graph import BaseGraph
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph import Graph

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


class RandomInputGeneratorGraphTraversalAlgorithm(RandomInputGenerator[BaseGraph, GraphSize]):
    """
    Random input generator for graph traversal algorithms (BFS and DFS).
    Generates either a graph or digraph with desired number of nodes and randomly distributed edges between them
    with input size being named tuple of integers specifying number of nodes and edges.
    """

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)

    def generate_random_input(self, input_size: GraphSize) -> BaseGraph:

        rng = random.Random(self.seed)
        if rng.randint(0, 1) == 1:
            graph: BaseGraph = DiGraph()
        else:
            graph = Graph()

        graph.add_nodes_from(range(input_size.nodes))
        random_edge_pairs = rng.sample(list(combinations(graph.nodes, 2)), input_size.edges)
        graph.add_edges_from((source, target, None) for source, target in random_edge_pairs)

        return graph


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
    if isinstance(algorithm, BreadthFirstSearch):
        return RandomInputGeneratorGraphTraversalAlgorithm
    raise ValueError('No random input generator assigned for this algorithm class.')
