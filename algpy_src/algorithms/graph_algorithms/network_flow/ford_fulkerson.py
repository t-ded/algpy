from collections import namedtuple
from typing import Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import VERBOSITY_LEVELS, Node, FlowEdgeData
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.flow_network import FlowNetwork
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge

FordFulkersonGraphSize = namedtuple('FordFulkersonGraphSize', 'edges max_capacity')


class FordFulkersonAlgorithm(Algorithm[FlowNetwork, FordFulkersonGraphSize, FlowNetwork]):
    """
    Ford-Fulkerson's algorithm for finding the maximum flow within a flow network.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name="Ford-Fulkerson's Max-Flow Algorithm",
            algorithm_family=AlgorithmFamily.MAX_FLOW,
            is_deterministic=True,
            best_case_time_complexity='|E|',
            best_case_description='maximum flow found in 1 iteration',
            average_case_time_complexity='|E| * f_max',
            worst_case_time_complexity='|E| * f_max',
            worst_case_description='every augmenting path improving current flow by 1',
            space_complexity='|V| + |E|',
        )

    def get_worst_case_arguments(self, input_size: FordFulkersonGraphSize) -> dict[str, Any]:
        """
        Generate a flow network with input_size.edges edges which will be a line graph
        of input_size.max_capacity edges with one bottleneck split-merge section.

        Parameters
        ----------
        input_size : FordFulkersonGraphSize
            Tuple of n_edges, max_capacity with desired flow network size and maximum edge capacity.
            Number of edges is expected to be at least 5 and the network will have (n_edges - 1) nodes.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with the created flow network as 'input_instance' value, which also stores the source and sink nodes as the first and last node in the chain.
        """
        n_edges = min(5, input_size.edges)
        n_nodes = n_edges - 1
        capacity = input_size.max_capacity
        g: FlowNetwork[int] = FlowNetwork({0: {}, n_nodes - 1: {}}, source=0, sink=n_nodes - 1)
        g.add_nodes_from(range(0, n_nodes))

        g.add_edges_from([
            (0, 1, FlowEdgeData(0, None, capacity)),
            (0, 2, FlowEdgeData(0, None, capacity)),
            (1, 2, FlowEdgeData(0, None, 1)),
            (1, 3, FlowEdgeData(0, None, capacity)),
            (2, 3, FlowEdgeData(0, None, capacity)),
        ])

        num_edges = 5
        current_last = 3
        while num_edges < input_size.edges:
            g.add_node(current_last + 1)
            g.add_edge((current_last, current_last + 1, FlowEdgeData(0, None, capacity)))
            num_edges += 1
        return {'input_instance': g}

    def run_algorithm(self, input_instance: FlowNetwork[Node], verbosity_level: VERBOSITY_LEVELS = 0, find_initial_feasible: bool = True,
                      *args: Any, **kwargs: Any) -> tuple[bool, FlowNetwork[Node]]:
        """
        Run function of Ford-Fulkerson's maximum flow algorithm.

        Parameters
        ----------
        input_instance : FlowNetwork[Node]
            Flow network within which to find the maximum flow. Also stores source and sink values.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print the flow in the beginning and in the end and
            2 meaning also print the maximum flow after each augmentation along with the augmentation path found.
        find_initial_feasible : bool (default True)
            If True, start the algorithm by finding an initial feasible flow.
            Initial feasible flow is a prerequisite for the Ford-Fulkerson's algorithm and if this parameter is set to False, it is assumed
            that the input_instance FlowNetwork object already has a feasible flow assigned to it. If that is not the case, setting this to False may lead to incorrect results.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, FlowNetwork[Node]]
            Returns True in the first index after termination (always terminates with integer capacities) and FlowNetwork with all edge flows set in the second index.
        """
        augmenting_path: list[tuple[Node, Node]]
        while augmenting_path := self.find_augmenting_path(input_instance):

            capacity = float('inf')
            current = input_instance.source
            for src, tgt in augmenting_path:

                candidate_capacity = float('inf')
                if current == src:
                    if not isinstance(flow_edge_data := input_instance.get_edge_data(src, tgt), NoEdge):
                        candidate_capacity = flow_edge_data.upper_bound - flow_edge_data.flow
                    current = tgt
                elif current == tgt:
                    if not isinstance(flow_edge_data := input_instance.get_edge_data(tgt, src), NoEdge):
                        candidate_capacity = flow_edge_data.flow - flow_edge_data.lower_bound
                    current = src

                if candidate_capacity < capacity:
                    capacity = candidate_capacity

            current = input_instance.source
            for src, tgt in augmenting_path:
                if current == src:
                    if not isinstance(flow_edge_data := input_instance.get_edge_data(src, tgt), NoEdge):
                        input_instance.change_flow_between_nodes(src, tgt, flow_edge_data.flow + capacity)
                    current = tgt
                elif current == tgt:
                    if not isinstance(flow_edge_data := input_instance.get_edge_data(tgt, src), NoEdge):
                        input_instance.change_flow_between_nodes(tgt, src, flow_edge_data.flow - capacity)
                    current = src

        return True, input_instance

    def find_augmenting_path(self, input_instance: Graph | DiGraph) -> list[tuple[Node, Node]]:
        """
        Find the next augmenting path along which to increase the flow.

        Parameters
        ----------
        input_instance
            Flow network within which to find the maximum flow. Also stores source and sink values.

        Returns
        -------
        augmenting_path: list[tuple[Node, Node]]
            Sequence of source-target pairs which provides the next augmenting path.
        """
        raise NotImplementedError()
