from abc import abstractmethod

from algpy_src.data_structures.data_structure import DataStructure


class Container(DataStructure):
    """
    Base class for all container-like data structures which implement methods insert, search, delete.
    """

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Generic Container Data Structure'

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        return 'N/A'

    @property
    @abstractmethod
    def best_case_insert_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def best_case_insert_description(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def average_case_insert_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def worst_case_insert_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def worst_case_insert_description(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def best_case_delete_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def best_case_delete_description(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def average_case_delete_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def worst_case_delete_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def worst_case_delete_description(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def best_case_search_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def best_case_search_description(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def average_case_search_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def worst_case_search_time_complexity(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def worst_case_search_description(self) -> str:
        raise NotImplementedError()
