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
        super().__init__()
        self._edges: set[tuple[Node, Node, EdgeData]] = set()
        self._is_directed = directed
        self._is_multigraph = multigraph
        self._adjacency_list: dict[Node, dict[Node, EdgeData | list[EdgeData]]] = {}

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
        return list(self._adjacency_list.keys())

    @property
    def edges(self) -> set[tuple[Node, Node, EdgeData]]:
        return self._edges

    @property
    def number_of_nodes(self) -> int:
        return len(self.nodes)

    @property
    def number_of_edges(self) -> int:
        return len(self._edges)

    @property
    def adjacency_list(self) -> dict[Node, dict[Node, EdgeData | list[EdgeData]]]:
        return self._adjacency_list

    @property
    def adjacency_matrix(self) -> list[list[Optional[EdgeData | list[EdgeData]]]]:
        adj_matrix: list[list[Optional[EdgeData | list[EdgeData]]]] = []
        for i, u in enumerate(self.nodes):
            adj_matrix.append([])
            for v in self.nodes:
                adj_matrix[i].append(self.adjacency_list.get(u, {}).get(v, None))
        return adj_matrix

    def add_nodes_from(self, nodes: Iterable[Node]) -> None:
        for node in nodes:
            self.add_node(node)

    def add_node(self, node: Node) -> None:
        self._adjacency_list.setdefault(node, {})

    def add_edges_from(self, edges: Iterable[tuple[Node, Node, EdgeData]]) -> None:
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge: tuple[Node, Node, EdgeData]) -> None:
        u, v, data = edge
        self.add_nodes_from({u, v})
        if self.is_multigraph:
            if v in self._adjacency_list[u]:
                cast(list[EdgeData], self._adjacency_list[u][v]).append(data)
                if not self.is_directed:
                    cast(list[EdgeData], self._adjacency_list[u][v]).append(data)
            else:
                self._adjacency_list[u][v] = [data]
                if not self.is_directed:
                    self._adjacency_list[v][u] = [data]
        else:
            self._adjacency_list[u][v] = data
            if not self._is_directed:
                self._adjacency_list[v][u] = data
        self.edges.add(edge)

    def neighbors(self, node: Node) -> set[Node]:
        return set(self._adjacency_list.get(node, {}).keys())

    def degree(self, node: Node) -> int:
        return len(self._adjacency_list.get(node, {}))

    @classmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[Node, dict[Node, EdgeData]]) -> G:
        raise NotImplementedError()
