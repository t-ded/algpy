from algpy_src.base.utils import underscore_formatter
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

    def __str__(self) -> str:
        return f'LoadTask (id={self._identifier}, size={underscore_formatter(self._size) if self.size > 1_000 else self.size})'

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
