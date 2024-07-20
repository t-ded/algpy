from __future__ import annotations

from typing import Optional

from algpy_src.base.constants import Node, Edge, MultiEdgeData
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.multidigraph import MultiDiGraph


class MultiGraph(MultiDiGraph):
    """
    Undirected multigraph class.
    Adjacency list representation is assumed for simplicity.
    """

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, MultiEdgeData]]]) -> None:
        """
        Constructor of the MultiGraph class.

        Parameters
        ----------
        adjacency_list : Optional[dict[Node, dict[Node, dict[Node, MultiEdgeData]]]] (default None)
            Optional adjacency list from which to build the graph.
        """
        super().__init__(adjacency_list)
        super()._fill_to_undirected()

    @property
    def name(self) -> str:
        return 'MultiGraph'

    @property
    def is_directed(self) -> bool:
        return False

    @property
    def is_multigraph(self) -> bool:
        return True

    @affects_adjacency_matrix
    def add_edge(self, edge: Edge) -> None:
        """
        Add a single edge to the graph.
        An edge is a tuple of source node, destination node and edge data.
        If an edge already exists between the two nodes, new edge's data is added to the multi edge data of the present edge.
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
    def remove_edge(self, source: Node, target: Node, *data: MultiEdgeData) -> None:
        """
        Remove an edge from the graph.
        If an edge is not present in the graph, it is silently ignored.

        Parameters
        ----------
        source : Node
            Source node of the edge to remove.
        target : Node
            Target node of the edge to remove.
        *data : MultiEdgeData
            Data of the edge to be removed.
            If not given, all edges between the two nodes are removed.
            Otherwise, each corresponding data entry is removed from the multiedge between the two nodes.
        """
        super().remove_edge(source, target, data)
        super().remove_edge(target, source, data)
