from __future__ import annotations

from typing import Optional

from algpy_src.base.constants import Node, SingleEdgeData, Edge, MultiEdgeData
from algpy_src.data_structures.graphs.base_graph import BaseGraph
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge


class MultiDiGraph(BaseGraph[Node, MultiEdgeData]):
    """
    Directed multigraph class.
    Adjacency list representation is assumed for simplicity.
    """

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, MultiEdgeData]]]) -> None:
        """
        Constructor of the MultiDiGraph class.

        Parameters
        ----------
        adjacency_list : Optional[dict[Node, dict[Node, dict[Node, MultiEdgeData]]]] (default None)
            Optional adjacency list from which to build the graph.
        """
        super().__init__(adjacency_list)

    @property
    def name(self) -> str:
        return 'MultiDiGraph'

    @property
    def is_directed(self) -> bool:
        return True

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
            The edge to add represented as a tuple of (source node, destination node, edge data).
        """
        u, v, data = edge
        self.add_nodes_from({u, v})
        if not isinstance(data, set):
            data = {data}
        self._adjacency_list[u].setdefault(v, set()).update(data)
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
            Data of the edge to be removed.
            If not given, all edges between the two nodes are removed.
            Otherwise, each corresponding data entry is removed from the multiedge between the two nodes.
        """
        if source not in self.nodes or target not in self.nodes:
            return
        present_data: MultiEdgeData | NoEdge = self._adjacency_list[source].get(target, NoEdge())
        if present_data != NoEdge:
            if not data:
                del self._adjacency_list[source][target]
                self.edges.remove((source, target, present_data))
            else:
                for value in data:
                    self._adjacency_list[source][target].remove(value)
