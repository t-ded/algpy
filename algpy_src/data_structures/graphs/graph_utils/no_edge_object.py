from typing import Generic

from algpy_src.base.constants import SingleEdgeData


class NoEdge(Generic[SingleEdgeData]):

    def __repr__(self) -> str:
        return 'NoEdge'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoEdge)
