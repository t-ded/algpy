from typing import TypeVar, Generic

from algpy_src.base.constants import Comparable
from algpy_src.data_structures.container import Container

_K = TypeVar('_K')
_V = TypeVar('_V', bound=Comparable)


class FibonacciHeap(Container, Generic[_K, _V]):
    """
    Fibonacci heap container data structure implementation.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def space_complexity(self) -> str:
        raise NotImplementedError

    @property
    def best_case_insert_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def best_case_insert_description(self) -> str:
        raise NotImplementedError

    @property
    def average_case_insert_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def worst_case_insert_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def worst_case_insert_description(self) -> str:
        raise NotImplementedError

    @property
    def best_case_delete_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def best_case_delete_description(self) -> str:
        raise NotImplementedError

    @property
    def average_case_delete_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def worst_case_delete_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def worst_case_delete_description(self) -> str:
        raise NotImplementedError

    @property
    def best_case_search_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def best_case_search_description(self) -> str:
        raise NotImplementedError

    @property
    def average_case_search_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def worst_case_search_time_complexity(self) -> str:
        raise NotImplementedError

    @property
    def worst_case_search_description(self) -> str:
        raise NotImplementedError

    def insert(self, key: _K, value: _V) -> None:
        """
        Insert a given key associated with a comparable value used to maintain the heap property of the keys.

        Parameters
        ----------
        key : _K
            Key to insert.
        value : _V
            Value to associate the key with. Used to compare the keys and maintain the heap property.
        """
        raise NotImplementedError

    def extract_min(self) -> _K:
        """
        Extract key associated with the minimum value.

        Returns
        -------
        min_value_key : _K
            Returns the key associated with the minimum value.
        """
        raise NotImplementedError
