from __future__ import annotations

from abc import abstractmethod
from typing import Generic, Optional, Iterable

from algpy_src.base.constants import Node, EdgeData, Edge
from algpy_src.data_structures.data_structure import DataStructure
from algpy_src.data_structures.graphs.graph_utils.affects_adjacency_matrix import affects_adjacency_matrix
from algpy_src.data_structures.graphs.graph_utils.no_edge_object import NoEdge


class BaseGraph(DataStructure, Generic[Node, EdgeData]):
    """
    Base class for all graphs.
    Adjacency list representation is assumed for simplicity.
    """

    def __init__(self, adjacency_list: Optional[dict[Node, dict[Node, EdgeData]]] = None) -> None:
        """
        Constructor of the BaseGraph class.
        Initializes set of edges, adjacency list and adjacency matrix.

        Parameters
        ----------
        adjacency_list : Optional[dict[Node, dict[Node, EdgeData]]] (default None)
            Optional adjacency list from which to build the graph.
        """
        super().__init__()
        self._edges: set[tuple[Node, Node, EdgeData]] = set()
        self._adjacency_list: dict[Node, dict[Node, EdgeData]] = {}
        self._adjacency_matrix: list[list[EdgeData | NoEdge]] = []
        self._adjacency_matrix_is_actual: bool = True
        if adjacency_list is not None:
            self._adjacency_list = adjacency_list.copy()
            self._fill_missing_nodes_adjacency_list(adjacency_list)
            self._fill_missing_edges_adjacency_list()

    @affects_adjacency_matrix
    def _fill_missing_nodes_adjacency_list(self, adjacency_list: dict[Node, dict[Node, EdgeData]]) -> None:
        """
        Helper method for building the graph from given adjacency list to ensure that all nodes are present in the adjacency list as expected.

        Parameters
        ----------
        adjacency_list : dict[Node, dict[Node, EdgeData]]
            Adjacency list from which the graph is being built.
        """
        for node in adjacency_list:
            for neighbour in adjacency_list[node]:
                self._adjacency_list.setdefault(neighbour, {})

    @affects_adjacency_matrix
    def _fill_missing_edges_adjacency_list(self) -> None:
        """
        Helper method for building the graph from given adjacency list to ensure that all edges are present in the adjacency list as expected.
        """
        for node in self._adjacency_list:
            for neighbour, data in self._adjacency_list[node].items():
                if self.is_multigraph and isinstance(data, set):
                    for single_edge_data in data:
                        self._edges.add((node, neighbour, single_edge_data))
                else:
                    self._edges.add((node, neighbour, data))

    @affects_adjacency_matrix
    def _fill_to_undirected(self) -> None:
        for node in self.nodes:
            for neighbour, data in self._adjacency_list[node].items():
                self._adjacency_list[neighbour][node] = data

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseGraph) and self._adjacency_list == other._adjacency_list

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Base Graph'

    @property
    def space_complexity(self) -> str:
        return 'V + E'

    @property
    @abstractmethod
    def is_directed(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def is_multigraph(self) -> bool:
        raise NotImplementedError()

    @property
    def nodes(self) -> list[Node]:
        """
        Retrieve the nodes of this graph.
        Nodes can be represented by any Python object and the order retrieved here corresponds to the order of being added to the graph.

        Returns
        -------
        nodes : list[Node]
            Nodes of this graph.
        """
        return list(self._adjacency_list.keys())

    @property
    def edges(self) -> set[Edge]:
        """
        Retrieve the edges of this graph.
        Edges are represented as tuples of (source node, destination node, edge data).
        The order retrieved here corresponds to the order of being added to the graph and there can be multiple edges between two nodes in case of a multigraph.
        This method retrieves only one direction of each edge even for undirected graph, which is internally represented as a directed graph with edges going both ways.

        Returns
        -------
        edges : set[Edge]
            Edges of this graph.
        """
        return self._edges

    @property
    def number_of_nodes(self) -> int:
        """
        Retrieve the number of nodes of this graph.

        Returns
        -------
        number_of_nodes : int
            Number of nodes of this graph.
        """
        return len(self.nodes)

    @property
    def number_of_edges(self) -> int:
        """
        Retrieve the number of edges of this graph.
        In case of an undirected graph, each edge is counted only once despite being internally represented as a directed graph.

        Returns
        -------
        number_of_edges : int
            Number of edges of this graph.
        """
        return len(self._edges)

    @property
    def adjacency_list(self) -> dict[Node, dict[Node, EdgeData]]:
        """
        Getter for the adjacency list representation of the graph.

        Returns
        -------
        adjacency_list: dict[Node, dict[Node, EdgeData]]
            Adjacency list representation of the graph, represented as a dict of node : neighbours pairs with
            neighbours being a dict of neighbour : edge data or set of edge data in case of a multigraph.
        """
        return self._adjacency_list

    @property
    def adjacency_matrix(self) -> list[list[EdgeData | NoEdge]]:
        """
        Getter for the adjacency matrix of the graph.
        Note that the graph is internally represented as an adjacency list, thus the adjacency matrix is built in O(n^2) time with O(n^2) space complexity for each call of this method.
        It is then cached as the graph's attribute until further change in the graph.

        Returns
        -------
        adjacency_matrix : list[list[EdgeData | NoEdge]]
            Adjacency matrix representation of the graph object represented as a list of lists with edges represented either by the data itself or set of data in case of a multigraph.
            Symmetrical for undirected graph.
        """
        if not self._adjacency_matrix_is_actual:
            self._build_adjacency_matrix()
            self._adjacency_matrix_is_actual = True
        return self._adjacency_matrix

    def _build_adjacency_matrix(self) -> None:
        """
        Builder method for the adjacency matrix of this graph. Should assign the self._adjacency_matrix attribute.
        """
        self._adjacency_matrix = []
        for u in self.nodes:
            neighbours: list[EdgeData | NoEdge] = []
            for v in self.nodes:
                if v in self._adjacency_list[u]:
                    neighbours.append(self._adjacency_list[u][v])
                else:
                    neighbours.append(NoEdge())
            self._adjacency_matrix.append(neighbours)

    def add_nodes_from(self, nodes: Iterable[Node]) -> None:
        """
        Add multiple nodes from an iterable.

        Parameters
        ----------
        nodes : Iterable[Node]
            Iterable from which to add the nodes.
        """
        for node in nodes:
            self.add_node(node)

    @affects_adjacency_matrix
    def add_node(self, node: Node) -> None:
        """
        Add a single node to the graph.
        Nothing changes if the node already exists.

        Parameters
        ----------
        node : Node
            Node to add.
        """
        self._adjacency_list.setdefault(node, {})

    def remove_nodes_from(self, nodes_to_remove: Iterable[Node]) -> None:
        """
        Remove a given bunch of nodes from the graph.

        Parameters
        ----------
        nodes_to_remove : Iterable[Node]
            Nodes to be removed from the graph.
        """
        for node in nodes_to_remove:
            self.remove_node(node)

    @affects_adjacency_matrix
    def remove_node(self, node: Node) -> None:
        """
        Remove given node from the graph along with all its edges.

        Parameters
        ----------
        node : Node
            Node to be removed.
            If not present in the graph, it is silently ignored.
        """
        if node in self.nodes:
            for other_node in self.nodes:
                if node in self._adjacency_list[other_node]:
                    self.remove_edge((other_node, node, self._adjacency_list[other_node][node]))
            del self._adjacency_list[node]

    def add_edges_from(self, edges: Iterable[Edge]) -> None:
        """
        Add multiple edges from an iterable.

        Parameters
        ----------
        edges : Iterable[Edge]
            Iterable from which to add the edges.
            Edges are represented as tuples of (source node, destination node, edge data).
        """
        for edge in edges:
            self.add_edge(edge)

    def get_edge_data(self, source: Node, target: Node) -> EdgeData | NoEdge:
        if source not in self.nodes:
            raise KeyError('Source node is not present in the graph.')
        if target not in self.nodes:
            raise KeyError('Target node is not present in the graph.')
        return self._adjacency_list[source].get(target, NoEdge())

    @affects_adjacency_matrix
    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        """
        Add a single edge to the graph.
        An edge is a tuple of source node, destination node and edge data. In case of an undirected graph, the reverse edge is also added.
        If an edge is already present in the graph between two nodes and the graph is not a multigraph, edge's data is rewritten by the input of this method.
        Both nodes are silently added to the graph in case they are not present in the graph.

        Parameters
        ----------
        edge : Edge
            The edge to add represented as a tuple of (source node, destination node, edge data).
        """
        raise NotImplementedError()

    def remove_edges_from(self, edges_to_remove: Iterable[Edge | tuple[Node, Node]]) -> None:
        """
        Remove a given bunch of edges from the graph.

        Parameters
        ----------
        edges_to_remove : Iterable[Edge | tuple[Node, Node]]
            Edges to be removed from the graph, given either as tuple(s) (source node, destination node, edge data) or just (source node, destination node).
        """
        for edge in edges_to_remove:
            self.remove_edge(*edge)

    @affects_adjacency_matrix
    @abstractmethod
    def remove_edge(self, source: Node, target: Node, *data: EdgeData) -> None:
        """
        Remove an edge between two nodes from the graph.
        If an edge is not present in the graph, it is silently ignored.
        Either direction can be given for an undirected graph, both respective opposite edges will be removed.
        If data is given, only the edge with matching EdgeData will be removed (both in case of a multigraph and simple graph).
        If data is not given for a multigraph, all edges between the two nodes will be removed.

        Parameters
        ----------
        source : Node
            Source node of the edge to remove.
        target : Node
            Target node of the edge to remove.
        *data : EdgeData
            EdgeData of the edge to be removed.
        """
        raise NotImplementedError()

    def neighbors(self, node: Node) -> set[Node]:
        """
        Return a set of adjacent nodes for a given node.

        Parameters
        ----------
        node : Node
            Node for which to find the neighbours.
            If not present in the graph, empty set is returned.

        Returns
        -------
        neighbours : set[Node]
            A set of adjacent nodes.
        """
        return set(self._adjacency_list.get(node, {}).keys())

    def indegree(self, node: Node) -> int:
        """
        Return indegree for a given node.

        Parameters
        ----------
        node : Node
            Node for which to find the indegree.
            If not present in the graph, 0 is returned.

        Returns
        -------
        indegree : int
            Indegree of the given node.
        """
        if not self.is_directed:
            return sum(len(edges) if isinstance(edges, set) else 1 for edges in self._adjacency_list.get(node, {}).values())

        indegree = 0
        for edge in self._edges:
            if edge[1] == node:
                indegree += len(edge[2]) if isinstance(edge[2], set) else 1
        return indegree

    def outdegree(self, node: Node) -> int:
        """
        Return outdegree for a given node.

        Parameters
        ----------
        node : Node
            Node for which to find the outdegree.
            If not present in the graph, 0 is returned.

        Returns
        -------
        outdegree : int
            Outdegree of the given node.
        """
        return sum(len(edges) if isinstance(edges, set) else 1 for edges in self._adjacency_list.get(node, {}).values())

    def degree(self, node: Node) -> int:
        """
        Return degree for a given node.

        Parameters
        ----------
        node : Node
            Node for which to find the degree.
            If not present in the graph, 0 is returned.

        Returns
        -------
        degree : int
            Degree of the given node.
        """
        if self.is_directed:
            return self.indegree(node) + self.outdegree(node)
        return self.outdegree(node)
