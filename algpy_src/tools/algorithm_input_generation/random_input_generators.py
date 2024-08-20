import random
from abc import ABC, abstractmethod
from itertools import combinations
from typing import Optional, Generic, Iterable, TypeVar

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmFamily
from algpy_src.base.constants import InputSize, ProblemInstance, Comparable, GraphSize, LoadBalancingTaskSize
from algpy_src.data_structures.graphs.base_graph import BaseGraph
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.feature_graph import FeatureGraph
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.system_design.load_task import LoadTask
from algpy_src.data_structures.system_design.server import Server

A = TypeVar('A', bound=Algorithm)


class RandomInputGenerator(ABC, Generic[ProblemInstance, InputSize]):
    """
    Base class for random input generators.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
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

    def __init__(self, seed: Optional[int] = None) -> None:
        super().__init__(seed)

    def generate_random_input(self, input_size: int) -> Iterable[Comparable]:
        rng = random.Random(self.seed)
        return (rng.randint(1, input_size) for _ in range(input_size))


class RandomInputGeneratorSearchingAlgorithm(RandomInputGenerator[Iterable[Comparable], int]):
    """
    Random input generator for searching algorithms.
    Generates a sorted iterable of random integers with input size being integer specifying number of items and sort it.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        super().__init__(seed)

    def generate_random_input(self, input_size: int) -> Iterable[Comparable]:
        rng = random.Random(self.seed)
        return sorted(rng.randint(1, input_size) for _ in range(input_size))


class RandomInputGeneratorGraphTraversalAlgorithm(RandomInputGenerator[BaseGraph, GraphSize]):
    """
    Random input generator for graph traversal algorithms (BFS and DFS or shortest paths algorithms).
    Generates either a graph or digraph with desired number of nodes and randomly distributed edges between them
    with input size being named tuple of integers specifying number of nodes and edges.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
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


class RandomInputGeneratorGraphRelationalClassificationAlgorithm(RandomInputGenerator[FeatureGraph, GraphSize]):
    """
    Random input generator for algorithm of relational classification on feature graphs.
    Generates a graph with desired number of nodes and randomly distributed edges between them
    with input size being named tuple of integers specifying number of nodes and edges.
    Then, random ground truth labels are added to randomly sampled half of the nodes.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        super().__init__(seed)

    def generate_random_input(self, input_size: GraphSize) -> FeatureGraph:

        feature_graph: FeatureGraph = FeatureGraph()
        rng = random.Random(self.seed)

        for node in range(input_size.nodes):
            if rng.uniform(0, 1) > 0.5:
                feature_graph.add_node_with_features(node, rng.randint(0, 1))
            else:
                feature_graph.add_node(node)

        random_edge_pairs = rng.sample(list(combinations(feature_graph.nodes, 2)), input_size.edges)
        feature_graph.add_edges_from((source, target, None) for source, target in random_edge_pairs)

        return feature_graph


class RandomInputGeneratorLoadBalancingAlgorithms(RandomInputGenerator[tuple[Iterable[LoadTask], list[Server]], LoadBalancingTaskSize]):
    """
    Random input generator for load balancing algorithms.
    Generates a sequence of tasks with random loads and a sequence of available servers with random capacities.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        super().__init__(seed)

    def generate_random_input(self, input_size: LoadBalancingTaskSize) -> tuple[list[LoadTask], list[Server]]:

        rng = random.Random(self.seed)
        tasks: list[LoadTask] = []
        servers: list[Server] = []

        for i in range(input_size.num_tasks):
            tasks.append(LoadTask(f'random_{i}', rng.uniform(0, 10 ** 5)))
        for j in range(input_size.num_servers):
            servers.append(Server(rng.randint(0, 10 ** 8), f'random_{j}'))

        return tasks, servers


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
    if algorithm.algorithm_family == AlgorithmFamily.SORTING:
        return RandomInputGeneratorSortingAlgorithm
    if algorithm.algorithm_family == AlgorithmFamily.SEARCHING:
        return RandomInputGeneratorSearchingAlgorithm
    if algorithm.algorithm_family == AlgorithmFamily.GRAPH_TRAVERSAL:
        return RandomInputGeneratorGraphTraversalAlgorithm
    if algorithm.algorithm_family == AlgorithmFamily.MESSAGE_PASSING:
        return RandomInputGeneratorGraphRelationalClassificationAlgorithm
    if algorithm.algorithm_family == AlgorithmFamily.LOAD_BALANCING:
        return RandomInputGeneratorLoadBalancingAlgorithms
    raise ValueError('No random input generator assigned for this algorithm class.')
