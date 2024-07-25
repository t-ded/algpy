from typing import Optional

from algpy_src.base.constants import Node, SingleEdgeData
from algpy_src.data_structures.graphs.digraph import DiGraph


class TraversalGraph(DiGraph):

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] = None) -> None:
        """
        Constructor of the TraversalGraph class.

        Parameters
        ----------
        adjacency_list : adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] (default None)
            Optional adjacency list from which to build the traversal graph.
        """
        super().__init__(adjacency_list)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TraversalGraph) and list(self._adjacency_list.items()) == list(other._adjacency_list.items())
