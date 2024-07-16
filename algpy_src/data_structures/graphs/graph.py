from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Type, Generic, Optional, Iterable, cast

from algpy_src.data_structures.data_structure import DataStructure

G = TypeVar('G', bound='Graph')
Node = TypeVar('Node', bound=object)
EdgeData = TypeVar('EdgeData', bound=object)


class Graph(DataStructure, Generic[Node, EdgeData]):
    """
    Base class for all graphs.
    Adjacency list representation is assumed for simplicity.
    """

    def __init__(self, directed: bool = False, multigraph: bool = False) -> None:
        """
        Constructor of the Graph class. Initializes set of edges, directed and multigraph identifiers and adjacency list.

        Parameters
        ----------
        directed : bool (default False)
             Whether to take this graph as directed.
             In terms of its adjacency list, undirected graph is represented as directed graph with edges going both ways
        multigraph : bool (default False)
            Whether to take this graph as a multigraph.
            In terms of its adjacency list and matrix, edge data is represented as list with each entry representing a single edge between the two respective nodes.
        """
        super().__init__()
        self._edges: set[tuple[Node, Node, EdgeData]] = set()
        self._is_directed = directed
        self._is_multigraph = multigraph
        self._adjacency_list: dict[Node, dict[Node, EdgeData | set[EdgeData]]] = {}
        self._adjacency_matrix: list[list[Optional[EdgeData | set[EdgeData]]]] = []
        self._adjacency_matrix_is_actual: bool = True

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Base Graph'

    @property
    def space_complexity(self) -> str:
        return 'V + E'

    @property
    def is_directed(self) -> bool:
        return self._is_directed

    @property
    def is_multigraph(self) -> bool:
        return self._is_multigraph

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
    def edges(self) -> set[tuple[Node, Node, EdgeData]]:
        """
        Retrieve the edges of this graph.
        Edges are represented as tuples of (source node, destination node, edge data).
        The order retrieved here corresponds to the order of being added to the graph and there can be multiple edges between two nodes in case of a multigraph.
        This method retrieves only one direction of each edge even for undirected graph, which is internally represented as a directed graph with edges going both ways.

        Returns
        -------
        edges : set[tuple[Node, Node, EdgeData]]
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
    def adjacency_list(self) -> dict[Node, dict[Node, EdgeData | set[EdgeData]]]:
        """
        Getter for the adjacency list representation of the graph.

        Returns
        -------
        adjacency_list: dict[Node, dict[Node, dict[Node, EdgeData | set[EdgeData]]]]
            Adjacency list representation of the graph, represented as a dict of node : neighbours pairs with
            neighbours being a dict of neighbour : edge data or set of edge data in case of a multigraph.
        """
        return self._adjacency_list

    @property
    def adjacency_matrix(self, cache_as_attribute: bool = False) -> list[list[Optional[EdgeData | set[EdgeData]]]]:
        """
        Getter for the adjacency matrix of the graph.
        Note that the graph is internally represented as an adjacency list, thus the adjacency matrix is built in O(n^2) time with O(n^2) space complexity for each call of this method.
        It can then be cached as the graph's attribute until further change in the graph.

        Parameters
        -------
        cache_as_attribute : bool (default False)
            Whether to retain the adjacency matrix as the graph's attribute.

        Returns
        -------
        adjacency_matrix : list[list[Optional[EdgeData | set[EdgeData]]]]
            Adjacency matrix representation of the graph object represented as a list of lists with edges represented either by the data itself or set of data in case of a multigraph.
            Symmetrical for undirected graph.
        """
        if not self._adjacency_matrix_is_actual:
            adj_matrix: list[list[Optional[EdgeData | set[EdgeData]]]] = []
            for i, u in enumerate(self.nodes):
                adj_matrix.append([])
                for v in self.nodes:
                    adj_matrix[i].append(self.adjacency_list.get(u, {}).get(v, None))
            if cache_as_attribute is True:
                self._adjacency_matrix = adj_matrix
                self._adjacency_matrix_is_actual = True
            return adj_matrix
        return self._adjacency_matrix

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

    def add_node(self, node: Node) -> None:
        """
        Add a single node to the graph.
        Nothing changes if the node already exists.

        Parameters
        ----------
        node : Node
            Node to add.
        """
        if node not in self._adjacency_list:
            self._adjacency_list[node] = {}
            self._adjacency_matrix_is_actual = False

    def add_edges_from(self, edges: Iterable[tuple[Node, Node, EdgeData]]) -> None:
        """
        Add multiple edges from an iterable.

        Parameters
        ----------
        edges : Iterable[tuple[Node, Node, EdgeData]]
            Iterable from which to add the edges.
            Edges are represented as tuples of (source node, destination node, edge data).
        """
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge: tuple[Node, Node, EdgeData]) -> None:
        """
        Add a single edge to the graph.
        An edge is a tuple of source node, destination node and edge data. In case of an undirected graph, the reverse edge is also added.
        If an edge is already present in the graph between two nodes and the graph is not a multigraph, edge's data is rewritten by the input of this method.
        Both nodes are silently added to the graph in case they are not present in the graph.

        Parameters
        ----------
        edge : tuple[Node, Node, EdgeData]
            The edge to add represented as a tuple of (source node, destination node, edge data).
        """
        u, v, data = edge
        self.add_nodes_from({u, v})
        if self.is_multigraph:
            if v in self._adjacency_list[u]:
                if data not in cast(set[EdgeData], self._adjacency_list[u][v]):
                    self._adjacency_matrix_is_actual = False
                cast(set[EdgeData], self._adjacency_list[u][v]).add(data)
                if not self.is_directed:
                    cast(set[EdgeData], self._adjacency_list[v][u]).add(data)
            else:
                self._adjacency_list[u][v] = {data}
                if not self.is_directed:
                    self._adjacency_list[v][u] = {data}
        else:
            if self._adjacency_list[u].get(v, None) != data:
                self._adjacency_list[u][v] = data
                if not self._is_directed:
                    self._adjacency_list[v][u] = data
                self._adjacency_matrix_is_actual = False
        self.edges.add(edge)

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
        return sum(len(edges) if isinstance(edges, set) else 1 for edges in self._adjacency_list.get(node, {}).values())

    @classmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[Node, dict[Node, EdgeData]]) -> G:
        raise NotImplementedError()
