from abc import abstractmethod

from algpy_src.base.complexity_object import ComplexityObject


class DataStructure(ComplexityObject):
    """
    Base class for all data structures.
    """

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Generic Data Structure'

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        return 'N/A'
