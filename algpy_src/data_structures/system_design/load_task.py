from algpy_src.data_structures.data_structure import DataStructure


class LoadTask(DataStructure):
    """
    Task with a pre-defined load to be assigned to a server.
    """

    def __init__(self, identifier: str, size: float) -> None:
        super().__init__()
        self._identifier = identifier
        self._size = size

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LoadTask) and self._identifier == other._identifier

    @property
    def name(self) -> str:
        return 'LoadTask'

    @property
    def space_complexity(self) -> str:
        return '1'

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def size(self) -> float:
        return self._size
