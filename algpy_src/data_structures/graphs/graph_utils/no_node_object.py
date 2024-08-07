class NoNode:

    def __repr__(self) -> str:
        return 'NoNode'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoNode)
