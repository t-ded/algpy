from abc import ABC, abstractmethod


class ComplexityObject(ABC):
    """
    Base class for any object with time or space complexity measures
    """

    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Generic Complexity Object'
