from __future__ import annotations

from typing import Optional

from algpy_src.base.constants import Node, SingleEdgeData, Edge
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix


class Graph(DiGraph):
    """
    Simple graph class (undirected, not multigraph).
    Adjacency list representation is assumed for simplicity.
    Internally, Graph is represented as a DiGraph with edges going both ways.
    """

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] = None) -> None:
        """
        Constructor of the Graph class.

        Parameters
        ----------
        adjacency_list : adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] (default None)
            Optional adjacency list from which to build the graph.
            If one direction edges are given, they are filled to their other direction.
            If edges in both directions are given with conflicting data, this data is arbitrarily rewritten to one of the entries.
        """
        super().__init__(adjacency_list)
        super()._fill_to_undirected()

    @property
    def name(self) -> str:
        return 'Graph'

    @property
    def is_directed(self) -> bool:
        return False

    @property
    def is_multigraph(self) -> bool:
        return False

    @affects_adjacency_matrix
    def add_edge(self, edge: Edge) -> None:
        """
        Add a single edge to the graph.
        An edge is a tuple of two nodes and edge data.
        If an edge is already present in the graph between two nodes, edge's data is rewritten by the input of this method.
        Both nodes are silently added to the graph in case they are not present in the graph.

        Parameters
        ----------
        edge : Edge
            The edge to add represented as a tuple of (nodeA, nodeB, edge data).
        """
        u, v, data = edge
        super().add_edge(edge)
        self._adjacency_list[v].setdefault(u, data)

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
        super().remove_edge(source, target, data)
        super().remove_edge(target, source, data)
