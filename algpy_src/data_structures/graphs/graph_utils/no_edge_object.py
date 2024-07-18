from typing import Generic

from algpy_src.base.constants import SingleEdgeData


class NoEdge(Generic[SingleEdgeData]):

    def __repr__(self) -> str:
        return 'NoEdge'
