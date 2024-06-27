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

    @abstractmethod
    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information of the data structure (e.g., insertion, deletion, retrieval etc.).
        """
        raise NotImplementedError()

    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the data structure.
        """
        print(f'Space complexity of the {self.name} data structure is O({self.space_complexity}).')
