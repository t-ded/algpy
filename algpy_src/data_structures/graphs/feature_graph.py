from typing import Optional, override, TypeVar, Generic

from algpy_src.base.constants import Node, SingleEdgeData
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode

F = TypeVar('F')


class FeatureGraph(DiGraph, Generic[F]):

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] = None) -> None:
        """
        Constructor of the FeatureGraph class.

        Parameters
        ----------
        adjacency_list : adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] (default None)
            Optional adjacency list from which to build the traversal graph.
        """
        super().__init__(adjacency_list)
        self._node_features: dict[Node, F] = {}

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, FeatureGraph) and self == other and self._node_features == other.node_features

    @override
    @property
    def name(self) -> str:
        return 'Feature Graph'

    @property
    def node_features(self) -> dict[Node, F]:
        """
        Getter for the node features dictionary of the graph.

        Returns
        -------
        node_features: dict[Node, F]
            Dictionary of node features assigned to each node.
        """
        return self._node_features

    @affects_adjacency_matrix
    def add_node_with_features(self, node: Node, features: F) -> None:
        """
        Add a single node to the graph and assign its features.
        If the node already exists, its features are rewritten.

        Parameters
        ----------
        node : Node
            Node to add.
        features : F
            Features to be assigned to the node
        """
        super().add_node(node)
        self._node_features[node] = features

    @override
    def remove_node(self, node: Node) -> None:
        """
        Remove a node from the graph.
        If a node does not exist in the graph, it is silently ignored.

        Parameters
        ----------
        node : Node
            Node to be removed.
        """
        super().remove_node(node)
        self._node_features.pop(node)

    def get_node_features(self, node: Node) -> F | NoNode:
        """
        Return node features of the given node.

        Parameters
        ----------
        node : Node
            Node to retrieve the features for.

        Returns
        -------
        node_features : F | NoNode
            Node features of the given node.
            Returns NoNode() object if the node is not present in the graph.
        """
        return self._node_features.get(node, NoNode())
