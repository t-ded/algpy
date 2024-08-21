from typing import Optional, TypeVar, Generic

from algpy_src.base.constants import Node, SingleEdgeData
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.graph_utils.no_feature_object import NoFeature
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode

F = TypeVar('F')


class FeatureGraph(Graph, Generic[F]):

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] = None, node_features: Optional[dict[Node, F]] = None) -> None:
        """
        Constructor of the FeatureGraph class.

        Parameters
        ----------
        adjacency_list : adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] (default None)
            Optional adjacency list from which to build the feature graph.
        node_features : Optional[dict[Node, F]] (default None)
            Node features mapping to start the graph from. If any nodes present here are not in the adjacency list, they are silently added.
        """
        super().__init__(adjacency_list)
        if node_features is None:
            node_features = {}
        self._node_features: dict[Node, F] = node_features
        self.add_nodes_from(set(node_features.keys()) - set(self._adjacency_list.keys()))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FeatureGraph) and self._adjacency_list == other.adjacency_list and self._node_features == other.node_features

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

    def add_nodes_with_features_from(self, node_features_mapping: dict[Node, F]) -> None:
        """
        Add nodes along with their features from a bunch.

        Parameters
        ----------
        node_features_mapping : dict[Node, F]
            Dictionary of node : node features pairs to add as nodes.
        """
        for node, feature in node_features_mapping.items():
            self.add_node_with_features(node, feature)

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

    def get_node_features(self, node: Node) -> F | NoNode | NoFeature:
        """
        Return node features of the given node.

        Parameters
        ----------
        node : Node
            Node to retrieve the features for.

        Returns
        -------
        node_features : F | NoNode | NoFeature
            Node features of the given node.
            Returns NoNode() object if the node is not present in the graph and NoFeature() object if it does not have features assigned.
        """
        if node not in self.nodes:
            return NoNode()
        return self._node_features.get(node, NoFeature())
