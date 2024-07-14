from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Type, Generic

from algpy_src.base.constants import GRAPH_REPRESENTATIONS
from algpy_src.data_structures.data_structure import DataStructure

G = TypeVar('G', bound='Graph')
Node = TypeVar('Node', bound=object)
Edge = TypeVar('Edge', bound=tuple[object, object, object])
EdgeData = TypeVar('EdgeData', bound=object)


class Graph(DataStructure, Generic[Node, Edge, EdgeData]):
    """
    Base class for all graphs.
    """

    def __init__(self, directed: bool = False, multigraph: bool = False, representation: GRAPH_REPRESENTATIONS = 'list') -> None:
        super().__init__()
        self._nodes: set[Node] = set()
        self._edges: set[Edge] = set()
        self._is_directed = directed
        self._is_multigraph = multigraph
        self._representation = representation
        self._adjacency_list: dict[Node, dict[Node, EdgeData | list[EdgeData]]] = {}
        self._adjacency_matrix: list[list[EdgeData | list[EdgeData]]] = []

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Base Graph'

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        raise NotImplementedError()

    @property
    def is_directed(self) -> bool:
        return self._is_directed

    @property
    def is_multigraph(self) -> bool:
        return self._is_multigraph

    @property
    def representation(self) -> str:
        return 'Adjacency ' + self._representation

    @property
    def nodes(self) -> set[Node]:
        return self._nodes

    @property
    def edges(self) -> set[Edge]:
        return self._edges

    @property
    def number_of_nodes(self) -> int:
        return len(self._nodes)

    @property
    def number_of_edges(self) -> int:
        return len(self._edges)

    @property
    @abstractmethod
    def adjacency_list(self) -> dict[Node, dict[Node, EdgeData]]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def adjacency_matrix(self) -> list[list[EdgeData]]:
        raise NotImplementedError()

    def add_nodes_from(self, nodes: set[Node]) -> None:
        for node in nodes:
            self.add_node(node)

    @abstractmethod
    def add_node(self, node: Node) -> None:
        raise NotImplementedError()

    def add_edges_from(self, edges: set[Edge]) -> None:
        for edge in edges:
            self.add_edge(edge)

    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[Node, dict[Node, EdgeData]]) -> G:
        raise NotImplementedError()
