from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Type

from algpy_src.data_structures.data_structure import DataStructure

G = TypeVar('G', bound='Graph')


class Graph(DataStructure):
    """
    Base class for all graphs.
    """

    def __init__(self, directed: bool = False, multigraph: bool = False) -> None:
        super().__init__()
        self._nodes: set[object] = set()
        self._edges: set[tuple[object, object, object]] = set()
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
    def nodes(self) -> set[object]:
        return self._nodes

    @property
    def edges(self) -> set[tuple[object, object, object]]:
        return self._edges

    @property
    def number_of_nodes(self) -> int:
        return len(self._nodes)

    @property
    def number_of_edges(self) -> int:
        return len(self._edges)

    @property
    @abstractmethod
    def adjacency_list(self) -> dict[object, dict[object, object | list[object]]]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def adjacency_matrix(self) -> list[list[object | list[object]]]:
        raise NotImplementedError()

    @abstractmethod
    def add_node(self, node: object) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_edge(self, edge: tuple[object, object, object]) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[object, dict[object, object]]) -> G:
        raise NotImplementedError()
