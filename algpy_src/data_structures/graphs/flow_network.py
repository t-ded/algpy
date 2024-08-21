import math
from typing import Optional

from algpy_src.base.constants import Node, FlowEdgeData
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge


class FlowNetwork(DiGraph):

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, FlowEdgeData]]] = None, check_input_flow_validity: bool = False) -> None:
        """
        Constructor of the FlowNetwork class.

        Parameters
        ----------
        adjacency_list : adjacency_list: Optional[dict[Node, dict[Node, FlowEdge]]] (default None)
            Optional adjacency list from which to build the flow network. Edge data are named tuples with numeric fields (lower_bound, flow, upper_bound).
            Flow values between nodes may be None in case Flow has not been assigned yet.
        check_input_flow_validity : bool (default False)
            Validity of flow given in this constructor may be optionally checked with computation cost of O(n^2).
        """
        super().__init__(adjacency_list)
        if check_input_flow_validity and adjacency_list is not None:
            self.check_flow_validity()

    def check_flow_validity(self) -> None:
        for node in self.adjacency_list.keys():

            for out_neighbour, out_edge in self.adjacency_list[node].items():
                if not self.is_flow_within_bounds(out_edge):
                    raise ValueError(f'Given edge between nodes {node}, {out_neighbour} has initial flow of {out_edge.flow},'
                                     f' which is outside the bounds of [{out_edge.lower_bound}, {out_edge.upper_bound}].')

            flow_balance = self.get_node_balance(node)
            if not math.isclose(flow_balance, 0):
                raise ValueError(f"Flow balance of node {node} is {flow_balance}, which does not follow Kirchhoff's law.")

    @staticmethod
    def is_flow_within_bounds(edge_data: FlowEdgeData) -> bool:
        return edge_data.flow is None or edge_data.lower_bound < edge_data.flow < edge_data.upper_bound

    def get_node_balance(self, node: Node) -> int | float:
        flow_balance = 0
        for out_neighbour, out_edge in self.adjacency_list[node].items():
            flow_balance += out_edge.flow if out_edge.flow is not None else 0
        for in_neighbour, in_edge in self.adjacency_list_transposed[node].items():
            flow_balance -= in_edge.flow if in_edge.flow is not None else 0
        return flow_balance

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FlowNetwork) and self._adjacency_list == other.adjacency_list

    @property
    def name(self) -> str:
        return 'Flow Network'

    @affects_adjacency_matrix
    def change_flow_between_nodes(self, source: Node, target: Node, new_flow: int | float) -> None:
        """
        Change flow between two nodes to new_flow.
        Raises ValueError if new flow is not within bounds for the edge between the two nodes (including case when edge between the two nodes does not exist).

        Parameters
        ----------
        source : Node
            Source of the edge with flow to be changed.
        target : Node
            Target of the edge with flow to be changed.
        new_flow : int | float
            New value of the flow to be assigned to the edge.
        """
        current_flow_edge = self.get_edge_data(source, target)
        if not isinstance(current_flow_edge, NoEdge):
            self.adjacency_list[source][target].flow = new_flow
