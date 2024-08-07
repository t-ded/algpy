class NoEdge:

    def __repr__(self) -> str:
        return 'NoEdge'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoEdge)
