from collections import defaultdict
from typing import Any, Generic

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.algorithms.graph_algorithms.network_flow.ford_fulkerson import FordFulkersonAlgorithm
from algpy_src.base.constants import VERBOSITY_LEVELS, FlowEdgeData, GraphSize, Node
from algpy_src.data_structures.graphs.flow_network import FlowNetwork
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge


class FeasibleFlowAlgorithm(Algorithm[FlowNetwork, GraphSize, FlowNetwork], Generic[Node]):
    """
    Algorithm for assigning a feasible flow to a given flow network.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name="Feasible Flow Algorithm",
            algorithm_family=AlgorithmFamily.MAX_FLOW,
            is_deterministic=True,
            best_case_time_complexity='|E|',
            best_case_description='all flow edge lower bounds set to zero',
            average_case_time_complexity='|V| * |E| ^ 2',
            worst_case_time_complexity='|V| * |E| ^ 2',
            worst_case_description='every augmenting path improving current flow by 1',
            space_complexity='|V| + |E|',
        )

    def get_worst_case_arguments(self, input_size: GraphSize) -> dict[str, Any]:
        """
        Generate a flow network with input_size.nodes nodes and input_size.edges edges.
        The graph instance starts as a star graph, sequentially adding new star roots until desired number of edges is reached or until the graph is fully connected.

        Parameters
        ----------
        input_size : int
            Tuple of n_nodes, n_edges with desired flow network size.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with the created flow network as 'input_instance' value, which also stores the source and sink nodes as the first and last node in the range.
        """
        g: FlowNetwork[int] = FlowNetwork({0: {}, input_size.nodes - 1: {}}, source=0, sink=input_size.nodes - 1)
        g.add_nodes_from(range(0, input_size.nodes))
        num_edges = 0
        root = 0
        while num_edges < input_size.edges and root + 1 < input_size.nodes:
            for new_neighbour in range(root + 1, input_size.nodes):
                g.add_edge((root, new_neighbour, FlowEdgeData(0, None, 1)))
                num_edges += 1
                if num_edges == input_size.edges:
                    break
            root += 1
        return {'input_instance': g}

    def run_algorithm(self, input_instance: FlowNetwork, verbosity_level: VERBOSITY_LEVELS = 0,
                      *args: Any, **kwargs: Any) -> tuple[bool, FlowNetwork]:
        """
        Run function of initial feasible flow setting algorithm.

        Parameters
        ----------
        input_instance : FlowNetwork
            Flow network within which to find the feasible flow. Also stores source and sink values.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print the flow in the beginning and in the end and
            2 meaning also print progress after each step of the algorithm.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, FlowNetwork]
            Returns True in the first index if feasible flow exists in the network and FlowNetwork with the assigned feasible flow in the second network.
        """
        if input_instance.max_lower_bound == 0:
            for edge in input_instance.edges:
                input_instance.change_flow_between_nodes(edge[0], edge[1], 0)
                return True, input_instance

        input_instance_copy: FlowNetwork[str | int] = FlowNetwork(
            {'proxy_source': {}, 'proxy_sink': {}},
            source='proxy_source',
            sink='proxy_sink'
        )
        input_instance_copy.add_edge((input_instance.sink, input_instance.source, FlowEdgeData(0, None, float('inf'))))
        node_balances: defaultdict[Node, int] = defaultdict()
        for src, target, flow_edge in input_instance.edges:
            input_instance_copy.add_edge((src, target, FlowEdgeData(0, 0, flow_edge[2].upper_bound - flow_edge[2].lower_bound)))
            node_balances[src] -= flow_edge[2].lower_bound
            node_balances[target] += flow_edge[2].lower_bound

        for node, balance in node_balances.items():
            if balance > 0:
                input_instance_copy.add_edge((input_instance_copy.source, node, FlowEdgeData(0, 0, balance)))
            elif balance < 0:
                input_instance_copy.add_edge((node, input_instance_copy.sink, FlowEdgeData(0, 0, -balance)))

        res, filled_instance = FordFulkersonAlgorithm().run_algorithm(
            input_instance=input_instance_copy,
            verbosity_level=verbosity_level,
            find_initial_feasible=False
        )
        if res is True:
            for src, target, flow_edge in input_instance.edges:
                new_edge_data = filled_instance.get_edge_data(src, target)
                if not isinstance(new_edge_data, NoEdge):
                    input_instance.change_flow_between_nodes(src, target, new_edge_data.flow)

        return False, input_instance
