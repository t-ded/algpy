from typing import Iterable, TypeVar, cast

import numpy as np

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmFamily
from algpy_src.algorithms.graph_algorithms.network_flow.ford_fulkerson import FordFulkersonGraphSize
from algpy_src.base.constants import InputSize, GraphSize, LoadBalancingTaskSize

A = TypeVar('A', bound=Algorithm)


def generate_increasing_input_size_sequence(algorithm: A, max_input_size: InputSize, sequence_length: int = 10) -> Iterable[InputSize]:
    """
    Generate increasing input size sequence for the given algorithm.

    Parameters
    ----------
    algorithm : Algorithm
        The algorithm to generate input sizes for.
    max_input_size : InputSize
        Maximal input size to use. Specific datetype and form depends on the algorithm.
    sequence_length : Optional[int] (default 10)
        Number of input size elements in the returned sequence.

    Returns
    -------
    increasing_input_size_sequence : Iterable[InputSize]
        Input size sequence with increasing difficulty.
    """
    if algorithm.algorithm_family == AlgorithmFamily.SORTING or algorithm.algorithm_family == AlgorithmFamily.SEARCHING:
        if isinstance(max_input_size, int):
            return list(np.linspace(1, max_input_size, num=sequence_length, dtype=int))
        raise ValueError('ax_input_size must be an integer for SORTING and SEARCHING algorithm families increasing input size sequence generation')

    if algorithm.algorithm_family == AlgorithmFamily.GRAPH_TRAVERSAL or algorithm.algorithm_family == AlgorithmFamily.MESSAGE_PASSING:
        if isinstance(max_input_size, GraphSize):
            n_nodes = np.linspace(1, max_input_size.nodes, num=sequence_length, dtype=int)
            n_edges = np.linspace(1, max_input_size.edges, num=sequence_length, dtype=int)
            return cast(list[InputSize], [GraphSize(*(nodes, edges)) for nodes, edges in zip(n_nodes, n_edges)])
        raise ValueError('max_input_size must be of GraphSize type (i.e., pair of integers) for TRAVERSAL and MESSAGE_PASSING algorithm families increasing input size sequence generation')

    if algorithm.algorithm_family == AlgorithmFamily.MAX_FLOW:
        if isinstance(max_input_size, FordFulkersonGraphSize):
            n_edges = np.linspace(1, max_input_size.edges, num=sequence_length, dtype=int)
            upper_bounds = np.linspace(1, max_input_size.max_capacity, num=sequence_length, dtype=int)
            return cast(list[InputSize], [FordFulkersonGraphSize(*(nodes, edges)) for nodes, edges in zip(n_edges, upper_bounds)])
        raise ValueError('max_input_size must be of FordFulkersonGraphSize type for MAX_FLOW algorithm family increasing input size sequence generation')

    if algorithm.algorithm_family == AlgorithmFamily.BACKTRACKING:
        if isinstance(max_input_size, int):
            return list(np.linspace(1, max_input_size, num=sequence_length, dtype=int))
        raise ValueError('max_input_size must be an integer for BACKTRACKING algorithm family increasing input size sequence generation')

    if algorithm.algorithm_family == AlgorithmFamily.LOAD_BALANCING:
        if isinstance(max_input_size, LoadBalancingTaskSize):
            n_tasks = np.linspace(1, max_input_size.num_tasks, num=sequence_length, dtype=int)
            n_servers = np.linspace(1, max_input_size.num_servers, num=sequence_length, dtype=int)
            return cast(list[InputSize], [LoadBalancingTaskSize(*(tasks, servers)) for tasks, servers in zip(n_tasks, n_servers)])
        raise ValueError('max_input_size must be of LoadBalancingTaskSize type (i.e., pair of integers) for LOAD_BALANCING algorithm family increasing input size sequence generation')

    raise ValueError('No increasing input size sequence generator assigned for this algorithm family.')
