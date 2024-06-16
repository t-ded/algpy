from abc import ABC, abstractmethod
from .constants import COMPLEXITIES


class ComplexityObject(ABC):
    """
    Base class for any object with time or space complexity measures
    """

    def __init__(self):
        pass

    @abstractmethod
    def print_complexity_info(self, which: COMPLEXITIES = 'both') -> None:
        """
        Print all desired complexity information for the given object.

        Parameters
        ----------
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
        Print the time complexity information.
        """
        raise NotImplementedError()

    @abstractmethod
    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information.
        """
        raise NotImplementedError()
