from __future__ import annotations

from typing import Type, TypeVar

from algpy_src.data_structures.graphs.graph import Graph, Node, EdgeData

G = TypeVar('G', bound=Graph)


class ExampleDirectedSimpleGraph(Graph):

    def __init__(self) -> None:
        super().__init__(directed=True, multigraph=False)

    @property
    def name(self) -> str:
        return 'Example Directed Simple Graph'

    @classmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[object, dict[object, object]]) -> G:
        return cls()


class ExampleSimpleGraph(Graph):

    def __init__(self) -> None:
        super().__init__(directed=False, multigraph=False)

    @property
    def name(self) -> str:
        return 'Example Simple Graph'

    @classmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[object, dict[object, object]]) -> G:
        return cls()


class ExampleDirectedMultigraph(Graph):

    def __init__(self) -> None:
        super().__init__(directed=True, multigraph=True)

    @property
    def name(self) -> str:
        return 'Example Directed Multigraph'

    @classmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[Node, dict[Node, EdgeData]]) -> G:
        return cls()


class ExampleMultigraph(Graph):

    def __init__(self) -> None:
        super().__init__(directed=False, multigraph=True)

    @property
    def name(self) -> str:
        return 'Example Multigraph'

    @classmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[Node, dict[Node, EdgeData]]) -> G:
        return cls()
