from abc import abstractmethod
from base.complexity_object import ComplexityObject
from base.constants import COMPLEXITIES


class Algorithm(ComplexityObject):
    """
    Base class for all algorithms.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def print_complexity_info(self, which: COMPLEXITIES = 'both') -> None:
        """
        Print the complexity information for the algorithm.

        Parameters:
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
        Print the time complexity information of the algorithm.
        """
        raise NotImplementedError()

    @abstractmethod
    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the algorithm.
        """
        raise NotImplementedError()
