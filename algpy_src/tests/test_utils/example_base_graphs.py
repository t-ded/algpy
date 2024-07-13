from __future__ import annotations

from typing import Type, TypeVar

from algpy_src.data_structures.graphs.graph import Graph

G = TypeVar('G', bound=Graph)


class ExampleDirectedSimpleGraph(Graph):

    def __init__(self):
        super().__init__(directed=True, multigraph=False)
        self.add_nodes_from({'ExampleNodeA', 'ExampleNodeB'})
        self.add_edges_from({('ExampleNodeA', 'ExampleNodeB', 1)})

    @property
    def name(self) -> str:
        return 'Example Directed Simple Graph'

    @property
    def space_complexity(self) -> str:
        return 'N/A'

    @property
    def adjacency_list(self) -> dict[object, dict[object, object | list[object]]]:
        return {'ExampleNodeA': {'ExampleNodeB': 1}}

    @property
    def adjacency_matrix(self) -> list[list[object | list[object]]]:
        return [[1, 0], [0, 0]]

    def add_node(self, node: object) -> None:
        self._nodes.add(node)

    def add_edge(self, edge: tuple[object, object, object]) -> None:
        self._edges.add(edge)

    @classmethod
    def from_adjacency_list(cls: Type[G], adjacency_list: dict[object, dict[object, object]]) -> G:
        return cls()
