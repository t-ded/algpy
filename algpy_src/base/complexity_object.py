from abc import ABC, abstractmethod

from algpy_src.base.constants import COMPLEXITIES
from algpy_src.base.utils import print_delimiter


class ComplexityObject(ABC):
    """
    Base class for any object with time or space complexity measures
    """

    def __init__(self):
        self.n_ops = 0

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Generic Complexity Object'

    @abstractmethod
    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information of the complexity object.
        """
        raise NotImplementedError()

    @abstractmethod
    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the complexity object.
        """
        raise NotImplementedError()

    def print_complexity_info(self, which: COMPLEXITIES = 'both') -> None:
        """
        Print the complexity information for the complexity object.

        Parameters:
            which (str)
                Select the type of complexity measure you want to print (one of 'both', 'time' or 'space').
        """
        print_delimiter()
        if which == 'time' or which == 'both':
            self.print_time_complexity_info()
            print_delimiter(n=5)
        if which == 'space' or which == 'both':
            self.print_space_complexity_info()
        print_delimiter()
