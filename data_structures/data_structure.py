from abc import abstractmethod
from base.complexity_object import ComplexityObject
from base.constants import COMPLEXITIES


class DataStructure(ComplexityObject):
    """
    Base class for all data structures.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    @property
    def name(self) -> str:
        return 'Generic Data Structure'

    def print_complexity_info(self, which: COMPLEXITIES = 'both') -> None:
        """
        Print the complexity information for the data structure.

        Parameters:
            which (str)
                Select the type of complexity measure you want to print (one of 'both', 'time' or 'space').
        """
        if which == 'time' or which == 'both':
            self.print_time_complexity_info()
        if which == 'space' or which == 'both':
            self.print_space_complexity_info()

    @abstractmethod
    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information of the data structure.
        """
        raise NotImplementedError()

    @abstractmethod
    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the data structure.
        """
        raise NotImplementedError()