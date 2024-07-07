from abc import ABC, abstractmethod


class ComplexityObject(ABC):
    """
    Base class for any object with time or space complexity measures
    """

    def __init__(self) -> None:
        self._n_ops = 0

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Generic Complexity Object'

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        return 'N/A'

    @property
    def n_ops(self) -> int:
        return self._n_ops

    def increment_n_ops(self, increment: int = 1) -> None:
        """
        Convenience method to increment self.n_ops
        """
        self._n_ops += increment

    def reset_n_ops(self) -> None:
        """
        Convenience method to reset self.n_ops
        """
        self._n_ops = 0
