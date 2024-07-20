from __future__ import annotations

from typing import Optional

from algpy_src.base.constants import Node, SingleEdgeData, Edge
from algpy_src.data_structures.graphs.base_graph import BaseGraph
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge


class DiGraph(BaseGraph[Node, SingleEdgeData]):
    """
    Simple directed graph class (not multigraph).
    Adjacency list representation is assumed for simplicity.
    """

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] = None) -> None:
        """
        Constructor of the DiGraph class.

        Parameters
        ----------
        adjacency_list : Optional[dict[Node, dict[Node, dict[Node, EdgeData]]]] (default None)
            Optional adjacency list from which to build the graph.
        """
        super().__init__(adjacency_list)

    @property
    def name(self) -> str:
        return 'DiGraph'

    @property
    def is_directed(self) -> bool:
        return True

    @property
    def is_multigraph(self) -> bool:
        return False

    @affects_adjacency_matrix
    def add_edge(self, edge: Edge) -> None:
        """
        Add a single edge to the graph.
        An edge is a tuple of source node, destination node and edge data.
        If an edge is already present in the graph between two nodes, edge's data is rewritten by the input of this method.
        Both nodes are silently added to the graph in case they are not present in the graph.

        Parameters
        ----------
        edge : Edge
            The edge to add represented as a tuple of (source node, destination node, edge data).
        """
        u, v, data = edge
        self.add_nodes_from({u, v})
        self._adjacency_list[u].setdefault(v, data)
        self.edges.add(edge)

    @affects_adjacency_matrix
    def remove_edge(self, source: Node, target: Node, *data: SingleEdgeData) -> None:
        """
        Remove an edge from the graph.
        If an edge is not present in the graph, it is silently ignored.

        Parameters
        ----------
        source : Node
            Source node of the edge to remove.
        target : Node
            Target node of the edge to remove.
        *data : SingleEdgeData
            Data of the edge to be removed. Only one entry has to be given for a simple graph.
        """
        if source not in self.nodes or target not in self.nodes:
            return
        if len(data) > 1:
            raise ValueError('Simple graph cannot have more than 1 edge between two nodes.')
        present_data: SingleEdgeData | NoEdge = self._adjacency_list[source].get(target, NoEdge())
        if present_data == NoEdge or (data and present_data != data[0]):
            return
        del self._adjacency_list[source][target]
        self.edges.remove((source, target, present_data))
