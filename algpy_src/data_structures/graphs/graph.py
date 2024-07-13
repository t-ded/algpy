from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Type, Generic

from algpy_src.data_structures.data_structure import DataStructure

G = TypeVar('G', bound='Graph')
N = TypeVar('N', bound=object)
E = TypeVar('E', bound=tuple[object, object, object])


class Graph(DataStructure, Generic[N, E]):
    """
    Base class for all graphs.
    """

    def __init__(self, directed: bool = False, multigraph: bool = False) -> None:
        super().__init__()
        self._nodes: set[N] = set()
        self._edges: set[E] = set()
        self._is_directed = directed
        self._is_multigraph = multigraph

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
    def nodes(self) -> set[N]:
        return self._nodes

    @property
    def edges(self) -> set[E]:
        return self._edges

    @property
    def number_of_nodes(self) -> int:
        return len(self._nodes)

    @property
    def number_of_edges(self) -> int:
        return len(self._edges)

    @property
    @abstractmethod
    def adjacency_list(self) -> dict[N, dict[N, object | list[object]]]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def adjacency_matrix(self) -> list[list[object | list[object]]]:
        raise NotImplementedError()

    def add_nodes_from(self, nodes: set[N]) -> None:
        for node in nodes:
            self.add_node(node)

    @abstractmethod
    def add_node(self, node: N) -> None:
        raise NotImplementedError()

    def add_edges_from(self, edges: set[E]) -> None:
        for edge in edges:
            self.add_edge(edge)

    @abstractmethod
    def add_edge(self, edge: E) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[N, dict[N, object | list[object]]]) -> G:
        raise NotImplementedError()
