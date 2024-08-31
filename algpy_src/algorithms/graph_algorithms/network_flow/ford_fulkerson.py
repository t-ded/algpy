from collections import namedtuple, defaultdict
from collections.abc import Iterator
from typing import Any, Optional

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import VERBOSITY_LEVELS, Node, FlowEdgeData, Edge
from algpy_src.base.utils import alternating_binary_generator
from algpy_src.data_structures.graphs.flow_network import FlowNetwork
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge
from algpy_src.data_structures.linear.stack import Stack

FordFulkersonGraphSize = namedtuple('FordFulkersonGraphSize', 'edges max_capacity')


class FordFulkersonAlgorithm(Algorithm[FlowNetwork, FordFulkersonGraphSize, FlowNetwork]):
    """
    Ford-Fulkerson's algorithm for finding the maximum flow within a flow network.
    """

    def __init__(self) -> None:
        super().__init__()
        self._worst_case_alternating_generator: Iterator[bool] = alternating_binary_generator()

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
        n_edges = max(5, input_size.edges)
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
            g.add_edge((current_last, current_last + 1, FlowEdgeData(0, None, 2 * capacity)))
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
        if find_initial_feasible is True:
            is_possible_to_set_feasible = self._set_feasible_flow(input_instance)
            if not is_possible_to_set_feasible:
                return False, input_instance

        augmenting_path: Optional[list[Edge]] = self._find_augmenting_path(input_instance)
        while augmenting_path:

            capacity = float('inf')
            current = input_instance.source
            for src, tgt, flow_edge in augmenting_path:

                candidate_capacity = float('inf')
                if current == src:
                    candidate_capacity = flow_edge.upper_bound - flow_edge.flow
                    current = tgt
                elif current == tgt:
                    candidate_capacity = flow_edge.flow - flow_edge.lower_bound
                    current = src

                if candidate_capacity < capacity:
                    capacity = candidate_capacity

            current = input_instance.source
            for src, tgt, flow_edge in augmenting_path:
                if current == src:
                    input_instance.change_flow_between_nodes(src, tgt, flow_edge.flow + capacity)
                    self.increment_n_ops()
                    current = tgt
                elif current == tgt:
                    input_instance.change_flow_between_nodes(src, tgt, flow_edge.flow - capacity)
                    self.increment_n_ops()
                    current = src

            augmenting_path = self._find_augmenting_path(input_instance)

        return True, input_instance

    def _find_augmenting_path(self, input_instance: FlowNetwork[Node]) -> Optional[list[Edge]]:
        """
        Find the next augmenting path along which to increase the flow.
        To demonstrate the worst case of the pure Ford-Fulkerson's algorithm, this always finds the longest augmenting path
        in contrast to Edmonds-Karp's variant of finding the shortest path.

        Parameters
        ----------
        input_instance : FlowNetwork[Node]
            Flow network within which to find the maximum flow. Also stores source and sink values.

        Returns
        -------
        augmenting_path: list[Edge] | None
            Return None if no augmenting path is found, otherwise return a sequence of edges representing the augmenting path from source to sink.
        """
        visited: set[Node] = set()
        stack: Stack[tuple[Node, list[Edge]]] = Stack()
        stack.push((input_instance.source, []))
        longest_path: Optional[list[Edge]] = None
        to_reverse: bool = next(self._worst_case_alternating_generator)

        while stack.size > 0:
            current_node, path_so_far = stack.pop()

            if current_node in visited:
                continue
            visited.add(current_node)

            if current_node == input_instance.sink:
                if longest_path is None or len(path_so_far) > len(longest_path):
                    longest_path = path_so_far

            for successor, flow_edge_data in sorted(input_instance.adjacency_list[current_node].items(), reverse=to_reverse):
                if successor not in visited and flow_edge_data.flow < flow_edge_data.upper_bound:
                    stack.push((successor, path_so_far + [(current_node, successor, flow_edge_data)]))

            for predecessor, flow_edge_data in input_instance.adjacency_list_transposed[current_node].items():
                if predecessor not in visited and flow_edge_data.lower_bound < flow_edge_data.flow:
                    stack.push((predecessor, path_so_far + [(predecessor, current_node, flow_edge_data)]))

        return longest_path

    @staticmethod
    def _set_feasible_flow(input_instance: FlowNetwork[Node]) -> bool:
        if input_instance.max_lower_bound == 0:
            for edge in input_instance.edges:
                input_instance.change_flow_between_nodes(edge[0], edge[1], 0)
            return True

        input_instance_copy: FlowNetwork[str | int] = FlowNetwork(
            {'proxy_source': {}, 'proxy_sink': {}},
            source='proxy_source',
            sink='proxy_sink'
        )
        input_instance_copy.add_edge((input_instance.sink, input_instance.source, FlowEdgeData(0, None, float('inf'))))
        node_balances: defaultdict[Node, int] = defaultdict(int)
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
            find_initial_feasible=False
        )
        if res is True:
            for src, target, flow_edge in input_instance.edges:
                new_edge_data = filled_instance.get_edge_data(src, target)
                if not isinstance(new_edge_data, NoEdge):
                    input_instance.change_flow_between_nodes(src, target, new_edge_data.flow)
            return True

        return False