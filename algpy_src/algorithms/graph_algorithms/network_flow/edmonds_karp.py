from typing import Any, Optional

from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.algorithms.graph_algorithms.network_flow.ford_fulkerson import FordFulkersonAlgorithm
from algpy_src.base.constants import Node, Edge, GraphSize
from algpy_src.data_structures.graphs.flow_network import FlowNetwork
from algpy_src.data_structures.linear.queue import Queue


class EdmondsKarp(FordFulkersonAlgorithm):
    """
    Edmonds-Karp's algorithm for finding the maximum flow within a flow network.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name="Edmonds-Karp's Max-Flow Algorithm",
            algorithm_family=AlgorithmFamily.MAX_FLOW,
            is_deterministic=True,
            best_case_time_complexity='|E|',
            best_case_description='maximum flow found in 1 iteration',
            average_case_time_complexity='|V| * |E| ^ 2',
            worst_case_time_complexity='|V| * |E| ^ 2',
            worst_case_description='every augmenting path improving current flow by 1',
            space_complexity='|V| + |E|',
        )

    def get_worst_case_arguments(self, input_size: GraphSize) -> dict[str, Any]:  # type: ignore
        """
        Generate a flow network with input_size.edges edges which will be a line graph
        of input_size.max_capacity edges with one bottleneck split-merge section.

        Parameters
        ----------
        input_size : GraphSize
            Tuple of n_nodes, n_edges with desired dimensions of the graph.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with the created flow network as 'input_instance' value, which also stores the source and sink nodes as the first and last node in the chain.
        """
        n_edges = max(2, input_size.edges)
        n_nodes = 2 + n_edges // 2
        g: FlowNetwork[int] = FlowNetwork({0: {}, n_nodes - 1: {}}, source=0, sink=n_nodes - 1)
        g.add_nodes_from(range(0, n_nodes))
        if input_size.nodes > n_nodes:
            g.add_nodes_from((node + n_nodes for node in range(0, input_size.nodes - n_nodes)))

        for intermediate in range(1, n_nodes - 1):
            g.add_edge(0, intermediate)
            if len(g.edges) < n_edges:
                g.add_edge(intermediate, n_nodes - 1)

        return {'input_instance': g}

    def _find_augmenting_path(self, input_instance: FlowNetwork[Node]) -> Optional[list[Edge]]:
        """
        Find the next augmenting path along which to increase the flow.
        In contrast to Ford-Fulkerson's algorithm, in Edmonds-Karp's algorithm we always select the shortest path via BFS.

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
        queue: Queue[tuple[Node, list[Edge]]] = Queue()
        queue.enqueue((input_instance.source, []))
        shortest_path: Optional[list[Edge]] = None

        while queue.size > 0:
            current_node, path_so_far = queue.dequeue()

            if current_node in visited:
                continue
            visited.add(current_node)

            if current_node == input_instance.sink:
                return path_so_far

            for successor, flow_edge_data in input_instance.adjacency_list[current_node].items():
                if successor not in visited and flow_edge_data.flow < flow_edge_data.upper_bound:
                    queue.enqueue((successor, path_so_far + [(current_node, successor, flow_edge_data)]))

            for predecessor, flow_edge_data in input_instance.adjacency_list_transposed[current_node].items():
                if predecessor not in visited and flow_edge_data.lower_bound < flow_edge_data.flow:
                    queue.enqueue((predecessor, path_so_far + [(predecessor, current_node, flow_edge_data)]))

        return shortest_path
